#!/usr/bin/env python3
"""Adversarial exact-rational tests of the normalized complete-graph gap.

For p_i=x_i/sum(x), M/k0=diag(1/p_i)-11^T.  Each test uses rational
positive p with sum one.  Besides a floating eigensolve used only to locate
possible counterexamples, the script restricts M-2I to p^perp and checks an
exact Fraction LDL^T factorization.  Positive pivots are an exact certificate
for that finite input, not a proof for all inputs.
"""
from __future__ import annotations

from fractions import Fraction as F
import platform

import numpy as np
import scipy


def normalize(xs: list[F]) -> list[F]:
    total = sum(xs, F(0))
    assert total > 0 and all(x > 0 for x in xs)
    return [x / total for x in xs]


def split(total: F, n: int) -> list[F]:
    weights = [F(i) for i in range(1, n + 1)]
    scale = total / sum(weights, F(0))
    return [scale * w for w in weights]


def rational_matrix(p: list[F]) -> list[list[F]]:
    n = len(p)
    return [[(F(1, 1) / p[i] if i == j else F(0)) - F(1)
             for j in range(n)] for i in range(n)]


def restricted_shift(p: list[F]) -> list[list[F]]:
    """Return B^T(M-2I)B exactly, with columns spanning p^perp."""
    n = len(p)
    m = rational_matrix(p)
    for i in range(n):
        m[i][i] -= F(2)
    # b_j=e_j-(p_j/p_last)e_last, j=0,...,n-2.
    b = [[F(0) for _ in range(n - 1)] for _ in range(n)]
    for j in range(n - 1):
        b[j][j] = F(1)
        b[n - 1][j] = -p[j] / p[n - 1]
    h = [[F(0) for _ in range(n - 1)] for _ in range(n - 1)]
    for a in range(n - 1):
        for c in range(n - 1):
            h[a][c] = sum(
                b[i][a] * m[i][j] * b[j][c]
                for i in range(n) for j in range(n)
            )
    return h


def exact_ldl_pivots(a: list[list[F]]) -> list[F]:
    n = len(a)
    ell = [[F(0) for _ in range(n)] for _ in range(n)]
    pivots: list[F] = []
    for j in range(n):
        ell[j][j] = F(1)
        d = a[j][j] - sum(ell[j][k] * ell[j][k] * pivots[k]
                           for k in range(j))
        if d <= 0:
            raise AssertionError(f"nonpositive exact LDL pivot at {j}: {d}")
        pivots.append(d)
        for i in range(j + 1, n):
            ell[i][j] = (
                a[i][j]
                - sum(ell[i][k] * ell[j][k] * pivots[k]
                      for k in range(j))
            ) / d
    return pivots


def family_cases(n: int) -> list[tuple[str, list[F], F | None]]:
    # Small enough to approach the sharp boundary while retaining a useful
    # floating diagnostic beside the exact rational certificate.
    tiny = F(1, 10**6)
    boundary_x = [F(1), F(1)] + [tiny] * (n - 2)
    q_above = F(500001, 10**6)
    q_below = F(499999, 10**6)
    dominant = F(999, 1000)
    two_heavy_tail = F(1, 1000)
    asymmetric_tail = F(1, 10**6)
    asymmetric_first = F(1, 2) + F(1, 10**8)
    cases = [
        ("specified-boundary", normalize(boundary_x),
         F(2) + F(n - 2) * tiny),
        ("half-above", [q_above] + split(F(1) - q_above, n - 1), None),
        ("half-below", [q_below] + split(F(1) - q_below, n - 1), None),
        ("dominant-999/1000", [dominant] + split(F(1) - dominant, n - 1), None),
        ("two-heavy", [((F(1) - two_heavy_tail) / 2)] * 2
         + split(two_heavy_tail, n - 2), None),
        ("at-half", [F(1, 2)] + split(F(1, 2), n - 1), None),
        ("effective-two-half-above",
         [asymmetric_first, F(1) - asymmetric_tail - asymmetric_first]
         + split(asymmetric_tail, n - 2), None),
        ("geometric", normalize([F(1, 2**i) for i in range(n)]), None),
    ]
    for _, p, _ in cases:
        assert sum(p, F(0)) == 1 and all(v > 0 for v in p)
    return cases


def run() -> None:
    print("ADVERSARIAL_RATIONAL_SPECTRAL_GAP_TESTS")
    print(f"python={platform.python_version()} numpy={np.__version__} scipy={scipy.__version__}")
    print("normalization=M/k0=diag(1/p)-11^T, p=x/sum(x)")
    print("exact_check=Fraction LDL^T positivity of B^T(M/k0-2I)B on p^perp")
    count = 0
    smallest_gap = float("inf")
    worst = ""
    for n in range(4, 11):
        for name, p, expected_boundary in family_cases(n):
            h = restricted_shift(p)
            pivots = exact_ldl_pivots(h)
            mf = np.diag([float(F(1) / z) for z in p]) - np.ones((n, n))
            eig = np.linalg.eigvalsh(mf)
            kernel = abs(eig[0])
            gap = eig[1] - 2.0
            if gap < smallest_gap:
                smallest_gap, worst = gap, f"N={n}:{name}"
            assert kernel < 3e-7
            assert gap > -3e-10
            if expected_boundary is not None:
                # Repeated largest p leaves the antisymmetric heavy-state mode
                # untouched by 11^T, so its eigenvalue is exactly 1/p_1.
                assert F(1) / p[0] == expected_boundary
                assert abs(eig[1] - float(expected_boundary)) < 3e-9
            print(
                f"N={n} family={name} pmax={float(max(p)):.12g} "
                f"lambda_min_plus={eig[1]:.12g} gap={gap:.3e} "
                f"kernel_abs={kernel:.3e} exact_LDL=PASS "
                f"min_pivot={float(min(pivots)):.3e}"
            )
            count += 1
    print(f"cases={count} exact_rational_certificates={count}")
    print(f"smallest_float_gap={smallest_gap:.12g} at {worst}")
    print("specified_boundary_exact=lambda_min_plus/k0=2+(N-2)delta for delta=1e-6")
    print("status=PASS_NO_COUNTEREXAMPLE_IN_TESTED_FAMILIES")


if __name__ == "__main__":
    run()
