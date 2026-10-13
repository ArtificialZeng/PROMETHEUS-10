#!/usr/bin/env python3
"""Compare independent source representations only after both are reconstructed."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
A_DATA = json.loads((ROOT / "evidence/input-a.json").read_text(encoding="utf-8"))
B_DATA = json.loads((ROOT / "evidence/input-b.json").read_text(encoding="utf-8"))


def parse(values, symbols=None):
    symbols = symbols or {}
    return sp.Matrix([[sp.sympify(x, locals=symbols) for x in row] for row in values])


def unvec(column, n):
    return sp.Matrix(n, n, lambda a, b: column[a + n * b])


def choi_from_superoperator(superop, n):
    order = [(0, 0), (1, 0), (0, 1), (1, 1)]
    outputs = {pair: unvec(superop[:, k], n) for k, pair in enumerate(order)}
    return sp.Matrix(n * n, n * n, lambda r, c:
                     outputs[(r // n, c // n)][r % n, c % n])


lam = sp.symbols("lambda", real=True)
n = A_DATA["dimension"]
C_a = parse(A_DATA["choi_matrix"])
S_b = parse(B_DATA["superoperator_matrix"])
C_b = choi_from_superoperator(S_b, n)

t = sp.sqrt(1 - lam)
A = sp.kronecker_product(sp.diag(1, 1 / t), sp.eye(n))
D = sp.kronecker_product(sp.sqrt(lam) * sp.Matrix([[0, 0], [1, 0]]), sp.eye(n))
Q_a = (A * C_a * A.T - D * C_a * D.T / (1 - lam)).applyfunc(sp.simplify)

S_psi = sp.Matrix([
    [1, 0, 0, lam],
    [0, t, 0, 0],
    [0, 0, t, 0],
    [0, 0, 0, 1 - lam]
])
Q_b = choi_from_superoperator((S_b * S_psi.inv()).applyfunc(sp.simplify), n)

choi_difference = (C_a - C_b).applyfunc(sp.simplify)
quotient_difference = (Q_a - Q_b).applyfunc(sp.simplify)
assert choi_difference == sp.zeros(n * n)
assert quotient_difference == sp.zeros(n * n)

result = {
    "basis_map": {
        "route_a_choi_order": A_DATA["choi_basis"],
        "route_b_vector_order": B_DATA["operator_basis_order"],
        "reshuffle_rule": "superoperator column E_ij is vec(Phi(E_ij)); set C[(i,a),(j,b)]=Phi(E_ij)[a,b]",
        "indexing": "zero-based computational basis; input tensor factor first; vec is column-major"
    },
    "shared_only_before_comparison": "source version, dimension, computational labels x=|1>, x_perp=|0>, and published vectorization convention",
    "not_shared_during_reconstruction": "Route B did not read input-a.json or Route A output; Route A did not read input-b.json or Route B output.",
    "source_choi_entrywise_difference": [[str(x) for x in row] for row in choi_difference.tolist()],
    "quotient_entrywise_difference": [[str(x) for x in row] for row in quotient_difference.tolist()],
    "source_inputs_match_exactly_after_map": True,
    "quotients_match_exactly_after_map": True,
    "all_assertions_passed": True
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
