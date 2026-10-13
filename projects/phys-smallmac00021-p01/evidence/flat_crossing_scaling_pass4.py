#!/usr/bin/env python3
"""Exact flat-band collision and scaling consequences of the pass-3 recurrence.

This producer uses only the already proved scalar recurrence.  In particular it
does not import or construct the depth-six graph; that is left to the separate
direct checker.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
RESULT = HERE / "flat-crossing-scaling-pass4.json"
PASS3 = HERE / "cycle-schur-pass3.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if not expected or Path(sys.executable).resolve() != Path(expected).resolve():
        raise RuntimeError(
            f"scientific Python mismatch: executable={sys.executable!r}, "
            f"PHYSICS_PYTHON={expected!r}"
        )
    if RESULT.exists():
        raise RuntimeError(f"refusing to overwrite {RESULT}")

    source_digest = sha256(PROJECT / "source.md")
    if source_digest != "2277938a2d7c3fb54fd70b23283223428aed10897daeb1379f36c16fe85b2d12":
        raise RuntimeError("immutable source hash changed")
    pass3 = json.loads(PASS3.read_text(encoding="utf-8"))
    if pass3["verification"]["symbolic_six_port_residual_zero"] is not True:
        raise RuntimeError("pass-3 recurrence certificate is not in passing state")

    # t=J^2, y=z^2, and s=t+y is the flat-band factor.  Work in
    # ZZ[s,t] via y=s-t so exact divisibility by s is explicit.
    s, t, j = sp.symbols("s t J", real=True)
    y = s - t
    A = sp.Integer(1) + y
    U = sp.Integer(1)
    states: dict[int, dict[str, sp.Expr]] = {}
    for k in range(2, 9):
        r = sp.expand(2 * A + 1 + (t - y) * U)
        expected_A0 = 1 - 3 ** (k - 2) * t
        expected_U0 = sp.Integer(3 ** (k - 2))
        if sp.expand(A.subs(s, 0) - expected_A0) != 0:
            raise RuntimeError(f"flat-locus A formula failed at k={k}")
        if sp.expand(U.subs(s, 0) - expected_U0) != 0:
            raise RuntimeError(f"flat-locus U formula failed at k={k}")
        quotient, remainder = sp.div(sp.Poly(r - 3, s, domain=sp.ZZ[t]), sp.Poly(s, s, domain=sp.ZZ[t]))
        if remainder.as_expr() != 0:
            raise RuntimeError(f"r_k-3 is not divisible by s at k={k}")
        R0 = sp.expand(quotient.as_expr().subs(s, 0))
        if R0 != 5 ** (k - 2):
            raise RuntimeError(f"transverse flat-factor quotient failed at k={k}")
        states[k] = {"A": A, "U": U, "r": r, "R0": R0}
        A = sp.expand(A * r - 2)
        U = sp.expand(U * r)

    # At depth k, D_k/s^c has nonzero flat-locus coefficient
    # b_k z^(3^(k-2)), where b_k=15^e and e=(3^(k-2)-2k+3)/4.
    # Combining it with the exact characteristic quotient leaves the stated
    # normalized collision polynomial.  For k=6 it is t^41(1-27t).
    k = 6
    c6 = (3 ** (k - 2) - 1) // 2
    exponent_b6 = (3 ** (k - 2) - 2 * k + 3) // 4
    normalized_k6 = sp.Poly(t ** (c6 + 1) * (1 - 3 ** (k - 3) * t), t, domain=sp.ZZ)
    if (
        c6 != 40
        or exponent_b6 != 18
        or sp.expand(normalized_k6.as_expr() - t**41 * (1 - 27 * t)) != 0
    ):
        raise RuntimeError("k=6 reduced collision polynomial changed")

    collision_J = sp.Poly(1 - 27 * j**2, j, domain=sp.QQ)
    positive_count = int(collision_J.count_roots(sp.Rational(0), sp.Rational(2)))
    interval = (sp.Rational(192450089729875, 10**15), sp.Rational(192450089729876, 10**15))
    interval_count = int(collision_J.count_roots(*interval))
    if positive_count != 1 or interval_count != 1:
        raise RuntimeError("positive k=6 collision root isolation failed")

    # The uncancelled symmetric channel at depth k is A_(k-1).  Its
    # derivatives give the exact transverse branch slope.  Here n=k-3.
    n = k - 3
    factor = states[k - 1]["A"]
    t0 = sp.Rational(1, 3**n)
    y_derivative = sp.diff(factor, s).subs({s: 0, t: t0})
    flat_direction_derivative = sp.diff(factor.subs(s, 0), t).subs(t, t0)
    t_derivative_at_fixed_y = sp.simplify(y_derivative + flat_direction_derivative)
    slope = sp.factor(t_derivative_at_fixed_y / y_derivative)
    separation = sp.factor(1 - slope)
    if (y_derivative, t_derivative_at_fixed_y, slope, separation) != (
        sp.Rational(197, 3), sp.Rational(116, 3), sp.Rational(116, 197), sp.Rational(81, 197)
    ):
        raise RuntimeError("k=6 transverse derivative formula failed")

    table = []
    for depth in range(3, 9):
        order = depth - 3
        denominator = 5 ** (order + 1) + 6 * 3**order + 1
        numerator = 5 ** (order + 1) - 6 * 3**order + 1
        table.append({
            "k": depth,
            "cycle_flat_positive_multiplicity": (3 ** (depth - 2) - 1) // 2,
            "collision_J_squared": f"1/{3**order}" if order else "1",
            "collision_J": "1" if order == 0 else f"3^(-{order}/2)",
            "source_lambda": "1/2" if order == 0 else f"3^(-{order}/2)/2",
            "dispersive_dx_dJ": str(sp.Rational(numerator, denominator)),
            "first_order_x_separation": str(sp.Rational(12 * 3**order, denominator)),
        })

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
        "input_binding": {
            "source_sha256": source_digest,
            "pass3_recurrence_file": "evidence/cycle-schur-pass3.json",
            "pass3_recurrence_sha256": sha256(PASS3),
            "direct_graph_used_by_producer": False,
            "sector": "all canonical Hermitian cycle generators projected to +1",
            "normalization": "A_k=2h_k, C_k(z,J)=det(zI-A_k), t=J^2, y=z^2, s=t+y; physical x uses y=-x^2 and source lambda=|x|/2",
        },
        "all_depth_flat_locus": {
            "domain": "integer k>=2; nonzero real J for collision classification",
            "A_k_at_s_zero": "1-3^(k-2)*t",
            "U_k_at_s_zero": "3^(k-2)",
            "r_k_at_s_zero": "3",
            "exact_divisibility": "r_k-3=s*R_k(s,t)",
            "R_k_at_s_zero": "5^(k-2)",
            "cycle_exponent": "c_k=(3^(k-2)-1)/2",
            "D_reduced_coefficient": "(D_k/s^c_k)|_(s=0)=b_k*z^(3^(k-2)), b_k=15^((3^(k-2)-2k+3)/4), hence nonzero for z!=0",
            "characteristic_remainder": "(C_k/s^c_k)|_(s=0)=(-1)^(c_k-1)*b_k*3^(k-1)*t^(c_k+1)*(1-3^(k-3)*t)",
            "unique_nonzero_collision": "J_k^2=3^(-(k-3)), so J_k^+=3^(-(k-3)/2) and J_k^-=-J_k^+ for every k>=3",
            "multiplicity": "generic positive flat band c_k; at J=+/-J_k each physical sign x=+/-|J_k| has multiplicity exactly c_k+1",
            "channel": "the extra simple root is the boundary-symmetric A1 channel alpha+2 beta; cycle-flat modes have zero corner response",
            "scaling": "J_(k+1)/J_k=lambda_(k+1)/lambda_k=1/sqrt(3), Delta_k=0 for the tracked crossing",
        },
        "transversality": {
            "n_definition": "n=k-3",
            "partial_A_(k-1)_partial_y_at_collision": "(5^(n+1)+6*3^n+1)/12",
            "dispersive_dx_dJ": "(5^(n+1)-6*3^n+1)/(5^(n+1)+6*3^n+1)",
            "first_order_x_separation_from_flat": "12*3^n/(5^(n+1)+6*3^n+1)",
            "source_lambda_separation": "one half of the x separation",
            "k6": {
                "partial_fixed_y": str(t_derivative_at_fixed_y),
                "partial_y": str(y_derivative),
                "dispersive_dx_dJ": str(slope),
                "flat_dx_dJ": "1",
                "first_order_x_separation": str(separation),
                "first_order_source_lambda_separation": str(separation / 2),
            },
        },
        "k6_collision": {
            "cycle_exponent": c6,
            "reduced_D_constant_exponent": {"base": 15, "exponent": exponent_b6},
            "primitive_normalized_flat_locus_remainder": sp.sstr(normalized_k6.as_expr()),
            "nonzero_collision_polynomial_in_J": "1-27*J^2",
            "positive_root_count_on_0_lt_J_le_2": positive_count,
            "positive_root_isolating_interval": [str(interval[0]), str(interval[1])],
            "isolated_root_count": interval_count,
            "J_exact": "sqrt(3)/9=1/(3*sqrt(3))",
            "J_decimal": float(sp.sqrt(3) / 9),
            "x_exact": "sqrt(3)/9",
            "source_lambda_exact": "sqrt(3)/18",
            "predicted_positive_multiplicity": c6 + 1,
        },
        "finite_table": table,
        "limitations": [
            "The all-depth statement is conditional on the signed recurrence proved in pass 3 and remains restricted to the all-cycle-+1 finite open single-particle sector.",
            "No physical fermion-parity projection, many-body gap, other cycle sector, or thermodynamic phase transition is inferred.",
            "This producer does not independently reconstruct the graph; the separate replay performs the direct k=6 test.",
            "Literature novelty is not assessed by this calculation.",
        ],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass",
        "result": str(RESULT.relative_to(PROJECT)),
        "k6_J": result["k6_collision"]["J_exact"],
        "k6_multiplicity": result["k6_collision"]["predicted_positive_multiplicity"],
        "k6_slope": result["transversality"]["k6"]["dispersive_dx_dJ"],
        "all_depth_ratio": "1/sqrt(3)",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
