#!/usr/bin/env python3
"""Exact checks for the d=5 hypocycloid-gate obstruction.

This script does not search for, or claim, a unitary realization of the test
bracelet matrix.  It certifies that the matrix is circulant and bracelet and
that its first Fourier eigenvalue lies strictly outside H_5.  The accompanying
analytic note proves that this excludes unistochasticity, because every
circulant unistochastic matrix obeys the H_d bound.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


EXPECTED_SOURCE_SHA256 = (
    "ba451f66e9a4ccdb10042f48bc7773d87ed35d33939f431b3f216134e2939389"
)


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    source_hash = hashlib.sha256((project / "source.md").read_bytes()).hexdigest()
    assert source_hash == EXPECTED_SOURCE_SHA256

    # A separate exact convention check uses a genuinely noncommuting premise
    # unitary.  V is circulant unitary, while a nonconstant diagonal left phase
    # L makes U=L*V fail [U,S]=0 without changing any squared moduli.
    n = 5
    v_demo = sp.eye(n) + (sp.I - 1) * sp.ones(n) / n
    left_phase = sp.diag(1, -1, sp.I, -sp.I, 1)
    u_demo = left_phase * v_demo
    shift = sp.zeros(n)
    for j in range(n):
        shift[(j + 1) % n, j] = 1
    assert sp.simplify(u_demo.conjugate().T * u_demo - sp.eye(n)) == sp.zeros(n)
    assert u_demo * shift != shift * u_demo
    b_demo = (sp.Rational(17, 25),) + (sp.Rational(2, 25),) * 4
    for i in range(n):
        for j in range(n):
            modulus_squared = sp.expand_complex(
                u_demo[i, j] * sp.conjugate(u_demo[i, j])
            )
            assert modulus_squared == b_demo[(i - j) % n]

    a = sp.Rational(209, 500)
    c = sp.Rational(3, 40)
    d = sp.Rational(7, 500)
    b = (a, c, d, c, a)
    assert sum(b) == 1 and all(x >= 0 for x in b)
    b_matrix = sp.Matrix(n, n, lambda i, j: b[(i - j) % n])
    assert all(sum(b_matrix[i, j] for j in range(n)) == 1 for i in range(n))
    assert all(sum(b_matrix[i, j] for i in range(n)) == 1 for j in range(n))

    # For a circulant matrix, all row and column bracelet tests reduce, up to
    # cyclic reindexing, to separations s=1 and s=2.
    lengths_s1 = (sp.sqrt(a * c), sp.sqrt(c * d), sp.sqrt(c * d),
                  sp.sqrt(a * c), a)
    assert a > sp.sqrt(a * c) and a > sp.sqrt(c * d)

    # A rational lower certificate for the only nontrivial inequality:
    # after multiplying by 1000, sqrt(ac)=sqrt(31350)/1000 and
    # sqrt(cd)=sqrt(1050)/1000.  The two strict lower bounds below give
    # 2 sqrt(ac)+2 sqrt(cd)-a > 1/1250 > 0.
    assert 31350 > 177**2
    assert sp.Rational(1050) > sp.Rational(162, 5) ** 2
    certified_s1_lower_margin = sp.Rational(1, 1250)
    actual_s1_margin = sp.simplify(sum(lengths_s1) - 2 * a)
    assert actual_s1_margin > certified_s1_lower_margin

    lengths_s2 = (sp.sqrt(a * d), c, sp.sqrt(a * d),
                  sp.sqrt(a * c), sp.sqrt(a * c))
    assert sp.sqrt(a * c) >= max(sp.sqrt(a * d), c)
    # The maximum already occurs twice, so the s=2 bracelet inequality is
    # immediate; the remaining two separations are reindexings of s=1,s=2.
    assert sum(lengths_s2) >= 2 * sp.sqrt(a * c)

    omega = sp.exp(2 * sp.pi * sp.I / 5)
    lambda_1 = sp.simplify(sum(b[r] * omega ** (-r) for r in range(5)))
    radial = sp.Rational(93, 400) + sp.Rational(343, 2000) * sp.sqrt(5)
    assert sp.simplify(sp.expand_complex(
        lambda_1 - radial * sp.exp(sp.I * sp.pi / 5)
    )) == 0

    # On arg(z)=pi/5, h(pi/5)=3 exp(i*pi/5)/5.  The exact lower chain
    # sqrt(5)>11/5>15/7 proves radial>3/5 without decimal arithmetic.
    assert sp.Rational(5) > sp.Rational(11, 5) ** 2
    assert sp.Rational(11, 5) > sp.Rational(15, 7)
    radial_excess = sp.simplify(radial - sp.Rational(3, 5))
    assert radial_excess > 0

    print("exact d=5 hypocycloid-gate obstruction")
    print(f"source_sha256={source_hash}")
    print("check.noncommuting_exact_unitary_with_circulant_moduli=PASS")
    print("b=(209/500,3/40,7/500,3/40,209/500)")
    print("check.simplex_and_circulant=PASS")
    print(f"bracelet.s1.actual_margin={actual_s1_margin}")
    print(f"bracelet.s1.certified_lower_margin={certified_s1_lower_margin}")
    print("check.bracelet_all_row_column_pairs=PASS")
    print("lambda_1=radial*exp(i*pi/5)")
    print(f"radial={radial}")
    print(f"radial_minus_H5_boundary={radial_excess}")
    print("check.lambda_1_strictly_outside_H5=PASS")
    print("conclusion=bracelet_but_not_unistochastic_by_commutator_trace_lemma")
    print("status=PASS")


if __name__ == "__main__":
    main()
