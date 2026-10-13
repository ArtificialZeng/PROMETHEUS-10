#!/usr/bin/env python3
"""Exact confluent formulas and high-precision checks for phys-00020-p03.

The script writes no files.  It evaluates the closed finite-sum Ritz formula,
the exact Frobenius norm of the inverse-tail remainder, and independent
eigenvalues of T.T*T.  All small singular values reported as ``direct`` are
computed with mpmath, not with the projected four-state pencil.
"""

from __future__ import annotations

from fractions import Fraction
import platform
import sys

import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import eigh


def sums(N: int, r: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    q = r * r
    A = mp.fsum(q**i for i in range(N))
    B = mp.fsum(i * q**i for i in range(N))
    D = mp.fsum(i * i * q**i for i in range(N))
    Delta = A * D - B * B
    m = N * A - 2 * B
    return A, B, D, Delta, m


def closed_ritz(N: int, r: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    _, _, _, Delta, m = sums(N, r)
    root = mp.sqrt(m * m + 4 * Delta)
    phi1 = (root + m) / 2
    # This product form avoids cancellation in (root-m)/2.
    phi2 = Delta / phi1
    scale = r ** (N + 1)
    return scale / phi1, scale / phi2, phi1, phi2


def tail_frobenius(N: int, r: mp.mpf) -> mp.mpf:
    q = r * r
    return mp.sqrt(
        mp.fsum((N - 1 - t) * t * t * q ** (N + t) for t in range(1, N - 1))
    )


def direct_small_singular_values(N: int, r: mp.mpf, dps: int = 110) -> list[mp.mpf]:
    with mp.workdps(dps):
        T = mp.matrix(N)
        for i in range(N):
            T[i, i] = r * r
            if i + 1 < N:
                T[i, i + 1] = 2 * r
            if i + 2 < N:
                T[i, i + 2] = 1
        vals = sorted(mp.eigsy(T.T * T, eigvals_only=True))
        return [mp.sqrt(max(mp.mpf("0"), vals[i])) for i in range(min(3, N))]


def pencil_values(N: int, r: float) -> np.ndarray:
    z = -r
    idx = np.arange(N, dtype=float)
    v0 = z**idx
    v1 = np.zeros(N, dtype=float)
    v1[1:] = idx[1:] * z ** (idx[1:] - 1)
    V = np.zeros((2 * N, 4), dtype=float)
    V[:N, 0], V[:N, 1] = v0, v1
    V[N:, 2], V[N:, 3] = v0[::-1], v1[::-1]
    S = np.eye(N, k=1)
    T = (r * np.eye(N) + S) @ (r * np.eye(N) + S)
    Z = np.zeros_like(T)
    H = np.block([[Z, T.T], [T, Z]])
    return eigh(V.T @ H @ V, V.T @ V, eigvals_only=True)[2:]


def exact_uniform_checks() -> None:
    N = 61
    eta2 = (
        Fraction(150 * N) ** 2
        * Fraction(4, 5) ** (2 * N + 2)
        * Fraction(N - 1)
        * Fraction(41, 25)
        / Fraction(9, 25) ** 3
    )
    eta_limit = Fraction(413, 1000)
    gap_bound = (
        Fraction(150 * N) * Fraction(4, 5) ** (N + 1) / (1 - eta_limit)
    )
    print("UNIFORM_RATIONAL_CHECKS")
    print(f"eta61_squared_decimal={float(eta2):.18e}")
    print(f"eta61_lt_413_over_1000_exact={eta2 < eta_limit * eta_limit}")
    print(f"E2_upper_using_eta413_decimal={float(gap_bound):.18e}")
    print(f"E2_upper_lt_1_over_25_exact={gap_bound < Fraction(1, 25)}")
    print("eta_ratio_squared_lt_one_for_N_ge_61=" + str(16 * 62 * 62 < 25 * 61 * 60))


def main() -> None:
    print("RUNTIME")
    print(f"python_executable={sys.executable}")
    print(f"python_version={platform.python_version()}")
    print(f"numpy_version={np.__version__}")
    print(f"scipy_version={scipy.__version__}")
    exact_uniform_checks()
    print("VALIDATION")
    with mp.workdps(110):
        for r_text in ("0.33333333333333333333333333333333333333333333333333", "0.5", "0.75"):
            r = mp.mpf(r_text)
            print(f"r={mp.nstr(r, 18)}")
            for N in (8, 12, 20, 40):
                direct = direct_small_singular_values(N, r, 110)
                ehat1, ehat2, phi1, phi2 = closed_ritz(N, r)
                eps = tail_frobenius(N, r)
                p = pencil_values(N, float(r))
                asym1 = (1 - r * r) * r ** (N + 1) / N
                asym2 = N * (1 - r * r) ** 3 * r ** (N - 1)
                print(
                    "N={} direct=[{},{}] closed=[{},{}] pencil=[{:.16e},{:.16e}] "
                    "relerr=[{},{}] eps_over_phi2={} scaled_actual=[{},{}] s3={} bulk={}".format(
                        N,
                        mp.nstr(direct[0], 24), mp.nstr(direct[1], 24),
                        mp.nstr(ehat1, 24), mp.nstr(ehat2, 24),
                        p[0], p[1],
                        mp.nstr(abs(direct[0] - ehat1) / direct[0], 8),
                        mp.nstr(abs(direct[1] - ehat2) / direct[1], 8),
                        mp.nstr(eps / phi2, 8),
                        mp.nstr(direct[0] / asym1, 12),
                        mp.nstr(direct[1] / asym2, 12),
                        mp.nstr(direct[2], 14),
                        mp.nstr((1-r)**2, 14),
                    )
                )


if __name__ == "__main__":
    main()
