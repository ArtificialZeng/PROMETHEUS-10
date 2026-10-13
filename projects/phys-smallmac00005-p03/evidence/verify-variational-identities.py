#!python3
"""Exact symbolic replay of the variational proof for the magnetic unit disk."""

import sympy as sp

r, b, rho = sp.symbols("r b rho", real=True)


def radial_operator(f, field, m):
    return -sp.diff(f, r, 2) - sp.diff(f, r) / r + (m / r - field * r / 2) ** 2 * f


phi = (1 - r**2) * sp.exp(-r**2 / 2)
v_minus = r * sp.exp(-r**2 / 2)
v_plus = r**2 * (3 - r**2) * sp.exp(-r**2 / 2)

assert sp.simplify(radial_operator(phi, 2, 0) - 6 * phi) == 0
assert sp.simplify(radial_operator(v_minus, 2, -1) - 6 * v_minus) == 0
assert sp.simplify(radial_operator(v_plus, 2, 2) - 6 * v_plus) == 0
assert sp.simplify(sp.diff(v_minus, r).subs(r, 1)) == 0
assert sp.simplify(sp.diff(v_plus, r).subs(r, 1)) == 0

norm_0 = sp.integrate(r, (r, 0, 1))
q_0 = sp.integrate((b * r / 2) ** 2 * r, (r, 0, 1))
R_0 = sp.factor(q_0 / norm_0)

f_1 = r
norm_1 = sp.integrate(f_1**2 * r, (r, 0, 1))
q_1 = sp.integrate((sp.diff(f_1, r) ** 2 + (1 / r - b * r / 2) ** 2 * f_1**2) * r, (r, 0, 1))
R_1 = sp.factor(q_1 / norm_1)

D_minus = sp.factor(6 + (b - 2) + (b**2 - 4) * rho / 4 - (5 + b**2 / 4))
D_plus = sp.factor(6 - 2 * (b - 2) + (b**2 - 4) * rho / 4 - 6)

print("T_2,0 phi = 6 phi: exact")
print("T_2,-1 v_minus = 6 v_minus and v_minus'(1)=0: exact")
print("T_2,2 v_plus = 6 v_plus and v_plus'(1)=0: exact")
print("R[u_0] =", R_0)
print("R[u_1] =", R_1)
print("R[v_minus]-(5+b^2/4) =", D_minus)
print("R[v_plus]-6 =", D_plus)
print("sign domains: 0<rho<1; 0<b<=2 for v_minus; 2<=b<=4 for v_plus")
