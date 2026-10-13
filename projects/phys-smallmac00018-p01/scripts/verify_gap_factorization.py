#!/usr/bin/env python3
"""Exact algebra and numerical sanity checks for the gap-sign factorization.

The symbolic assertions verify the displayed reductions.  The floating-point table
checks the selected physical branch but is not an interval proof that no other
Fejer--Riesz sectors occur.
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar


PI = np.pi
SQRT3 = np.sqrt(3.0)


def ham(theta: float, kappa: float, r: float, m: float) -> np.ndarray:
    return np.array(
        [
            [m - 2*r*np.cos(theta-2*PI/3), -1, -np.exp(-1j*kappa)],
            [-1, -2*r*np.cos(theta), -1],
            [-np.exp(1j*kappa), -1, -m - 2*r*np.cos(theta+2*PI/3)],
        ], dtype=complex,
    )


def symbolic_checks() -> None:
    E, r, q, theta = sp.symbols("E r q theta", real=True)
    f = (
        E**3 - 3*E*(1+r**2+q**2) + 2
        + 6*E*q*r*sp.sin(theta)
        - 6*q**2*r*sp.cos(theta)
        + 6*q*r**2*sp.sin(2*theta)
        + 2*r**3*sp.cos(3*theta)
    )
    s, c = sp.symbols("s c", real=True)
    A = 3*(1+r**2+q**2-2*q*r*s)
    Q = 3*q**2-r**2-6*q*r*s+4*r**2*s**2
    chambers = E**3-A*E-2*r*c*Q+2
    trig_to_sc = sp.expand_trig(f).subs({sp.sin(theta): s, sp.cos(theta): c})
    trig_to_sc = sp.expand(trig_to_sc.subs(c**3, c*(1-s**2)))
    trig_to_sc = sp.expand(trig_to_sc.subs(c**2, 1-s**2))
    assert sp.expand(trig_to_sc-chambers) == 0

    # Algebraic autocorrelations of the cubic Fejer factor.  Here B=z_c*z_v,
    # A=z_c+z_v, with conjugates conj(B)=1/B and conj(A)=A/B for unit roots.
    As, Bs, rho = sp.symbols("As Bs rho", nonzero=True)
    coeff = [-rho, Bs+rho*As/Bs, -(As+rho/Bs), sp.Integer(1)]
    coeff_star = [-rho, 1/Bs+rho*As, -(As/Bs+rho*Bs), sp.Integer(1)]
    corr = {
        k: sp.factor(sum(coeff[j+k]*coeff_star[j] for j in range(4-k)))
        for k in range(4)
    }
    t_abs = rho+1/rho
    assert sp.factor(corr[3]/rho+1) == 0
    assert sp.factor(corr[2]/rho-(2*As+t_abs/Bs)) == 0
    assert sp.factor(
        corr[1]/rho
        + 2*Bs+2*t_abs*As/Bs+As**2+1/Bs**2
    ) == 0

    # Fourier coefficient matching after -f=|p|^2 with two unit roots.
    # X=cos(phi)^2 and V=cos(delta)^2 in the sector
    # cos(phi)>0, sin(phi)<0, cos(delta)<0.
    X, V = sp.symbols("X V", real=True)
    relation = (
        -160*V*X**3 + 144*V*X**2 - 24*V*X + 4*V
        + 96*X**4 - 144*X**3 + 60*X**2 - 3
    )
    V_of_X = sp.factor(
        3*(2*X-1)**2*(8*X**2-4*X-1)
        / (4*(40*X**3-36*X**2+6*X-1))
    )
    assert sp.factor(relation.subs(V, V_of_X)) == 0

    root33 = sp.sqrt(33)
    Xc = (7+root33)/16
    Vc = (9-root33)/16
    rc2 = (69-11*root33)/8
    assert sp.simplify(V_of_X.subs(X, Xc)-Vc) == 0

    # Squared forms avoid asking the CAS to choose positive square-root branches.
    u2 = sp.factor(
        16*V*(1-X)*(4*X-1)**2/(9*(2*X-1)**2)
    )
    e2 = sp.factor(
        4*X*((2*X-1)*(1-X)+(2*X+1)*V)**2
        /(V*(4*X-1)**2)
    )
    assert sp.simplify(u2.subs({X: Xc, V: Vc})-1) == 0
    assert sp.simplify(e2.subs({X: Xc, V: Vc})-1/rc2) == 0

    print("SYMBOLIC kappa=0 chemical-potential trigonometric polynomial: PASS")
    print("SYMBOLIC cubic Fejer-factor Fourier autocorrelations: PASS")
    print("SYMBOLIC two-zero coefficient relation and V(X): PASS")
    print("SYMBOLIC cusp Xc=(7+sqrt(33))/16, Vc=(9-sqrt(33))/16: PASS")
    print("SYMBOLIC cusp u=q/r=1 and E=1 at r=rc: PASS")


def reduced_parameters(X: float) -> tuple[float, ...]:
    V = (
        3*(2*X-1)**2*(8*X**2-4*X-1)
        /(4*(40*X**3-36*X**2+6*X-1))
    )
    if not (0.0 < V < 1.0):
        raise ValueError("selected sector requires 0<V<1")
    x = np.sqrt(X)
    y = -np.sqrt(1-X)
    v = -np.sqrt(V)
    d2 = 2*X-1
    t = -4*v*x/d2
    if t < 2.0:
        raise ValueError("Fejer root parameter requires t>=2")
    u = 4*v*y*(4*X-1)/(3*d2)       # u=q/r
    e = (
        2*x*(d2*(1-X)+(2*X+1)*V)
        /(np.sqrt(V)*(4*X-1))
    )                               # e=E/r
    H = 2*(1+2*V)*t+8*v*x*(4*X-3)  # constant Fourier coefficient / r^3
    K = H+e**3-3*e*(1+u**2)
    cubic_roots = np.roots([K, 0.0, -3*e, 2.0])
    positive = sorted(
        root.real for root in cubic_roots
        if abs(root.imag) < 2e-7 and root.real > 0.0
    )
    if len(positive) != 2:
        raise RuntimeError(f"expected two positive cubic roots, got {cubic_roots}")
    r_physical = positive[-1]       # equivalently E=e*r >= 1
    rho = (t+np.sqrt(t*t-4))/2
    phi = -np.arccos(x)
    delta = np.arccos(v)
    theta_c = phi+delta
    theta_v = phi-delta
    return V, t, u, e, H, K, r_physical, rho, theta_c, theta_v, positive[0]


def f_value(theta: np.ndarray | float, E: float, r: float, q: float):
    return (
        E**3-3*E*(1+r*r+q*q)+2
        + 6*E*q*r*np.sin(theta)-6*q*q*r*np.cos(theta)
        + 6*q*r*r*np.sin(2*theta)+2*r**3*np.cos(3*theta)
    )


def local_extremum(r: float, m: float, band: int, maximize: bool) -> tuple[float, float]:
    grid = np.linspace(-PI, PI, 5000, endpoint=False)
    values = np.array([np.linalg.eigvalsh(ham(t, 0.0, r, m))[band] for t in grid])
    idx = int(np.argmax(values) if maximize else np.argmin(values))
    step = 2*PI/len(grid)
    sign = -1.0 if maximize else 1.0
    fit = minimize_scalar(
        lambda t: sign*np.linalg.eigvalsh(ham((t+PI)%(2*PI)-PI, 0.0, r, m))[band],
        bounds=(grid[idx]-step, grid[idx]+step), method="bounded",
        options={"xatol": 2e-14},
    )
    theta = (fit.x+PI)%(2*PI)-PI
    value = float(np.linalg.eigvalsh(ham(theta, 0.0, r, m))[band])
    return theta, value


def check_point(X: float, label: str) -> tuple[float, float, float]:
    V, t, u, e, H, K, r, rho, theta_c, theta_v, small_r = reduced_parameters(X)
    q = u*r
    m = SQRT3*q
    E = e*r
    assert E >= 1-2e-10

    # Direct evaluation of the exact Fejer--Riesz product.
    za = np.exp(1j*theta_c)
    zb = np.exp(1j*theta_v)
    zeta = rho/(za*zb)
    amp = np.sqrt(r**3/rho)
    grid = np.linspace(-PI, PI, 4096, endpoint=False)
    z = np.exp(1j*grid)
    square = np.abs(amp*(z-za)*(z-zb)*(z-zeta))**2
    factor_residual = float(np.max(np.abs(f_value(grid, E, r, q)+square)))
    positivity_violation = float(max(np.max(f_value(grid, E, r, q)), 0.0))

    ec = np.linalg.eigvalsh(ham(theta_c, 0.0, r, m))
    ev = np.linalg.eigvalsh(ham(theta_v, 0.0, r, m))
    pe_c = 3*E*E-3*(1+r*r+q*q-2*q*r*np.sin(theta_c))
    pe_v = 3*E*E-3*(1+r*r+q*q-2*q*r*np.sin(theta_v))
    assert pe_c > 0 and pe_v < 0
    assert abs(ec[2]-E) < 2e-7 and abs(ev[1]-E) < 2e-7

    tc_num, ec_num = local_extremum(r, m, 2, False)
    tv_num, ev_num = local_extremum(r, m, 1, True)
    gap = ec_num-ev_num
    print(
        f"{label} X={X:.12f} r={r:.12f} m={m:.12f} q/r={u:.12f} "
        f"E={E:.12f} theta_c={theta_c:+.12f} theta_v={theta_v:+.12f}"
    )
    print(
        f"  factor_residual={factor_residual:.3e} max(f,0)={positivity_violation:.3e} "
        f"P_E signs=({pe_c:+.6e},{pe_v:+.6e})"
    )
    print(
        f"  optimizer gap={gap:+.3e} theta residuals="
        f"({tc_num-theta_c:+.3e},{tv_num-theta_v:+.3e}); rejected small-r root={small_r:.12f}"
    )
    assert factor_residual < 2e-8
    assert positivity_violation < 2e-9
    assert abs(gap) < 2e-8
    return r, m, E


def X_for_r(target_r: float, lower_X_branch: bool) -> float:
    Xc = float((sp.Rational(7, 16)+sp.sqrt(33)/16).evalf(18))
    if lower_X_branch:
        lo, hi = 0.7500000005, Xc-1e-10
    else:
        lo, hi = Xc+1e-10, 0.9999999995
    return brentq(
        lambda X: reduced_parameters(X)[6]-target_r,
        lo, hi, xtol=2e-14, rtol=2e-14,
    )


def main() -> None:
    print("JOB phys-00018-p01-research-2c78871016c0")
    print("Finite numerical branch checks are sanity tests, not global interval certification.")
    symbolic_checks()
    rc = np.sqrt((69-11*np.sqrt(33))/8)
    Xc = (7+np.sqrt(33))/16
    print(f"CUSP rc={rc:.15f} Xc={Xc:.15f}")
    for target_r in (0.9, 1.0, 1.25, 1.5, 2.0):
        for name, lower in (("upper-m", True), ("lower-m", False)):
            X = X_for_r(target_r, lower)
            r, m, E = check_point(X, f"r={target_r:.2f} {name}")
            assert abs(r-target_r) < 2e-10
    print("GAP FACTORIZATION CHECKS: PASS")


if __name__ == "__main__":
    main()
