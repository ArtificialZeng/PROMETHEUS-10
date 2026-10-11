#!/usr/bin/env python3
"""Finite-dimensional stress test of the critical trace-norm theorem.

The theorem is analytic; this script probes the spectral-block reconstruction,
including a degenerate gate, a small fixed phase gap, and the published
two-qubit generator.  All cases retain the exact finite age support 0..t.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm, schur


def age_mass(t: int, gamma: float) -> np.ndarray:
    left = np.ones(t + 1)
    right = np.ones(t + 1)
    for k in range(t):
        left[k + 1] = left[k] * (k + gamma) / (k + 1)
        right[k + 1] = right[k] * (k + 1 - gamma) / (k + 1)
    return left[::-1] * right


def trace_norm(x: np.ndarray) -> float:
    return float(np.linalg.svd(x, compute_uv=False).sum())


def group_eigenvalues(u: np.ndarray, vectors: np.ndarray, tol: float = 2e-12):
    groups: list[dict[str, object]] = []
    for j, value in enumerate(u):
        for group in groups:
            if abs(value - group["value"]) < tol:
                group["indices"].append(j)
                break
        else:
            groups.append({"value": value, "indices": [j]})
    projectors = []
    values = []
    for group in groups:
        cols = vectors[:, group["indices"]]
        projectors.append(cols @ cols.conj().T)
        values.append(group["value"])
    return np.asarray(values), projectors


def evaluate_case(case: dict[str, object], gammas: list[float], times: list[int]):
    U = np.asarray(case["U"], dtype=complex)
    psi = np.asarray(case["psi"], dtype=complex)
    psi /= np.linalg.norm(psi)
    rho0 = np.outer(psi, psi.conj())
    triangular, vec = schur(U, output="complex")
    u = np.diag(triangular)
    # Complex Schur vectors are orthonormal, including inside degenerate spaces.
    values, projectors = group_eigenvalues(u, vec)
    pinched = sum((P @ rho0 @ P for P in projectors), np.zeros_like(rho0))
    q = np.asarray([np.linalg.norm(P @ psi) for P in projectors])
    occupied = q > 2e-13
    kappa = 0.0
    delta = np.inf
    for j in range(len(values)):
        for k in range(len(values)):
            if j == k or not (occupied[j] and occupied[k]):
                continue
            gap = abs(1 - values[j] * values[k].conjugate())
            kappa += q[j] * q[k] / gap
            delta = min(delta, gap)

    rows = []
    max_ratio = 0.0
    max_spectral_reconstruction_error = 0.0
    for gamma in gammas:
        for t in times:
            p = age_mass(t, gamma)
            orbit = rho0.copy()
            rho = p[0] * orbit
            # p is indexed by age, so start again with the age-zero term.
            rho = np.zeros_like(rho0)
            for b in range(t + 1):
                if b:
                    orbit = U @ orbit @ U.conj().T
                rho += p[b] * orbit

            spectral = pinched.copy()
            for j, Pj in enumerate(projectors):
                for k, Pk in enumerate(projectors):
                    if j == k:
                        continue
                    z = values[j] * values[k].conjugate()
                    F = np.dot(p, z ** np.arange(t + 1))
                    spectral += F * (Pj @ rho0 @ Pk)
            reconstruction_error = trace_norm(rho - spectral)
            max_spectral_reconstruction_error = max(
                max_spectral_reconstruction_error, reconstruction_error
            )
            distance = trace_norm(rho - pinched)
            endpoint_sum = p[0] + p[-1]
            bound = 2 * endpoint_sum * kappa
            ratio = 0.0 if bound == 0 else distance / bound
            max_ratio = max(max_ratio, ratio)
            rows.append(
                {
                    "gamma": gamma,
                    "t": t,
                    "trace_norm_to_pinching": distance,
                    "weighted_fixed_gap_bound": bound,
                    "ratio": ratio,
                    "normalization_error": abs(float(p.sum()) - 1.0),
                    "min_density_eigenvalue": float(np.linalg.eigvalsh(rho).min()),
                }
            )
    return {
        "id": case["id"],
        "dimension": len(psi),
        "distinct_occupied_eigenvalues": int(occupied.sum()),
        "minimum_occupied_chord_gap": None if not np.isfinite(delta) else float(delta),
        "weighted_gap_constant": kappa,
        "max_trace_bound_ratio": max_ratio,
        "max_spectral_reconstruction_trace_norm_error": max_spectral_reconstruction_error,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_H = np.array(
        [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
        dtype=float,
    )
    source_U = expm(1j * np.pi / 4 * source_H)
    phases_degenerate = np.array([0.0, np.pi / 3, np.pi / 3, np.pi])
    phases_small_gap = np.array([0.0, 0.071, 1.1, 2.4, 4.9])
    cases = [
        {
            "id": "wald_noninteracting_theta_pi_over_4",
            "U": source_U,
            "psi": np.array([0, 0, 0, 1], dtype=complex),
        },
        {
            "id": "degenerate_gate",
            "U": np.diag(np.exp(1j * phases_degenerate)),
            "psi": np.array([1, 1j, -2, 0.7 - 0.2j], dtype=complex),
        },
        {
            "id": "small_fixed_gap",
            "U": np.diag(np.exp(1j * phases_small_gap)),
            "psi": np.array([1, -0.4j, 0.3 + 0.2j, -0.9, 0.1j], dtype=complex),
        },
        {
            "id": "one_dimensional_trivial",
            "U": np.array([[np.exp(0.3j)]]),
            "psi": np.array([1], dtype=complex),
        },
    ]
    gammas = [0.2, 0.5, 0.8]
    times = [1, 2, 3, 8, 32, 128, 512]
    results = [evaluate_case(c, gammas, times) for c in cases]
    max_ratio = max(x["max_trace_bound_ratio"] for x in results)
    max_reconstruction_error = max(
        x["max_spectral_reconstruction_trace_norm_error"] for x in results
    )
    min_eigenvalue = min(row["min_density_eigenvalue"] for x in results for row in x["rows"])
    max_norm_error = max(row["normalization_error"] for x in results for row in x["rows"])
    status = (
        "pass"
        if max_ratio <= 1 + 3e-12
        and max_reconstruction_error < 3e-11
        and min_eigenvalue > -3e-12
        and max_norm_error < 3e-12
        else "fail"
    )
    payload = {
        "status": status,
        "precision": "NumPy/SciPy complex128; complete ages 0..t",
        "tested_gamma": gammas,
        "tested_times": times,
        "max_trace_norm_over_weighted_bound": max_ratio,
        "max_spectral_reconstruction_trace_norm_error": max_reconstruction_error,
        "minimum_density_eigenvalue": min_eigenvalue,
        "max_age_normalization_error": max_norm_error,
        "cases": results,
        "limitations": [
            "Floating stress tests are not interval certificates.",
            "The analytic proof, not these samples, establishes the finite-dimensional theorem.",
            "The 0.071-radian case is a fixed gap and does not certify a gap-closing uniform limit.",
        ],
    }
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "cases"}, indent=2))
    if status != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
