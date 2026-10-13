"""Exact characteristic-polynomial obstruction for the Eq. (119) model.

This discovery script computes the general polynomial from both independently
reconstructed Hamiltonians.  It then eliminates the three elementary
symmetric polynomials in the squared one-particle energies from the universal
three-mode signed-sum polynomial.
"""

from __future__ import annotations

import sys

import numpy as np
import scipy
import sympy as sp

from input_a_direct import build_matrix as build_a
from input_b_bitwise import build_matrix as build_b


def main() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f", real=True)
    # Matrix.charpoly requires an assumption-free generator to retain the
    # requested symbol rather than silently replacing it.
    energy = sp.symbols("E")
    couplings = (a, b, c, d, e, f)

    matrix_a = build_a(couplings)
    matrix_b = build_b(couplings)
    polynomial_a = sp.Poly(matrix_a.charpoly(energy).as_expr(), energy)
    polynomial_b = sp.Poly(matrix_b.charpoly(energy).as_expr(), energy)
    coefficients = polynomial_a.all_coeffs()
    q6 = sp.factor(coefficients[2])
    q4 = sp.factor(coefficients[4])
    q2 = sp.factor(coefficients[6])
    q0 = coefficients[8]

    # Universal signed-sum coefficient map, with e_k the elementary
    # symmetric polynomials of t_j=epsilon_j**2.
    e1 = sp.factor(-q6 / 4)
    e2 = sp.factor((6 * e1**2 - q4) / 8)
    e3 = sp.factor((-q2 / 4 - e1**3 + 4 * e1 * e2) / 16)
    determinant_target_root = sp.factor(e1**2 - 4 * e2)
    obstruction = sp.factor(q0 - determinant_target_root**2)

    expected_q6 = -4 * e1
    expected_q4 = 6 * e1**2 - 8 * e2
    expected_q2 = -4 * (e1**3 - 4 * e1 * e2 + 16 * e3)

    print(f"python_executable={sys.executable}")
    print(f"python_version={sys.version.split()[0]}")
    print(f"numpy_version={np.__version__}")
    print(f"scipy_version={scipy.__version__}")
    print(f"sympy_version={sp.__version__}")
    print("GENERAL_CHARACTERISTIC_POLYNOMIAL")
    print(f"matrix_representations_equal={matrix_a == matrix_b}")
    print(f"characteristic_polynomials_equal={polynomial_a == polynomial_b}")
    print(f"polynomial_is_even={all(coefficients[k] == 0 for k in (1, 3, 5, 7))}")
    print("SIGNED_SUM_ELIMINATION")
    print(f"e1={e1}")
    print(f"e2={e2}")
    print(f"e3={e3}")
    print(f"q6_matches_-4e1={sp.expand(q6 - expected_q6) == 0}")
    print(f"q4_matches_6e1^2-8e2={sp.expand(q4 - expected_q4) == 0}")
    print(f"q2_matches_-4(e1^3-4e1e2+16e3)={sp.expand(q2 - expected_q2) == 0}")
    print(f"determinant_target_root=e1^2-4*e2={determinant_target_root}")
    print(f"factored_obstruction={obstruction}")


if __name__ == "__main__":
    main()
