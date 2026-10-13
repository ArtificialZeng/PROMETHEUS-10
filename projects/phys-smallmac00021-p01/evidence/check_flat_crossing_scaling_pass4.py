#!/usr/bin/env python3
"""Direct depth-six replay of the pass-4 flat-band collision prediction.

The checker does not import the symbolic producer.  It rebuilds the signed
324-mode graph, checks exact finite-field characteristic multiplicities and
ranks at algebraic reductions of J=sqrt(3)/9, and separately tracks the real
Hermitian spectrum and corner channel.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from flint import fmpz_mod_ctx, fmpz_mod_mat


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
GENERATOR = HERE / "reproduce_sierpinski_hanoi.py"
PREDICTION = HERE / "flat-crossing-scaling-pass4.json"
RESULT = HERE / "flat-crossing-scaling-pass4-replay.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generator():
    spec = importlib.util.spec_from_file_location("direct_k6_graph", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reproduced graph generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_modular_matrix(n: int, oriented, root_edge_count: int, prime: int, j_value: int):
    ctx = fmpz_mod_ctx(prime)
    rows = [[ctx(0) for _ in range(n)] for _ in range(n)]
    for edge, (u, v) in enumerate(oriented):
        weight = 1 if edge < root_edge_count else j_value
        rows[u][v] += ctx(weight)
        rows[v][u] -= ctx(weight)
    return fmpz_mod_mat(rows, ctx), ctx


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if not expected or Path(sys.executable).resolve() != Path(expected).resolve():
        raise RuntimeError("scientific Python binding mismatch")
    if RESULT.exists():
        raise RuntimeError(f"refusing to overwrite {RESULT}")

    prediction = json.loads(PREDICTION.read_text(encoding="utf-8"))
    if prediction["k6_collision"]["predicted_positive_multiplicity"] != 41:
        raise RuntimeError("unexpected analytic prediction")
    rr = load_generator()
    addresses, terms, frustration, _ = rr.graph_from_cells(6)
    cliques, root_edges, _ = rr.krausz_root(len(addresses), frustration)
    oriented, _, cycles, flux = rr.all_plus_orientation(terms, root_edges)
    n, augmented_edges, augmented_oriented, local, degrees = rr.augment_local(
        root_edges, oriented, cliques
    )
    counts = {
        "terms": len(terms),
        "root_vertices": len(cliques),
        "root_edges": len(root_edges),
        "cycles": len(cycles),
        "local_pendants": len(local),
        "modes": n,
    }
    expected_counts = {
        "terms": 243,
        "root_vertices": 204,
        "root_edges": 243,
        "cycles": 40,
        "local_pendants": 120,
        "modes": 324,
    }
    if counts != expected_counts or not all(item["projected_eigenvalue"] == 1 for item in flux):
        raise RuntimeError(f"direct graph or sector mismatch: {counts}")

    modular = []
    for prime in (1000033, 1000081):
        roots = [int(value) for value in sp.sqrt_mod(3, prime, all_roots=True)]
        if len(roots) != 2:
            raise RuntimeError(f"3 does not split as expected modulo {prime}")
        for sqrt3 in roots:
            j_value = sqrt3 * pow(9, -1, prime) % prime
            inv27 = pow(27, -1, prime)
            if j_value * j_value % prime != inv27:
                raise RuntimeError("algebraic J reduction failed")
            matrix, ctx = build_modular_matrix(
                n, augmented_oriented, len(root_edges), prime, j_value
            )
            kernel_matrix = matrix * matrix
            for index in range(n):
                kernel_matrix[index, index] += ctx(inv27)
            rank = int(kernel_matrix.rank())
            charpoly = matrix.charpoly()
            variable = charpoly.context().gen()
            flat_factor = variable * variable + inv27
            multiplicity = 0
            remainder = None
            reduced = charpoly
            while True:
                quotient, current_remainder = divmod(reduced, flat_factor)
                if current_remainder:
                    remainder = current_remainder
                    break
                reduced = quotient
                multiplicity += 1
            if rank != 242 or multiplicity != 41 or reduced.degree() != 242:
                raise RuntimeError(
                    f"direct finite-field special-point check failed modulo {prime}: "
                    f"rank={rank}, multiplicity={multiplicity}"
                )
            coefficients = [int(value) for value in reduced.coeffs()]
            modular.append({
                "prime": prime,
                "sqrt3_representative": sqrt3,
                "J_representative": j_value,
                "J_squared": inv27,
                "rank_of_A_squared_plus_J_squared_I": rank,
                "combined_kernel_dimension": n - rank,
                "flat_quadratic_factor_multiplicity": multiplicity,
                "reduced_degree": reduced.degree(),
                "first_nonzero_remainder_degree": remainder.degree(),
                "reduced_coefficient_sha256": hashlib.sha256(
                    json.dumps(coefficients, separators=(",", ":")).encode("ascii")
                ).hexdigest(),
            })

    def real_matrix(j_value: float) -> np.ndarray:
        matrix = np.zeros((n, n), dtype=float)
        for edge, (u, v) in enumerate(augmented_oriented):
            weight = 1.0 if edge < len(root_edges) else j_value
            matrix[u, v] = weight
            matrix[v, u] = -weight
        return matrix

    special_j = 1.0 / math.sqrt(27.0)
    special_A = real_matrix(special_j)
    eigenvalues, eigenvectors = np.linalg.eigh(1j * special_A)
    target_indices = np.flatnonzero(np.abs(eigenvalues - special_j) < 1.0e-10)
    if len(target_indices) != 41:
        raise RuntimeError(f"direct real spectrum found {len(target_indices)} target modes")
    target_residual = float(np.max(np.abs(eigenvalues[target_indices] - special_j)))
    outside = np.delete(eigenvalues, target_indices)
    nearest_outside = float(np.min(np.abs(outside - special_j)))

    corners = [index for index, degree in enumerate(degrees) if degree == 1]
    corner_block = eigenvectors[np.ix_(corners, target_indices)]
    left, singular_values, _ = np.linalg.svd(corner_block, full_matrices=False)
    corner_vector = left[:, 0] / left[0, 0]
    expected_corner = np.array([1.0, -1.0, -1.0], dtype=complex)
    corner_error = float(np.max(np.abs(corner_vector - expected_corner)))
    if singular_values[1] / singular_values[0] > 1.0e-10 or corner_error > 1.0e-10:
        raise RuntimeError("target eigenspace is not the single boundary-symmetric channel")

    epsilon = 1.0e-6
    tracking = []
    dispersive = {}
    for label, trial_j in (("below", special_j - epsilon), ("above", special_j + epsilon)):
        values = np.linalg.eigvalsh(1j * real_matrix(trial_j))
        flat_count = int(np.sum(np.abs(values - trial_j) < 1.0e-10))
        candidates = values[np.abs(values - trial_j) >= 1.0e-10]
        branch = float(candidates[np.argmin(np.abs(candidates - trial_j))])
        if flat_count != 40:
            raise RuntimeError(f"generic flat multiplicity changed {label} collision")
        dispersive[label] = branch
        tracking.append({
            "side": label,
            "J": trial_j,
            "flat_positive_multiplicity": flat_count,
            "nearest_dispersive_x": branch,
            "signed_x_minus_J": branch - trial_j,
            "absolute_separation": abs(branch - trial_j),
        })
    observed_slope = (dispersive["above"] - dispersive["below"]) / (2 * epsilon)
    predicted_slope = 116.0 / 197.0
    if abs(observed_slope - predicted_slope) > 2.0e-6:
        raise RuntimeError("direct branch slope does not match the exact symmetric channel")
    if not (tracking[0]["signed_x_minus_J"] > 0 and tracking[1]["signed_x_minus_J"] < 0):
        raise RuntimeError("dispersive branch does not exchange order across the flat band")

    # The sign of every pendant can be gauged away, giving the negative-J twin.
    gauge = np.ones(n)
    gauge[len(cliques):] = -1.0
    negative_residual = float(
        np.max(np.abs(real_matrix(-special_j) - gauge[:, None] * special_A * gauge[None, :]))
    )
    if negative_residual != 0.0:
        raise RuntimeError("J-sign gauge failed")

    result = {
        "schema_version": 1,
        "job_id": os.environ.get("PHYSICS_JOB_ID", "phys-00021-p01-research-2f16d322a2e4"),
        "status": "pass",
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
        },
        "prediction_binding": {
            "prediction_file": "evidence/flat-crossing-scaling-pass4.json",
            "prediction_sha256": sha256(PREDICTION),
            "prediction_producer_imported": False,
            "direct_generator": "evidence/reproduce_sierpinski_hanoi.py",
            "direct_generator_sha256": sha256(GENERATOR),
            "source_sha256": sha256(PROJECT / "source.md"),
        },
        "direct_graph": {
            **counts,
            "all_cycle_fluxes_plus_one": True,
            "corner_vertices": corners,
        },
        "exact_finite_field_checks": modular,
        "real_spectrum": {
            "J": special_j,
            "target_x": special_j,
            "target_positive_multiplicity": len(target_indices),
            "maximum_target_eigenvalue_residual": target_residual,
            "nearest_non_target_separation": nearest_outside,
            "corner_projection_singular_values": [float(value) for value in singular_values],
            "corner_projection_rank": 1,
            "normalized_direct_corner_vector_real": [float(value.real) for value in corner_vector],
            "normalized_direct_corner_vector_imag": [float(value.imag) for value in corner_vector],
            "canonical_boundary_gauge": [1, -1, -1],
            "canonical_channel": "A1 boundary-symmetric vector (1,1,1) after applying the recorded boundary gauge",
        },
        "branch_tracking": {
            "epsilon": epsilon,
            "points": tracking,
            "central_difference_dx_dJ": observed_slope,
            "exact_prediction_dx_dJ": "116/197",
            "order_exchange": "dispersive x is above x=J below the root and below x=J above the root",
        },
        "negative_J_gauge": {
            "diagonal": "+1 on 204 root modes and -1 on 120 pendants",
            "maximum_matrix_residual": negative_residual,
            "consequence": "an identical crossing occurs at negative J",
        },
        "limitations": "Finite-field checks are exact for the stated reductions and the real spectral replay directly checks the 324-mode matrix. The arbitrary-depth statement still rests on the pass-3 recurrence and the pass-4 induction, not on finite sampling.",
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass",
        "result": str(RESULT.relative_to(PROJECT)),
        "modular_cases": len(modular),
        "direct_positive_multiplicity": len(target_indices),
        "corner_projection_rank": 1,
        "observed_slope": observed_slope,
        "predicted_slope": "116/197",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
