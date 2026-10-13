#!/usr/bin/env python3
"""Independent exact ket-action and 2x2 trace-determinant replay of Example 8."""
import json
import sympy as sp

r = sp.sqrt(3)
I2 = sp.eye(2)
# Derived directly as action columns from Eqs. (39)-(41) at the chosen angles.
K = [sp.diag(sp.Rational(1, 2), -sp.Rational(1, 4)),
     sp.Matrix([[0, r / 2], [0, 0]]),
     sp.diag(r / 2, r / 4)]
A = [sp.diag(sp.Rational(1, 2), sp.Rational(1, 4)),
     sp.diag(0, r / 2),
     sp.diag(r / 2, r / 4)]

def trnorm_sq_2x2(x):
    h = x.conjugate().T * x
    # Exact 2x2 identity: (Tr|X|)^2=Tr(X^*X)+2|det X|.
    return sp.simplify(sp.trace(h) + 2 * sp.Abs(sp.det(x)))

def exact_matrix(m):
    return [[str(sp.simplify(m[i, j])) for j in range(m.cols)] for i in range(m.rows)]

tp1 = sp.simplify(sum((x.conjugate().T * x for x in K), sp.zeros(2)))
f1 = sp.simplify(sum((trnorm_sq_2x2(x) for x in K), sp.S.Zero) / 4)
fm_terms, fb_terms = [], []
for i in range(3):
    for j in range(3):
        fm_terms.append(sp.simplify(sp.trace(A[j] * A[i]) ** 2))
        fb_terms.append(sp.simplify(trnorm_sq_2x2(K[j] * A[i])))
f2m = sp.simplify(sum(fm_terms, sp.S.Zero) / 4)
f2b = sp.simplify(sum(fb_terms, sp.S.Zero) / 4)
tp2m = sp.simplify(sum(((A[j] * A[i]).conjugate().T * (A[j] * A[i]) for i in range(3) for j in range(3)), sp.zeros(2)))
# Conditional unitary recovery preserves each (K_j A_i)^*(K_j A_i), so this is the Bayesian TP test.
tp2b = sp.simplify(sum(((K[j] * A[i]).conjugate().T * (K[j] * A[i]) for i in range(3) for j in range(3)), sp.zeros(2)))

assert tp1 == I2 and tp2m == I2 and tp2b == I2
assert f1 == sp.Rational(3, 4)
assert f2m == sp.Rational(5, 8) and f2b == sp.Rational(5, 8)
assert all(x >= 0 for x in fm_terms + fb_terms)

out = {
    "method": "independently derived ket actions; exact SymPy arithmetic; direct 2x2 trace-determinant trace norm; CP from explicit Kraus factorization",
    "mixed_actions_as_matrices": [exact_matrix(x) for x in K],
    "tp_one_step_exact": exact_matrix(tp1),
    "tp_two_step_markov_exact": exact_matrix(tp2m),
    "tp_two_step_bayes_before_unitary_exact": exact_matrix(tp2b),
    "cp_check": "All one- and two-step maps are explicit Kraus sums; every branch contribution X rho X^* is completely positive.",
    "branch_count_each_strategy": 9,
    "markov_branch_trace_square_terms": [str(x) for x in fm_terms],
    "bayes_branch_trace_norm_square_terms": [str(x) for x in fb_terms],
    "F1_exact": str(f1),
    "F2_markov_exact": str(f2m),
    "F2_bayes_exact": str(f2b),
}
print(json.dumps(out, indent=2, sort_keys=True))
