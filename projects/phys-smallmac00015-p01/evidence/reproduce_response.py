#!/usr/bin/env python3
"""Compare direct and spectral weak response; replay the published N=2 baseline."""
from __future__ import annotations

import math
import sys

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp


def generator(E: np.ndarray, k0: float) -> np.ndarray:
    n = len(E)
    L = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                L[i, j] = k0 * math.exp((E[j] - E[i]) / 2.0)
    for i in range(n):
        L[i, i] = -sum(k0 * math.exp((E[i] - E[j]) / 2.0) for j in range(n) if j != i)
    return L


def generator_direction(E: np.ndarray, c: np.ndarray, k0: float) -> np.ndarray:
    n = len(E)
    dL = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            if i != j:
                lij = k0 * math.exp((E[j] - E[i]) / 2.0)
                dL[i, j] = lij * (c[j] - c[i]) / 2.0
    for i in range(n):
        dL[i, i] = -sum(
            k0 * math.exp((E[i] - E[j]) / 2.0) * (c[i] - c[j]) / 2.0
            for j in range(n) if j != i
        )
    return dL


def direct_term(E: np.ndarray, k0: float, omega: float, c: np.ndarray):
    L = generator(E, k0)
    pi = np.exp(-E)
    pi /= pi.sum()
    forcing = generator_direction(E, c, k0) @ pi
    R = np.linalg.solve(1j * omega * np.eye(len(E)) - L, forcing)
    A = 0.5 * float(np.real(np.vdot(R, -(omega**2) * c)))
    B = 0.5 * float(np.real(np.vdot(R, 1j * omega * c)))
    return A, B, R, L, pi


def spectral_term(E: np.ndarray, k0: float, omega: float, c: np.ndarray):
    x = np.exp(-E / 2.0)
    Q = float(x @ x)
    pi = x * x / Q
    sqrt_pi = x / math.sqrt(Q)
    M = k0 * (x.sum() * np.diag(1.0 / x) - np.ones((len(E), len(E))))
    lam, V = np.linalg.eigh(M)
    h = sqrt_pi * (c - np.dot(pi, c))
    a = V.conj().T @ h
    positive = lam > 1e-10 * max(1.0, float(lam[-1]))
    lp = lam[positive]
    ap = a[positive]
    A = 0.5 * float(np.sum(omega**2 * lp**2 * np.abs(ap) ** 2 / (lp**2 + omega**2)))
    B = 0.5 * float(np.sum(omega**2 * lp * np.abs(ap) ** 2 / (lp**2 + omega**2)))
    Zm = np.zeros_like(a, dtype=complex)
    Zm[positive] = -lp * ap / (lp + 1j * omega)
    R = sqrt_pi * (V @ Zm)
    return A, B, R, M, lam


def compare_case(name: str, E: list[float], k0: float, Omega: float, harmonics):
    Earr = np.array(E, dtype=float)
    Ad = Bd = As = Bs = 0.0
    max_r = max_col = max_db = max_kernel = 0.0
    all_lam = None
    for n, raw_c in harmonics:
        c = np.array(raw_c, dtype=complex)
        omega = n * Omega
        a1, b1, rd, L, pi = direct_term(Earr, k0, omega, c)
        a2, b2, rs, M, lam = spectral_term(Earr, k0, omega, c)
        Ad += a1
        Bd += b1
        As += a2
        Bs += b2
        max_r = max(max_r, float(np.max(np.abs(rd - rs))))
        max_col = max(max_col, float(np.max(np.abs(L.sum(axis=0)))))
        flow = np.diag(pi) @ L.T
        max_db = max(max_db, float(np.max(np.abs(flow - flow.T))))
        x = np.exp(-Earr / 2.0)
        max_kernel = max(max_kernel, float(np.linalg.norm(M @ x, ord=np.inf)))
        all_lam = lam
    scale_a = max(1.0, abs(Ad), abs(As))
    scale_b = max(1.0, abs(Bd), abs(Bs))
    ratio = As / Bs
    positive = all_lam[all_lam > 1e-10 * max(1.0, float(all_lam[-1]))]
    gauge = 0.73 - 0.41j
    gA = gB = 0.0
    for n, raw_c in harmonics:
        c = np.array(raw_c, dtype=complex) + gauge
        a, b, *_ = direct_term(Earr, k0, n * Omega, c)
        gA += a
        gB += b
    print(
        f"case={name} N={len(E)} A_direct={Ad:.16e} A_spectral={As:.16e} "
        f"B_direct={Bd:.16e} B_spectral={Bs:.16e} ratio={ratio:.16e} "
        f"lambda_min={positive[0]:.16e} lambda_max={positive[-1]:.16e} "
        f"relA={abs(Ad-As)/scale_a:.3e} relB={abs(Bd-Bs)/scale_b:.3e} "
        f"maxR={max_r:.3e} colsum={max_col:.3e} detailed_balance={max_db:.3e} "
        f"Mkernel={max_kernel:.3e} gaugeA={abs(gA-Ad):.3e} gaugeB={abs(gB-Bd):.3e}"
    )
    assert abs(Ad - As) / scale_a < 2e-12
    assert abs(Bd - Bs) / scale_b < 2e-12
    assert max_r < 2e-12 and max_col < 2e-12 and max_db < 2e-12 and max_kernel < 2e-11
    assert abs(gA - Ad) < 2e-12 and abs(gB - Bd) < 2e-12
    assert positive[0] - 2e-12 <= ratio <= positive[-1] + 2e-12
    return ratio


