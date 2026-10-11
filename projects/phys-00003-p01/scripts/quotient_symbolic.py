#!/usr/bin/env python3
"""Symmetry-reduced symbolic quotient calculation on the dimensionless domain.

Set m=gamma=T=1, kstar=a>0, k=a+b^2, kappa=b.  Positive changes of
units map every physical parameter tuple to exactly one such (a,b), so signs of
current diffusion differences are preserved by a nonsingular congruence.

SO(2) symmetry splits the four quotient directions into an invariant two-vector
spanned by A=x cross v and r^2 A, and one real angular-two doublet.  The latter
is calculated in complex variables from F=u^2 A.  This avoids a large generic
69 by 69 symbolic inverse while retaining the complete degree<=4 closure.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


a, b = sp.symbols("a b", positive=True, finite=True)
x, y, vx, vy = sp.symbols("x y vx vy", real=True)
I = sp.I


def real_generator(poly, spring, torque):
    return sp.expand(
        vx * sp.diff(poly, x)
        + vy * sp.diff(poly, y)
        + (-spring * x - torque * y - vx) * sp.diff(poly, vx)
        + (torque * x - spring * y - vy) * sp.diff(poly, vy)
        + sp.diff(poly, vx, 2)
        + sp.diff(poly, vy, 2)
    )


X = x**2 + y**2
V = vx**2 + vy**2
C = x * vx + y * vy
A = x * vy - y * vx

# A linearly independent basis for all nonconstant SO(2)-invariant real
# polynomials of total degree <=4.  A^2=XV-C^2 removes the tenth quartic.
INVARIANT_BASIS = [
    X,
    V,
    C,
    A,
    X**2,
    V**2,
    X * V,
    X * C,
    X * A,
    V * C,
    V * A,
    C**2,
    C * A,
]


def solve_polynomial_poisson(basis, generator, targets, means, variables):
    images = [-generator(phi) for phi in basis]
    monomials = set()
    for expr in images:
        monomials.update(sp.Poly(expr, *variables).monoms())
    for target, mean in zip(targets, means):
        monomials.update(sp.Poly(target - mean, *variables).monoms())
    monomials = sorted(monomials, key=lambda z: (sum(z), z))
    matrix = sp.Matrix(
        [
            [sp.Poly(expr, *variables).coeff_monomial(mon) for expr in images]
            for mon in monomials
        ]
    )
    rhs = sp.Matrix(
        [
            [sp.Poly(target - mean, *variables).coeff_monomial(mon) for target, mean in zip(targets, means)]
            for mon in monomials
        ]
    )
    # Select a generic full-rank square subsystem at one legal rational point.
    # Solving the normal equations would unnecessarily square the expressions.
    probe = matrix.subs({a: sp.Integer(2), b: sp.Integer(1)})
    pivot_rows = probe.T.rref()[1]
    assert len(pivot_rows) == len(basis)
    square = matrix[list(pivot_rows), :]
    square_rhs = rhs[list(pivot_rows), :]
    solutions = square.inv(method="DM") * square_rhs
    # The selected rows determine the coefficients generically.  Verify the
    # full polynomial identity later by direct substitution in each sector.
    hs = [sp.expand(sum(solutions[i, j] * basis[i] for i in range(len(basis)))) for j in range(len(targets))]
    return hs, solutions


def real_covariance(driven=True):
    if driven:
        k = a + b**2
        return sp.Matrix(
            [
                [1 / a, 0, 0, b / a],
                [0, 1 / a, -b / a, 0],
                [0, -b / a, k / a, 0],
                [b / a, 0, 0, k / a],
            ]
        )
    return sp.diag(1 / a, 1 / a, 1, 1)


def gaussian_moment_factory(covariance, dimension):
    @lru_cache(maxsize=None)
    def moment(alpha):
        if sum(alpha) == 0:
            return sp.Integer(1)
        if sum(alpha) % 2:
            return sp.Integer(0)
        indices = []
        for j, count in enumerate(alpha):
            indices.extend([j] * count)
        first = indices[0]
        total = 0
        for pos in range(1, len(indices)):
            second = indices[pos]
            rest = indices[1:pos] + indices[pos + 1 :]
            beta = tuple(rest.count(j) for j in range(dimension))
            total += covariance[first, second] * moment(beta)
        return sp.factor(total)

    return moment


def polynomial_expectation(poly, variables, moment):
    p = sp.Poly(sp.expand(poly), *variables)
    return sp.factor(sum(coefficient * moment(mon) for mon, coefficient in p.terms()))


def isotropic_block(driven=True):
    if driven:
        spring, torque = a + b**2, b
        means = [2 * b / a, 8 * b / a**2]
    else:
        spring, torque = a, sp.Integer(0)
        means = [sp.Integer(0), sp.Integer(0)]
    targets = [A, X * A]
    hs, _ = solve_polynomial_poisson(
        INVARIANT_BASIS,
        lambda f: real_generator(f, spring, torque),
        targets,
        means,
        (x, y, vx, vy),
    )
    moment = gaussian_moment_factory(real_covariance(driven), 4)
    ns = sp.Matrix(
        2,
        2,
        lambda i, j: polynomial_expectation((targets[i] - means[i]) * hs[j], (x, y, vx, vy), moment),
    )
    diffusion = ((ns + ns.T) / 2).applyfunc(sp.factor)
    residuals = [sp.cancel(-real_generator(hs[j], spring, torque) - targets[j] + means[j]) for j in range(2)]
    assert residuals == [0, 0]
    return diffusion, hs


# Independent formal complex variables, ordered (u,s,ubar,sbar).
uc, sc, ub, sb = sp.symbols("u s ub sb")
COMPLEX_VARS = (uc, sc, ub, sb)


def complex_generator(poly, spring, torque):
    return sp.expand(
        sc * sp.diff(poly, uc)
        + sb * sp.diff(poly, ub)
        + ((-spring + I * torque) * uc - sc) * sp.diff(poly, sc)
        + ((-spring - I * torque) * ub - sb) * sp.diff(poly, sb)
        + 4 * sp.diff(poly, sc, sb)
    )


# All weight +2 monomials of total degree 2 or 4.
WEIGHT_TWO_BASIS = [uc**2, uc * sc, sc**2]
for positive_u_power in range(4):
    positive_s_power = 3 - positive_u_power
    WEIGHT_TWO_BASIS.append(uc**positive_u_power * sc**positive_s_power * ub)
    WEIGHT_TWO_BASIS.append(uc**positive_u_power * sc**positive_s_power * sb)


def complex_covariance(driven=True):
    if driven:
        k = a + b**2
        return sp.Matrix(
            [
                [0, 0, 2 / a, -2 * I * b / a],
                [0, 0, 2 * I * b / a, 2 * k / a],
                [2 / a, 2 * I * b / a, 0, 0],
                [-2 * I * b / a, 2 * k / a, 0, 0],
            ]
        )
    return sp.Matrix([[0, 0, 2 / a, 0], [0, 0, 0, 2], [2 / a, 0, 0, 0], [0, 2, 0, 0]])


def conjugate_form(poly):
    return sp.expand(sp.conjugate(poly).xreplace({sp.conjugate(uc): ub, sp.conjugate(ub): uc, sp.conjugate(sc): sb, sp.conjugate(sb): sc}))


def angular_two_diffusion(driven=True):
    spring, torque = (a + b**2, b) if driven else (a, sp.Integer(0))
    area = (ub * sc - uc * sb) / (2 * I)
    target = sp.expand(uc**2 * area)
    hs, _ = solve_polynomial_poisson(
        WEIGHT_TWO_BASIS,
        lambda f: complex_generator(f, spring, torque),
        [target],
        [sp.Integer(0)],
        COMPLEX_VARS,
    )
    residual = sp.cancel(-complex_generator(hs[0], spring, torque) - target)
    assert residual == 0
    moment = gaussian_moment_factory(complex_covariance(driven), 4)
    # Re E[conj(F) H]/2 is the diffusion of Re(F)=(x^2-y^2)A.
    pairing = polynomial_expectation(conjugate_form(target) * hs[0], COMPLEX_VARS, moment)
    # a and b carry real/positive assumptions at construction, so ordinary
    # conjugation already fixes them and reverses I.
    diffusion = sp.factor((pairing + sp.conjugate(pairing)) / 4)
    return diffusion, hs[0]


def main():
    print("REDUCTION=m=gamma=T=1,kstar=a>0,k=a+b^2,kappa=b")
    print("QUOTIENT_SPLIT=isotropic_span(A,r^2*A)+angular_two_doublet")
    qd, _ = isotropic_block(True)
    print("driven_isotropic_symbolic_poisson_residual=zero_polynomial")
    qe, _ = isotropic_block(False)
    print("equilibrium_isotropic_symbolic_poisson_residual=zero_polynomial")
    delta = (qd - qe).applyfunc(sp.factor)
    print(f"Qiso_driven={qd.tolist()}")
    print(f"Qiso_equilibrium={qe.tolist()}")
    print(f"Qiso_delta={delta.tolist()}")
    print(f"Qiso_delta_00={sp.factor(delta[0,0])}")
    print(f"Qiso_delta_det={sp.factor(delta.det())}")
    ad, _ = angular_two_diffusion(True)
    print("driven_angular_two_symbolic_poisson_residual=zero_polynomial")
    ae, _ = angular_two_diffusion(False)
    print("equilibrium_angular_two_symbolic_poisson_residual=zero_polynomial")
    angular_delta = sp.factor(ad - ae)
    print(f"Dangular_driven={ad}")
    print(f"Dangular_equilibrium={ae}")
    print(f"Dangular_delta={angular_delta}")


if __name__ == "__main__":
    main()
