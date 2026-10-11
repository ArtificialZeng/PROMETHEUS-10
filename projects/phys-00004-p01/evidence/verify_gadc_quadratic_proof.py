#!/usr/bin/env python3
"""Exact audit of the remaining positive-temperature GADC inequality.

The symbolic part checks the multiplier identity used in
``gadc_quadratic_exact_proof.md``.  The numerical part is only a diagnostic
cross-check against the two independently reconstructed channel maps; the
scientific certificate is the exact identity and its sign decomposition.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import scipy
import sympy as sp
from scipy.stats import qmc

sys.path.insert(0, "evidence")
import method_a_kraus as method_a  # noqa: E402
import method_b_liouville as method_b  # noqa: E402
from verify_gadc_coefficients import coefficient_formula  # noqa: E402


def symbolic_certificate() -> dict[str, bool]:
    u, d, A, S, P, y = sp.symbols("u d A S P y")
    g = u + d
    q = 1 - g
    alpha = u * (1 - u)
    beta = d * (1 - d)
    tau = g - 2 * u * d
    contrast = d - u
    r_up = 1 - 2 * u + 2 * u**2
    energy = P + S / 2

    z0 = (1 - u) ** 2 * A + (1 - u) * d * S + d**2 * P
    z1 = u * (1 - u) * A + (1 - u) * (1 - d) * S + d * (1 - d) * P
    z2 = u * (1 - u) * A + u * d * S + d * (1 - d) * P
    z3 = u**2 * A + u * (1 - d) * S + (1 - d) ** 2 * P
    D0 = (
        z0 * z1 * z2 * z3
        - q * (1 - u) ** 2 * A * S * z2 * z3
        - q * d**2 * S * P * z1 * z3
        - q**2 * A * P * z1 * z2
        - q * (1 - d) ** 2 * S * P * z0 * z2
        - q * u**2 * A * S * z0 * z1
        + q**2 * (1 - u) ** 2 * u**2 * A**2 * S**2
        + q**2 * d**2 * (1 - d) ** 2 * S**2 * P**2
        - 2 * q**2 * (1 - u) * d * (1 - d) * u * A * S**2 * P
        + 2 * q**2 * (1 - u) * (1 - d) * A * S * P * z2
        + 2 * q**2 * u * d * A * S * P * z1
    )

    R = A * alpha + P * beta
    X0 = R + S * u * d
    X1 = R + S * (1 - u) * (1 - d)
    X = X0 * X1
    K = S * R + 4 * A * P * u * d
    J = X0**2 + u * d * q * (S**2 - 4 * A * P)

    E20 = (
        2 * alpha * (1 - alpha)
        - 2 * contrast**2 * q**2 * P**2
        + 4 * u * contrast * q**2 * P * S
        + 2 * contrast * q * r_up * P
        + g * q * r_up * S**2
        - 2 * u * q * r_up * S
    )
    E2 = E20 - 4 * q * tau * y
    one_d = alpha - 2 * u * q * energy + g * q * energy**2
    T = one_d - E2 / 2
    E4_min = D0 + 4 * u * d * q**2 * K * y**2 / (A * P) - 8 * u * d * q * X * y
    Q = sp.cancel(E4_min - T**2)

    kappa = g * (g - 4 * u * d)
    F = g * (2 - g) - 4 * u * d * q
    remainder = (
        g**2 * alpha**2 * A**2
        + 2 * u * d * alpha * F * A * S
        + 2 * u**2 * d**2 * g**2 * A * P
        + u * d * g**2 * (q + 2 * u * d) * S**2 / 2
        + 2 * u * d * beta * F * S * P
        + g**2 * beta**2 * P**2
    )
    positive_remainder = (
        g**2 * alpha**2 * A**2
        + 2 * u * d * alpha * g**2 * A * S
        + 2 * u**2 * d**2 * g**2 * A * P
        + u * d * g**2 * (q + 2 * u * d) * S**2 / 2
        + 2 * u * d * beta * g**2 * S * P
        + g**2 * beta**2 * P**2
    )
    G = S**2 / 4 + A * P - 2 * y
    H = A * P * S**2 / 4 - y**2

    normalization = {A: 1 - S - P}
    multiplier_residual = sp.factor(
        (
            A * P * tau * Q
            - A * P * q * G * (kappa * T + remainder)
            + 4 * S * u * d * q**2 * tau * R * H
        ).subs(normalization)
    )
    ellipse_residual = sp.factor(
        (K * D0 - 4 * A * P * u * d * X**2 - S * R * J**2).subs(normalization)
    )

    return {
        "X_minus_qK_identity": sp.expand(X - q * K - J) == 0,
        "D0_ellipse_identity_after_normalization": ellipse_residual == 0,
        "multiplier_identity_after_normalization": multiplier_residual == 0,
        "remainder_subtraction_identity": sp.expand(
            remainder - 4 * S * u * d * q * tau * R - positive_remainder
        )
        == 0,
        "F_minus_2q_tau_equals_g_squared": sp.expand(F - 2 * q * tau - g**2) == 0,
        "interval_slack_identity": sp.expand(A * P * G - H - (A * P - y) ** 2) == 0,
        "alpha_beta_identity": sp.expand(alpha * beta - u * d * (q + u * d)) == 0,
    }


def numerical_crosscheck(power: int = 16) -> dict[str, object]:
    unit = qmc.Sobol(d=6, scramble=True, seed=2026091205).random_base2(power)
    gamma = unit[:, 0]
    eta = 0.5 * unit[:, 1]
    state = -np.log(np.clip(unit[:, 2:5], np.finfo(float).tiny, 1.0))
    state /= np.sum(state, axis=1, keepdims=True)
    A, S, P = state.T
    phase_coordinate = 2.0 * unit[:, 5] - 1.0
    y_bound = 0.5 * S * np.sqrt(A * P)
    y = phase_coordinate * y_bound

    # Realize the exact worst-v boundary by choosing B,C with BC=y^2/(AP).
    v = np.divide(y**2, A * P, out=np.zeros_like(y), where=A * P > 0)
    split = np.sqrt(np.maximum(0.0, S**2 - 4.0 * v))
    B = 0.5 * (S + split)
    C = 0.5 * (S - split)
    probabilities = np.column_stack((A, B, C, P))
    phase = np.where(y >= 0.0, 0.0, np.pi)

    E2, E4, one_d, _ = coefficient_formula(gamma, eta, probabilities, phase)
    T = one_d - 0.5 * E2
    Q = E4 - T**2

    u = gamma * eta
    d = gamma * (1.0 - eta)
    q = 1.0 - gamma
    g = gamma
    alpha = u * (1.0 - u)
    beta = d * (1.0 - d)
    tau = g - 2.0 * u * d
    R = A * alpha + P * beta
    kappa = g * (g - 4.0 * u * d)
    F = g * (2.0 - g) - 4.0 * u * d * q
    remainder = (
        g**2 * alpha**2 * A**2
        + 2.0 * u * d * alpha * F * A * S
        + 2.0 * u**2 * d**2 * g**2 * A * P
        + 0.5 * u * d * g**2 * (q + 2.0 * u * d) * S**2
        + 2.0 * u * d * beta * F * S * P
        + g**2 * beta**2 * P**2
    )
    positive_remainder = remainder - 4.0 * S * u * d * q * tau * R
    G = 0.25 * S**2 + A * P - 2.0 * y
    H = 0.25 * A * P * S**2 - y**2
    identity_rhs = (
        A * P * q * G * (kappa * T + remainder)
        - 4.0 * S * u * d * q**2 * tau * R * H
    )
    identity_lhs = A * P * tau * Q
    lower_bound = A * P * q * G * (kappa * T + positive_remainder)

    # Directly compare a deterministic subset against both channel maps.
    max_ab = 0.0
    max_formula = 0.0
    for index in np.linspace(0, len(unit) - 1, 512, dtype=int):
        vector = np.sqrt(probabilities[index]).astype(complex)
        vector[3] *= np.exp(1j * phase[index])
        rho = np.outer(vector, vector.conj())
        output_a = method_a.apply_two(rho, float(gamma[index]), float(eta[index]))
        output_b = method_b.apply_two(rho, float(gamma[index]), float(eta[index]))
        max_ab = max(max_ab, float(np.max(np.abs(output_a - output_b))))
        actual_e2 = float((1.0 - np.real(np.trace(output_a @ output_a))) / 2.0)
        actual_e4 = float(np.real(np.linalg.det(output_a)))
        max_formula = max(
            max_formula,
            abs(actual_e2 - float(E2[index])),
            abs(actual_e4 - float(E4[index])),
        )

    positive = T > 0.0
    assert np.max(np.abs(identity_lhs - identity_rhs)) < 2e-16
    assert np.min(positive_remainder) > -2e-16
    assert np.min(Q[positive]) > -2e-13
    assert np.min(identity_lhs[positive] - lower_bound[positive]) > -2e-16
    assert max_ab < 5e-15
    assert max_formula < 5e-15
    return {
        "sampler": "scrambled Sobol with exact worst-v realization",
        "seed": 2026091205,
        "sample_count": int(len(unit)),
        "positive_T_count": int(np.sum(positive)),
        "minimum_Q_when_T_positive": float(np.min(Q[positive])),
        "minimum_manifest_remainder": float(np.min(positive_remainder)),
        "maximum_multiplier_identity_residual": float(
            np.max(np.abs(identity_lhs - identity_rhs))
        ),
        "minimum_interval_bound_residual_when_T_positive": float(
            np.min(identity_lhs[positive] - lower_bound[positive])
        ),
        "max_A_B_output_difference": max_ab,
        "max_coefficient_formula_error": max_formula,
        "interpretation": "diagnostic cross-check only; exact polynomial identities are the certificate",
    }


def main() -> None:
    report = {
        "status": "pass",
        "scope": "remaining full-domain pure-state GADC coefficient inequality",
        "exact": symbolic_certificate(),
        "numerical_crosscheck": numerical_crosscheck(),
        "software": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
        "limitations": [
            "The script certifies the displayed algebraic identities, not literature novelty.",
            "The final original-claim resolution also uses the previously audited pure-state, spectral-spread, and energy-ball reductions.",
            "Human author review and a fresh scientific referee remain required.",
        ],
    }
    assert all(report["exact"].values())
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
