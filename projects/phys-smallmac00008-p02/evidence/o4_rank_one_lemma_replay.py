#!/usr/bin/env python3
"""Exact algebra replay for the quaternionic core of the O(4) frame lemma.

This script is not a numerical existence test.  It checks, over SymPy's exact
polynomial ring, the identities used in evidence/o4-rank-one-proof.md:

* the nine L_i R_j form an orthogonal basis of Sym_0(R^4);
* S(a,b)=L_a R_b is symmetric, traceless, and satisfies
  S(a,b)^2=|a|^2 |b|^2 I;
* tr(S(a,b) G(M))=4 a^T M b.
"""

from __future__ import annotations

import platform

import numpy
import scipy
import sympy as sp


def matrix_from_columns(columns):
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


def main() -> None:
    # Quaternion basis is (1,i,j,k).  These are exact matrices for left and
    # right multiplication by the three imaginary quaternion units.
    li = matrix_from_columns(((0, 1, 0, 0), (-1, 0, 0, 0),
                              (0, 0, 0, 1), (0, 0, -1, 0)))
    lj = matrix_from_columns(((0, 0, 1, 0), (0, 0, 0, -1),
                              (-1, 0, 0, 0), (0, 1, 0, 0)))
    lk = matrix_from_columns(((0, 0, 0, 1), (0, 0, 1, 0),
                              (0, -1, 0, 0), (-1, 0, 0, 0)))
    ri = matrix_from_columns(((0, 1, 0, 0), (-1, 0, 0, 0),
                              (0, 0, 0, -1), (0, 0, 1, 0)))
    rj = matrix_from_columns(((0, 0, 1, 0), (0, 0, 0, 1),
                              (-1, 0, 0, 0), (0, -1, 0, 0)))
    rk = matrix_from_columns(((0, 0, 0, 1), (0, 0, -1, 0),
                              (0, 1, 0, 0), (-1, 0, 0, 0)))
    left = (li, lj, lk)
    right = (ri, rj, rk)
    identity = sp.eye(4)

    assert all(x.T == -x and x * x == -identity for x in left + right)
    assert all(l * r == r * l for l in left for r in right)

    basis = [[left[i] * right[j] for j in range(3)] for i in range(3)]
    assert all(e.T == e and sp.trace(e) == 0 for row in basis for e in row)
    gram = sp.Matrix(9, 9, lambda p, q: sp.trace(
        basis[p // 3][p % 3] * basis[q // 3][q % 3]))
    assert gram == 4 * sp.eye(9)

    a = sp.Matrix(sp.symbols("a1:4", real=True))
    b = sp.Matrix(sp.symbols("b1:4", real=True))
    m_symbols = sp.symbols("m11:14 m21:24 m31:34", real=True)
    m = sp.Matrix(3, 3, m_symbols)
    s = sp.zeros(4)
    g = sp.zeros(4)
    for i in range(3):
        for j in range(3):
            s += a[i] * b[j] * basis[i][j]
            g += m[i, j] * basis[i][j]

    aa = (a.T * a)[0]
    bb = (b.T * b)[0]
    assert s.T == s
    assert sp.trace(s) == 0
    assert sp.simplify(s * s - aa * bb * identity) == sp.zeros(4)
    assert sp.expand(sp.trace(s * g) - 4 * (a.T * m * b)[0]) == 0

    print("EXACT O(4) QUATERNION REPLAY: PASS")
    print("python=" + platform.python_version())
    print("numpy=" + numpy.__version__)
    print("scipy=" + scipy.__version__)
    print("sympy=" + sp.__version__)
    print("nine_basis_gram=4*I9")
    print("S_transpose=S; trace(S)=0")
    print("S^2=(a.a)(b.b)I4")
    print("trace(S*G(M))=4*a^T*M*b")


if __name__ == "__main__":
    main()
