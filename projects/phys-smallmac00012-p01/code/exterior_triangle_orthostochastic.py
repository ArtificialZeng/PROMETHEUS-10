#!/usr/bin/env python3
"""Exact audit of an exterior-algebra certificate for a qutrit product.

The accompanying proof shows that if one order-three unistochastic factor is
orthostochastic, then the product is unistochastic.  This script checks the
universal algebraic identities before orthogonality is imposed and replays
both a strict all-positive example and a degenerate saturated example in exact
SymPy arithmetic.  It is an audit of the proof, not a finite-search argument.
"""

from __future__ import annotations

import itertools

import sympy as sp


I = sp.I
R = sp.Rational
PAIRS = ((0, 1), (0, 2), (1, 2))


def require(condition: object, message: str) -> None:
    if condition is not True and condition != sp.S.true:
        raise AssertionError(message)
    print(f"PASS: {message}")


def zero(expression: sp.Expr) -> bool:
    return sp.expand(expression) == 0


def matrix_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    return left.shape == right.shape and all(
        sp.simplify(left[i, j] - right[i, j]) == 0
        for i in range(left.rows)
        for j in range(left.cols)
    )


def absolute_square(value: sp.Expr) -> sp.Expr:
    return sp.expand(value * sp.conjugate(value))


def squared_moduli(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(lambda value: sp.simplify(absolute_square(value)))


def h_value(matrix: sp.Matrix) -> sp.Expr:
    x = [sp.factor(matrix[i, 0] * matrix[i, 1]) for i in range(3)]
    return sp.factor(
        2 * (x[0] * x[1] + x[0] * x[2] + x[1] * x[2])
        - sum(value**2 for value in x)
    )


def certificate_vectors(P: sp.Matrix, Q: sp.Matrix) -> list[sp.Matrix]:
    """Return z_i=(<x_i,y_i>, x_i wedge y_i) for each row of real Q."""
    result: list[sp.Matrix] = []
    for i in range(3):
        x = sp.Matrix([Q[i, k] * P[k, 0] for k in range(3)])
        y = sp.Matrix([Q[i, k] * P[k, 1] for k in range(3)])
        inner = (x.H * y)[0]
        minors = [x[k] * y[l] - x[l] * y[k] for k, l in PAIRS]
        result.append(sp.Matrix([inner, *minors]))
    return result


def norm_squared(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify((vector.H * vector)[0])


def ckm_unitary(
    parameters: tuple[sp.Rational, ...], phase: sp.Expr
) -> sp.Matrix:
    """Exact standard CKM representative, with phase=exp(i delta)."""
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


def quaternion_rotation(w: int, x: int, y: int, z: int) -> sp.Matrix:
    """Exact SO(3) rotation from an unnormalised real quaternion."""
    n = w * w + x * x + y * y + z * z
    return sp.Matrix(
        [
            [w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z],
        ]
    ) / n


def exact_certificate_audit(P: sp.Matrix, Q: sp.Matrix, label: str) -> sp.Matrix:
    require(matrix_equal(P.H * P, sp.eye(3)), f"{label}: P is exactly unitary")
    require(matrix_equal(Q.T * Q, sp.eye(3)), f"{label}: Q is exactly orthogonal")
    A = squared_moduli(P)
    C = squared_moduli(Q)
    M = (C * A).applyfunc(sp.factor)
    vectors = certificate_vectors(P, Q)
    require(
        matrix_equal(sum(vectors, sp.zeros(4, 1)), sp.zeros(4, 1)),
        f"{label}: the three certificate vectors sum exactly to zero",
    )
    for i, vector in enumerate(vectors):
        require(
            sp.simplify(norm_squared(vector) - M[i, 0] * M[i, 1]) == 0,
            f"{label}: ||z_{i}||^2=M[{i},0]M[{i},1]",
        )
    require(
        all(sum(M[i, j] for i in range(3)) == 1 for j in range(3))
        and all(sum(M[i, j] for j in range(3)) == 1 for i in range(3)),
        f"{label}: product is exactly bistochastic",
    )
    inner_01 = sp.simplify((vectors[0].H * vectors[1])[0])
    real_inner_01 = sp.simplify((inner_01 + sp.conjugate(inner_01)) / 2)
    gram_form = sp.factor(
        4
        * (
            norm_squared(vectors[0]) * norm_squared(vectors[1])
            - real_inner_01**2
        )
    )
    require(
        sp.simplify(h_value(M) - gram_form) == 0,
        f"{label}: h equals the exact real-Gram nonnegativity certificate",
    )
    return M


print("EXTERIOR-ALGEBRA ORTHOSTOCHASTIC-FACTOR AUDIT")
print("COMMAND: python3 -B code/exterior_triangle_orthostochastic.py")
print("SCOPE: exact qutrit lemma; not a proof of closure for two arbitrary interior factors")

# The complex Lagrange identity is the norm step in the universal proof.
x_real = sp.symbols("xr0:3", real=True)
x_imag = sp.symbols("xi0:3", real=True)
y_real = sp.symbols("yr0:3", real=True)
y_imag = sp.symbols("yi0:3", real=True)
x_generic = [x_real[k] + I * x_imag[k] for k in range(3)]
y_generic = [y_real[k] + I * y_imag[k] for k in range(3)]
generic_inner = sum(sp.conjugate(x_generic[k]) * y_generic[k] for k in range(3))
generic_minors = [
    x_generic[k] * y_generic[l] - x_generic[l] * y_generic[k] for k, l in PAIRS
]
lagrange_residual = (
    sum(absolute_square(value) for value in x_generic)
    * sum(absolute_square(value) for value in y_generic)
    - absolute_square(generic_inner)
    - sum(absolute_square(value) for value in generic_minors)
)
require(zero(lagrange_residual), "complex Lagrange identity holds as a polynomial identity")

# If z_0+z_1+z_2=0, Heron's polynomial is a real-Gram determinant.
g00, g11, real_g01 = sp.symbols("g00 g11 real_g01", real=True)
g22 = g00 + g11 + 2 * real_g01
heron_from_gram = (
    2 * (g00 * g11 + g00 * g22 + g11 * g22)
    - g00**2
    - g11**2
    - g22**2
)
require(
    zero(heron_from_gram - 4 * (g00 * g11 - real_g01**2)),
    "Heron polynomial reduces to four times a real-Gram determinant",
)

# Symbolically expose exactly where orthogonality cancels the vector sum.
q_symbols = sp.symbols("q00:03 q10:13 q20:23", real=True)
Q_generic = sp.Matrix(3, 3, q_symbols)
p0_real = sp.symbols("a0:3", real=True)
p0_imag = sp.symbols("b0:3", real=True)
p1_real = sp.symbols("c0:3", real=True)
p1_imag = sp.symbols("d0:3", real=True)
p0 = [p0_real[k] + I * p0_imag[k] for k in range(3)]
p1 = [p1_real[k] + I * p1_imag[k] for k in range(3)]
gram = Q_generic.T * Q_generic

first_component_sum = sum(
    Q_generic[i, k] ** 2 * sp.conjugate(p0[k]) * p1[k]
    for i in range(3)
    for k in range(3)
)
first_component_expected = sum(
    gram[k, k] * sp.conjugate(p0[k]) * p1[k] for k in range(3)
)
require(
    zero(first_component_sum - first_component_expected),
    "summed inner-product component contracts with diag(Q^T Q)",
)
for k, l in PAIRS:
    delta = p0[k] * p1[l] - p0[l] * p1[k]
    minor_sum = sum(Q_generic[i, k] * Q_generic[i, l] * delta for i in range(3))
    require(
        zero(minor_sum - gram[k, l] * delta),
        f"summed wedge component ({k},{l}) contracts with (Q^T Q)[{k},{l}]",
    )

# The strictness obstruction: proportional wedge triples force proportional
# nonzero rows of Q, contradicting row orthogonality.
for i, j in itertools.combinations(range(3), 2):
    r01_i = Q_generic[i, 0] * Q_generic[i, 1]
    r02_i = Q_generic[i, 0] * Q_generic[i, 2]
    r12_i = Q_generic[i, 1] * Q_generic[i, 2]
    r01_j = Q_generic[j, 0] * Q_generic[j, 1]
    r02_j = Q_generic[j, 0] * Q_generic[j, 2]
    r12_j = Q_generic[j, 1] * Q_generic[j, 2]
    require(
        sp.factor(r01_i * r02_j - r02_i * r01_j)
        == sp.factor(
            Q_generic[i, 0]
            * Q_generic[j, 0]
            * (Q_generic[i, 1] * Q_generic[j, 2] - Q_generic[i, 2] * Q_generic[j, 1])
        ),
        f"row pair ({i},{j}): first proportionality obstruction factors exactly",
    )
    require(
        sp.factor(r01_i * r12_j - r12_i * r01_j)
        == sp.factor(
            Q_generic[i, 1]
            * Q_generic[j, 1]
            * (Q_generic[i, 0] * Q_generic[j, 2] - Q_generic[i, 2] * Q_generic[j, 0])
        ),
        f"row pair ({i},{j}): second proportionality obstruction factors exactly",
    )

# Strict all-positive exact replay: a genuinely complex CKM matrix on the
# right and a dense rational orthogonal matrix on the left.
p34 = (R(3, 5), R(4, 5))
p512 = (R(5, 13), R(12, 13))
p815 = (R(8, 17), R(15, 17))
parameters = (p34[0], p34[1], p512[0], p512[1], p815[0], p815[1])
P_strict = ckm_unitary(parameters, I)
Q_strict = quaternion_rotation(1, 2, 3, 4)
M_strict = exact_certificate_audit(P_strict, Q_strict, "strict")
strict_vectors = certificate_vectors(P_strict, Q_strict)
require(all(value != 0 for value in P_strict), "strict: every P entry is nonzero")
require(all(value != 0 for value in Q_strict), "strict: every Q entry is nonzero")
for i, j in itertools.combinations(range(3), 2):
    two_vectors = strict_vectors[i].row_join(strict_vectors[j])
    require(two_vectors.rank() == 2, f"strict: z_{i} and z_{j} are not proportional")
strict_h = h_value(M_strict)
require(strict_h > 0, "strict: exact product witness h is positive")

# A zero-entry branch is intentionally retained: taking P=I makes the product
# equal to the orthostochastic left factor, so h=0 is possible without
# contradicting the nonzero-entry strictness statement.
M_degenerate = exact_certificate_audit(sp.eye(3), Q_strict, "degenerate")
degenerate_h = h_value(M_degenerate)
require(degenerate_h == 0, "degenerate: zero-entry factor permits saturated h=0")

print(f"strict_Q={Q_strict}")
print(f"strict_product={M_strict}")
print(f"strict_product_h={strict_h}")
print(f"degenerate_product_h={degenerate_h}")
print("RESULT: if the left qutrit factor is orthostochastic and the right factor is")
print("unistochastic, the product satisfies the exact triangle criterion; by")
print("transposition the same holds with the factor order reversed.")
print("STRICTNESS: if both displayed realizers have no zero entries, the product lies")
print("in the strict unistochastic interior h>0.")
print("LIMITATION: two arbitrary non-orthostochastic interior factors remain unresolved.")
