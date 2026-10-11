#!/usr/bin/env python3
"""Standalone exact checker for the restricted-family theorem.

The proof path uses rational/symbolic algebra only.  Floating-point eigenvalues
and sampled parameter grids are deliberately absent.
"""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import sympy as sp


DOMAIN = (sp.Rational(-1, 5), sp.Rational(1, 5))


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(entry) == 0 for entry in matrix)


def rvec(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [matrix[row, col] for row in range(matrix.rows) for col in range(matrix.cols)]
    )


def partial_trace(matrix: sp.Matrix, traced: str) -> sp.Matrix:
    """Partial trace of a two-qubit matrix in B,A row-major order."""

    if traced == "B":
        return sp.Matrix(
            2,
            2,
            lambda a, ap: sum(matrix[2 * b + a, 2 * b + ap] for b in range(2)),
        ).applyfunc(sp.cancel)
    if traced == "A":
        return sp.Matrix(
            2,
            2,
            lambda b, bp: sum(matrix[2 * b + a, 2 * bp + a] for a in range(2)),
        ).applyfunc(sp.cancel)
    raise ValueError(traced)


def tensor_permutation() -> sp.Matrix:
    result = sp.zeros(16)
    for old in range(16):
        b1 = (old >> 3) & 1
        a1 = (old >> 2) & 1
        b2 = (old >> 1) & 1
        a2 = old & 1
        new = 8 * b1 + 4 * b2 + 2 * a1 + a2
        result[new, old] = 1
    return result


def complement_basis(size: int) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for row in range(size):
        for column in range(size):
            if row != column:
                vector = sp.zeros(size * size, 1)
                vector[size * row + column] = 1
                columns.append(vector)
    for row in range(size - 1):
        vector = sp.zeros(size * size, 1)
        vector[size * row + row] = 1
        vector[size * size - 1] = -1
        columns.append(vector)
    return sp.Matrix.hstack(*columns)


def ldl_pivots(matrix: sp.Matrix) -> list[sp.Expr]:
    lower, diagonal = matrix.LDLdecomposition(hermitian=False)
    if not zero_matrix(lower * diagonal * lower.T - matrix):
        raise AssertionError("LDL reconstruction failed")
    return [sp.factor(diagonal[index, index]) for index in range(matrix.rows)]


