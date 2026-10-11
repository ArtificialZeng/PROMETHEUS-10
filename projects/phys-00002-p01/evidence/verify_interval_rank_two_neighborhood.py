#!/usr/bin/env python3
"""Independent numerical and record-level check of the rank-two certificate.

This verifier does not import the interval research implementation.  It
reconstructs the physical two-jump Liouvillian on matrix units with NumPy and
SciPy, checks the recorded chart identity, finite-differences the whitened
augmented support Hessian, performs corrected fixed-a holdouts, and separately
checks the outward-rounded 256/320-bit certificate records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import root_scalar

import sys

ARB_PATH = "standard Python environment (python-flint)"
from flint import arb  # noqa: E402


EXPECTED_SOURCE_SHA256 = "7bfa09317b0b519a4be6488e9e980431f7cdd49e11fe6adf216f9b9d32dccfc8"
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SIGMA_X, SIGMA_Y, SIGMA_Z)
E = (
    np.array([[1, 0], [0, 0]], dtype=complex),
    np.array([[0, 0], [1, 0]], dtype=complex),
    np.array([[0, 1], [0, 0]], dtype=complex),
    np.array([[0, 0], [0, 1]], dtype=complex),
)


def midpoint(item: dict) -> float:
    text = item["midpoint"]
    if text.startswith("["):
        text = text[1:].split(" +/-", 1)[0]
    return float(text)


def root_midpoint(record: dict) -> np.ndarray:
    return np.array([midpoint(x) for x in record["root"]["enclosure"][:7]], dtype=float)


def chart(native: np.ndarray):
    h = native[:3]
    z = np.array([1j * native[5], native[3] + 1j * native[6], native[4]], dtype=complex)
    eta = np.array([native[7] + 1j * native[9], native[8] + 1j * native[10]], dtype=complex)
    w = np.array(
        [eta[0], eta[1], -(np.conj(z[0]) * eta[0] + np.conj(z[1]) * eta[1]) / np.conj(z[2])],
        dtype=complex,
    )
    return h, z, w


def super_from_action(action) -> np.ndarray:
    result = np.zeros((4, 4), dtype=complex)
    for col, matrix in enumerate(E):
        result[:, col] = action(matrix).reshape(4, order="F")
    return result


def liouvillian(h: np.ndarray, jumps: tuple[np.ndarray, ...]) -> np.ndarray:
    hamiltonian = sum(h[i] * PAULI[i] for i in range(3))
    jump_matrices = [sum(z[i] * PAULI[i] for i in range(3)) for z in jumps]

    def action(rho):
        value = -1j * (hamiltonian @ rho - rho @ hamiltonian)
        for jump in jump_matrices:
            gram = jump.conj().T @ jump
            value += jump @ rho @ jump.conj().T - 0.5 * (gram @ rho + rho @ gram)
        return value

    return super_from_action(action)


def values(y: np.ndarray, root: np.ndarray, whitening: np.ndarray, support_lambda: float):
    native = np.zeros(11)
    native[:7] = root
    native += whitening @ y
    h, z, w = chart(native)
    channel = expm(liouvillian(h, (z, w)))
    a = float(channel[0, 0].real)
    b = float(channel[3, 3].real)
    f = b - support_lambda * a
    g = f + (a - 0.5) ** 2
    return g, a, b, z, w, channel


def finite_difference_hessian(function, dimension: int, step: float) -> np.ndarray:
    result = np.zeros((dimension, dimension))
    origin = np.zeros(dimension)
    f0 = function(origin)
    for i in range(dimension):
        ei = np.zeros(dimension)
        ei[i] = step
        result[i, i] = (function(ei) - 2 * f0 + function(-ei)) / step**2
        for j in range(i + 1, dimension):
            ej = np.zeros(dimension)
            ej[j] = step
            value = (
                function(ei + ej)
                - function(ei - ej)
                - function(-ei + ej)
                + function(-ei - ej)
            ) / (4 * step**2)
            result[i, j] = result[j, i] = value
    return result


def all_margins_positive(record: dict) -> bool:
    selected = record["uniform_certificate"]["certified_radius_y_euclidean"]
    trial = next(row for row in record["radius_trials"] if row["radius"] == selected)
    # The compact Arb ball rendering may suppress a nonzero midpoint when the
    # relative radius is large; the separately stored directed lower endpoint
    # is the replayable positivity datum.
    return all(arb(item["lower"]) > 0 for item in trial["direct_gershgorin_margins"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()

    primary = json.loads(Path("evidence/interval-rank-two-neighborhood.json").read_text())
    replay = json.loads(Path("evidence/interval-rank-two-neighborhood-320.json").read_text())
    root = root_midpoint(primary)
    whitening = np.asarray(primary["rank_two_chart"]["whitening_matrix_rows"], dtype=float)
    replay_whitening = np.asarray(replay["rank_two_chart"]["whitening_matrix_rows"], dtype=float)
    support_lambda = midpoint(primary["root"]["enclosure"][7])

    def g_function(y):
        return values(y, root, whitening, support_lambda)[0]

    numerical_hessian = finite_difference_hessian(g_function, 11, 3e-5)
    hessian_symmetry = float(np.max(np.abs(numerical_hessian - numerical_hessian.T)))
    hessian_minus_identity = float(np.max(np.abs(numerical_hessian - np.eye(11))))
    numerical_eigenvalues = np.linalg.eigvalsh(numerical_hessian)

    rng = np.random.default_rng(1471435)
    orthogonality = []
    fixed_a_records = []
    base_g, base_a, base_b, _, _, base_channel = values(
        np.zeros(11), root, whitening, support_lambda
    )
    fd = 1e-6
    grad_a = np.zeros(11)
    for i in range(11):
        direction = np.zeros(11)
        direction[i] = fd
        grad_a[i] = (
            values(direction, root, whitening, support_lambda)[1]
            - values(-direction, root, whitening, support_lambda)[1]
        ) / (2 * fd)
    correction_direction = grad_a / np.dot(grad_a, grad_a)
    for index in range(16):
        raw = rng.normal(size=11)
        tangent = raw - grad_a * np.dot(grad_a, raw) / np.dot(grad_a, grad_a)
        tangent /= np.linalg.norm(tangent)
        step = 4e-5
        trial = step * tangent

        def constraint(correction):
            return values(trial + correction * correction_direction, root, whitening, support_lambda)[1] - 0.5

        root_result = root_scalar(constraint, x0=0.0, x1=1e-8, method="secant", xtol=1e-14)
        corrected = trial + root_result.root * correction_direction
        _, aval, bval, z, w, _ = values(corrected, root, whitening, support_lambda)
        orthogonality.append(float(abs(np.vdot(z, w))))
        fixed_a_records.append(
            {
                "index": index,
                "a_minus_half": aval - 0.5,
                "b_minus_root": bval - base_b,
                "z_dagger_w_abs": float(abs(np.vdot(z, w))),
                "correction": float(root_result.root),
            }
        )

    # Direct trace preservation and stochasticity checks at the reconstructed root.
    h0, z0, w0 = chart(np.r_[root, np.zeros(4)])
    l0 = liouvillian(h0, (z0, w0))
    trace_preservation_residual = float(np.max(np.abs(np.array([1, 0, 0, 1]) @ l0)))
    probability_column_residual = float(
        max(abs(base_channel[0, 0].real + base_channel[3, 0].real - 1),
            abs(base_channel[0, 3].real + base_channel[3, 3].real - 1))
    )

    source_hash = hashlib.sha256(Path("source.md").read_bytes()).hexdigest()
    primary_radius = arb(primary["uniform_certificate"]["certified_radius_y_euclidean"])
    replay_radius = arb(replay["uniform_certificate"]["certified_radius_y_euclidean"])
    primary_taylor = arb(primary["third_frechet_taylor_bound"]["certified_taylor_radius_y_euclidean"]["ball"])
    replay_taylor = arb(replay["third_frechet_taylor_bound"]["certified_taylor_radius_y_euclidean"]["ball"])
    conditions = {
        "source_immutable": source_hash == EXPECTED_SOURCE_SHA256,
        "primary_status_true": primary["status"]["rank_two_fixed_a_local_optimality_certified"],
        "replay_status_true": replay["status"]["rank_two_fixed_a_local_optimality_certified"],
        "primary_uniform_margins_positive": all_margins_positive(primary),
        "replay_uniform_margins_positive": all_margins_positive(replay),
        "same_selected_radius": (
            primary["uniform_certificate"]["certified_radius_y_euclidean"]
            == replay["uniform_certificate"]["certified_radius_y_euclidean"]
            == "1e-4"
        ),
        "positive_taylor_radii": primary_taylor > 0 and replay_taylor > 0,
        "taylor_radii_below_uniform_radius": primary_taylor < primary_radius and replay_taylor < replay_radius,
        "whitening_precision_replay_stable": float(np.max(np.abs(whitening - replay_whitening))) < 2e-13,
        "matrix_unit_hessian_near_whitened_identity": hessian_minus_identity < 1e-5,
        "matrix_unit_hessian_positive": float(numerical_eigenvalues[0]) > 0.999998,
        "chart_orthogonality_numerically_reproduced": max(orthogonality) < 1e-17,
        "fixed_a_holdouts_corrected": max(abs(row["a_minus_half"]) for row in fixed_a_records) < 2e-14,
        "fixed_a_holdouts_all_above_root": min(row["b_minus_root"] for row in fixed_a_records) > 0,
        "trace_preservation_reconstructed": trace_preservation_residual < 1e-14,
        "probability_columns_normalized": probability_column_residual < 1e-14,
    }
    passed = all(conditions.values())
    data = {
        "job_id": "phys-00002-p01-research-147b1435c704",
        "method": "Independent complex matrix-unit Liouvillian reconstruction, finite-difference chart Hessian, corrected fixed-a holdouts, and record-level 256/320-bit Arb checks",
        "comparisons": {
            "max_abs_numerical_hessian_minus_identity": hessian_minus_identity,
            "numerical_hessian_symmetry_residual": hessian_symmetry,
            "numerical_hessian_eigenvalues": numerical_eigenvalues.tolist(),
            "max_abs_whitening_256_minus_320": float(np.max(np.abs(whitening - replay_whitening))),
            "max_abs_z_dagger_w": max(orthogonality),
            "root_a_minus_half": base_a - 0.5,
            "root_b": base_b,
            "trace_preservation_residual": trace_preservation_residual,
            "probability_column_residual": probability_column_residual,
            "fixed_a_holdouts": fixed_a_records,
        },
        "conditions": conditions,
        "verification_passed": passed,
        "scientific_scope": "finite-radius fixed-a local optimality in the explicit nearby rank-at-most-two Kossakowski chart",
        "limitations": "Finite-difference and holdout tests are independent diagnostics, not the interval proof. Neither verifier nor primary certificate addresses rank-three directions, distant/unbounded generators, global optimality, or the Q2 boundary.",
        "source_sha256": source_hash,
    }
    Path(args.json).write_text(json.dumps(data, indent=2) + "\n")
    log_lines = [
        f"source immutable: {conditions['source_immutable']}",
        f"max |matrix-unit finite-difference Hessian-I|: {hessian_minus_identity:.12g}",
        f"numerical Hessian minimum eigenvalue: {numerical_eigenvalues[0]:.15g}",
        f"max chart |z^dagger w|: {max(orthogonality):.12g}",
        f"minimum corrected fixed-a b-b_root: {min(row['b_minus_root'] for row in fixed_a_records):.12g}",
        f"maximum corrected |a-1/2|: {max(abs(row['a_minus_half']) for row in fixed_a_records):.12g}",
        f"trace-preservation residual: {trace_preservation_residual:.12g}",
        f"probability-column residual: {probability_column_residual:.12g}",
        f"all verification conditions passed: {passed}",
        "SCIENCE LIMIT: local rank-at-most-two chart only; no global minimum, tails, rank-three, or Q2-boundary claim.",
    ]
    Path(args.log).write_text("\n".join(log_lines) + "\n")
    print(json.dumps({"json": args.json, "log": args.log, "verification_passed": passed}, indent=2))


if __name__ == "__main__":
    main()
