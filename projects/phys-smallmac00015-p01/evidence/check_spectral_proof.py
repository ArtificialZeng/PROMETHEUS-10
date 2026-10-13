#!/usr/bin/env python3
"""Symbolic and exact-arithmetic stress checks for spectral-gap-proof.md."""
from __future__ import annotations

from fractions import Fraction as F

import sympy as sp

from test_spectral_gap import exact_ldl_pivots, normalize, restricted_shift, split


def main() -> None:
    a, b = sp.symbols("a b")
    g = lambda z: z / (1 - 2 * z)
    claimed = 4 * a * b * (1 - a - b) / (
        (1 - 2 * a) * (1 - 2 * b) * (1 - 2 * a - 2 * b)
    )
    assert sp.factor(g(a + b) - g(a) - g(b) - claimed) == 0
    print("symbolic_superadditivity_factor=PASS")

    d1, d2, d3, lam = sp.symbols("d1 d2 d3 lam")
    diag = sp.diag(d1 - lam, d2 - lam, d3 - lam)
    lhs = (diag - sp.ones(3, 3)).det()
    rhs = (d1 - lam) * (d2 - lam) * (d3 - lam) * (
        1 - 1 / (d1 - lam) - 1 / (d2 - lam) - 1 / (d3 - lam)
    )
    assert sp.factor(lhs - rhs) == 0
    print("symbolic_matrix_determinant_lemma_N3=PASS")

    boundary_count = 0
    exact_gap_count = 0
    for n in range(3, 13):
        delta = F(1, 37)
        p = normalize([F(1), F(1)] + [delta] * (n - 2))
        expected = F(2) + F(n - 2) * delta
        # Direct exact eigenpair check for v=e1-e2.
        v = [F(1), F(-1)] + [F(0)] * (n - 2)
        for i in range(n):
            mv_i = v[i] / p[i] - sum(v, F(0))
            assert mv_i == expected * v[i]
        boundary_count += 1

        cases = [
            p,
            [F(1, 2)] + split(F(1, 2), n - 1),
            [F(3, 5)] + split(F(2, 5), n - 1),
            normalize([F(1, 3**i) for i in range(n)]),
        ]
        for case in cases:
            assert all(z > 0 for z in exact_ldl_pivots(restricted_shift(case)))
            exact_gap_count += 1
    print(f"exact_boundary_eigenpairs={boundary_count} range=N3..N12 status=PASS")
    print(f"exact_restricted_gap_certificates={exact_gap_count} status=PASS")
    print("audit_limit=symbolic_and_exact_stress_check_not_fresh_referee")
    print("status=PASS")


if __name__ == "__main__":
    main()
