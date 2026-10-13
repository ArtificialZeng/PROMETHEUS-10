#!/usr/bin/env python3
"""Exact symbolic audit of closure of order-three unistochastic matrices.

The proof has three ingredients: an exterior-algebra endpoint certificate for
an orthostochastic multiplier, the CKM chord between two orthostochastic
endpoints, and concavity of the qutrit Heron witness along that chord.  This
script audits the latter two as polynomial identities, then replays a fully
interior rational/algebraic holdout and an exact unitary completion.
"""

from __future__ import annotations

import sympy as sp


I = sp.I
R = sp.Rational


def require(condition: object, message: str) -> None:
    if condition is not True and condition != sp.S.true:
        raise AssertionError(message)
    print(f"PASS: {message}")


def matrix_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    return left.shape == right.shape and all(
        sp.simplify(left[i, j] - right[i, j]) == 0
        for i in range(left.rows)
        for j in range(left.cols)
    )


def squared_moduli(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(lambda value: sp.simplify(value * sp.conjugate(value)))


def bistochastic(a: sp.Expr, b: sp.Expr, c: sp.Expr, d: sp.Expr) -> sp.Matrix:
    return sp.Matrix(
        [
            [a, b, 1 - a - b],
            [c, d, 1 - c - d],
            [1 - a - c, 1 - b - d, a + b + c + d - 1],
        ]
    )


def h_value(matrix: sp.Matrix) -> sp.Expr:
    x = [sp.factor(matrix[i, 0] * matrix[i, 1]) for i in range(3)]
    return sp.factor(
        2 * (x[0] * x[1] + x[0] * x[2] + x[1] * x[2])
        - sum(value**2 for value in x)
    )


def coordinate_h(matrix: sp.Matrix) -> sp.Expr:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    return sp.factor(4 * a * b * c * d - (a + b + c + d - 1 - a * d - b * c) ** 2)


def ckm_unitary(
    parameters: tuple[sp.Expr, ...], phase: sp.Expr
) -> sp.Matrix:
    s12, c12, s13, c13, s23, c23 = parameters
    return sp.Matrix(
        [
            [c12 * c13, s12 * c13, s13 / phase],
            [
                -s12 * c23 - c12 * s23 * s13 * phase,
                c12 * c23 - s12 * s23 * s13 * phase,
                s23 * c13,
            ],
            [
                s12 * s23 - c12 * c23 * s13 * phase,
                -c12 * s23 - s12 * c23 * s13 * phase,
                c23 * c13,
            ],
        ]
    )


def ckm_probability(
    parameters: tuple[sp.Expr, ...], cosine_delta: sp.Expr
) -> sp.Matrix:
    s12, c12, s13, c13, s23, c23 = parameters
    return sp.Matrix(
        [
            [c12**2 * c13**2, s12**2 * c13**2, s13**2],
            [
                (s12 * c23) ** 2
                + (c12 * s23 * s13) ** 2
                + 2 * s12 * c23 * c12 * s23 * s13 * cosine_delta,
                (c12 * c23) ** 2
                + (s12 * s23 * s13) ** 2
                - 2 * c12 * c23 * s12 * s23 * s13 * cosine_delta,
                s23**2 * c13**2,
            ],
            [
                (s12 * s23) ** 2
                + (c12 * c23 * s13) ** 2
                - 2 * s12 * s23 * c12 * c23 * s13 * cosine_delta,
                (c12 * s23) ** 2
                + (s12 * c23 * s13) ** 2
                + 2 * c12 * s23 * s12 * c23 * s13 * cosine_delta,
                c23**2 * c13**2,
            ],
        ]
    ).applyfunc(sp.factor)


def complete_from_first_two_probability_columns(matrix: sp.Matrix) -> sp.Matrix:
    """Construct one exact unitary realizer when h(matrix)>0."""
    n = [sp.factor(matrix[i, 0] * matrix[i, 1]) for i in range(3)]
    lengths = [sp.sqrt(value) for value in n]
    cosine = sp.factor((n[2] - n[0] - n[1]) / (2 * lengths[0] * lengths[1]))
    sine = sp.sqrt(sp.factor(1 - cosine**2))
    phases = [sp.S.One, sp.simplify(cosine + I * sine)]
    phases.append(sp.simplify(-(lengths[0] + lengths[1] * phases[1]) / lengths[2]))
    first = sp.Matrix([sp.sqrt(matrix[i, 0]) for i in range(3)])
    second = sp.Matrix([sp.sqrt(matrix[i, 1]) * phases[i] for i in range(3)])
    third = sp.Matrix(
        [
            sp.conjugate(first[1] * second[2] - first[2] * second[1]),
            sp.conjugate(first[2] * second[0] - first[0] * second[2]),
            sp.conjugate(first[0] * second[1] - first[1] * second[0]),
        ]
    )
    return first.row_join(second).row_join(third)


print("EXACT QUTRIT UNISTOCHASTIC MONOID PROOF AUDIT")
print("COMMAND: python3 -B code/exact_qutrit_monoid_proof.py")
print("SCOPE: the frozen order-three proposition; exact finite-dimensional arithmetic")

# The generic qutrit witness in four bistochastic coordinates.
a, b, c, d = sp.symbols("a b c d", real=True)
generic_bistochastic = bistochastic(a, b, c, d)
require(
    sp.factor(h_value(generic_bistochastic) - coordinate_h(generic_bistochastic)) == 0,
    "Heron and four-coordinate qutrit witnesses agree identically",
)

# Concavity when only rows 1 and 2 move oppositely.  This is precisely the
# left CKM phase-normal direction after multiplication by a fixed A.
t, r, s = sp.symbols("t r s", real=True)
moving = bistochastic(a, b, c + t * r, d + t * s)
moving_polynomial = sp.Poly(sp.expand(coordinate_h(moving)), t)
leading = sp.factor(moving_polynomial.coeff_monomial(t**2))
leading_expected = sp.factor(
    4 * a * b * r * s - ((1 - b) * r + (1 - a) * s) ** 2
)
require(leading == leading_expected, "exact phase-chord quadratic coefficient is identified")
off_diagonal = a * b + a + b - 1
quadratic_form = sp.Matrix(
    [[-(1 - b) ** 2, off_diagonal], [off_diagonal, -(1 - a) ** 2]]
)
require(
    sp.factor(quadratic_form.det() - 4 * a * b * (1 - a - b)) == 0,
    "concavity-form determinant is 4ab(1-a-b)",
)
require(
    sp.factor((sp.Matrix([r, s]).T * quadratic_form * sp.Matrix([r, s]))[0] - leading)
    == 0,
    "quadratic coefficient equals the negative-semidefinite form",
)
print(
    "CERTIFICATE: for a>=0, b>=0, a+b<=1 the form has nonpositive diagonal "
    "and nonnegative determinant, hence h is concave along the full CKM chord."
)

# Universal CKM chord and its exact real orthogonal endpoints.  Polynomial
# reduction modulo the three circle relations audits endpoint orthogonality.
s12, c12, s13, c13, s23, c23, xphase = sp.symbols(
    "s12 c12 s13 c13 s23 c23 x", real=True
)
parameters_symbolic = (s12, c12, s13, c13, s23, c23)
C_symbolic = ckm_probability(parameters_symbolic, xphase)
C_plus = ckm_probability(parameters_symbolic, 1)
C_minus = ckm_probability(parameters_symbolic, -1)
require(
    matrix_equal(
        C_symbolic,
        ((1 + xphase) * C_plus + (1 - xphase) * C_minus) / 2,
    ),
    "every CKM probability matrix is the affine chord of its two real endpoints",
)
D = sp.Matrix([[0, 0, 0], [1, -1, 0], [-1, 1, 0]])
normal_scale = 2 * s12 * c12 * s13 * s23 * c23
require(
    matrix_equal(C_symbolic.diff(xphase), normal_scale * D),
    "the CKM chord has the rank-one opposite-row direction",
)

circle_relations = [
    s12**2 + c12**2 - 1,
    s13**2 + c13**2 - 1,
    s23**2 + c23**2 - 1,
]
groebner = sp.groebner(
    circle_relations, s12, c12, s13, c13, s23, c23, order="grevlex"
)
for endpoint in (-1, 1):
    Q_endpoint = ckm_unitary(parameters_symbolic, sp.Integer(endpoint))
    residuals = list(Q_endpoint.T * Q_endpoint - sp.eye(3))
    require(
        all(groebner.reduce(sp.expand(value))[1] == 0 for value in residuals),
        f"CKM endpoint {endpoint:+d} is orthogonal modulo the three circle identities",
    )
    require(
        matrix_equal(squared_moduli(Q_endpoint), ckm_probability(parameters_symbolic, endpoint)),
        f"CKM endpoint {endpoint:+d} realizes its probability matrix entry by entry",
    )

# Fully interior exact holdout, separate from the earlier boundary examples.
p34 = (R(3, 5), R(4, 5))
p512 = (R(5, 13), R(12, 13))
p815 = (R(8, 17), R(15, 17))
parameters_a = (p34[0], p34[1], p512[0], p512[1], p815[0], p815[1])
parameters_c = (p815[0], p815[1], p34[0], p34[1], p512[0], p512[1])
phase_a = R(5, 13) + I * R(12, 13)
phase_c = R(3, 5) + I * R(4, 5)
P_holdout = ckm_unitary(parameters_a, phase_a)
Q_holdout = ckm_unitary(parameters_c, phase_c)
require(matrix_equal(P_holdout.H * P_holdout, sp.eye(3)), "holdout right realizer is exactly unitary")
require(matrix_equal(Q_holdout.H * Q_holdout, sp.eye(3)), "holdout left realizer is exactly unitary")
A_holdout = squared_moduli(P_holdout)
C_holdout = squared_moduli(Q_holdout)
M_holdout = (C_holdout * A_holdout).applyfunc(sp.factor)
require(all(value > 0 for value in A_holdout), "holdout right factor is entrywise positive")
require(all(value > 0 for value in C_holdout), "holdout left factor is entrywise positive")
require(h_value(A_holdout) > 0 and h_value(C_holdout) > 0, "both holdout factors are strict interior points")

x = sp.symbols("x", real=True)
C_holdout_chord = ckm_probability(parameters_c, x)
f = sp.Poly(sp.expand(h_value(C_holdout_chord * A_holdout)), x)
require(f.degree() == 2, "holdout product witness is exactly quadratic on the left CKM chord")
require(f.coeff_monomial(x**2) < 0, "holdout chord is strictly concave")
f_minus = sp.factor(f.as_expr().subs(x, -1))
f_plus = sp.factor(f.as_expr().subs(x, 1))
require(f_minus >= 0 and f_plus >= 0, "holdout orthostochastic endpoint products have h>=0")
target_x = R(3, 5)
linear_endpoint_chord = sp.factor(
    (1 - target_x) * f_minus / 2 + (1 + target_x) * f_plus / 2
)
target_h = sp.factor(h_value(M_holdout))
require(
    sp.factor(target_h - f.as_expr().subs(x, target_x)) == 0,
    "holdout target equals the CKM-chord polynomial at cos(delta_C)=3/5",
)
require(target_h >= linear_endpoint_chord > 0, "exact concavity lower bound certifies holdout h>0")

W_holdout = complete_from_first_two_probability_columns(M_holdout)
require(matrix_equal(W_holdout.H * W_holdout, sp.eye(3)), "exact holdout completion W is unitary")
require(matrix_equal(squared_moduli(W_holdout), M_holdout), "exact holdout W realizes C*A entry by entry")

# One singular CKM chart branch: s13=0 makes the phase-normal scale vanish and
# the whole chord collapse to a single orthostochastic matrix.
singular_parameters = (p34[0], p34[1], sp.S.Zero, sp.S.One, p512[0], p512[1])
singular_plus = ckm_probability(singular_parameters, 1)
singular_minus = ckm_probability(singular_parameters, -1)
require(matrix_equal(singular_plus, singular_minus), "s13=0 singular chart collapses the CKM chord")
require(
    matrix_equal(
        squared_moduli(ckm_unitary(singular_parameters, 1)), singular_plus
    ),
    "collapsed singular endpoint remains exactly orthostochastic",
)

print(f"concavity_leading_coefficient={leading}")
print(f"holdout_endpoint_h_minus={f_minus}")
print(f"holdout_endpoint_h_plus={f_plus}")
print(f"holdout_linear_endpoint_bound={linear_endpoint_chord}")
print(f"holdout_product_h={target_h}")
print(
    "RESULT: every order-three unistochastic product is unistochastic.  The two "
    "orthostochastic endpoints are admissible by the exterior certificate, and "
    "concavity carries h>=0 across the entire CKM chord."
)
print("PHYSICAL RESULT: every two-step measured qutrit channel in the frozen model has a one-step U(3) realization.")
