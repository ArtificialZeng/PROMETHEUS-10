#!/usr/bin/env python3
"""Independent two-time Gaussian/Wick replay of quotient diffusion matrices.

This script starts from the complex SDE in the coordinate order
(Re u, Re s, Im u, Im s)=(x1,v1,x2,v2).  It does not import the real Poisson or
symmetry-reduced symbolic implementations.  At each lag it constructs the full
eight-variable two-time covariance and evaluates moments through Isserlis
pairing, then integrates the symmetrized correlations on [0,infinity).
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import eigvals, expm, solve_continuous_lyapunov


CASES = [
    (1.0, 1.0, 2.0, 1.0, 1.0),
    (2.0, 3.0, 5.0, 7.0, -1.0),
    (3.0 / 2.0, 4.0 / 3.0, 3.0, 5.0 / 2.0, 1.0 / 2.0),
]


def reconstruct(m, gamma, spring, temperature, torque):
    complex_drift = np.array(
        [[0.0, 1.0], [(-spring + 1j * torque) / m, -gamma / m]], dtype=complex
    )
    re, im = complex_drift.real, complex_drift.imag
    drift = np.block([[re, -im], [im, re]])
    noise = np.diag(
        [0.0, 2.0 * gamma * temperature / m**2, 0.0, 2.0 * gamma * temperature / m**2]
    )
    return drift, noise


def current_basis():
    # y=(x1,v1,x2,v2), A=x1*v2-x2*v1.
    prefactors = [(0, 0), (2, 0), (1, 1), (0, 2)]
    currents = []
    for px, py in prefactors:
        current = {}
        alpha = [0, 0, 0, 0]
        alpha[0], alpha[2], alpha[3] = px + 1, py, 1
        current[tuple(alpha)] = 1.0
        alpha = [0, 0, 0, 0]
        alpha[0], alpha[1], alpha[2] = px, 1, py + 1
        current[tuple(alpha)] = -1.0
        currents.append(current)
    return currents


CURRENTS = current_basis()
UPPER = [(i, j) for i in range(4) for j in range(i, 4)]


def gaussian_moment_factory(covariance):
    @lru_cache(maxsize=None)
    def moment(alpha):
        degree = sum(alpha)
        if degree == 0:
            return 1.0
        if degree % 2:
            return 0.0
        indices = []
        for i, count in enumerate(alpha):
            indices.extend([i] * count)
        first = indices[0]
        total = 0.0
        for pos in range(1, len(indices)):
            second = indices[pos]
            rest = indices[1:pos] + indices[pos + 1 :]
            beta = tuple(rest.count(i) for i in range(len(alpha)))
            total += covariance[first, second] * moment(beta)
        return float(total)

    return moment


def one_time_means(covariance):
    moment = gaussian_moment_factory(covariance)
    return np.array(
        [sum(c * moment(alpha) for alpha, c in current.items()) for current in CURRENTS]
    )


def cross_expectation(left, right, moment):
    total = 0.0
    for alpha, ca in left.items():
        for beta, cb in right.items():
            joined = tuple(alpha) + tuple(beta)
            total += ca * cb * moment(joined)
    return total


def wick_matrix(m, gamma, spring, temperature, torque):
    drift, noise = reconstruct(m, gamma, spring, temperature, torque)
    spectral_abscissa = float(np.max(eigvals(drift).real))
    if not spectral_abscissa < 0:
        raise AssertionError("unstable drift")
    covariance = solve_continuous_lyapunov(drift, -noise)
    covariance = (covariance + covariance.T) / 2
    residual = float(np.linalg.norm(drift @ covariance + covariance @ drift.T + noise, ord=np.inf))
    means = one_time_means(covariance)

    def integrand(time):
        cross = expm(drift * time) @ covariance
        joint = np.block([[covariance, cross], [cross.T, covariance]])
        moment = gaussian_moment_factory(joint)
        values = []
        for i, j in UPPER:
            forward = cross_expectation(CURRENTS[i], CURRENTS[j], moment) - means[i] * means[j]
            backward = cross_expectation(CURRENTS[j], CURRENTS[i], moment) - means[j] * means[i]
            values.append((forward + backward) / 2)
        return np.asarray(values)

    values, error = quad_vec(
        integrand,
        0.0,
        np.inf,
        epsabs=2e-9,
        epsrel=2e-10,
        norm="max",
        limit=700,
    )
    matrix = np.zeros((4, 4))
    for value, (i, j) in zip(values, UPPER):
        matrix[i, j] = matrix[j, i] = value
    return {
        "matrix": matrix,
        "means": means,
        "spectral_abscissa": spectral_abscissa,
        "lyapunov_residual_inf": residual,
        "quad_vec_error": float(error),
    }


def fmt(array):
    return np.array2string(
        np.asarray(array), precision=15, separator=",", suppress_small=False, max_line_width=100000
    ).replace("\n", "")


def main():
    print("METHOD_B=complex-coordinate full two-time covariance + eight-variable Wick pairing")
    print("coordinate_order=(Re_u,Re_s,Im_u,Im_s)=(x1,v1,x2,v2)")
    print("quotient_basis=(1,x1^2,x1*x2,x2^2)*R*x")
    print("integration=symmetrized_cross_correlations_on_[0,infinity)")
    for parameters in CASES:
        m, gamma, k, temperature, kappa = parameters
        kstar = k - m * kappa**2 / gamma**2
        if not kstar > 0:
            raise AssertionError("inadmissible case")
        driven = wick_matrix(m, gamma, k, temperature, kappa)
        equilibrium = wick_matrix(m, gamma, kstar, temperature, 0.0)
        delta = driven["matrix"] - equilibrium["matrix"]
        eigenvalues = np.linalg.eigvalsh(delta)
        print(f"case_parameters_m_gamma_k_T_kappa={parameters}")
        print(f"kstar={kstar:.17g}")
        print(f"driven_means={fmt(driven['means'])}")
        print(f"equilibrium_means={fmt(equilibrium['means'])}")
        print(f"Q_driven={fmt(driven['matrix'])}")
        print(f"Q_equilibrium={fmt(equilibrium['matrix'])}")
        print(f"Q_delta={fmt(delta)}")
        print(f"Q_delta_eigenvalues={fmt(eigenvalues)}")
        print(f"driven_spectral_abscissa={driven['spectral_abscissa']:.17g}")
        print(f"equilibrium_spectral_abscissa={equilibrium['spectral_abscissa']:.17g}")
        print(f"max_lyapunov_residual_inf={max(driven['lyapunov_residual_inf'], equilibrium['lyapunov_residual_inf']):.17g}")
        print(f"max_quad_vec_error={max(driven['quad_vec_error'], equilibrium['quad_vec_error']):.17g}")
    print("status=PASS")


if __name__ == "__main__":
    main()
