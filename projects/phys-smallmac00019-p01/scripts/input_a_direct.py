"""Input A: direct Kronecker-product transcription of arXiv:2012.07857v2 Eq. (119)."""

from __future__ import annotations

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)


def build_matrix(couplings: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Return H in basis |q1 q2 q3>, index 4*q1+2*q2+q3."""
    a, b, c, d, e, f = couplings
    kron = sp.kronecker_product
    terms = (
        a * kron(I2, Z, I2),
        b * kron(Y, X, I2),
        c * kron(X, Y, I2),
        d * kron(Z, I2, Y),
        e * kron(Y, I2, X),
        f * kron(I2, I2, Z),
    )
    return sum(terms, sp.zeros(8))


if __name__ == "__main__":
    print(build_matrix((1, 1, 1, 1, 1, 1)))