def compare_representations() -> None:
    print("WEAK_RESPONSE_REPRESENTATION_COMPARISON")
    r2 = compare_case(
        "N2-zero-offset", [0.0, 0.0], 1.3, 0.7,
        [(1, [1.0 - 0.3j, -0.2 + 0.4j]), (2, [0.3 + 0.1j, -0.6 + 0.2j])],
    )
    assert abs(r2 - 2.6) < 2e-12
    compare_case(
        "N3-biased", [0.4, -0.7, 0.2], 0.9, 1.1,
        [(1, [1.0 + 0.2j, -0.4 + 0.7j, 0.1 - 0.3j]),
         (3, [-0.2 + 0.5j, 0.8 - 0.1j, -0.6 + 0.4j])],
    )
    compare_case(
        "N5-biased", [-1.1, 0.3, 0.8, -0.2, 1.4], 1.7, 0.45,
        [(1, [0.4 + 0.2j, -0.9 + 0.3j, 0.1 - 0.8j, 0.7 + 0.6j, -0.3 + 0.1j]),
         (2, [0.2 - 0.2j, 0.5 + 0.9j, -0.7 + 0.3j, 0.1 - 0.5j, 0.6 + 0.4j])],
    )
    print("RESPONSE_COMPARISON_STATUS=PASS")


def nonlinear_two_state(k0: float, omega: float, eps: float, nodes: int):
    period = 2.0 * math.pi / omega

    def rhs(t, y):
        delta = eps * math.sin(omega * t)
        k12 = k0 * math.exp(delta / 2.0)
        k21 = k0 * math.exp(-delta / 2.0)
        return np.array([-(k12 + k21) * y[0] + k21])

    opts = dict(method="DOP853", rtol=2e-13, atol=2e-15)
    end0 = solve_ivp(rhs, (0.0, period), [0.0], **opts).y[0, -1]
    end1 = solve_ivp(rhs, (0.0, period), [1.0], **opts).y[0, -1]
    multiplier = end1 - end0
    p0 = end0 / (1.0 - multiplier)
    t = np.linspace(0.0, period, nodes)
    sol = solve_ivp(rhs, (0.0, period), [p0], t_eval=t, **opts)
    if not sol.success:
        raise RuntimeError(sol.message)
    p1 = sol.y[0]
    edot = eps * omega * np.cos(omega * t)
    eddot = -eps * omega**2 * np.sin(omega * t)
    A = float(simpson(p1 * eddot, x=t) / period)
    B = float(simpson(p1 * edot, x=t) / period)
    phase = math.atan2(omega * B, A)
    return A, B, phase, abs(p1[-1] - p1[0]), float(min(p1.min(), (1.0-p1).min()))


def baseline() -> None:
    print("PUBLISHED_N2_BASELINE")
    print("source=B.12-B.15; alpha=1/2; DeltaE0=0; DeltaE=eps*sin(Omega*t)")
    print("analytic A2=k0^2*Omega^2/[2(4k0^2+Omega^2)]")
    print("analytic B2=k0*Omega^2/[4(4k0^2+Omega^2)]")
    print("analytic phase=atan[Omega/(2k0)] and A2/B2=2k0")
    print("solver=DOP853 rtol=2e-13 atol=2e-15; quadrature=Simpson nodes=16385")
    print("k0 Omega eps A/eps2 B/eps2 phase target abs_error closure min_probability")
    final_errors = []
    for k0, omega in [(1.0, 0.3), (1.0, 1.0), (1.0, 3.0), (0.7, 1.4)]:
        previous = None
        for eps in (0.08, 0.04, 0.02, 0.01):
            A, B, phase, closure, pmin = nonlinear_two_state(k0, omega, eps, 16385)
            target = math.atan(omega / (2.0 * k0))
            err = abs(phase - target)
            print(f"{k0:.6g} {omega:.6g} {eps:.6g} {A/eps**2:.12e} {B/eps**2:.12e} "
                  f"{phase:.12e} {target:.12e} {err:.3e} {closure:.3e} {pmin:.6e}")
            if previous is not None:
                assert err < 0.32 * previous
            previous = err
        final_errors.append(previous)
    coarse = nonlinear_two_state(1.0, 1.0, 0.01, 8193)[2]
    fine = nonlinear_two_state(1.0, 1.0, 0.01, 32769)[2]
    print(f"quadrature_phase_8193_vs_32769={abs(coarse-fine):.3e}")
    print(f"max_phase_error_at_eps_0.01={max(final_errors):.3e}")
    assert max(final_errors) < 3e-6
    assert abs(coarse - fine) < 2e-10
    print("BASELINE_STATUS=PASS")


if __name__ == "__main__":
    print(f"Python={sys.version.replace(chr(10), ' ')}")
    print(f"NumPy={np.__version__}")
    print(f"SciPy={scipy.__version__}")
    compare_representations()
    baseline()
