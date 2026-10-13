#!/usr/bin/env python3
"""Independent 100-digit finite-entropy checks for the U(16) analysis.

This implementation does not import the double-precision Hessian code.  It
checks the weakest discovered phase direction with a direct 4x4 partial trace,
an exactly factorizable phase gauge, and one support-opening Givens rotation
with a direct 16x16 partial trace.
"""

from __future__ import annotations

import mpmath as mp


mp.mp.dps = 100
r = mp.mpf(1) / 2
d = 3 + r * r
c1 = mp.matrix([[r / mp.sqrt(d), 1 / mp.sqrt(d)],
                [1 / mp.sqrt(d), 1 / mp.sqrt(d)]])


def kron(a: mp.matrix, b: mp.matrix) -> mp.matrix:
    result = mp.matrix(a.rows * b.rows, a.cols * b.cols)
    for i in range(a.rows):
        for j in range(a.cols):
            for k in range(b.rows):
                for ell in range(b.cols):
                    result[i * b.rows + k, j * b.cols + ell] = a[i, j] * b[k, ell]
    return result


c = kron(c1, c1)


def entropy_from_rho(rho: mp.matrix) -> mp.mpf:
    values = mp.eighe(rho, eigvals_only=True)
    answer = mp.mpf("0")
    for value in values:
        if value > mp.mpf("1e-90"):
            answer -= value * mp.log(value, 2)
    return answer


def active_phase_entropy(theta: mp.matrix, t: mp.mpf) -> mp.mpf:
    amplitude = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            amplitude[i, j] = c[i, j] * mp.exp(1j * t * theta[i, j])
    return entropy_from_rho(amplitude * amplitude.H)


raw_theta = mp.matrix([
    ["+0.74691523008180893", "-0.24894407648606701", "-0.24894407532978102", "-0.24902707826596068"],
    ["-0.24894407248467451", "+0.079290476898495596", "+0.05735117506208124", "+0.11230242052409793"],
    ["-0.24894407545520827", "+0.057351175751901948", "+0.079290477883514246", "+0.11230242181979228"],
    ["-0.24902708214192579", "+0.11230242383566967", "+0.11230242238418593", "+0.024422235922070188"],
])


def remove_factorizable_phase(theta: mp.matrix) -> mp.matrix:
    row_mean = [sum(theta[i, j] for j in range(4)) / 4 for i in range(4)]
    col_mean = [sum(theta[i, j] for i in range(4)) / 4 for j in range(4)]
    grand = sum(theta[i, j] for i in range(4) for j in range(4)) / 16
    result = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            result[i, j] = theta[i, j] - row_mean[i] - col_mean[j] + grand
    norm = mp.sqrt(sum(result[i, j] ** 2 for i in range(4) for j in range(4)))
    return result / norm


theta = remove_factorizable_phase(raw_theta)
f0 = active_phase_entropy(theta, mp.mpf("0"))


def full_amplitude(w: mp.matrix) -> mp.matrix:
    result = mp.matrix(16, 16)
    for i in range(4):
        for a in range(4):
            for j in range(4):
                for b in range(4):
                    result[4 * i + a, 4 * j + b] = c[i, j] * w[4 * a + b, 4 * i + j]
    return result


def full_entropy(w: mp.matrix) -> mp.mpf:
    amplitude = full_amplitude(w)
    return entropy_from_rho(amplitude * amplitude.H)


def support_rotation(t: mp.mpf) -> mp.matrix:
    w = mp.eye(16)
    x, y = 0, 5
    angle = t / mp.sqrt(2)
    w[x, x] = mp.cos(angle)
    w[y, y] = mp.cos(angle)
    w[y, x] = mp.sin(angle)
    w[x, y] = -mp.sin(angle)
    return w


def fmt(value: mp.mpf, digits: int = 50) -> str:
    return mp.nstr(value, digits)


print(f"mpmath_dps={mp.mp.dps}")
print(f"canonical_entropy_bits={fmt(f0, 60)}")
print("weakest_phase_double_centered")
for i in range(4):
    print("  " + " ".join(fmt(theta[i, j], 30) for j in range(4)))
print("weakest_phase_finite_differences")
for text_step in ("0.02", "0.01", "0.005", "0.0025", "0.00125"):
    step = mp.mpf(text_step)
    plus = active_phase_entropy(theta, step)
    minus = active_phase_entropy(theta, -step)
    delta_plus = plus - f0
    delta_minus = minus - f0
    curvature = (plus + minus - 2 * f0) / (step * step)
    print(
        f"  step={text_step} delta_plus={fmt(delta_plus)} "
        f"delta_minus={fmt(delta_minus)} curvature={fmt(curvature)}"
    )

# A factorizable table theta_ij=a_i+b_j is exactly a local-ancilla gauge.
a_phase = [mp.mpf("0.1"), mp.mpf("-0.3"), mp.mpf("0.7"), mp.mpf("-0.2")]
b_phase = [mp.mpf("0.4"), mp.mpf("-0.5"), mp.mpf("0.2"), mp.mpf("0.9")]
gauge_theta = mp.matrix(4, 4)
for i in range(4):
    for j in range(4):
        gauge_theta[i, j] = a_phase[i] + b_phase[j]
gauge_delta = active_phase_entropy(gauge_theta, mp.mpf("0.37")) - f0
print(f"factorizable_phase_gauge_delta_bits={fmt(gauge_delta, 30)}")

mu = (c[0, 0] ** 2 + c[1, 1] ** 2) / 2
print(f"support_opening_mu_norm2={fmt(mu, 60)}")
print("support_opening_finite_differences")
for text_step in ("0.02", "0.01", "0.005", "0.0025", "0.00125", "0.000625"):
    step = mp.mpf(text_step)
    delta = full_entropy(support_rotation(step)) - f0
    leading = -2 * mu * step * step * mp.log(step, 2)
    print(
        f"  step={text_step} delta_bits={fmt(delta)} "
        f"leading_bits={fmt(leading)} ratio={fmt(delta/leading,30)}"
    )
