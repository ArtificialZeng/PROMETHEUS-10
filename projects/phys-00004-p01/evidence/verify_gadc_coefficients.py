#!/usr/bin/env python3
"""Verify the positive-temperature pure-output coefficient reduction.

This is diagnostic research evidence for the frozen two-use GADC problem.  It
checks exact formulas for E2 and E4, compares them with both existing channel
implementations, and attacks (but does not prove) the resulting sufficient
coefficient inequality on a deterministic full-domain Sobol sample.
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


def coefficient_formula(
    gamma: np.ndarray | float,
    eta: np.ndarray | float,
    probabilities: np.ndarray,
    phase: np.ndarray | float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return E2, E4, the one-use determinant d(e), and the v coefficient.

    The last axis of ``probabilities`` is (A,B,C,P).  All operations broadcast.
    """
    gamma = np.asarray(gamma, dtype=float)
    eta = np.asarray(eta, dtype=float)
    phase = np.asarray(phase, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    A, B, C, P = np.moveaxis(probabilities, -1, 0)
    S = B + C
    v = B * C
    y = np.sqrt(np.maximum(0.0, A * P * v)) * np.cos(phase)

    up = gamma * eta
    down = gamma * (1.0 - eta)
    q = 1.0 - gamma
    alpha = up * (1.0 - up)
    beta = down * (1.0 - down)
    contrast = down - up
    tau = gamma - 2.0 * up * down
    r_up = 1.0 - 2.0 * up + 2.0 * up**2

    E2 = (
        2.0 * alpha * (1.0 - alpha)
        - 2.0 * contrast**2 * q**2 * P**2
        + 4.0 * up * contrast * q**2 * P * S
        + 2.0 * contrast * q * r_up * P
        + gamma * q * r_up * S**2
        - 2.0 * up * q * r_up * S
        - 4.0 * q * tau * y
    )

    z0 = (1.0 - up) ** 2 * A + (1.0 - up) * down * S + down**2 * P
    z1 = (
        up * (1.0 - up) * A
        + (1.0 - up) * (1.0 - down) * S
        + down * (1.0 - down) * P
    )
    z2 = up * (1.0 - up) * A + up * down * S + down * (1.0 - down) * P
    z3 = up**2 * A + up * (1.0 - down) * S + (1.0 - down) ** 2 * P

    x01 = np.sqrt(np.maximum(0.0, q * A * S)) * (1.0 - up)
    x02 = np.sqrt(np.maximum(0.0, q * S * P)) * down
    x03 = q * np.sqrt(np.maximum(0.0, A * P))
    x13 = np.sqrt(np.maximum(0.0, q * S * P)) * (1.0 - down)
    x23 = np.sqrt(np.maximum(0.0, q * A * S)) * up
    D0 = (
        z0 * z1 * z2 * z3
        - x01**2 * z2 * z3
        - x02**2 * z1 * z3
        - x03**2 * z1 * z2
        - x13**2 * z0 * z2
        - x23**2 * z0 * z1
        + x01**2 * x23**2
        + x02**2 * x13**2
        - 2.0 * x01 * x02 * x13 * x23
        + 2.0 * x01 * x03 * x13 * z2
        + 2.0 * x02 * x03 * x23 * z1
    )

    K = A * S * alpha + S * P * beta + 4.0 * A * P * up * down
    coefficient_v = 4.0 * up * down * q**2 * K
    X0 = A * alpha + S * up * down + P * beta
    X1 = A * alpha + S * (1.0 - up) * (1.0 - down) + P * beta
    E4 = D0 + coefficient_v * v - 8.0 * up * down * q * X0 * X1 * y

    energy = P + 0.5 * S
    one_use_determinant = alpha - 2.0 * up * q * energy + gamma * q * energy**2
    return E2, E4, one_use_determinant, coefficient_v


def exact_checks() -> dict[str, bool]:
    """Symbolically verify the compact E2 identity and structured D0 formula."""
    A, B, C, P, y, up, down = sp.symbols("A B C P y up down")
    q = 1 - up - down
    S = B + C
    gamma = up + down
    alpha = up * (1 - up)
    contrast = down - up
    tau = gamma - 2 * up * down
    r_up = 1 - 2 * up + 2 * up**2

    z0 = (1 - up) ** 2 * A + (1 - up) * down * S + down**2 * P
    z1 = (
        up * (1 - up) * A
        + (1 - up) * (1 - down) * B
        + up * down * C
        + down * (1 - down) * P
    )
    z2 = (
        up * (1 - up) * A
        + up * down * B
        + (1 - up) * (1 - down) * C
        + down * (1 - down) * P
    )
    z3 = up**2 * A + up * (1 - down) * S + (1 - down) ** 2 * P
    off_squared_sum = q * (
        (1 - up) ** 2 * A * S
        + down**2 * P * S
        + 4 * down * (1 - up) * y
    )
    off_squared_sum += q * (
        up**2 * A * S
        + (1 - down) ** 2 * P * S
        + 4 * up * (1 - down) * y
    )
    off_squared_sum += q**2 * (A * P + B * C)
    actual_E2 = sp.expand((1 - (z0**2 + z1**2 + z2**2 + z3**2 + 2 * off_squared_sum)) / 2)
    predicted_E2 = (
        2 * alpha * (1 - alpha)
        - 2 * contrast**2 * q**2 * P**2
        + 4 * up * contrast * q**2 * P * S
        + 2 * contrast * q * r_up * P
        + gamma * q * r_up * S**2
        - 2 * up * q * r_up * S
        - 4 * q * tau * y
    )
    # The formula uses A+B+C+P=1.  Eliminate A in both expressions.
    E2_identity = sp.expand(
        (actual_E2 - predicted_E2).subs(A, 1 - B - C - P)
    ) == 0

    z0s, z1s, z2s, z3s = sp.symbols("z0s z1s z2s z3s")
    a01, a02, a03, a13, a23 = sp.symbols("a01 a02 a03 a13 a23")
    structured = sp.Matrix(
        [
            [z0s, a01, a02, a03],
            [a01, z1s, 0, a13],
            [a02, 0, z2s, a23],
            [a03, a13, a23, z3s],
        ]
    )
    structured_D0 = (
        z0s * z1s * z2s * z3s
        - a01**2 * z2s * z3s
        - a02**2 * z1s * z3s
        - a03**2 * z1s * z2s
        - a13**2 * z0s * z2s
        - a23**2 * z0s * z1s
        + a01**2 * a23**2
        + a02**2 * a13**2
        - 2 * a01 * a02 * a13 * a23
        + 2 * a01 * a03 * a13 * z2s
        + 2 * a02 * a03 * a23 * z1s
    )
    D0_identity = sp.expand(structured.det() - structured_D0) == 0

    # A homogeneous exact determinant check.  Keep the coherence scale as an
    # indeterminate t, compute by fraction-free elimination, then reduce every
    # even power t^(2j) to q^j.  This verifies both affine coefficients in
    # v=BC and y, not merely the structured four-by-four determinant template.
    aa, bb, cc, dd, phase_root, t = sp.symbols(
        "aa bb cc dd phase_root t", nonzero=True
    )
    Ah, Bh, Ch, Ph = aa**2, bb**2, cc**2, dd**2
    Sh, vh = Bh + Ch, Bh * Ch
    yh = aa * bb * cc * dd * (phase_root + 1 / phase_root) / 2
    h0 = (1 - up) ** 2 * Ah + (1 - up) * down * Sh + down**2 * Ph
    h1 = (
        up * (1 - up) * Ah
        + (1 - up) * (1 - down) * Bh
        + up * down * Ch
        + down * (1 - down) * Ph
    )
    h2 = (
        up * (1 - up) * Ah
        + up * down * Bh
        + (1 - up) * (1 - down) * Ch
        + down * (1 - down) * Ph
    )
    h3 = up**2 * Ah + up * (1 - down) * Sh + (1 - down) ** 2 * Ph
    homogeneous_output = sp.Matrix(
        [
            [
                h0,
                t * ((1 - up) * aa * bb + down * cc * dd / phase_root),
                t * ((1 - up) * aa * cc + down * bb * dd / phase_root),
                q * aa * dd / phase_root,
            ],
            [
                t * ((1 - up) * aa * bb + down * cc * dd * phase_root),
                h1,
                q * bb * cc,
                t * (up * aa * cc + (1 - down) * bb * dd / phase_root),
            ],
            [
                t * ((1 - up) * aa * cc + down * bb * dd * phase_root),
                q * bb * cc,
                h2,
                t * (up * aa * bb + (1 - down) * cc * dd / phase_root),
            ],
            [
                q * aa * dd * phase_root,
                t * (up * aa * cc + (1 - down) * bb * dd * phase_root),
                t * (up * aa * bb + (1 - down) * cc * dd * phase_root),
                h3,
            ],
        ]
    )
    raw_determinant = homogeneous_output.det(method="domain-ge")
    polynomial_t = sp.Poly(sp.expand(raw_determinant), t)
    assert all(exponent[0] % 2 == 0 for exponent, _ in polynomial_t.terms())
    actual_E4 = sp.expand(
        sum(
            coefficient * q ** (exponent[0] // 2)
            for exponent, coefficient in polynomial_t.terms()
        )
    )

    h1s = (
        up * (1 - up) * Ah
        + (1 - up) * (1 - down) * Sh
        + down * (1 - down) * Ph
    )
    h2s = up * (1 - up) * Ah + up * down * Sh + down * (1 - down) * Ph
    b01 = q * (1 - up) ** 2 * Ah * Sh
    b02 = q * down**2 * Sh * Ph
    b03 = q**2 * Ah * Ph
    b13 = q * (1 - down) ** 2 * Sh * Ph
    b23 = q * up**2 * Ah * Sh
    D0_polynomial = (
        h0 * h1s * h2s * h3
        - b01 * h2s * h3
        - b02 * h1s * h3
        - b03 * h1s * h2s
        - b13 * h0 * h2s
        - b23 * h0 * h1s
        + q**2 * (1 - up) ** 2 * up**2 * Ah**2 * Sh**2
        + q**2 * down**2 * (1 - down) ** 2 * Sh**2 * Ph**2
        - 2 * q**2 * (1 - up) * down * (1 - down) * up * Ah * Sh**2 * Ph
        + 2 * q**2 * (1 - up) * (1 - down) * Ah * Sh * Ph * h2s
        + 2 * q**2 * up * down * Ah * Sh * Ph * h1s
    )
    Kh = (
        Ah * Sh * up * (1 - up)
        + Sh * Ph * down * (1 - down)
        + 4 * Ah * Ph * up * down
    )
    X0h = Ah * up * (1 - up) + Sh * up * down + Ph * down * (1 - down)
    X1h = (
        Ah * up * (1 - up)
        + Sh * (1 - up) * (1 - down)
        + Ph * down * (1 - down)
    )
    predicted_E4 = sp.expand(
        D0_polynomial
        + 4 * up * down * q**2 * Kh * vh
        - 8 * up * down * q * X0h * X1h * yh
    )
    E4_identity = sp.expand(actual_E4 - predicted_E4) == 0

    e_symbol = sp.symbols("e_symbol")
    d_symbol = (
        alpha - 2 * up * q * e_symbol + gamma * q * e_symbol**2
    )
    r_squared = (
        (1 - 2 * up) ** 2
        + 4 * gamma * q * (2 * up / gamma - e_symbol) * e_symbol
    )
    one_use_identity = sp.factor(
        (1 - r_squared - 4 * d_symbol) * gamma
    ) == 0
    return {
        "E2_identity_after_normalization": E2_identity,
        "full_E4_affine_identity": E4_identity,
        "structured_D0_determinant_identity": D0_identity,
        "E4_v_coefficient_manifestly_nonnegative": True,
        "one_minus_r_squared_equals_four_d": one_use_identity,
    }


def numerical_crosschecks(sample_count: int = 2048) -> dict[str, float | int]:
    rng = np.random.default_rng(2026091203)
    max_ab = 0.0
    max_e2 = 0.0
    max_e4 = 0.0
    min_cv = float("inf")
    for _ in range(sample_count):
        probabilities = rng.dirichlet(np.full(4, 0.8))
        gamma = float(rng.uniform(0.0, 1.0))
        eta = float(rng.uniform(0.0, 0.5))
        phase = float(rng.uniform(-np.pi, np.pi))
        vector = np.sqrt(probabilities).astype(complex)
        vector[3] *= np.exp(1j * phase)
        rho = np.outer(vector, vector.conj())
        output_a = method_a.apply_two(rho, gamma, eta)
        output_b = method_b.apply_two(rho, gamma, eta)
        max_ab = max(max_ab, float(np.max(np.abs(output_a - output_b))))
        actual_e2 = float((1.0 - np.real(np.trace(output_a @ output_a))) / 2.0)
        actual_e4 = float(np.real(np.linalg.det(output_a)))
        formula_e2, formula_e4, _, coefficient_v = coefficient_formula(
            gamma, eta, probabilities, phase
        )
        max_e2 = max(max_e2, abs(actual_e2 - float(formula_e2)))
        max_e4 = max(max_e4, abs(actual_e4 - float(formula_e4)))
        min_cv = min(min_cv, float(coefficient_v))
    assert max_ab < 5e-15
    assert max_e2 < 5e-15
    assert max_e4 < 5e-15
    assert min_cv >= -1e-16
    return {
        "sample_count": sample_count,
        "seed": 2026091203,
        "max_A_B_output_difference": max_ab,
        "max_E2_formula_error": max_e2,
        "max_E4_formula_error": max_e4,
        "minimum_v_coefficient": min_cv,
    }


def sobol_attack(power: int = 18) -> dict[str, object]:
    unit = qmc.Sobol(d=6, scramble=True, seed=2026091204).random_base2(power)
    gamma = unit[:, 0]
    eta = 0.5 * unit[:, 1]
    energy = unit[:, 2]
    lower = np.maximum(0.0, 2.0 * energy - 1.0)
    P = lower + unit[:, 3] * (energy - lower)
    S = 2.0 * (energy - P)
    probabilities = np.column_stack(
        (
            1.0 - 2.0 * energy + P,
            S * unit[:, 4],
            S * (1.0 - unit[:, 4]),
            P,
        )
    )
    phase = 2.0 * np.pi * unit[:, 5]
    E2, E4, one_d, coefficient_v = coefficient_formula(
        gamma, eta, probabilities, phase
    )
    sqrt_E4 = np.sqrt(np.maximum(E4, 0.0))
    shell_margin = E2 + 2.0 * sqrt_E4 - 2.0 * one_d

    A, B, C, P_formula = np.moveaxis(probabilities, -1, 0)
    v = B * C
    y = np.sqrt(np.maximum(0.0, A * P_formula * v)) * np.cos(phase)
    minimum_v = np.divide(
        y**2,
        A * P_formula,
        out=np.zeros_like(y),
        where=A * P_formula > 0.0,
    )
    worst_E4_at_fixed_y = E4 - coefficient_v * (v - minimum_v)
    reduced_shell_margin = (
        E2 + 2.0 * np.sqrt(np.maximum(worst_E4_at_fixed_y, 0.0)) - 2.0 * one_d
    )
    squaring_threshold = one_d - 0.5 * E2
    positive_threshold = squaring_threshold > 0.0
    squared_margin = worst_E4_at_fixed_y - squaring_threshold**2

    radicand = np.maximum(0.0, 1.0 - 4.0 * gamma * eta * (1.0 - eta))
    unconstrained = np.minimum(
        1.0,
        eta
        + np.divide(
            np.sqrt(radicand),
            2.0 * np.sqrt(gamma),
            out=np.full_like(gamma, np.inf),
            where=gamma > 0.0,
        ),
    )
    x_e = np.minimum(energy, unconstrained)
    r_x = np.sqrt(
        np.maximum(
            0.0,
            (1.0 - 2.0 * eta * gamma) ** 2
            + 4.0 * gamma * (1.0 - gamma) * (2.0 * eta - x_e) * x_e,
        )
    )
    bound = r_x - 2.0 * (1.0 - gamma) * (energy - x_e)
    original_margin = 2.0 * E2 + 4.0 * sqrt_E4 - (1.0 - bound**2)
    saturated = energy > unconstrained

    def record(mask: np.ndarray) -> dict[str, object]:
        indices = np.flatnonzero(mask)
        local = int(indices[np.argmin(original_margin[mask])])
        return {
            "count": int(len(indices)),
            "minimum_original_margin": float(original_margin[local]),
            "shell_margin_at_minimizer": float(shell_margin[local]),
            "index": local,
            "gamma": float(gamma[local]),
            "eta": float(eta[local]),
            "energy": float(energy[local]),
            "probabilities": [float(x) for x in probabilities[local]],
            "phase": float(phase[local]),
        }

    product_residuals = []
    for g, z, e in (
        (0.17, 0.04, 0.23),
        (0.51, 0.21, 0.67),
        (0.89, 0.49, 0.41),
    ):
        product_probabilities = np.array(
            [(1.0 - e) ** 2, e * (1.0 - e), e * (1.0 - e), e**2]
        )
        pE2, pE4, pd, _ = coefficient_formula(
            g, z, product_probabilities, 0.0
        )
        product_residuals.append(float(pE2 + 2.0 * np.sqrt(pE4) - 2.0 * pd))

    assert float(np.min(coefficient_v)) >= -1e-15
    assert float(np.min(shell_margin)) > -2e-13
    assert float(np.min(reduced_shell_margin)) > -2e-13
    assert float(np.min(squared_margin[positive_threshold])) > -2e-13
    assert float(np.min(original_margin)) > -2e-13
    assert max(abs(x) for x in product_residuals) < 2e-14
    return {
        "sampler": "scrambled Sobol",
        "seed": 2026091204,
        "sample_count": int(len(unit)),
        "all": record(np.ones(len(unit), dtype=bool)),
        "unsaturated_branch": record(~saturated),
        "saturated_branch": record(saturated),
        "minimum_shell_margin": float(np.min(shell_margin)),
        "minimum_reduced_shell_margin": float(np.min(reduced_shell_margin)),
        "minimum_squared_margin_when_threshold_positive": float(
            np.min(squared_margin[positive_threshold])
        ),
        "positive_squaring_threshold_count": int(np.sum(positive_threshold)),
        "minimum_v_coefficient": float(np.min(coefficient_v)),
        "product_shell_equality_residuals": product_residuals,
        "interpretation": "finite diagnostic attack, not a universal proof",
    }


def main() -> None:
    report = {
        "status": "pass",
        "scope": "pure two-use GADC coefficients and sufficient inequality attack",
        "exact": exact_checks(),
        "numerical_crosschecks": numerical_crosschecks(),
        "sobol_attack": sobol_attack(),
        "software": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
        "limitations": [
            "The coefficient identities and v-monotonicity reduction are exact.",
            "The Sobol attack is finite and cannot establish the remaining inequality.",
            "No failed sufficient inequality or ergotropy counterexample was observed.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
