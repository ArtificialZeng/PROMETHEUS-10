#!/usr/bin/env python3
"""Exact checks for evidence/universal-annulus-ordering-proof.md."""

from __future__ import annotations

import hashlib
import json
import platform
from fractions import Fraction
from pathlib import Path

import numpy
import scipy
import sympy as sp


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "evidence" / "universal-annulus-ordering-check.log"
JOB_ID = "phys-00014-p01-research-a9dc33666c01"
EXPECTED_SOURCE_SHA256 = "09e4298d6fe204d0a61183176bc886c43625d5978131ec455d594ce331874d4f"


def main() -> None:
    source_sha = hashlib.sha256((PROJECT / "source.md").read_bytes()).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("immutable source.md hash mismatch")

    r, b, c, x, t = sp.symbols("r b c x t", positive=True)
    m = sp.symbols("m", real=True)
    phi = (1 - r**2) * sp.exp(-r**2 / 2)
    f1 = r * sp.exp(-r**2 / 2)
    f2 = r**2 * (3 - r**2) * sp.exp(-r**2 / 2)

    def op(index: int, field: sp.Expr, f: sp.Expr) -> sp.Expr:
        return sp.simplify(
            -sp.diff(f, r, 2)
            - sp.diff(f, r) / r
            + (sp.Rational(index) / r - field * r / 2) ** 2 * f
        )

    # Previously derived exact sign numerator for d R_1 / dx.
    P = (
        c**3 * x**2 * sp.exp(c * x)
        - c**3 * x * sp.exp(c * x)
        + c**2 * x**2 * sp.exp(c)
        + c**2 * x**2 * sp.exp(c * x)
        - 2 * c**2 * x * sp.exp(c * x)
        + 2 * c * x * sp.exp(c)
        - 3 * c * x * sp.exp(c * x)
        + c * sp.exp(c * x)
        - sp.exp(c)
        + sp.exp(c * x)
    )
    H = sp.simplify(sp.exp(c * t - c) * P.subs(x, 1 - t))
    h3_expected = c**3 * sp.exp(c * t) * (
        c**2 * (1 - t) ** 2 - 4 * c * (1 - t) - 1
    )

    C = sp.symbols("C", real=True)
    shift_expected = (b - 2) * (-m + (b + 2) * C / 4)
    potential_shift_average = sp.expand(
        -m * (b - 2) + (b**2 - 4) * C / 4
    )

    z = sp.symbols("z", positive=True)
    moment1 = sp.integrate(
        (sp.Rational(4, 5) - z) * z * sp.exp(-z),
        (z, sp.Rational(1, 16), 1),
    )
    moment2 = sp.integrate(
        (sp.Rational(4, 5) - z) * z**2 * (3 - z) ** 2 * sp.exp(-z),
        (z, sp.Rational(1, 16), 1),
    )
    moment1_expected = sp.exp(-1) * (
        sp.Rational(17, 5) - sp.Rational(1637, 1280) * sp.exp(sp.Rational(15, 16))
    )
    moment2_expected = sp.exp(-1) * (
        sp.Rational(344, 5)
        - sp.Rational(140644469, 5242880) * sp.exp(sp.Rational(15, 16))
    )

    q = sp.symbols("q", positive=True)
    alpha = sp.symbols("alpha", positive=True)
    delta = sp.symbols("delta", real=True)
    gamma = b**2 * (1 + q) / 8
    completed = sp.expand(
        alpha * (m - b / (2 * alpha)) ** 2
        + b**2 * ((1 + q) / 8 - 1 / (4 * alpha))
    )

    symbolic = {
        "barta_identity": sp.simplify(op(0, b, phi) / phi - (6 + (b**2 - 4) * r**2 / 4)) == 0,
        "f1_b2_eigenmode": sp.simplify(op(1, 2, f1) - 2 * f1) == 0,
        "f2_b2_eigenmode": sp.simplify(op(2, 2, f2) - 6 * f2) == 0,
        "f1_outer_neumann": sp.diff(f1, r).subs(r, 1) == 0,
        "f2_outer_neumann": sp.diff(f2, r).subs(r, 1) == 0,
        "H_at_zero": sp.simplify(H.subs(t, 0)) == 0,
        "H_prime_at_zero": sp.simplify(sp.diff(H, t).subs(t, 0)) == 0,
        "H_second_at_zero": sp.simplify(sp.diff(H, t, 2).subs(t, 0) - c**2 * (c**2 - 1)) == 0,
        "H_third_factorization": sp.simplify(sp.diff(H, t, 3) - h3_expected) == 0,
        "field_shift_identity": sp.simplify(potential_shift_average - shift_expected) == 0,
        "moment1_antiderivative": sp.simplify(moment1 - moment1_expected) == 0,
        "moment2_antiderivative": sp.simplify(moment2 - moment2_expected) == 0,
        "constant_mode_completion": sp.simplify(completed - (alpha * m**2 - b * m + gamma)) == 0,
    }

    u = Fraction(15, 16)
    exp_upper = 1 + u + u**2 / 2 + (u**3 / 6) / (1 - u / 4)
    rational = {
        "exp_tail_upper_exact": str(exp_upper),
        "exp_tail_upper_below_64_over_25": exp_upper < Fraction(64, 25),
        "moment1_positive_lower": str(Fraction(17, 5) - Fraction(1637, 1280) * Fraction(64, 25)),
        "moment2_positive_lower": str(Fraction(344, 5) - Fraction(140644469, 5242880) * Fraction(64, 25)),
        "moment1_lower_positive": Fraction(17, 5) - Fraction(1637, 1280) * Fraction(64, 25) > 0,
        "moment2_lower_positive": Fraction(344, 5) - Fraction(140644469, 5242880) * Fraction(64, 25) > 0,
        "small_a_constant_factor": str(Fraction(34, 5)),
        "small_a_constant_below_8": Fraction(34, 5) < 8,
        "thin_ring_trial_upper": str(Fraction(252, 25)),
        "thin_ring_upper_below_12": Fraction(252, 25) < 12,
        "exp_3_over_2_partial_sum": str(sum(Fraction(3, 2) ** k / __import__("math").factorial(k) for k in range(4))),
        "exp_3_over_2_partial_sum_above_4": sum(Fraction(3, 2) ** k / __import__("math").factorial(k) for k in range(4)) > 4,
    }

    all_checks = all(symbolic.values()) and all(
        value for key, value in rational.items() if key.endswith(("positive", "_8", "_12", "_4", "_25"))
    )
    # Explicitly avoid depending on the suffix filter for the decisive booleans.
    all_checks = all_checks and all(
        rational[key]
        for key in (
            "exp_tail_upper_below_64_over_25",
            "moment1_lower_positive",
            "moment2_lower_positive",
            "small_a_constant_below_8",
            "thin_ring_upper_below_12",
            "exp_3_over_2_partial_sum_above_4",
        )
    )

    record = {
        "job_id": JOB_ID,
        "source_sha256": source_sha,
        "environment": {
            "python": platform.python_version(),
            "numpy": numpy.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
        "symbolic_checks": symbolic,
        "exact_rational_checks": rational,
        "verdict": "PASS" if all_checks else "FAIL",
    }
    OUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": all_checks, "output": str(OUT.relative_to(PROJECT))}, sort_keys=True))
    if not all_checks:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
