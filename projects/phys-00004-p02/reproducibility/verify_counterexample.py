#!/usr/bin/env python3
"""Verify the exact qutrit counterexample using only rational arithmetic."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


def f(value: str) -> Fraction:
    return Fraction(value)


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def determinant3(matrix):
    a, b, c = matrix[0]
    d, e, g = matrix[1]
    h, i, j = matrix[2]
    return a * (e * j - g * i) - b * (d * j - g * h) + c * (d * i - e * h)


def bilinear(left, matrix, right):
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in range(3)
        for column in range(3)
    )


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> None:
    certificate_path = Path(__file__).with_name("certificate.json")
    data = json.loads(certificate_path.read_text(encoding="utf-8"))
    require(data.get("schema") == 1, "unsupported certificate schema")

    unitary = [[f(value) for value in row] for row in data["unitary"]]
    identity = [
        [Fraction(int(row == column)) for column in range(3)]
        for row in range(3)
    ]
    require(matmul(transpose(unitary), unitary) == identity, "U^T U != I")
    require(determinant3(unitary) == 1, "det(U) != 1")

    overlap = [[entry * entry for entry in row] for row in unitary]
    expected_overlap = [[f(value) for value in row] for row in data["overlap"]]
    require(overlap == expected_overlap, "C != |U|^2")
    require(all(sum(row) == 1 for row in overlap), "a row of C does not sum to 1")
    require(
        all(sum(column) == 1 for column in transpose(overlap)),
        "a column of C does not sum to 1",
    )

    parameters = data["parameters"]
    lam, mu = f(parameters["lambda"]), f(parameters["mu"])
    r, s = f(parameters["r"]), f(parameters["s"])
    threshold = (1 - mu) * (1 - lam) / (mu * lam)
    require(0 < lam < 1 and 0 < mu < 1, "lambda or mu outside (0,1)")
    require(lam + mu > 1, "lambda + mu is not greater than 1")
    require(r == 1 / mu and s == 1 / (1 - lam), "incorrect exponent map")
    require(threshold == f(parameters["spectral_threshold"]), "wrong threshold")

    gram = matmul(transpose(overlap), overlap)
    ones = [Fraction(1)] * 3
    require(matvec(gram, ones) == ones, "C^T C does not preserve the uniform mode")
    threshold_minus_gram = [
        [threshold * int(row == column) - gram[row][column] for column in range(3)]
        for row in range(3)
    ]
    basis = [[f(value) for value in vector] for vector in data["sum_zero_basis"]]
    require(all(sum(vector) == 0 for vector in basis), "basis is not in the sum-zero subspace")
    q_form = [
        [bilinear(basis[row], threshold_minus_gram, basis[column]) for column in range(2)]
        for row in range(2)
    ]
    expected_q = [
        [f(value) for value in row]
        for row in data["expected_spectral_quadratic_form"]
    ]
    require(q_form == expected_q, "unexpected spectral quadratic form")
    q_determinant = q_form[0][0] * q_form[1][1] - q_form[0][1] ** 2
    require(q_form[0][0] > 0, "first spectral principal minor is not positive")
    require(
        q_determinant == f(data["expected_spectral_quadratic_form_determinant"])
        and q_determinant > 0,
        "spectral quadratic form is not positive definite",
    )

    witness = [f(value) for value in data["witness"]]
    image = matvec(overlap, witness)
    expected_image = [f(value) for value in data["expected_witness_image"]]
    require(image == expected_image, "incorrect witness image")
    output_sum = sum(value**4 for value in image)
    input_sum = sum(value**3 for value in witness)
    require(
        output_sum == f(data["expected_output_fourth_power_sum"]),
        "incorrect fourth-power sum",
    )
    require(
        input_sum == f(data["expected_input_third_power_sum"]),
        "incorrect third-power sum",
    )
    numerator = sum((15 * value) ** 4 for value in image)
    require(numerator.denominator == 1, "unexpected output denominator")
    integer_gap = 3 * numerator.numerator**3 - 15**12 * input_sum.numerator**4
    require(integer_gap == int(data["expected_integer_gap"]), "incorrect norm gap")
    require(integer_gap > 0, "witness does not strictly exceed the MUB value")

    report = {
        "status": "PASS",
        "determinant_U": str(determinant3(unitary)),
        "spectral_threshold": str(threshold),
        "spectral_quadratic_form": [[str(value) for value in row] for row in q_form],
        "spectral_quadratic_form_determinant": str(q_determinant),
        "witness_image": [str(value) for value in image],
        "output_fourth_power_sum": str(output_sum),
        "input_third_power_sum": str(input_sum),
        "integer_norm_gap": str(integer_gap),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
