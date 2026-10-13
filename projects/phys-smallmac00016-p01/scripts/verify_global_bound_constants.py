#!/usr/bin/env python3
"""Exact arithmetic checks for evidence/exact-global-certificate.md."""

import sympy as sp


p = sp.Rational(18, 25)
q = sp.Rational(7, 25)
gamma = sp.Rational(3, 10)
r = 1 - gamma
c = gamma / 2
d0_sq = p**2 * r
d1_sq = q**2 * r
z0 = p - c
z1 = q - c
t0 = sp.simplify(d1_sq / (d1_sq + c**2 - z1**2))

assert t0 == sp.Rational(49, 54)
assert sp.simplify(5 * d1_sq + 49 * z1**2 - 49 * c**2) == 0
assert sp.Rational(18, 7) - sp.Rational(285, 1274) > 0
one_clock = sp.simplify(2 * r + r**2)
fidelity = sp.simplify((1 + one_clock) / 4)
history_gap = sp.simplify(sp.Rational(1831, 2500) - fidelity)
assert one_clock == sp.Rational(189, 100)
assert fidelity == sp.Rational(289, 400)
assert history_gap == sp.Rational(99, 10000)

print(f"t_cross={t0}")
print("gram_boundary_identity=" + str(sp.simplify(5*d1_sq + 49*z1**2))
      + "=49c2=" + str(49*c**2))
print("endpoint_derivative_lower=" + str(
    sp.Rational(18, 7) - sp.Rational(285, 1274)))
print(f"one_clock_frobenius_squared_bound={one_clock}")
print(f"exact_F2M={fidelity}")
print(f"history_witness_advantage={history_gap}")
print("exact_constant_checks=PASS")
