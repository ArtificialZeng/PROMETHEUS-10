#!/usr/bin/env python3
"""Freeze the all-depth three-copy Schur recurrence before direct hold-outs.

This producer deliberately does not import the graph generator or the exact k=5
certificate.  It uses only the already established k<=4 scalar response, proves
the abstract six-port algebra symbolically, and freezes k=5 response values and
k=6 modular characteristic-polynomial coefficients for a later direct checker.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from flint import fmpz_mod_poly_ctx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
PASS2 = HERE / "cycle-schur-pass2.json"
FREEZE = HERE / "cycle-schur-pass3-freeze.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def poly_digest(expr: sp.Expr, *gens: sp.Symbol) -> tuple[str, int, int]:
    poly = sp.Poly(expr, *gens, domain=sp.ZZ)
    canonical = json.dumps(
        [[list(monomial), str(coefficient)] for monomial, coefficient in poly.terms()],
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest(), len(poly.terms()), poly.total_degree()


def scalar_states(J: sp.Symbol, z: sp.Symbol) -> dict[int, dict[str, sp.Expr]]:
    # alpha_k=A_k/(z U_k), beta_k=1/(z U_k), d_k=D_k U_k^2.
    A = z**2 + 1
    U = sp.Integer(1)
    states: dict[int, dict[str, sp.Expr]] = {}
    for k in range(2, 7):
        r = sp.expand(2 * A + 1 + (J**2 - z**2) * U)
        states[k] = {"A": A, "U": U, "r": r}
        A, U = sp.expand(A * r - 2), sp.expand(U * r)
    return states


def mod_state_and_characteristic(
    prime: int, j_num: int, j_den: int, target_k: int
) -> list[int]:
    ctx = fmpz_mod_poly_ctx(prime)
    zero = ctx(0)
    one = ctx(1)
    z = ctx.gen()
    j = (j_num * pow(j_den, -1, prime)) % prime
    j2 = ctx((j * j) % prime)
    A = z**2 + one
    U = one
    D = z
    for _k in range(2, target_k):
        r = 2 * A + one + (j2 - z**2) * U
        A, U, D = A * r - 2 * one, U * r, D**3 * U * (r - 3 * one)
    numerator = D * (A + 2 * one) * (A - one) ** 2
    denominator = z**3 * U
    quotient, remainder = divmod(numerator, denominator)
    if remainder != zero:
        raise RuntimeError("modular characteristic formula did not divide exactly")
    if quotient.degree() != {5: 108, 6: 324}[target_k]:
        raise RuntimeError(f"unexpected characteristic degree {quotient.degree()}")
    coefficients = [int(value) for value in quotient.coeffs()]
    if len(coefficients) != quotient.degree() + 1:
        raise RuntimeError("coefficient serialization lost internal zeros")
    return coefficients


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if not expected or Path(sys.executable).resolve() != Path(expected).resolve():
        raise RuntimeError(
            f"scientific Python mismatch: executable={sys.executable!r}, "
            f"PHYSICS_PYTHON={expected!r}"
        )
    if FREEZE.exists():
        raise RuntimeError(f"refusing to overwrite frozen prediction {FREEZE}")

    pass2 = json.loads(PASS2.read_text(encoding="utf-8"))
    J, z = sp.symbols("J z")

    # Universal signed six-port representative.  The interface vertices are
    # p0,p1,p2; the outer vertices are o0,o1,o2.  Three copy triangles have
    # positive holonomy and the unique quotient/macro cycle has holonomy -1.
    a, b, q = sp.symbols("a b q")
    C = sp.Matrix([[q, b, b], [b, q, -b], [b, -b, q]])
    B = sp.Matrix([[b, b, 0], [b, 0, b], [0, b, -b]])
    raw_response = a * sp.eye(3) - B.T * C.inv() * B
    output_gauge = sp.diag(1, -1, -1)
    canonical = (output_gauge * raw_response * output_gauge).applyfunc(
        lambda value: sp.factor(sp.cancel(value))
    )
    alpha_next = sp.factor((a * (q + b) - 2 * b**2) / (q + b))
    beta_next = sp.factor(b**2 / (q + b))
    expected_response = sp.ones(3) * beta_next + sp.eye(3) * (alpha_next - beta_next)
    if any(sp.cancel(value) != 0 for value in canonical - expected_response):
        raise RuntimeError("generic six-port response identity failed")
    det_C = sp.factor(C.det())
    if sp.cancel(det_C - (q - 2 * b) * (q + b) ** 2) != 0:
        raise RuntimeError("generic interface determinant identity failed")

    # Exhaust the abstract sign class.  Fixing three copy-cycle holonomies to
    # +1 and the independent interface holonomy to -1 leaves one gauge orbit.
    edges = [
        (0, 1), (0, 3), (1, 3),
        (0, 2), (0, 4), (2, 4),
        (1, 2), (1, 5), (2, 5),
    ]
    canonical_sign = [1, 1, 1, 1, 1, 1, -1, 1, -1]
    admissible = []
    gauge_equivalent = 0
    for mask in range(1 << len(edges)):
        signs = [(-1 if (mask >> index) & 1 else 1) for index in range(len(edges))]
        if signs[0] * signs[1] * signs[2] != 1:
            continue
        if signs[3] * signs[4] * signs[5] != 1:
            continue
        if signs[6] * signs[7] * signs[8] != 1:
            continue
        if signs[0] * signs[3] * signs[6] != -1:
            continue
        admissible.append(signs)
        found = False
        for gauge_mask in range(1 << 5):  # vertex 0 fixed to +1
            gauge = [1] + [(-1 if (gauge_mask >> (v - 1)) & 1 else 1) for v in range(1, 6)]
            transformed = [
                canonical_sign[index] * gauge[u] * gauge[v]
                for index, (u, v) in enumerate(edges)
            ]
            if transformed == signs:
                found = True
                break
        if found:
            gauge_equivalent += 1
    if len(admissible) != 32 or gauge_equivalent != 32:
        raise RuntimeError("abstract sign-cohomology orbit check failed")

    states = scalar_states(J, z)
    # Independently anchor the recurrence against the already certified k=4
    # response, without using any k=5 direct result.
    for k in (2, 3, 4):
        stored = pass2["schur_closure"]["responses"][str(k)]
        alpha_stored = sp.sympify(stored["alpha_k"], locals={"J": J, "z": z})
        beta_stored = sp.sympify(stored["beta_k"], locals={"J": J, "z": z})
        if sp.cancel(alpha_stored - states[k]["A"] / (z * states[k]["U"])) != 0:
            raise RuntimeError(f"A/U recurrence failed alpha anchor at k={k}")
        if sp.cancel(beta_stored - 1 / (z * states[k]["U"])) != 0:
            raise RuntimeError(f"A/U recurrence failed beta anchor at k={k}")

    state_records = {}
    for k in range(2, 7):
        A_k, U_k, r_k = states[k]["A"], states[k]["U"], states[k]["r"]
        A_hash, A_terms, A_degree = poly_digest(A_k, J, z)
        U_hash, U_terms, U_degree = poly_digest(U_k, J, z)
        r_hash, r_terms, r_degree = poly_digest(r_k, J, z)
        state_records[str(k)] = {
            "A_k": sp.sstr(A_k),
            "U_k": sp.sstr(U_k),
            "r_k": sp.sstr(r_k),
            "A_sha256": A_hash,
            "U_sha256": U_hash,
            "r_sha256": r_hash,
            "A_terms": A_terms,
            "U_terms": U_terms,
            "r_terms": r_terms,
            "A_total_degree": A_degree,
            "U_total_degree": U_degree,
            "r_total_degree": r_degree,
        }

    response_points = [
        (2, 5, 7, 11),
        (-3, 7, 5, 13),
        (11, 17, 19, 23),
    ]
    k5_predictions = []
    A5, U5 = states[5]["A"], states[5]["U"]
    for jn, jd, zn, zd in response_points:
        substitutions = {J: sp.Rational(jn, jd), z: sp.Rational(zn, zd)}
        alpha_value = sp.factor((A5 / (z * U5)).subs(substitutions))
        beta_value = sp.factor((1 / (z * U5)).subs(substitutions))
        if alpha_value.q == 0 or beta_value.q == 0:
            raise RuntimeError("invalid frozen response value")
        k5_predictions.append({
            "J": f"{jn}/{jd}",
            "z": f"{zn}/{zd}",
            "alpha_5": str(alpha_value),
            "beta_5": str(beta_value),
        })

    modular_cases = [
        {"prime": 1000003, "J_num": 7, "J_den": 13},
        {"prime": 1000033, "J_num": 11, "J_den": 17},
    ]
    for case in modular_cases:
        coefficients = mod_state_and_characteristic(
            case["prime"], case["J_num"], case["J_den"], 6
        )
        encoded = json.dumps(coefficients, separators=(",", ":")).encode("ascii")
        case["coefficient_order"] = "ascending powers of z"
        case["degree"] = len(coefficients) - 1
        case["predicted_coefficients"] = coefficients
        case["predicted_coefficients_sha256"] = hashlib.sha256(encoded).hexdigest()

    payload = {
        "schema_version": 1,
        "job_id": os.environ.get("PHYSICS_JOB_ID", "phys-00021-p01-research-407f59d97b19"),
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
        },
        "input_binding": {
            "source_sha256": sha256(PROJECT / "source.md"),
            "pass2_certificate": "evidence/cycle-schur-pass2.json",
            "pass2_certificate_sha256": sha256(PASS2),
            "direct_graph_generator_used": False,
            "exact_k5_certificate_used": False,
        },
        "all_depth_sign_lemma": {
            "cycle_rank_identity": "c_(k+1)=3*c_k+1",
            "copy_holonomies": [1, 1, 1],
            "quotient_macro_holonomy": -1,
            "canonical_edges": [[list(edge), sign] for edge, sign in zip(edges, canonical_sign)],
            "admissible_signings": len(admissible),
            "signings_in_one_vertex_gauge_orbit": gauge_equivalent,
            "interpretation": "Three translated address-prefix copies inherit all internal +1-sector cycle data; the unique self-similar quotient cycle has the base-cell holonomy -1, so every depth is gauge-equivalent to this six-port representative.",
        },
        "generic_schur_identity": {
            "q_k": "2*alpha_k-z+J^2/z",
            "det_C_k": "(q_k-2*beta_k)*(q_k+beta_k)^2",
            "alpha_next": "alpha_k-2*beta_k^2/(q_k+beta_k)",
            "beta_next": "beta_k^2/(q_k+beta_k)",
            "output_boundary_gauge": [1, -1, -1],
            "symbolic_residual_zero": True,
        },
        "cancellation_safe_polynomial_recurrence": {
            "definitions": "alpha_k=A_k/(z U_k), beta_k=1/(z U_k), d_k=D_k U_k^2",
            "base_k2": {"A_2": "z^2+1", "U_2": "1", "D_2": "z"},
            "update": {
                "r_k": "2*A_k+1+(J^2-z^2)*U_k",
                "A_next": "A_k*r_k-2",
                "U_next": "U_k*r_k",
                "D_next": "D_k^3*U_k*(r_k-3)",
            },
            "reconstruction": {
                "d_k": "D_k*U_k^2",
                "P_k": "exact quotient D_k*(A_k+2)*(A_k-1)^2/(z^3*U_k)",
            },
            "anchors_k2_through_k4_exact": True,
            "states": state_records,
        },
        "frozen_k5_direct_response_tests": k5_predictions,
        "frozen_k6_modular_characteristic_tests": modular_cases,
        "scope": {
            "prediction_only": "No direct k=5 response, direct k=6 matrix, or exact-k5 factor certificate was read by this producer.",
            "not_claimed": "No crossing-location continuation, scaling law, other cycle sector, many-body parity projection, thermodynamic transition, or novelty claim.",
        },
    }
    FREEZE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "prediction_frozen",
        "file": str(FREEZE.relative_to(PROJECT)),
        "sha256": sha256(FREEZE),
        "k5_response_points": len(k5_predictions),
        "k6_modular_cases": [
            {"prime": case["prime"], "hash": case["predicted_coefficients_sha256"]}
            for case in modular_cases
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
