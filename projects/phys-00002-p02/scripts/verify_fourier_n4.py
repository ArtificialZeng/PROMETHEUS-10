#!/usr/bin/env python3
"""Audit the unrestricted N=4 Grinko--Uola Fourier criterion.

The script compares four representations:

1. the eight-channel Fourier SOCP with all four triple coefficients free;
2. the Fourier transform of the Andrejic--Kunjwal (AK) parent vector part;
3. an explicit analytic dual certificate; and
4. the unrestricted sixteen-effect qubit parent SDP.

It also verifies, symbolically, the Walsh-transform identities and the planar
three-unit-vector lemma used by the analytic certificate.  No result from a
failed or non-optimal numerical solve is accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import product
from pathlib import Path
from typing import Any

import cvxpy as cp
import numpy as np
import sympy as sp


MU = np.asarray([(1, *tail) for tail in product((-1, 1), repeat=3)], dtype=float)
TRIPLES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
C = np.asarray(
    [[np.prod(mu[list(indices)]) for indices in TRIPLES] for mu in MU],
    dtype=float,
)
CHAIN_LABELS = ((1, -1, -1, -1), (1, 1, -1, -1), (1, 1, 1, -1), (1, 1, 1, 1))
CHAIN_ROWS = tuple(
    int(np.flatnonzero(np.all(MU == np.asarray(label, dtype=float), axis=1))[0])
    for label in CHAIN_LABELS
)
SOURCE_SHA256 = "f4df96a62655110bba6043cfb7b266e7f042ab2eadb15a45ea20af70fb89c028"
SOLVER_OPTIONS = {
    "solver": "CLARABEL",
    "tol_gap_abs": 1.0e-10,
    "tol_gap_rel": 1.0e-10,
    "tol_feas": 1.0e-10,
    "max_iter": 500,
}
PARENT_SOLVER_OPTIONS = {
    "solver": "CLARABEL",
    "tol_gap_abs": 1.0e-8,
    "tol_gap_rel": 1.0e-8,
    "tol_feas": 1.0e-8,
    "max_iter": 500,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def vectors_from_angles(angles: np.ndarray) -> np.ndarray:
    return np.column_stack(
        (np.cos(angles), np.sin(angles), np.zeros(angles.shape[0]))
    )


def denominator(angles: np.ndarray) -> float:
    return float(np.sum(np.sin(np.diff(angles) / 2.0)) + np.cos(angles[-1] / 2.0))


def ak_fourier_primal(angles: np.ndarray) -> dict[str, Any]:
    """Fourier-transform the vector part of the AK endpoint/chord parent.

    At visibility one, the restricted odd Fourier function has four nonzero
    values: 4(n1-n2), 4(n2-n3), 4(n3-n4), and 4(n1+n4).  Its constant and
    degree-one Walsh coefficients are exactly n1,...,n4; the remaining four
    coefficients are precisely the unrestricted N=4 triple channels.
    """

    n = vectors_from_angles(angles)
    differences = (n[0] - n[1], n[1] - n[2], n[2] - n[3], n[0] + n[3])
    weights = np.asarray([np.linalg.norm(vector) / 2.0 for vector in differences])
    directions = np.asarray([vector / np.linalg.norm(vector) for vector in differences])
    restricted_odd = np.zeros((8, 3), dtype=float)
    for row, vector in zip(CHAIN_ROWS, differences, strict=True):
        restricted_odd[row] = 4.0 * vector

    low_basis = np.column_stack((np.ones(8), MU[:, 1], MU[:, 2], MU[:, 3]))
    full_basis = np.column_stack((low_basis, C))
    coefficients = full_basis.T @ restricted_odd / 8.0
    x_ak = coefficients[4:]
    b = MU @ n
    reconstructed = b + C @ x_ak
    return {
        "n": n,
        "weights": weights,
        "directions": directions,
        "restricted_odd": restricted_odd,
        "low_coefficients": coefficients[:4],
        "x_ak": x_ak,
        "b": b,
        "reconstructed": reconstructed,
        "basis_orthogonality_residual": float(
            np.max(np.abs(full_basis.T @ full_basis - 8.0 * np.eye(8)))
        ),
        "low_coefficient_residual": float(np.max(np.abs(coefficients[:4] - n))),
        "reconstruction_residual": float(np.max(np.abs(reconstructed - restricted_odd))),
        "objective": float(np.sum(np.linalg.norm(reconstructed, axis=1))),
    }


def analytic_dual(angles: np.ndarray, primal: dict[str, Any]) -> dict[str, Any]:
    """Construct the degree-at-most-one dual function on the half cube."""

    u1, u2, u3, u4 = primal["directions"]
    a0 = -(u1 + u4) / 2.0
    a2 = (u1 - u2) / 2.0
    a3 = (u2 - u3) / 2.0
    a4 = (u3 - u4) / 2.0
    y = (
        a0[None, :]
        + MU[:, 1, None] * a2[None, :]
        + MU[:, 2, None] * a3[None, :]
        + MU[:, 3, None] * a4[None, :]
    )
    norms = np.linalg.norm(y, axis=1)
    chain_values = np.asarray([y[row] for row in CHAIN_ROWS])
    stationarity = C.T @ y
    dual_objective = -float(np.sum(primal["b"] * y))
    return {
        "y": y,
        "norms": norms,
        "chain_interpolation_residual": float(
            np.max(np.abs(chain_values + primal["directions"]))
        ),
        "stationarity_residual": float(np.max(np.abs(stationarity))),
        "max_norm": float(np.max(norms)),
        "max_unit_ball_violation": float(np.max(np.maximum(norms - 1.0, 0.0))),
        "objective": dual_objective,
        "primal_dual_gap": float(primal["objective"] - dual_objective),
    }


def solve_fourier_socp(vectors: np.ndarray) -> dict[str, Any]:
    """Solve all eight norm channels with all four triple vectors free."""

    b = MU @ vectors
    x = cp.Variable((4, 3), name="four_triple_vectors")
    t = cp.Variable(8, name="eight_norm_epigraphs")
    constraints = [cp.SOC(t[row], b[row] + C[row] @ x) for row in range(8)]
    problem = cp.Problem(cp.Minimize(cp.sum(t)), constraints)
    value = problem.solve(**SOLVER_OPTIONS)
    if problem.status != cp.OPTIMAL or value is None or not np.isfinite(value):
        raise RuntimeError(f"Fourier SOCP failed: status={problem.status}, value={value}")

    residual_vectors = b + C @ x.value
    residual_norms = np.linalg.norm(residual_vectors, axis=1)
    dual_lambdas = np.asarray(
        [float(np.asarray(constraint.dual_value[0]).reshape(-1)[0]) for constraint in constraints]
    )
    dual_vectors = np.asarray(
        [np.asarray(constraint.dual_value[1], dtype=float).reshape(3) for constraint in constraints]
    )
    dual_objective = -float(np.sum(b * dual_vectors))
    return {
        "status": problem.status,
        "solver": problem.solver_stats.solver_name,
        "iterations": int(problem.solver_stats.num_iters),
        "solve_time_seconds": float(problem.solver_stats.solve_time),
        "objective": float(value),
        "dual_objective": dual_objective,
        "absolute_primal_dual_gap": float(abs(value - dual_objective)),
        "relative_primal_dual_gap": float(abs(value - dual_objective) / max(1.0, abs(value))),
        "primal_cone_violation": float(
            np.max(np.maximum(residual_norms - np.asarray(t.value), 0.0))
        ),
        "epigraph_activity_residual": float(np.max(np.abs(np.asarray(t.value) - residual_norms))),
        "dual_cone_violation": float(
            np.max(np.maximum(np.linalg.norm(dual_vectors, axis=1) - dual_lambdas, 0.0))
        ),
        "x_stationarity_residual": float(np.max(np.abs(C.T @ dual_vectors))),
        "t_stationarity_residual": float(np.max(np.abs(1.0 - dual_lambdas))),
        "x": np.asarray(x.value),
        "residual_norms": residual_norms,
    }


def solve_direct_parent_sdp(angles: np.ndarray) -> dict[str, Any]:
    """Maximize visibility over sixteen unrestricted Hermitian 2x2 effects."""

    n = vectors_from_angles(angles)
    labels = np.asarray(list(product((-1, 1), repeat=4)), dtype=int)
    effects = [cp.Variable((2, 2), hermitian=True, name=f"G_{row:02d}") for row in range(16)]
    eta = cp.Variable(name="eta")
    identity = np.eye(2, dtype=complex)
    sigma_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma_y = np.asarray([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    constraints: list[Any] = [eta >= 0.0, eta <= 1.0]
    constraints.extend(effect >> 0 for effect in effects)
    constraints.append(sum(effects, np.zeros((2, 2), dtype=complex)) == identity)
    for measurement in range(4):
        target = identity / 2.0 + eta * (
            n[measurement, 0] * sigma_x + n[measurement, 1] * sigma_y
        ) / 2.0
        marginal = sum(
            (effects[row] for row in range(16) if labels[row, measurement] == 1),
            np.zeros((2, 2), dtype=complex),
        )
        constraints.append(marginal == target)

    problem = cp.Problem(cp.Maximize(eta), constraints)
    value = problem.solve(**PARENT_SOLVER_OPTIONS)
    if problem.status != cp.OPTIMAL or value is None or not np.isfinite(value):
        raise RuntimeError(f"Direct parent SDP failed: status={problem.status}, value={value}")

    numeric_effects = [np.asarray(effect.value) for effect in effects]
    normalization_residual = np.max(
        np.abs(sum(numeric_effects, np.zeros((2, 2), dtype=complex)) - identity)
    )
    marginal_residual = 0.0
    for measurement in range(4):
        target = identity / 2.0 + float(eta.value) * (
            n[measurement, 0] * sigma_x + n[measurement, 1] * sigma_y
        ) / 2.0
        marginal = sum(
            (numeric_effects[row] for row in range(16) if labels[row, measurement] == 1),
            np.zeros((2, 2), dtype=complex),
        )
        marginal_residual = max(marginal_residual, float(np.max(np.abs(marginal - target))))
    minimum_eigenvalue = min(
        float(np.min(np.linalg.eigvalsh((effect + effect.conjugate().T) / 2.0)))
        for effect in numeric_effects
    )
    return {
        "status": problem.status,
        "solver": problem.solver_stats.solver_name,
        "iterations": int(problem.solver_stats.num_iters),
        "solve_time_seconds": float(problem.solver_stats.solve_time),
        "eta": float(value),
        "normalization_residual": float(normalization_residual),
        "marginal_residual": float(marginal_residual),
        "minimum_effect_eigenvalue": minimum_eigenvalue,
    }


def symbolic_checks() -> dict[str, str]:
    """Prove the two algebraic identities used by the certificate."""

    symbols = sp.symbols("n1x n1y n2x n2y n3x n3y n4x n4y", real=True)
    n = [sp.Matrix(symbols[2 * index : 2 * index + 2]) for index in range(4)]
    r = [sp.zeros(2, 1) for _ in range(8)]
    vectors = (4 * (n[0] - n[1]), 4 * (n[1] - n[2]), 4 * (n[2] - n[3]), 4 * (n[0] + n[3]))
    for row, vector in zip(CHAIN_ROWS, vectors, strict=True):
        r[row] = vector
    low_characters = (
        [1] * 8,
        [int(mu[1]) for mu in MU],
        [int(mu[2]) for mu in MU],
        [int(mu[3]) for mu in MU],
    )
    for index, character in enumerate(low_characters):
        coefficient = sum(
            (r[row] * character[row] for row in range(8)), sp.zeros(2, 1)
        ) / 8
        assert sp.simplify(coefficient - n[index]) == sp.zeros(2, 1)

    p, q = sp.symbols("p q", real=True)
    norm_squared = 3 + 2 * sp.cos(p + q) - 2 * sp.cos(p) - 2 * sp.cos(q)
    factorized_slack = 8 * sp.cos((p + q) / 2) * sp.sin(p / 2) * sp.sin(q / 2)
    assert sp.trigsimp(1 - norm_squared - factorized_slack) == 0
    return {
        "walsh_identity": "PASS: the four low Walsh coefficients of the AK four-support function are symbolically n_1,n_2,n_3,n_4",
        "unit_vector_lemma_identity": "PASS: 1-||u(a)+u(c)-u(b)||^2 = 8 cos((p+q)/2) sin(p/2) sin(q/2)",
        "lemma_domain": "For p,q>=0 and p+q<=pi the right-hand side is nonnegative; the project domain gives strict ordered spans below pi.",
    }


def case_record(name: str, angle_values: tuple[float, float, float, float], direct_sdp: bool) -> dict[str, Any]:
    angles = np.asarray(angle_values, dtype=float)
    if not (angles[0] == 0.0 and np.all(np.diff(angles) > 0.0) and angles[-1] < np.pi):
        raise ValueError(f"inadmissible angles for {name}: {angles}")
    d_value = denominator(angles)
    primal = ak_fourier_primal(angles)
    dual = analytic_dual(angles, primal)
    socp = solve_fourier_socp(vectors_from_angles(angles))
    expected_objective = 8.0 * d_value
    record: dict[str, Any] = {
        "name": name,
        "angles_radians": angles.tolist(),
        "minimum_gap": float(np.min(np.diff(angles))),
        "pi_minus_alpha_4": float(np.pi - angles[-1]),
        "D": d_value,
        "formula_eta": 1.0 / d_value,
        "expected_fourier_objective": expected_objective,
        "ak_fourier": {
            key: value
            for key, value in primal.items()
            if key
            in {
                "basis_orthogonality_residual",
                "low_coefficient_residual",
                "reconstruction_residual",
                "objective",
            }
        },
        "analytic_dual": {
            key: value
            for key, value in dual.items()
            if key
            in {
                "chain_interpolation_residual",
                "stationarity_residual",
                "max_norm",
                "max_unit_ball_violation",
                "objective",
                "primal_dual_gap",
            }
        },
        "clarabel_fourier_socp": {
            key: value
            for key, value in socp.items()
            if key
            not in {"x", "residual_norms"}
        },
        "socp_minus_formula_objective": float(socp["objective"] - expected_objective),
        "socp_threshold_eta": float(8.0 / socp["objective"]),
        "socp_threshold_minus_formula_eta": float(8.0 / socp["objective"] - 1.0 / d_value),
    }
    if direct_sdp:
        parent = solve_direct_parent_sdp(angles)
        parent["eta_minus_formula"] = float(parent["eta"] - 1.0 / d_value)
        record["direct_sixteen_effect_parent_sdp"] = parent
    return record


def held_out_scan(seed: int = 20260912, count: int = 128) -> dict[str, Any]:
    """Numerically attack the certificate on unequal and near-boundary gaps."""

    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    max_analytic_gap = 0.0
    max_dual_violation = 0.0
    max_socp_formula = 0.0
    max_socp_gap = 0.0
    max_stationarity = 0.0
    for index in range(count):
        # Every fourth point uses log-uniform raw gaps to approach coincidences
        # and the alpha_4 -> pi boundary.  The others use broad Dirichlet gaps.
        if index % 4 == 0:
            raw = 10.0 ** rng.uniform(-8.0, 0.0, size=4)
        else:
            raw = rng.gamma(shape=rng.uniform(0.15, 2.5), scale=1.0, size=4)
        gaps = raw / np.sum(raw) * (np.pi - 2.0e-8)
        angles = np.asarray([0.0, gaps[0], gaps[0] + gaps[1], gaps[0] + gaps[1] + gaps[2]])
        primal = ak_fourier_primal(angles)
        dual = analytic_dual(angles, primal)
        socp = solve_fourier_socp(vectors_from_angles(angles))
        expected = 8.0 * denominator(angles)
        analytic_gap = abs(primal["objective"] - dual["objective"])
        formula_error = abs(socp["objective"] - expected)
        max_analytic_gap = max(max_analytic_gap, analytic_gap)
        max_dual_violation = max(max_dual_violation, dual["max_unit_ball_violation"])
        max_socp_formula = max(max_socp_formula, formula_error)
        max_socp_gap = max(max_socp_gap, socp["absolute_primal_dual_gap"])
        max_stationarity = max(max_stationarity, socp["x_stationarity_residual"])
        records.append(
            {
                "index": index,
                "minimum_gap": float(np.min(np.diff(angles))),
                "pi_minus_alpha_4": float(np.pi - angles[-1]),
                "socp_formula_objective_error": float(formula_error),
                "analytic_dual_ball_violation": float(dual["max_unit_ball_violation"]),
                "socp_primal_dual_gap": float(socp["absolute_primal_dual_gap"]),
            }
        )
    worst_formula = max(records, key=lambda item: item["socp_formula_objective_error"])
    closest_gap = min(records, key=lambda item: item["minimum_gap"])
    closest_endpoint = min(records, key=lambda item: item["pi_minus_alpha_4"])
    return {
        "seed": seed,
        "count": count,
        "generation": "mixed Dirichlet and log-uniform positive four-gap partitions of pi-2e-8; fourth gap is pi-alpha_4",
        "max_analytic_primal_dual_gap": max_analytic_gap,
        "max_analytic_dual_ball_violation": max_dual_violation,
        "max_clarabel_objective_error_vs_8D": max_socp_formula,
        "max_clarabel_reported_primal_dual_gap": max_socp_gap,
        "max_clarabel_x_stationarity_residual": max_stationarity,
        "worst_formula_case": worst_formula,
        "smallest_internal_gap_case": closest_gap,
        "closest_alpha4_to_pi_case": closest_endpoint,
    }


def gu_published_counterexample_check() -> dict[str, Any]:
    """Reproduce Grinko--Uola's out-of-scope unequal-length SOCP value."""

    vectors = np.asarray(
        [[0.7, 0.0, 0.0], [0.8, 0.4, 0.0], [0.3, 0.4, 0.0], [0.1, 0.2, 0.0]],
        dtype=float,
    )
    result = solve_fourier_socp(vectors)
    return {
        "scope": "implementation benchmark only; radii are unequal and this point is outside the frozen common-visibility target",
        "source_value_approximately": 7.957386,
        "computed_value": result["objective"],
        "difference_from_rounded_source_value": float(result["objective"] - 7.957386),
        "solver_status": result["status"],
        "absolute_primal_dual_gap": result["absolute_primal_dual_gap"],
        "primal_cone_violation": result["primal_cone_violation"],
        "dual_cone_violation": result["dual_cone_violation"],
        "x_stationarity_residual": result["x_stationarity_residual"],
    }


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    return value