def certify_positive(expr: sp.Expr, variable: sp.Symbol, label: str) -> str:
    """Certify a rational expression as positive on [-1/5,1/5]."""

    expression = sp.factor(sp.cancel(expr))
    numerator, denominator = map(sp.factor, sp.fraction(expression))
    left, right = DOMAIN
    details = []
    for name, polynomial in (("numerator", numerator), ("denominator", denominator)):
        poly = sp.Poly(polynomial, variable, domain=sp.QQ)
        roots = 0 if poly.degree() <= 0 else int(poly.count_roots(left, right))
        if roots != 0:
            raise AssertionError(f"{label}: {name} has {roots} roots on the domain")
        if polynomial.subs(variable, left) == 0 or polynomial.subs(variable, right) == 0:
            raise AssertionError(f"{label}: {name} vanishes at an endpoint")
        details.append(f"{name}_roots={roots}")
    value_at_zero = sp.factor(expression.subs(variable, 0))
    if value_at_zero <= 0:
        raise AssertionError(f"{label}: sign at zero is {value_at_zero}")
    return f"{label}: PASS ({', '.join(details)}, value_at_zero={value_at_zero})"


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [sp.sstr(sp.factor(matrix[row, col])) for col in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("reproduction-output.json")
    )
    args = parser.parse_args()

    s, t = sp.symbols("s t", real=True)
    identity = sp.eye(2)
    pauli_x = sp.Matrix([[0, 1], [1, 0]])
    pauli_z = sp.diag(1, -1)
    imaginary = sp.I
    magic = sp.Matrix(
        [
            [0, 0, 1, imaginary],
            [-1, imaginary, 0, 0],
            [1, imaginary, 0, 0],
            [0, 0, 1, -imaginary],
        ]
    ) / sp.sqrt(2)
    if not zero_matrix(magic.conjugate().T * magic - sp.eye(4)):
        raise AssertionError("magic basis is not unitary")
    if not zero_matrix(magic[:, 2] - rvec(identity) / sp.sqrt(2)):
        raise AssertionError("identity is not the third magic-basis vector")

    weights_e = [
        sp.Rational(1, 4),
        sp.Rational(3, 10),
        sp.Rational(1, 10),
        sp.Rational(7, 20),
    ]
    weights_f = [
        sp.Rational(3, 10),
        sp.Rational(1, 5),
        sp.Rational(1, 10),
        sp.Rational(2, 5),
    ]
    base_e = (magic * sp.diag(*weights_e) * magic.conjugate().T).applyfunc(sp.cancel)
    base_f = (magic * sp.diag(*weights_f) * magic.conjugate().T).applyfunc(sp.cancel)
    choi_e = (
        base_e + s * sp.kronecker_product(pauli_z, identity) / 4
    ).applyfunc(sp.cancel)
    choi_f = (
        base_f + t * sp.kronecker_product(pauli_x, identity) / 4
    ).applyfunc(sp.cancel)

    physical_checks = []
    for label, choi, variable, pauli in (
        ("E", choi_e, s, pauli_z),
        ("F", choi_f, t, pauli_x),
    ):
        if not zero_matrix(choi - choi.conjugate().T):
            raise AssertionError(f"J_{label} is not Hermitian")
        if sp.cancel(sp.trace(choi) - 1) != 0:
            raise AssertionError(f"J_{label} is not normalized")
        if not zero_matrix(partial_trace(choi, "B") - identity / 2):
            raise AssertionError(f"J_{label} is not trace preserving")
        expected_output = identity / 2 + variable * pauli / 2
        if not zero_matrix(partial_trace(choi, "A") - expected_output):
            raise AssertionError(f"J_{label} output marginal is wrong")
        physical_checks.append(
            f"J_{label}: Hermitian, trace one, Tr_B=I/2, "
            "lambda_min>=1/20 by the exact Weyl bound"
        )

    inverse_e = choi_e.inv().applyfunc(sp.cancel)
    inverse_f = choi_f.inv().applyfunc(sp.cancel)
    magic_e = (magic.conjugate().T * inverse_e * magic).applyfunc(
        lambda entry: sp.factor(sp.re(entry))
    )
    magic_f = (magic.conjugate().T * inverse_f * magic).applyfunc(
        lambda entry: sp.factor(sp.re(entry))
    )
    expected_magic_e = sp.diag(
        24 / (6 - 5 * s**2),
        20 / (6 - 5 * s**2),
        140 / (14 - 25 * s**2),
        40 / (14 - 25 * s**2),
    )
    expected_magic_f = sp.diag(
        160 / (48 - 25 * t**2),
        40 / (8 - 25 * t**2),
        80 / (8 - 25 * t**2),
        120 / (48 - 25 * t**2),
    )
    if not zero_matrix(magic_e - expected_magic_e):
        raise AssertionError("E magic-basis inverse formula failed")
    if not zero_matrix(magic_f - expected_magic_f):
        raise AssertionError("F magic-basis inverse formula failed")

    radius_e = sp.factor(expected_magic_e[2, 2])
    radius_f = sp.factor(expected_magic_f[2, 2])
    radius_checks = []
    for label, matrix, radius, variable in (
        ("E", expected_magic_e, radius_e, s),
        ("F", expected_magic_f, radius_f, t),
    ):
        for index in (0, 1, 3):
            radius_checks.append(
                certify_positive(
                    radius - matrix[index, index],
                    variable,
                    f"{label}_radius_gap_{index}",
                )
            )

    multiplier_e = sp.diag(
        10 * (7 - 5 * s) / (14 - 25 * s**2),
        10 * (7 + 5 * s) / (14 - 25 * s**2),
    )
    multiplier_f = sp.Matrix([[40, -50 * t], [-50 * t, 40]]) / (8 - 25 * t**2)
    if sp.cancel(sp.trace(multiplier_e) - radius_e) != 0:
        raise AssertionError("trace L_E differs from R_E")
    if sp.cancel(sp.trace(multiplier_f) - radius_f) != 0:
        raise AssertionError("trace L_F differs from R_F")

    multiplier_checks = [
        certify_positive(multiplier_e[0, 0], s, "L_E_minor_1"),
        certify_positive(multiplier_e.det(), s, "L_E_minor_2"),
        certify_positive(multiplier_f[0, 0], t, "L_F_minor_1"),
        certify_positive(multiplier_f.det(), t, "L_F_minor_2"),
    ]
    ceiling_e = sp.kronecker_product(identity, multiplier_e.T)
    ceiling_f = sp.kronecker_product(identity, multiplier_f.T)
    remainder_e = (ceiling_e - inverse_e / 2).applyfunc(sp.cancel)
    remainder_f = (ceiling_f - inverse_f / 2).applyfunc(sp.cancel)
    identity_vector = rvec(identity)
    complement = complement_basis(2)
    if not zero_matrix(remainder_e * identity_vector):
        raise AssertionError("Q_E misses vec(I_2)")
    if not zero_matrix(remainder_f * identity_vector):
        raise AssertionError("Q_F misses vec(I_2)")
    gram_e = (complement.T * remainder_e * complement).applyfunc(sp.cancel)
    gram_f = (complement.T * remainder_f * complement).applyfunc(sp.cancel)
    pivots_e = ldl_pivots(gram_e)
    pivots_f = ldl_pivots(gram_f)
    remainder_checks = []
    for label, pivots, variable in (
        ("Q_E", pivots_e, s),
        ("Q_F", pivots_f, t),
    ):
        for index, pivot in enumerate(pivots, start=1):
            remainder_checks.append(
                certify_positive(pivot, variable, f"{label}_LDL_pivot_{index}")
            )

    permutation = tensor_permutation()
    if not zero_matrix(permutation.T * permutation - sp.eye(16)):
        raise AssertionError("tensor-leg permutation is not unitary")
    joint_inverse = (
        permutation
        * sp.kronecker_product(inverse_e, inverse_f)
        * permutation.T
    )
    joint_multiplier = sp.kronecker_product(multiplier_e, multiplier_f)
    joint_ceiling = sp.kronecker_product(sp.eye(4), joint_multiplier.T)
    predicted_remainder = (
        permutation
        * (
            sp.kronecker_product(remainder_e, ceiling_f)
            + sp.kronecker_product(inverse_e / 2, remainder_f)
        )
        * permutation.T
    )
    if not zero_matrix(joint_ceiling - joint_inverse / 4 - predicted_remainder):
        raise AssertionError("tensor remainder identity failed")
    if sp.cancel(sp.trace(joint_multiplier) - radius_e * radius_f) != 0:
        raise AssertionError("joint multiplier trace is not R_E R_F")

    exact_point = {s: sp.Rational(1, 10), t: sp.Rational(1, 8)}
    exact_remainder = (joint_ceiling - joint_inverse / 4).subs(exact_point)
    exact_remainder = exact_remainder.applyfunc(sp.cancel)
    if exact_remainder.rank() != 15:
        raise AssertionError("exact-point joint remainder does not have rank 15")
    if not zero_matrix(exact_remainder * rvec(sp.eye(4))):
        raise AssertionError("exact-point joint remainder misses vec(I_4)")
    product_radius = sp.factor((radius_e * radius_f).subs(exact_point))
    if product_radius != sp.Rational(573440, 5357):
        raise AssertionError("exact-point product radius changed")

    record = {
        "schema": 1,
        "scope": "exact restricted family on |s|,|t|<=1/5; no arbitrary-channel claim",
        "software": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "physical_checks": physical_checks,
        "radius_checks": radius_checks,
        "local_radii": {
            "R_E(s)": sp.sstr(radius_e),
            "R_F(t)": sp.sstr(radius_f),
        },
        "multipliers": {
            "L_E(s)": matrix_strings(multiplier_e),
            "L_F(t)": matrix_strings(multiplier_f),
            "positive_definiteness": multiplier_checks,
        },
        "local_remainders": {
            "Q_E_LDL_pivots": [sp.sstr(value) for value in pivots_e],
            "Q_F_LDL_pivots": [sp.sstr(value) for value in pivots_f],
            "interval_checks": remainder_checks,
            "kernel": "span{rvec(I_2)} for each local remainder",
        },
        "tensor_check": {
            "permutation": "B1,A1,B2,A2 -> B1,B2,A1,A2",
            "remainder_identity": "PASS",
            "joint_trace": sp.sstr(sp.factor(sp.trace(joint_multiplier))),
            "saturation": "V=I_4",
        },
        "exact_point": {
            "s": "1/10",
            "t": "1/8",
            "product_radius": sp.sstr(product_radius),
            "joint_remainder_rank": 15,
            "joint_kernel": "span{rvec(I_4)}",
        },
        "conclusion": "b(E_s tensor F_t)=b(E_s)b(F_t) on the full closed square",
        "limitation": "the universal arbitrary-channel conjecture remains unresolved",
    }
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"PASS: wrote {args.output}")


if __name__ == "__main__":
    main()
