#!/usr/bin/env python3
"""Exact alpha_+ certificate for the rank-deficient calibration channel."""

import sympy as sp


def partial_trace_a(matrix):
    return sp.Matrix(2, 2, lambda b, bp: sum(
        matrix[2 * a + b, 2 * a + bp] for a in range(2)
    ))


# A-major Choi matrix of N_{1,1/4}, independently displayed in the
# reproduction packet.  This script performs only exact arithmetic.
choi = sp.Matrix([
    [1, 0, 0, sp.Rational(1, 2)],
    [0, 0, 0, 0],
    [0, 0, sp.Rational(3, 4), 0],
    [sp.Rational(1, 2), 0, 0, sp.Rational(1, 4)],
])

# The zero primal variable proves alpha_+ >= 0.
primal_h_plus = sp.zeros(2)
primal_slack = choi - sp.kronecker_product(sp.eye(2), primal_h_plus)

# For max Tr H subject to H>=0 and J-I tensor H>=0, a weak-dual feasible
# operator obeys Y>=0 and Tr_A Y>=I.  The vector below lies in ker(J).
kappa = sp.Matrix([1, 0, 0, -2])
dual_y_plus = kappa * kappa.T
dual_partial_trace = partial_trace_a(dual_y_plus)
dual_objective = sp.trace(choi * dual_y_plus)

assert primal_h_plus.is_positive_semidefinite
assert primal_slack.is_positive_semidefinite
assert dual_y_plus.is_positive_semidefinite
assert (dual_partial_trace - sp.eye(2)).is_positive_semidefinite
assert choi * kappa == sp.zeros(4, 1)
assert dual_objective == 0

# Weak duality is explicit: for every primal-feasible H,
# Tr H <= Tr[(Tr_A Y)H] = Tr[Y(I tensor H)] <= Tr[YJ] = 0.
# Together with H=0, this brackets the optimum exactly.
print("CHANNEL=N_{p=1,eta=1/4}")
print("ARITHMETIC=exact SymPy rationals; no tolerance")
print("PRIMAL_H_PLUS=" + str(primal_h_plus.tolist()))
print("PRIMAL_OBJECTIVE=" + str(sp.trace(primal_h_plus)))
print("DUAL_Y_PLUS=" + str(dual_y_plus.tolist()))
print("DUAL_Y_PLUS_EIGENVALUES=" + str(dual_y_plus.eigenvals()))
print("DUAL_PARTIAL_TRACE_A=" + str(dual_partial_trace.tolist()))
print("DUAL_PARTIAL_TRACE_A_MINUS_I=" + str((dual_partial_trace - sp.eye(2)).tolist()))
print("DUAL_OBJECTIVE_TR_JY=" + str(dual_objective))
print("WEAK_DUAL_CHAIN=Tr(H)<=Tr[(Tr_A Y)H]=Tr[Y(I tensor H)]<=Tr[YJ]=0")
print("CERTIFIED_BRACKET=0 <= alpha_+ <= 0")
print("RESULT=PASS; alpha_+(N_{1,1/4})=0 exactly")
