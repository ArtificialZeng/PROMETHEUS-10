#!/usr/bin/env python3
"""Exact regression checks for the all-n Pfaffian-congruence proof.

The finite checks are diagnostics only; the all-n certificate is the rational
kernel identity and the algebraic Pfaffian-minor argument recorded separately.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pfaffian_third_column import KernelCoefficients, add, multiply, pfaffian, shift  # noqa: E402
import pfaffian_osasm as source_pf  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    u, v, r = sp.symbols("u v r")
    b = (v - u) / ((1 - u * v) * ((1 - r * u) * (1 - r * v) - u * v))
    c = -r / 2
    x = u / (1 - c * u)
    y = v / (1 - c * v)
    centered_from_transform = b.subs({u: x, v: y}, simultaneous=True) / (
        (1 - c * u) * (1 - c * v)
    )
    d_minus = (1 + r * u / 2) * (1 + r * v / 2) - u * v
    d_plus = (1 - r * u / 2) * (1 - r * v / 2) - u * v
    centered_closed = (v - u) / (d_minus * d_plus)

    checks: list[tuple[str, bool, str]] = []
    checks.append((
        "centered binomial-transform kernel",
        sp.cancel(centered_from_transform - centered_closed) == 0,
        "T(-r/2) B_r T(-r/2)^T has the stated rational generating function",
    ))
    checks.append((
        "simultaneous-sign parity",
        sp.cancel(centered_closed.subs({u: -u, v: -v}, simultaneous=True) + centered_closed) == 0,
        "E(-u,-v)=-E(u,v), hence E_ij=0 for i+j even",
    ))
    a = (1 + u) * (1 + v) * b
    checks.append((
        "source kernel split",
        sp.cancel(a - (v - u) * (1 + u) * (1 + v) /
                  ((1 - u * v) * ((1 - r * u) * (1 - r * v) - u * v))) == 0,
        "A=(I+S)B_r(I+S)^T",
    ))
    laurent_ok = True
    # The proof only needs i=m-3,m-2, hence i>=1 for m>=4.  The i=0 next
    # coefficient is exceptional because the nominal i-1 contributions do
    # not exist.
    for i in range(1, 15):
        scaled = sp.cancel(source_pf.last_column(i) * source_pf.t ** (i + 1))
        leading = sp.cancel(scaled.subs(source_pf.t, 0))
        next_coefficient = sp.cancel(sp.diff(scaled, source_pf.t).subs(source_pf.t, 0))
        expected_leading = (-1) ** (i + 1) * source_pf.r ** (-i - 2)
        expected_next = (
            (-1) ** i
            * (i + source_pf.r + source_pf.r**2)
            * source_pf.r ** (-i - 2)
        )
        laurent_ok &= sp.cancel(leading - expected_leading) == 0
        laurent_ok &= sp.cancel(next_coefficient - expected_next) == 0
    checks.append((
        "BFK last-column Laurent coefficients",
        laurent_ok,
        "independent exact extraction from the source rational function for i=1..14",
    ))
    n = sp.symbols("n", integer=True, positive=True)
    scalar_difference = sp.expand(
        ((1 - r - r**2) + r * (1 + (n - 1) * r))
        - (1 + (n - 2) * r**2)
    )
    checks.append((
        "final scalar reduction",
        scalar_difference == 0,
        "the minor relation converts the BFK low-t formula to the target RHS",
    ))

    for target_n in range(2, 9):
        order = 2 * target_n
        kernel = KernelCoefficients(order)
        c0, _ = pfaffian(tuple(range(order - 2)), kernel)
        c1, _ = pfaffian(tuple(range(order - 3)) + (order - 2,), kernel)
        expected = multiply(add((1,), shift((1,), 1, target_n - 1)), c0)
        checks.append((
            f"finite symbolic-polynomial regression n={target_n}",
            add(c1, expected, scale=-1) == (),
            f"C1=(1+{target_n - 1}r)C0 at matrix order {order}",
        ))

    lines = ["Exact all-n reduction regression checks"]
    failures: list[str] = []
    for name, passed, detail in checks:
        lines.append(f"{name}: {'PASS' if passed else 'FAIL'}; {detail}")
        if not passed:
            failures.append(name)
    lines.append(f"OVERALL: {'PASS' if not failures else 'FAIL'}")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("failed checks: " + ", ".join(failures))


if __name__ == "__main__":
    main()
