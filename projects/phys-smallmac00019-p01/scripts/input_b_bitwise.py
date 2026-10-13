"""Input B: independently derived computational-basis action for Eq. (119)."""

from __future__ import annotations

import sympy as sp


def build_matrix(couplings: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Build H column by column without Pauli matrices or Kronecker products."""
    a, b, c, d, e, f = couplings
    matrix = sp.zeros(8)
    for column in range(8):
        q1 = (column >> 2) & 1
        q2 = (column >> 1) & 1
        q3 = column & 1

        # Z2 and Z3 leave the bit string fixed.
        matrix[column, column] += a * (-1) ** q2 + f * (-1) ** q3

        # Y|q> = i*(-1)^q |1-q>; X|q> = |1-q>.
        row = 4 * (1 - q1) + 2 * (1 - q2) + q3
        matrix[row, column] += b * sp.I * (-1) ** q1

        row = 4 * (1 - q1) + 2 * (1 - q2) + q3
        matrix[row, column] += c * sp.I * (-1) ** q2

        row = 4 * q1 + 2 * q2 + (1 - q3)
        matrix[row, column] += d * sp.I * (-1) ** (q1 + q3)

        row = 4 * (1 - q1) + 2 * q2 + (1 - q3)
        matrix[row, column] += e * sp.I * (-1) ** q1

    return matrix


if __name__ == "__main__":
    print(build_matrix((1, 1, 1, 1, 1, 1)))