def build_artifact(project: Path) -> dict[str, Any]:
    source_hash = sha256(project / "source.md")
    if source_hash != SOURCE_SHA256:
        raise RuntimeError(f"immutable source hash changed: {source_hash}")

    pi = math.pi
    cases = [
        ("symmetric-published", (0.0, pi / 4.0, pi / 2.0, 3.0 * pi / 4.0)),
        ("reproduction-unequal", (0.0, pi / 9.0, 7.0 * pi / 18.0, 5.0 * pi / 6.0)),
        ("adversarial-first-coincidence", (0.0, 1.0e-6, 1.4, 3.0)),
        ("adversarial-middle-coincidence", (0.0, 0.2, 0.200001, 2.8)),
        ("adversarial-last-coincidence", (0.0, 0.1, 2.9, 2.900001)),
        ("adversarial-near-antipodal", (0.0, 0.31, 1.77, pi - 1.0e-6)),
        ("adversarial-all-clustered", (0.0, 1.0e-6, 2.0e-6, 3.0e-6)),
        ("adversarial-opposite-cluster", (0.0, pi - 3.0e-6, pi - 2.0e-6, pi - 1.0e-6)),
    ]
    case_results = [case_record(name, values, direct_sdp=True) for name, values in cases]
    scan = held_out_scan()
    benchmark = gu_published_counterexample_check()

    tolerances = {
        "symbolic_checks": "exact",
        "analytic_numeric_identity": 2.0e-11,
        "analytic_dual_ball_violation": 2.0e-12,
        "clarabel_objective_vs_8D": 2.0e-7,
        "clarabel_relative_primal_dual_gap": 2.0e-8,
        "clarabel_stationarity": 2.0e-7,
        "direct_parent_eta_vs_formula": 2.0e-7,
        "direct_parent_equalities": 2.0e-7,
        "direct_parent_minimum_eigenvalue": -2.0e-7,
    }

    for case in case_results:
        assert case["ak_fourier"]["low_coefficient_residual"] <= tolerances["analytic_numeric_identity"]
        assert case["ak_fourier"]["reconstruction_residual"] <= tolerances["analytic_numeric_identity"]
        assert abs(case["analytic_dual"]["primal_dual_gap"]) <= tolerances["analytic_numeric_identity"]
        assert case["analytic_dual"]["max_unit_ball_violation"] <= tolerances["analytic_dual_ball_violation"]
        assert abs(case["socp_minus_formula_objective"]) <= tolerances["clarabel_objective_vs_8D"]
        assert case["clarabel_fourier_socp"]["relative_primal_dual_gap"] <= tolerances["clarabel_relative_primal_dual_gap"]
        assert case["clarabel_fourier_socp"]["x_stationarity_residual"] <= tolerances["clarabel_stationarity"]
        parent = case["direct_sixteen_effect_parent_sdp"]
        assert abs(parent["eta_minus_formula"]) <= tolerances["direct_parent_eta_vs_formula"]
        assert parent["normalization_residual"] <= tolerances["direct_parent_equalities"]
        assert parent["marginal_residual"] <= tolerances["direct_parent_equalities"]
        assert parent["minimum_effect_eigenvalue"] >= tolerances["direct_parent_minimum_eigenvalue"]

    assert scan["max_analytic_primal_dual_gap"] <= tolerances["analytic_numeric_identity"]
    assert scan["max_analytic_dual_ball_violation"] <= tolerances["analytic_dual_ball_violation"]
    assert scan["max_clarabel_objective_error_vs_8D"] <= tolerances["clarabel_objective_vs_8D"]
    assert benchmark["solver_status"] == cp.OPTIMAL
    # The paper prints both the objective and optimizer only approximately;
    # agreement at 2e-5 validates channel/sign conventions without treating
    # the rounded display as a high-precision reference value.
    assert abs(benchmark["difference_from_rounded_source_value"]) <= 2.0e-5

    return to_jsonable(
        {
            "job_id": "phys-00002-p02-research-1baba23d8e78",
            "status": "pass",
            "source_sha256": source_hash,
            "criterion": "N=4 Grinko-Uola Eq. (8)/(13): minimize eight Euclidean norms over all four unrestricted triple-index Fourier vectors; compatibility iff the minimum is at most 8 for unbiased qubit measurements",
            "symbolic_checks": symbolic_checks(),
            "cases": case_results,
            "held_out_scan": scan,
            "published_implementation_benchmark": benchmark,
            "tolerances": tolerances,
            "interpretation": "The explicit AK Fourier point and the explicit feasible Fourier dual have the same value 8D. Hence the unrestricted Fourier minimum is exactly 8D throughout the strict ordered planar common-length domain; solver agreement is corroboration, not the proof.",
            "limitations": "The analytic conclusion uses the Grinko-Uola necessary-and-sufficient theorem for finite unbiased binary qubit measurements. Numerical solver success alone is not used as a scientific certificate. No statement is made for unequal radii, biases, noncoplanar measurements, or boundary points outside the frozen strict domain.",
        }
    )


