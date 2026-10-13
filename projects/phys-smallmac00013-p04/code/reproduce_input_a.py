#!/usr/bin/env python3
"""Route A: direct Choi transcription plus the primary source's Eq. (3)."""

import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evidence/input-a.json").read_text(encoding="utf-8"))


def matrix_from_strings(values, symbols=None):
    symbols = symbols or {}
    return sp.Matrix([[sp.sympify(x.replace("lambda", "lam"), locals=symbols)
                       for x in row] for row in values])


def partial_trace_out(matrix, n):
    return sp.Matrix(n, n, lambda i, j: sp.simplify(
        sum(matrix[n * i + a, n * j + a] for a in range(n))))


lam = sp.symbols("lambda", real=True)
n = DATA["dimension"]
C = matrix_from_strings(DATA["choi_matrix"])
target = matrix_from_strings(DATA["published_quotient"], {"lam": lam})

t = sp.sqrt(1 - lam)
K_inv_T = sp.diag(1, 1 / t)
L_T = sp.sqrt(lam) * sp.Matrix([[0, 0], [1, 0]])
A = sp.kronecker_product(K_inv_T, sp.eye(n))
D = sp.kronecker_product(L_T, sp.eye(n))
quotient = A * C * A.T - D * C * D.T / (1 - lam)
quotient = quotient.applyfunc(sp.simplify)

assert C == C.conjugate().T
assert partial_trace_out(C, n) == sp.eye(n)
assert C.rank() == 3
assert (quotient - target).applyfunc(sp.simplify) == sp.zeros(n * n)

active = [0, 2, 3]
source_principal_minors = {}
for size in range(1, len(active) + 1):
    for subset in itertools.combinations(active, size):
        source_principal_minors[",".join(map(str, subset))] = str(
            sp.factor(C.extract(subset, subset).det()))
assert all(C.extract(subset, subset).det() > 0
           for size in range(1, len(active) + 1)
           for subset in itertools.combinations(active, size))

principal_minors = {}
for size in range(1, len(active) + 1):
    for subset in itertools.combinations(active, size):
        minor = quotient.extract(subset, subset).det()
        principal_minors[",".join(map(str, subset))] = str(sp.factor(minor))

assert sp.simplify(
    quotient.extract(active, active).det() - (1 - 6 * lam) / (27 * (1 - lam) ** 2)
) == 0
endpoint_rank = quotient.subs(lam, sp.Rational(1, 6)).rank()
assert endpoint_rank == 2

result = {
    "route": "A_direct_Choi_plus_source_Eq3",
    "choi_hermitian": True,
    "trace_preserving_partial_trace": [[str(x) for x in row] for row in partial_trace_out(C, n).tolist()],
    "source_choi_rank": C.rank(),
    "source_active_principal_minors": source_principal_minors,
    "source_choi_positive_semidefinite": True,
    "quotient_matches_published_entrywise": True,
    "active_indices_zero_based_input_first_basis": active,
    "active_principal_minors": principal_minors,
    "full_active_determinant": str(sp.factor(quotient.extract(active, active).det())),
    "quotient_rank_at_lambda_1_over_6": endpoint_rank,
    "cp_interval_exact": "0 <= lambda <= 1/6",
    "interval_reason": "All principal minors are nonnegative on [0,1/6]; the active 3x3 determinant is negative for 1/6<lambda<1.",
    "all_assertions_passed": True
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
