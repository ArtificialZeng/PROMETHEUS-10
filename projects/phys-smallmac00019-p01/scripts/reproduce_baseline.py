"""Exact and numerical reproduction of the Eq. (119) all-equal benchmark."""

from __future__ import annotations

import argparse
import itertools
import sys

import numpy as np
import scipy
import sympy as sp

from input_a_direct import build_matrix as build_a
from input_b_bitwise import build_matrix as build_b


LABELS = ("a", "b", "c", "d", "e", "f")
WORDS = {
    "a": "IZI",
    "b": "YXI",
    "c": "XYI",
    "d": "ZIY",
    "e": "YIX",
    "f": "IIZ",
}


def anticommutes(word_1: str, word_2: str) -> bool:
    parity = sum(
        p != "I" and q != "I" and p != q for p, q in zip(word_1, word_2)
    )
    return bool(parity % 2)


def graph_data() -> tuple[list[tuple[str, str]], list[tuple[str, ...]]]:
    edges = [
        (p, q)
        for p, q in itertools.combinations(LABELS, 2)
        if anticommutes(WORDS[p], WORDS[q])
    ]
    edge_set = {frozenset(edge) for edge in edges}
    independent_sets = []
    for size in range(len(LABELS) + 1):
        for subset in itertools.combinations(LABELS, size):
            if all(
                frozenset(pair) not in edge_set
                for pair in itertools.combinations(subset, 2)
            ):
                independent_sets.append(subset)
    return edges, independent_sets


def matrix_rows(matrix: sp.Matrix) -> list[str]:
    return ["[" + ", ".join(str(matrix[r, c]) for c in range(8)) + "]" for r in range(8)]


def input_report() -> None:
    couplings = sp.symbols("a b c d e f", real=True)
    matrix_a = build_a(couplings)
    matrix_b = build_b(couplings)
    delta = matrix_a - matrix_b
    print("INPUT_COMPARISON")
    print("source=arXiv:2012.07857v2 Eq. (119)")
    print("basis_order=|000>,|001>,|010>,|011>,|100>,|101>,|110>,|111>")
    print("index_map=index(|q1 q2 q3>)=4*q1+2*q2+q3")
    print("input_a=left-to-right Kronecker products q1 tensor q2 tensor q3")
    print("input_b=columnwise bit actions; Y|q>=i*(-1)^q|1-q>")
    print("convention_map=A tensor factor j <-> B bit qj; identical standard X,Y,Z phases")
    print(f"shape={matrix_a.rows}x{matrix_a.cols}")
    print(f"all_64_symbolic_entries_equal={delta == sp.zeros(8)}")
    print(f"nonzero_symbolic_differences={sum(entry != 0 for entry in delta)}")
    print(f"symbolic_hermitian_for_real_couplings={matrix_a == matrix_a.adjoint()}")
    print(f"symbolic_trace={sp.simplify(sp.trace(matrix_a))}")
    print("matrix_at_a=b=c=d=e=f=1:")
    for row in matrix_rows(matrix_a.subs(dict(zip(couplings, (1,) * 6)))):
        print(row)


def baseline_report() -> None:
    energy = sp.symbols("E")
    x = sp.symbols("x")
    weights = dict(zip(LABELS, sp.symbols("a b c d e f", real=True)))
    matrix = build_a((1, 1, 1, 1, 1, 1))
    charpoly_matrix = sp.Poly(matrix.charpoly(energy).as_expr(), energy)

    edges, independent_sets = graph_data()
    polynomial = 0
    for subset in independent_sets:
        polynomial += x ** len(subset) * sp.prod(weights[v] ** 2 for v in subset)
    polynomial = sp.Poly(sp.expand(polynomial), x)
    counts = {
        size: sum(len(subset) == size for subset in independent_sets)
        for size in range(4)
    }
    equal_polynomial = sp.Poly(
        polynomial.as_expr().subs({value: 1 for value in weights.values()}), x
    )

    # P_G(-1/epsilon^2)=0 gives t=epsilon^2 as a root of
    # t^3 - 6 t^2 + 8 t - 2.  Its elementary symmetric data are (6,8,2).
    t = sp.symbols("t")
    t_polynomial = sp.Poly(t**3 - 6 * t**2 + 8 * t - 2, t)
    e1, e2, e3 = 6, 8, 2
    free_charpoly = sp.Poly(
        energy**8
        - 4 * e1 * energy**6
        + (6 * e1**2 - 8 * e2) * energy**4
        - 4 * (e1**3 - 4 * e1 * e2 + 16 * e3) * energy**2
        + (e1**2 - 4 * e2) ** 2,
        energy,
    )

    numeric_matrix = np.asarray(matrix.tolist(), dtype=np.complex128)
    matrix_eigenvalues = np.linalg.eigvalsh(numeric_matrix)
    roots_t = np.sort(np.asarray([float(root) for root in sp.nroots(t_polynomial)], dtype=float))
    epsilons = np.sqrt(roots_t)
    signed_sums = np.sort(
        np.asarray(
            [sum(sign * eps for sign, eps in zip(signs, epsilons))
             for signs in itertools.product((-1.0, 1.0), repeat=3)]
        )
    )
    max_error = float(np.max(np.abs(matrix_eigenvalues - signed_sums)))
    tolerance = 1.0e-12

    print("BASELINE_REPRODUCTION")
    print("source=arXiv:2012.07857v2 Eq. (119), Eq. (5)-(6), discussion after Eq. (119)")
    print("coupling_point=a=b=c=d=e=f=1 energy unit")
    print("matrix_method=exact SymPy 8x8 characteristic polynomial plus Hermitian eigvalsh")
    print("graph_method=Pauli-word anticommutation parity and exhaustive independent-set enumeration")
    print("graph_edges=" + repr(edges))
    print("independent_sets=" + repr(independent_sets))
    print("independent_set_counts=" + repr(counts))
    print("weighted_independence_polynomial=" + str(polynomial.as_expr()))
    print("all_equal_independence_polynomial=" + str(equal_polynomial.as_expr()))
    print("source_root_convention=P_G(-1/epsilon_j^2)=0")
    print("squared_single_particle_polynomial=" + str(t_polynomial.as_expr()))
    print("squared_single_particle_energies=" + np.array2string(roots_t, precision=15))
    print("single_particle_energies=" + np.array2string(epsilons, precision=15))
    print("matrix_characteristic_polynomial=" + str(charpoly_matrix.as_expr()))
    print("free_signed_sum_characteristic_polynomial=" + str(free_charpoly.as_expr()))
    print(f"exact_characteristic_polynomial_match={charpoly_matrix == free_charpoly}")
    print("matrix_eigenvalues=" + np.array2string(matrix_eigenvalues, precision=15))
    print("free_signed_sums=" + np.array2string(signed_sums, precision=15))
    print(f"max_abs_sorted_spectrum_error={max_error:.17g}")
    print(f"numeric_tolerance={tolerance:.1e}")
    print(f"numeric_spectrum_match={max_error <= tolerance}")
    print("scaling=for common real J, epsilon_j=abs(J)*sqrt(t_j); J=0 gives three zero modes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("section", choices=("input", "baseline", "all"), nargs="?", default="all")
    args = parser.parse_args()
    print(f"python_executable={sys.executable}")
    print(f"python_version={sys.version.split()[0]}")
    print(f"numpy_version={np.__version__}")
    print(f"scipy_version={scipy.__version__}")
    print(f"sympy_version={sp.__version__}")
    if args.section in ("input", "all"):
        input_report()
    if args.section in ("baseline", "all"):
        baseline_report()


if __name__ == "__main__":
    main()
