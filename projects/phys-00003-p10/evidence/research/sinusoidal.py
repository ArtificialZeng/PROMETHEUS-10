"""Exact Fourier-Bessel representation; numerical tools do not certify rounding.

Independent Gaussian-score/density-SLD checks are in compare_representations.py.
No mutable checkpoint or state inputs are read.
"""
import math
import numpy as np
from scipy.special import jv


def coefficients(k, R, kappa, N=60):
    n = np.arange(-N, N + 1)
    lam = 2 * k + n * kappa
    c = jv(n, 2 * R) * np.exp(-lam * lam / 4)
    return n, lam, c


def fourier(t, k, R, kappa, N=60):
    """Carrier frame: m=e^(2ik mu) S(t), t=kappa*mu+phi.

    Return S, carrier-stripped alpha derivative, and QFI. The phase offset
    changes t only; its constant carrier-frame phase has no effect on QFI.
    """
    n, lam, c = coefficients(k, R, kappa, N)
    phase = np.exp(1j * np.asarray(t)[..., None] * n)
    s = np.sum(phase * c, axis=-1)
    d = 1j * np.sqrt(2) * np.sum(phase * (lam * c), axis=-1)
    gap = 1 - np.abs(s) ** 2
    dot = np.real(np.conj(s) * d)
    with np.errstate(divide='ignore', invalid='ignore'):
        qfi = np.abs(d) ** 2 + dot ** 2 / gap
    if k == 0 and R == 0:
        qfi = np.zeros_like(qfi)
    return s, d, qfi


def tail_bounds(k, R, kappa, N):
    """Analytic absolute tails for m and alpha derivatives of orders 1,2.

    The formulas are exact bounds in real arithmetic; evaluations here are
    floating-point approximations, not outward-rounded interval endpoints.
    """
    if R == 0:
        return (0.0, 0.0, 0.0)
    p = N + 1
    q = R / (N + 2)
    if q >= 1:
        return (math.inf, math.inf, math.inf)
    log_b = R * R + p * math.log(R) - math.lgamma(p + 1)
    b = math.exp(log_b)
    t0 = 1 / (1 - q)
    t1 = p / (1 - q) + q / (1 - q) ** 2
    t2 = p * p / (1 - q) + 2 * p * q / (1 - q) ** 2 + q * (1 + q) / (1 - q) ** 3
    a = 2 * abs(k)
    return (2 * b * t0,
            2 * math.sqrt(2) * b * (a * t0 + kappa * t1),
            4 * b * (a * a * t0 + 2 * a * kappa * t1 + kappa * kappa * t2))


def perturbative_coefficient(k, kappa):
    return (16 * k * math.exp(-2*k*k-kappa*kappa/4)
            * (kappa * math.cosh(k*kappa) - 2*k * math.sinh(k*kappa)))
