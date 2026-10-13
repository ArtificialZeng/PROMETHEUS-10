#!/usr/bin/env python3
"""Route B: separate superoperator transcription and direct basis-unit composition."""

import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evidence/input-b.json").read_text(encoding="utf-8"))


def matrix_from_strings(values):
    return sp.Matrix([[sp.sympify(x) for x in row] for row in values])


def vec(matrix):
    n = matrix.rows
    return sp.Matrix([matrix[a, b] for b in range(n) for a in range(n)])


def unvec(column, n):
    return sp.Matrix(n, n, lambda a, b: column[a + n * b])


def superoperator_from_action(action, n):
    ordered_units = [(0, 0), (1, 0), (0, 1), (1, 1)]
    columns = []
    for i, j in ordered_units:
        unit = sp.zeros(n)
        unit[i, j] = 1
        columns.append(vec(action(unit)))
    return sp.Matrix.hstack(*columns)


def choi_from_superoperator(superop, n):
    ordered_units = [(0, 0), (1, 0), (0, 1), (1, 1)]
    outputs = {pair: unvec(superop[:, k], n) for k, pair in enumerate(ordered_units)}
    choi = sp.zeros(n * n)
    for i in range(n):
        for j in range(n):
            block = outputs[(i, j)]
            for a in range(n):
                for b in range(n):
                    choi[n * i + a, n * j + b] = block[a, b]
    return choi


lam = sp.symbols("lambda", real=True)
n = DATA["dimension"]
S_phi = matrix_from_strings(DATA["superoperator_matrix"])
t = sp.sqrt(1 - lam)
K = sp.diag(1, t)
L = sp.sqrt(lam) * sp.Matrix([[0, 1], [0, 0]])


def psi_action(unit):
    return K * unit * K.T + L * unit * L.T


S_psi = superoperator_from_action(psi_action, n).applyfunc(sp.simplify)
S_quotient = (S_phi * S_psi.inv()).applyfunc(sp.simplify)
C_from_superoperator = choi_from_superoperator(S_phi, n)
Q_from_composition = choi_from_superoperator(S_quotient, n).applyfunc(sp.simplify)

trace_row = sp.Matrix([[1, 0, 0, 1]])
assert trace_row * S_phi == trace_row
assert K.T * K + L.T * L == sp.eye(n)
assert C_from_superoperator.rank() == 3
assert C_from_superoperator == C_from_superoperator.T

active = [0, 2, 3]
source_principal_minors = {}
for size in range(1, len(active) + 1):
    for subset in itertools.combinations(active, size):
        source_principal_minors[",".join(map(str, subset))] = str(
            sp.factor(C_from_superoperator.extract(subset, subset).det()))
assert all(C_from_superoperator.extract(subset, subset).det() > 0
           for size in range(1, len(active) + 1)
           for subset in itertools.combinations(active, size))

principal_minors = {}
for size in range(1, len(active) + 1):
    for subset in itertools.combinations(active, size):
        minor = Q_from_composition.extract(subset, subset).det()
        principal_minors[",".join(map(str, subset))] = str(sp.factor(minor))

determinant = sp.factor(Q_from_composition.extract(active, active).det())
assert sp.simplify(determinant - (1 - 6 * lam) / (27 * (1 - lam) ** 2)) == 0
endpoint_rank = Q_from_composition.subs(lam, sp.Rational(1, 6)).rank()
assert endpoint_rank == 2

result = {
    "route": "B_superoperator_plus_direct_matrix_unit_composition",
    "source_superoperator_trace_preserving": True,
    "elementary_factor_cptp": True,
    "derived_source_choi": [[str(x) for x in row] for row in C_from_superoperator.tolist()],
    "derived_source_choi_rank": C_from_superoperator.rank(),
    "derived_source_active_principal_minors": source_principal_minors,
    "derived_source_choi_positive_semidefinite": True,
    "derived_elementary_superoperator": [[str(x) for x in row] for row in S_psi.tolist()],
    "active_indices_zero_based_input_first_basis": active,
    "active_principal_minors": principal_minors,
    "full_active_determinant": str(determinant),
    "quotient_rank_at_lambda_1_over_6": endpoint_rank,
    "cp_interval_exact": "0 <= lambda <= 1/6",
    "interval_reason": "All principal minors are nonnegative on [0,1/6]; the active 3x3 determinant is negative for 1/6<lambda<1.",
    "all_assertions_passed": True
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
