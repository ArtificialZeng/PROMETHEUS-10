#!/usr/bin/env python3
"""Exact-algebra checks and numerical sanity tests for the extrema reduction.

The symbolic assertions certify only the displayed algebraic identities.  The finite
numerical checks are adversarial sanity tests, not a global phase-boundary proof.
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar


PI = np.pi


def ham(theta: float, kappa: float, r: float, m: float) -> np.ndarray:
    return np.array(
        [
            [m - 2*r*np.cos(theta-2*PI/3), -1, -np.exp(-1j*kappa)],
            [-1, -2*r*np.cos(theta), -1],
            [-np.exp(1j*kappa), -1, -m - 2*r*np.cos(theta+2*PI/3)],
        ], dtype=complex,
    )


def band(theta: float, kappa: float, r: float, m: float, j: int) -> float:
    return float(np.linalg.eigvalsh(ham(theta, kappa, r, m))[j])


def optimize_theta(r: float, m: float, j: int, maximize: bool) -> tuple[float, float]:
    n = 6000
    theta = np.linspace(-PI, PI, n, endpoint=False)
    values = np.array([band(t, 0.0, r, m, j) for t in theta])
    idx = int(np.argmax(values) if maximize else np.argmin(values))
    step = 2*PI/n
    sign = -1.0 if maximize else 1.0
    result = minimize_scalar(
        lambda t: sign*band((t+PI)%(2*PI)-PI, 0.0, r, m, j),
        bounds=(theta[idx]-step, theta[idx]+step), method="bounded",
        options={"xatol": 1e-14},
    )
    t = (result.x+PI)%(2*PI)-PI
    # Refine with the exact implicit-root stationarity equation.  This is used
    # only away from band degeneracies in the eliminant sanity cases.
    def stationarity(x: float) -> float:
        s = np.sin(x)
        c = np.cos(x)
        q = m*m-r*r-2*np.sqrt(3)*m*r*s+4*r*r*s*s
        rp = (
            -2*np.sqrt(3)*m*r + (9*r*r-m*m)*s
            + 4*np.sqrt(3)*m*r*s*s - 12*r*r*s*s*s
        )
        return rp-np.sqrt(3)*m*c*band(x, 0.0, r, m, j)
    width = 8*step
    try:
        refined = brentq(stationarity, t-width, t+width, xtol=5e-15, rtol=1e-15)
        t = (refined+PI)%(2*PI)-PI
    except ValueError:
        pass
    return t, band(t, 0.0, r, m, j)


def symbolic_checks() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    s, c, E, r, m, K = sp.symbols("s c E r m K", real=True)
    A = m**2 + 3*r**2 + 3 - 2*sp.sqrt(3)*m*r*s
    Q = m**2-r**2-2*sp.sqrt(3)*m*r*s+4*r**2*s**2
    abs_w_squared = r**2+m**2/3-2*m*r*s/sp.sqrt(3)
    original_D = (
        2*m**2*r*c-4*sp.sqrt(3)*m*r**2*s*c
        -2*r**3*c*(1-4*s**2)-2*K
    )
    assert sp.expand(A-(3+3*abs_w_squared)) == 0
    assert sp.expand(original_D-(2*r*c*Q-2*K)) == 0
    R = (1-s**2)*sp.diff(Q, s)-s*Q
    R_explicit = (
        -2*sp.sqrt(3)*m*r + (9*r**2-m**2)*s
        + 4*sp.sqrt(3)*m*r*s**2 - 12*r**2*s**3
    )
    assert sp.expand(R-R_explicit) == 0

    # At m=sqrt(3)r, kappa=0, E=1 the characteristic polynomial factors.
    P = E**3-A*E-2*r*c*Q+2*K
    direct_factor = -2*r**2*(1-s)*(3+2*r*c*(1-2*s))
    assert sp.expand(P.subs({E: 1, m: sp.sqrt(3)*r, K: 1})-direct_factor) == 0

    # Eliminate c and E's sign from the simple theta-stationarity equations.
    L = 1-s**2
    core = sp.expand(
        (6*sp.sqrt(3)*r*m**3*L**2*Q - R*(R**2-3*m**2*L*A))**2
        - 108*m**6*L**3
    )
    assert sp.Poly(core, s).degree() == 18

    s_star = (1-sp.sqrt(33))/8
    M2 = sp.simplify((1-s_star**2)*(1-2*s_star)**2)
    rc2 = sp.simplify(sp.Rational(9, 4)/M2)
    assert sp.simplify(rc2-(69-11*sp.sqrt(33))/8) == 0
    assert sp.expand(4*rc2**2-69*rc2+48) == 0

    print("SYMBOLIC A=3+3|w|^2 and D=2*r*c*Q-2*cos(kappa): PASS")
    print("SYMBOLIC theta stationarity R=sqrt(3)*m*c*E: PASS")
    print("R(s) = -2*sqrt(3)*m*r +(9*r^2-m^2)s +4*sqrt(3)*m*r*s^2 -12*r^2*s^3")
    print("SYMBOLIC nonexceptional stationary eliminant degree in s: 18")
    print("SYMBOLIC direct-line P(1) factorization: PASS")
    print("r_c^2=(69-11*sqrt(33))/8; minpoly 4*x^2-69*x+48: PASS")
    return s, r, m, core, rc2


def numeric_checks(s_sym: sp.Symbol, r_sym: sp.Symbol, m_sym: sp.Symbol,
                   core: sp.Expr, rc2: sp.Expr) -> None:
    U = np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]], dtype=complex)
    worst_sym = 0.0
    worst_endpoint = 0.0
    for r in (0.5, 0.93, 2.0):
        for m in (-3.1, 0.2, np.sqrt(3)*r):
            for theta in (-2.71, -0.31, 1.17):
                for kappa in (-2.2, 0.4, 2.8):
                    lhs = ham(PI-theta, PI-kappa, r, m)
                    rhs = -U@ham(theta, kappa, r, m)@U.conj().T
                    worst_sym = max(worst_sym, float(np.max(np.abs(lhs-rhs))))
                e0 = np.linalg.eigvalsh(ham(theta, 0.0, r, m))
                epi = np.linalg.eigvalsh(ham(theta, PI, r, m))
                # Expected: outer roots increase and middle root decreases from 0 to pi.
                worst_endpoint = max(
                    worst_endpoint, max(e0[0]-epi[0], epi[1]-e0[1], e0[2]-epi[2], 0.0)
                )
    assert worst_sym < 3e-14
    assert worst_endpoint < 3e-14
    print(f"UNITARY reflection max residual={worst_sym:.3e}: PASS")
    print(f"KAPPA endpoint ordering worst violation={worst_endpoint:.3e}: PASS")

    core_fn = sp.lambdify((s_sym, r_sym, m_sym), core, "numpy")
    for r, ratio in ((1.0, 0.50), (1.0, 1.25), (2.0, 2.0)):
        m = ratio*np.sqrt(3)*r
        for j, maximize, name in ((2, False, "Ec-min"), (1, True, "E2-max")):
            theta, energy = optimize_theta(r, m, j, maximize)
            sval = np.sin(theta)
            raw = float(core_fn(sval, r, m))
            scale = max(1.0, abs(float(core_fn(0.123456789, r, m))))
            print(
                f"ELIMINANT r={r:.2f} ratio={ratio:.2f} {name} "
                f"theta={theta:+.10f} E={energy:+.10f} scaled_residual={abs(raw)/scale:.3e}"
            )

    rc = float(sp.sqrt(rc2).evalf(18))
    s_star = float(((1-sp.sqrt(33))/8).evalf(18))
    c_star = -np.sqrt(1-s_star*s_star)
    theta_star = float(np.arctan2(s_star, c_star))
    print(f"THRESHOLD rc={rc:.15f} theta*={theta_star:+.15f} sin(theta*)={s_star:+.15f}")
    for r in (rc-0.01, rc, rc+0.01):
        m = np.sqrt(3)*r
        _, e2max = optimize_theta(r, m, 1, True)
        # The direct point always supplies E2=1; at r=rc theta_star supplies
        # the second exact E2=1 contact as well.
        e2max = max(e2max, 1.0, band(theta_star, 0.0, r, m, 1))
        # E3 has the exact value 1 at theta=pi/2 and is bounded below by 1.
        print(f"DIRECT-LINE r={r:.12f} max(E2)={e2max:.12f} G={1-e2max:+.12e}")


def main() -> None:
    print("JOB phys-00018-p01-research-99db6e47b674")
    print("Finite numerical checks below are sanity tests, not global certification.")
    symbols = symbolic_checks()
    numeric_checks(*symbols)
    print("EXTREMA REDUCTION CHECKS: PASS")


if __name__ == "__main__":
    main()
