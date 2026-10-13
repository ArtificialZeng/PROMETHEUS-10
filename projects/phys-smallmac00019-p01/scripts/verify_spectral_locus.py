"""Independent exact checks for the spectral-locus argument.

The script checks the chiral Pauli symmetry, factors the universal obstruction
in the four nonnegative spectral magnitudes, and exercises every algebraic
branch plus representative zero/degenerate intersections with exact integer
arithmetic.  Numerical eigenvalues are not used to establish the locus.
"""

from __future__ import annotations

import itertools

import sympy as sp

from input_b_bitwise import build_matrix


def kron_word(word: str) -> sp.Matrix:
    matrices = {
        "I": sp.eye(2),
        "X": sp.Matrix([[0, 1], [1, 0]]),
        "Y": sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        "Z": sp.diag(1, -1),
    }
    return sp.kronecker_product(*(matrices[letter] for letter in word))


def obstruction_at(point: tuple[int, ...]) -> sp.Expr:
    a, b, c, d, e, f = point
    energy = sp.symbols("E")
    coeffs = sp.Poly(build_matrix(point).charpoly(energy).as_expr(), energy).all_coeffs()
    q6, q4, q0 = coeffs[2], coeffs[4], coeffs[8]
    e1 = -q6 / 4
    e2 = (6 * e1**2 - q4) / 8
    return sp.factor(q0 - (e1**2 - 4 * e2) ** 2)


def main() -> None:
    labels = ("a", "b", "c", "d", "e", "f")
    words = ("IZI", "YXI", "XYI", "ZIY", "YIX", "IIZ")
    gamma = kron_word("YYY")
    anticommutators = [sp.simplify(gamma * kron_word(w) + kron_word(w) * gamma) for w in words]
    print("CHIRAL_CHECK")
    print(f"gamma_word=YYY")
    print(f"gamma_squared_identity={gamma * gamma == sp.eye(8)}")
    print(f"anticommutes_with_all_six_terms={all(x == sp.zeros(8) for x in anticommutators)}")

    l1, l2, l3, l4 = sp.symbols("lambda1 lambda2 lambda3 lambda4")
    lambdas = (l1, l2, l3, l4)
    squared = [x**2 for x in lambdas]
    s1 = sum(squared)
    s2 = sum(squared[i] * squared[j] for i, j in itertools.combinations(range(4), 2))
    q = sp.expand(4 * s2 - s1**2)
    product = sp.prod(lambdas)
    universal = sp.factor(64 * product**2 - q**2)
    print("UNIVERSAL_REAL_SPECTRUM_FACTOR")
    print(f"64_product_squared_minus_Q_squared={universal}")
    print("For 0<=lambda1<=lambda2<=lambda3<=lambda4, a zero factor reduces to")
    print("lambda4=lambda1+lambda2+lambda3 or lambda4+lambda1=lambda2+lambda3,")
    print("including their zero and repeated-value intersections.")

    branch_points = {
        "c=0": (1, 2, 0, 3, 4, 5),
        "d=0": (1, 2, 3, 0, 4, 5),
        "a=f": (5, 2, 3, 4, 6, 5),
        "a=-f": (-5, 2, 3, 4, 6, 5),
        "b=e": (1, 6, 3, 4, 6, 5),
        "b=-e": (1, -6, 3, 4, 6, 5),
        "origin": (0, 0, 0, 0, 0, 0),
        "c=d=0 intersection": (1, 2, 0, 0, 4, 5),
        "a=f=0 coordinate stratum": (0, 2, 3, 4, 6, 0),
        "b=e=0 coordinate stratum": (1, 0, 3, 4, 0, 5),
    }
    off_points = {
        "generic": (1, 2, 3, 4, 5, 6),
        "a=0 but f!=0 and b^2!=e^2": (0, 2, 3, 4, 5, 6),
        "b=0 but e!=0 and a^2!=f^2": (1, 0, 3, 4, 5, 6),
    }
    print("EXACT_BRANCH_AND_ZERO_STRATUM_CHECKS")
    for name, point in branch_points.items():
        print(f"{name}: point={point}, obstruction={obstruction_at(point)}")
    print("EXACT_OFF_LOCUS_CHECKS")
    for name, point in off_points.items():
        print(f"{name}: point={point}, obstruction={obstruction_at(point)}")


if __name__ == "__main__":
    main()
