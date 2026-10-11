#!/usr/bin/env python3
"""Independent complex-coordinate covariance/Wick baseline reproduction.

This implementation reconstructs the dynamics from u=x1+i*x2 and s=v1+i*v2,
computes the stationary covariance numerically, and integrates the two-time Wick
correlator.  It never imports or reads baseline_poisson.py or its outputs.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigvals, expm, solve_continuous_lyapunov


CASES = [
    (1.0, 1.0, 2.0, 1.0, 1.0),
    (2.0, 3.0, 5.0, 7.0, 1.0),
    (2.0, 3.0, 5.0, 7.0, -1.0),
    (1.5, 4.0 / 3.0, 3.0, 2.5, 0.5),
    (5.0, 2.0, 4.0, 3.0, 0.5),
]


def reconstruct_from_complex(m, gamma, k, temperature, kappa):
    # In complex coordinates: du=s dt,
    # m ds=(-k+i*kappa)u dt-gamma*s dt+complex isotropic noise.
    complex_drift = np.array(
        [[0.0, 1.0], [(-k + 1j * kappa) / m, -gamma / m]], dtype=complex
    )
    real = complex_drift.real
    imag = complex_drift.imag
    # y=(Re u,Re s,Im u,Im s)=(x1,v1,x2,v2).
    drift = np.block([[real, -imag], [imag, real]])
    noise_covariance = np.diag(
        [0.0, 2.0 * gamma * temperature / m**2, 0.0, 2.0 * gamma * temperature / m**2]
    )
    work_form = np.zeros((4, 4))
    work_form[0, 3] = work_form[3, 0] = kappa / 2.0
    work_form[2, 1] = work_form[1, 2] = -kappa / 2.0
    return drift, noise_covariance, work_form


def published_zero_field(m, gamma, k, temperature, kappa):
    kstar = k - m * kappa**2 / gamma**2
    mean = 2.0 * kappa**2 * temperature / (gamma * kstar)
    diffusion = (
        2.0
        * kappa**2
        * temperature**2
        * (k**2 + kappa**2 + 3.0 * m * k * kappa**2 / gamma**2)
        / (gamma * kstar**3)
    )
    return mean, diffusion


def reproduce_case(parameters):
    m, gamma, k, temperature, kappa = parameters
    kstar = k - m * kappa**2 / gamma**2
    if not (m > 0 and gamma > 0 and k > 0 and temperature > 0 and kappa != 0 and kstar > 0):
        raise ValueError("inadmissible parameter tuple")
    drift, noise_covariance, work_form = reconstruct_from_complex(*parameters)
    eigenvalues = eigvals(drift)
    spectral_abscissa = float(np.max(eigenvalues.real))
    if not spectral_abscissa < 0:
        raise AssertionError("drift is not strictly stable")
    covariance = solve_continuous_lyapunov(drift, -noise_covariance)
    covariance = (covariance + covariance.T) / 2.0
    lyapunov_residual = drift @ covariance + covariance @ drift.T + noise_covariance
    residual_norm = float(np.linalg.norm(lyapunov_residual, ord=np.inf))

    mean = float(np.trace(work_form @ covariance))

    def wick_covariance(time):
        two_time = expm(drift * time) @ covariance
        return float(2.0 * np.trace(work_form @ two_time @ work_form @ two_time.T))

    diffusion_quad, quadrature_error = quad(
        wick_covariance, 0.0, np.inf, epsabs=2e-11, epsrel=2e-11, limit=500
    )

    # Independent evaluation of the same Wick integral: if
    # X=int_0^inf exp(M^T t) F exp(M t)dt, then M^T X+XM=-F.
    wick_integral_matrix = solve_continuous_lyapunov(drift.T, -work_form)
    diffusion_resolvent = float(
        2.0 * np.trace(wick_integral_matrix @ covariance @ work_form @ covariance)
    )
    expected_mean, expected_diffusion = published_zero_field(*parameters)
    mean_abs_error = abs(mean - expected_mean)
    diffusion_abs_error = abs(diffusion_quad - expected_diffusion)
    integration_cross_error = abs(diffusion_quad - diffusion_resolvent)
    tolerance = 2e-9 * max(1.0, abs(expected_diffusion))
    passed = (
        residual_norm < 2e-11
        and mean_abs_error < 2e-10 * max(1.0, abs(expected_mean))
        and diffusion_abs_error < tolerance
        and integration_cross_error < tolerance
        and quadrature_error < tolerance
    )
    if not passed:
        raise AssertionError("covariance/Wick reproduction failed tolerance")
    return {
        "parameters_m_gamma_k_T_kappa": parameters,
        "kstar": kstar,
        "spectral_abscissa": spectral_abscissa,
        "lyapunov_residual_inf": residual_norm,
        "mean_rate_wick": mean,
        "mean_rate_published": expected_mean,
        "mean_abs_error": mean_abs_error,
        "D_quad_wick": diffusion_quad,
        "D_resolvent_wick": diffusion_resolvent,
        "D_published": expected_diffusion,
        "D_abs_error": diffusion_abs_error,
        "quad_error_estimate": quadrature_error,
        "quad_resolvent_abs_difference": integration_cross_error,
        "tolerance": tolerance,
        "pass": passed,
    }


def main():
    print("METHOD_B=complex-coordinate two-time covariance + Wick contractions")
    print("complex_basis=(u=x1+i*x2,s=v1+i*v2)")
    print("real_numerical_order=(Re_u,Re_s,Im_u,Im_s)=(x1,v1,x2,v2)")
    print("stationary_covariance=independent_numerical_Lyapunov_solve")
    print("D_convention=integral_0_infinity_centered_autocovariance=lim_Var_over_2t")
    for case in CASES:
        print(f"case={reproduce_case(case)}")
    print("status=PASS")


if __name__ == "__main__":
    main()