def log_lines(artifact: dict[str, Any]) -> list[str]:
    lines = [
        "N=4 unrestricted Fourier/SOCP and sixteen-effect parent audit",
        f"job_id={artifact['job_id']}",
        f"source_sha256={artifact['source_sha256']}",
        artifact["symbolic_checks"]["walsh_identity"],
        artifact["symbolic_checks"]["unit_vector_lemma_identity"],
    ]
    for case in artifact["cases"]:
        socp = case["clarabel_fourier_socp"]
        dual = case["analytic_dual"]
        parent = case["direct_sixteen_effect_parent_sdp"]
        lines.append(
            f"{case['name']}: D={case['D']:.16g}; q_SOCP={socp['objective']:.16g}; "
            f"q-8D={case['socp_minus_formula_objective']:.3e}; "
            f"solver_gap={socp['absolute_primal_dual_gap']:.3e}; "
            f"x_stationarity={socp['x_stationarity_residual']:.3e}; "
            f"analytic_dual_ball_violation={dual['max_unit_ball_violation']:.3e}; "
            f"eta_parent={parent['eta']:.16g}; eta_parent-1/D={parent['eta_minus_formula']:.3e}; "
            f"parent_eq_residual={max(parent['normalization_residual'], parent['marginal_residual']):.3e}; "
            f"parent_min_eigenvalue={parent['minimum_effect_eigenvalue']:.3e}"
        )
    scan = artifact["held_out_scan"]
    lines.append(
        f"held_out_scan: count={scan['count']}; max|q_SOCP-8D|={scan['max_clarabel_objective_error_vs_8D']:.3e}; "
        f"max_solver_gap={scan['max_clarabel_reported_primal_dual_gap']:.3e}; "
        f"max_analytic_dual_ball_violation={scan['max_analytic_dual_ball_violation']:.3e}"
    )
    benchmark = artifact["published_implementation_benchmark"]
    lines.append(
        f"GU unequal-length implementation benchmark: computed={benchmark['computed_value']:.12f}; "
        f"source_rounded={benchmark['source_value_approximately']:.6f}; "
        f"difference={benchmark['difference_from_rounded_source_value']:.3e} (outside target scope)"
    )
    lines.append("RESULT: PASS")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--log-out", type=Path)
    args = parser.parse_args()
    artifact = build_artifact(args.project.resolve())
    output = json.dumps(artifact, indent=2, ensure_ascii=False) + "\n"
    if args.json_out is not None:
        args.json_out.write_text(output, encoding="utf-8")
    if args.log_out is not None:
        args.log_out.write_text("\n".join(log_lines(artifact)) + "\n", encoding="utf-8")
    print("\n".join(log_lines(artifact)))


if __name__ == "__main__":
    main()
