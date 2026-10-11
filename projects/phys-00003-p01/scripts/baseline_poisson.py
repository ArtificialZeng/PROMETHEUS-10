#!/usr/bin/env python3
"""Exact real-basis Poisson reproduction of the zero-field work baseline.

This implementation starts from the four real SDE coordinates in source.md.
It neither imports nor reads the covariance/Wick implementation or its output.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

import sympy as sp


def symbolic_baseline():
    m, gamma, k, temperature = sp.symbols("m gamma k T", positive=True, finite=True)
    kappa = sp.symbols("kappa", real=True, nonzero=True, finite=True)
    kstar = k - m * kappa**2 / gamma**2

    # z=(x1,x2,v1,v2), dz=A z dt+B dW.
    A = sp.Matrix(
        [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [-k / m, -kappa / m, -gamma / m, 0],
            [kappa / m, -k / m, 0, -gamma / m],
        ]
    )
    Q = sp.diag(0, 0, 2 * gamma * temperature / m**2, 2 * gamma * temperature / m**2)
    R = sp.Matrix([[0, -1], [1, 0]])
    sigma_xx = temperature / kstar * sp.eye(2)
    sigma_vx = temperature * kappa / (gamma * kstar) * R
    sigma_vv = temperature * k / (m * kstar) * sp.eye(2)
    Sigma = sigma_xx.row_join(sigma_vx.T).col_join(sigma_vx.row_join(sigma_vv))

    lyapunov_residual = (A * Sigma + Sigma * A.T + Q).applyfunc(sp.factor)
    assert lyapunov_residual == sp.zeros(4)

    # f=z^T F z=kappa (R x).v=kappa(x1*v2-x2*v1).
    F = sp.zeros(4)
    F[0, 3] = F[3, 0] = kappa / 2
    F[1, 2] = F[2, 1] = -kappa / 2
    mean = sp.factor(sp.trace(F * Sigma))

    # h=z^T H z solves -Lh=f-<f>.  The quadratic sector is an exact
    # invariant subspace of the full polynomial space of total degree <=4.
    hs = sp.symbols("h00 h01 h02 h03 h11 h12 h13 h22 h23 h33")
    H = sp.Matrix(
        [
            [hs[0], hs[1], hs[2], hs[3]],
            [hs[1], hs[4], hs[5], hs[6]],
            [hs[2], hs[5], hs[7], hs[8]],
            [hs[3], hs[6], hs[8], hs[9]],
        ]
    )
    sylvester = A.T * H + H * A + F
    equations = [sylvester[i, j] for i in range(4) for j in range(i, 4)]
    coeff_matrix, rhs = sp.linear_eq_to_matrix(equations, hs)
    solution = sp.linsolve((coeff_matrix, rhs), hs)
    solution_tuple = next(iter(solution))
    Hsol = H.subs(dict(zip(hs, solution_tuple)))
    assert (A.T * Hsol + Hsol * A + F).applyfunc(sp.factor) == sp.zeros(4)

    poisson_constant = sp.factor(sp.trace(Q * Hsol) - mean)
    assert poisson_constant == 0
    diffusion = sp.factor(2 * sp.trace(F * Sigma * Hsol * Sigma))

    expected_mean = sp.factor(2 * kappa**2 * temperature / (gamma * kstar))
    expected_diffusion = sp.factor(
        2
        * kappa**2
        * temperature**2
        * (k**2 + kappa**2 + 3 * m * k * kappa**2 / gamma**2)
        / (gamma * kstar**3)
    )
    assert sp.factor(mean - expected_mean) == 0
    assert sp.factor(diffusion - expected_diffusion) == 0

    return {
        "symbols": (m, gamma, k, temperature, kappa),
        "A": A,
        "Q": Q,
        "Sigma": Sigma,
        "F": F,
        "mean": mean,
        "diffusion": diffusion,
        "expected_mean": expected_mean,
        "expected_diffusion": expected_diffusion,
    }


def monomial_basis(max_degree: int):
    return sorted(
        [alpha for alpha in product(range(max_degree + 1), repeat=4) if sum(alpha) <= max_degree],
        key=lambda alpha: (sum(alpha), alpha),
    )


def add_term(poly, alpha, coefficient):
    if coefficient:
        poly[alpha] = sp.factor(poly.get(alpha, 0) + coefficient)
        if poly[alpha] == 0:
            del poly[alpha]


def generator_on_monomial(alpha, A, noise_strength):
    """Return L z^alpha as an exponent->coefficient dictionary."""
    out = {}
    for i in range(4):
        if alpha[i] == 0:
            continue
        for j in range(4):
            if A[i, j] == 0:
                continue
            beta = list(alpha)
            beta[i] -= 1
            beta[j] += 1
            add_term(out, tuple(beta), alpha[i] * A[i, j])
    for i in (2, 3):
        if alpha[i] >= 2:
            beta = list(alpha)
            beta[i] -= 2
            add_term(out, tuple(beta), noise_strength * alpha[i] * (alpha[i] - 1))
    return out


def exact_degree_four_check(parameter_values):
    """Solve the complete nonconstant degree<=4 Poisson system exactly."""
    m, gamma, k, temperature, kappa = map(sp.Rational, parameter_values)
    kstar = k - m * kappa**2 / gamma**2
    assert kstar > 0 and kappa != 0
    A = sp.Matrix(
        [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [-k / m, -kappa / m, -gamma / m, 0],
            [kappa / m, -k / m, 0, -gamma / m],
        ]
    )
    noise_strength = gamma * temperature / m**2
    basis = monomial_basis(4)
    nonconstant = basis[1:]
    row_index = {alpha: i for i, alpha in enumerate(nonconstant)}
    matrix = sp.zeros(len(nonconstant))
    constant_row = sp.zeros(1, len(nonconstant))
    for col, alpha in enumerate(nonconstant):
        image = generator_on_monomial(alpha, A, noise_strength)
        for beta, coefficient in image.items():
            if sum(beta) == 0:
                constant_row[0, col] -= coefficient
            else:
                matrix[row_index[beta], col] -= coefficient

    mean = 2 * kappa**2 * temperature / (gamma * kstar)
    rhs = sp.zeros(len(nonconstant), 1)
    # g=kappa*x1*v2-kappa*x2*v1-mean; constant handled separately.
    rhs[row_index[(1, 0, 0, 1)], 0] = kappa
    rhs[row_index[(0, 1, 1, 0)], 0] = -kappa
    coefficients = matrix.inv() * rhs
    constant_residual = sp.factor((constant_row * coefficients)[0] + mean)
    assert constant_residual == 0

    degree_four_nonzero = [
        (alpha, coefficients[i])
        for i, alpha in enumerate(nonconstant)
        if sum(alpha) in (3, 4) and coefficients[i] != 0
    ]
    assert not degree_four_nonzero

    R = sp.Matrix([[0, -1], [1, 0]])
    sigma_xx = temperature / kstar * sp.eye(2)
    sigma_vx = temperature * kappa / (gamma * kstar) * R
    sigma_vv = temperature * k / (m * kstar) * sp.eye(2)
    Sigma = sigma_xx.row_join(sigma_vx.T).col_join(sigma_vx.row_join(sigma_vv))

    @lru_cache(maxsize=None)
    def gaussian_moment(alpha):
        degree = sum(alpha)
        if degree == 0:
            return sp.Integer(1)
        if degree % 2:
            return sp.Integer(0)
        indices = []
        for idx, count in enumerate(alpha):
            indices.extend([idx] * count)
        first = indices[0]
        total = 0
        for pos in range(1, len(indices)):
            second = indices[pos]
            remaining = indices[1:pos] + indices[pos + 1 :]
            beta = tuple(remaining.count(i) for i in range(4))
            total += Sigma[first, second] * gaussian_moment(beta)
        return sp.factor(total)

    # D=<g,h>; the constant part of g drops because <h> need not be zero,
    # so compute the centered expectation explicitly.
    mean_h = sum(coefficients[i] * gaussian_moment(alpha) for i, alpha in enumerate(nonconstant))
    f_times_h = 0
    for i, alpha in enumerate(nonconstant):
        if coefficients[i] == 0:
            continue
        beta1 = list(alpha)
        beta1[0] += 1
        beta1[3] += 1
        beta2 = list(alpha)
        beta2[1] += 1
        beta2[2] += 1
        f_times_h += coefficients[i] * kappa * (
            gaussian_moment(tuple(beta1)) - gaussian_moment(tuple(beta2))
        )
    diffusion = sp.factor(f_times_h - mean * mean_h)
    expected = sp.factor(
        2
        * kappa**2
        * temperature**2
        * (k**2 + kappa**2 + 3 * m * k * kappa**2 / gamma**2)
        / (gamma * kstar**3)
    )
    assert sp.factor(diffusion - expected) == 0
    return {
        "parameters": [str(value) for value in (m, gamma, k, temperature, kappa)],
        "kstar": str(kstar),
        "basis_size_including_constant": len(basis),
        "unknown_nonconstant_coefficients": len(nonconstant),
        "degree_3_or_4_solution_coefficients_nonzero": len(degree_four_nonzero),
        "constant_equation_residual": str(constant_residual),
        "mean": str(mean),
        "diffusion": str(diffusion),
        "expected_diffusion": str(expected),
    }


def main():
    result = symbolic_baseline()
    print("METHOD_A=real-coordinate stationary covariance + exact polynomial Poisson solve")
    print("coordinate_order=(x1,x2,v1,v2)")
    print("lyapunov_residual=zero_symbolically")
    print(f"mean_rate={result['mean']}")
    print(f"published_mean_rate={result['expected_mean']}")
    print("mean_identity_residual=0")
    print(f"D_var_over_2t={result['diffusion']}")
    print(f"published_D_var_over_2t={result['expected_diffusion']}")
    print("diffusion_identity_residual=0")
    for values in [(1, 1, 2, 1, 1), (2, 3, 5, 7, 1)]:
        check = exact_degree_four_check(values)
        print(f"full_degree_le_4_check={check}")
    print("status=PASS")


if __name__ == "__main__":
    main()
