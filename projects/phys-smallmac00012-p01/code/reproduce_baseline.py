#!/usr/bin/env python3
"""Exact reproduction of the order-three criterion and published baselines."""

import sympy as sp


R = sp.Rational
I3 = sp.eye(3)


def require(condition, message):
    if condition is not True and condition != sp.S.true:
        raise AssertionError(message)
    print(f"PASS: {message}")


def matrix_equal(left, right):
    if left.shape != right.shape:
        return False
    return all(sp.simplify(left[i, j] - right[i, j]) == 0
               for i in range(left.rows) for j in range(left.cols))


def moduli_squared(unitary):
    return unitary.applyfunc(lambda z: sp.simplify(z * sp.conjugate(z)))


def is_bistochastic(matrix):
    entries_nonnegative = all(entry.is_nonnegative is True for entry in matrix)
    row_sums = all(sp.simplify(sum(matrix[i, j] for j in range(3)) - 1) == 0 for i in range(3))
    col_sums = all(sp.simplify(sum(matrix[i, j] for i in range(3)) - 1) == 0 for j in range(3))
    return entries_nonnegative and row_sums and col_sums


def h_value(matrix):
    x = [sp.simplify(matrix[i, 0] * matrix[i, 1]) for i in range(3)]
    h = 2 * (x[0]*x[1] + x[0]*x[2] + x[1]*x[2]) - sum(value**2 for value in x)
    return x, sp.factor(h)


def kraus_operators(unitary):
    result = []
    for i in range(3):
        for j in range(3):
            elementary = sp.zeros(3)
            elementary[i, j] = unitary[i, j]
            result.append(elementary)
    return result


def channel_superoperator(unitary):
    total = sp.zeros(9)
    for operator in kraus_operators(unitary):
        total += sp.kronecker_product(sp.conjugate(operator), operator)
    return total.applyfunc(sp.simplify)


def check_realizer(name, matrix, unitary):
    require(matrix_equal(unitary.H * unitary, I3), f"{name}: supplied realizer is exactly unitary")
    require(matrix_equal(moduli_squared(unitary), matrix), f"{name}: |U_ij|^2 equals the target row by row")


def report_case(name, matrix, expected_h, realizer=None):
    require(is_bistochastic(matrix), f"{name}: matrix is exactly bistochastic")
    x, h = h_value(matrix)
    require(sp.simplify(h - expected_h) == 0, f"{name}: exact h={sp.sstr(expected_h)}")
    print(f"CASE {name}: x={[sp.sstr(v) for v in x]}, h={sp.sstr(h)}")
    if realizer is not None:
        check_realizer(name, matrix, realizer)


print("EXACT QUTRIT REPRODUCTION — SymPy exact arithmetic")
print(f"SymPy version: {sp.__version__}")

# Direct unitary/Kraus reconstruction of a concrete factorisable-factor case.
t, s = R(1, 4), R(1, 3)
A = sp.Matrix([[t, 1-t, 0], [1-t, t, 0], [0, 0, 1]])
C = sp.Matrix([[1, 0, 0], [0, s, 1-s], [0, 1-s, s]])
M = C * A
U = sp.Matrix([[sp.sqrt(t), sp.sqrt(1-t), 0],
               [sp.sqrt(1-t), -sp.sqrt(t), 0],
               [0, 0, 1]])
V = sp.Matrix([[1, 0, 0],
               [0, sp.sqrt(s), sp.sqrt(1-s)],
               [0, sp.sqrt(1-s), -sp.sqrt(s)]])
W = sp.Matrix([[R(1, 2), sp.sqrt(3)/2, 0],
               [R(1, 2), -1/(2*sp.sqrt(3)), sp.sqrt(R(2, 3))],
               [1/sp.sqrt(2), -1/sp.sqrt(6), -1/sp.sqrt(3)]])

require(is_bistochastic(A) and is_bistochastic(C) and is_bistochastic(M), "factor matrices and ordered product C*A are bistochastic")
check_realizer("T12(1/4)", A, U)
check_realizer("T23(1/3)", C, V)
require(matrix_equal(M, sp.Matrix([[R(1,4), R(3,4), 0], [R(1,4), R(1,12), R(2,3)], [R(1,2), R(1,6), R(1,3)]])), "ordered product C*A matches the transcribed column convention")
require(matrix_equal(V * U, W), "ordinary sparse unitary product V*U equals the displayed W in this benchmark")
check_realizer("factorisable product", M, W)

for label, unitary in (("U", U), ("V", V), ("W", W)):
    tp_sum = sum((operator.H * operator for operator in kraus_operators(unitary)), sp.zeros(3))
    require(matrix_equal(tp_sum, I3), f"{label}: Kraus completeness sum is I3")

require(matrix_equal(channel_superoperator(V) * channel_superoperator(U), channel_superoperator(W)), "full dephase-unitary-dephase superoperators satisfy Phi_V o Phi_U = Phi_W")
print("BASELINE factorisable product M=C*A:")
print(M)
print("BASELINE exact realizer W:")
print(W)

# Interior: flat matrix and the exact order-three Fourier realizer.
omega = -R(1, 2) + sp.I*sp.sqrt(3)/2
F3 = sp.Matrix([[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]) / sp.sqrt(3)
J3 = sp.ones(3) / 3
report_case("interior_flat", J3, R(1, 27), F3)

# Strictly positive saturated triangle supplied by the factorisable baseline.
report_case("saturated_positive", M, 0, W)
L0, L1, L2 = sp.sqrt(3)/4, sp.sqrt(3)/12, sp.sqrt(3)/6
require(sp.simplify(L0-L1-L2) == 0, "saturated_positive: L0=L1+L2")
cos11 = sp.simplify((L2**2-L0**2-L1**2)/(2*L0*L1))
cos21 = sp.simplify((L1**2-L2**2-L0**2)/(2*L0*L2))
cosdiff = sp.simplify((L0**2-L1**2-L2**2)/(2*L1*L2))
require((cos11, cos21, cosdiff) == (-1, -1, 1), "saturated_positive: published phase cosines give phases pi,pi")

# Exactly two positive links: equal is feasible; unequal is infeasible.
M_two_equal = sp.Matrix([[R(1,2), R(1,2), 0], [R(1,2), R(1,2), 0], [0, 0, 1]])
O_two_equal = sp.Matrix([[1/sp.sqrt(2), 1/sp.sqrt(2), 0], [1/sp.sqrt(2), -1/sp.sqrt(2), 0], [0, 0, 1]])
report_case("two_positive_equal_zero", M_two_equal, 0, O_two_equal)

M_two_unequal = sp.Matrix([[R(1,4), R(1,4), R(1,2)], [R(1,4), R(3,4), 0], [R(1,2), 0, R(1,2)]])
report_case("two_positive_unequal_zero", M_two_unequal, -R(1,64))

# All links zero: phase quotient formulas are skipped, direct completion works.
report_case("all_zero_identity", I3, 0, I3)

# Published non-unistochastic qutrit example Q, Rajchel-Mieldzioc et al. Eq. (5).
Q = sp.Matrix([[0, R(1,2), R(1,2)], [R(1,2), 0, R(1,2)], [R(1,2), R(1,2), 0]])
report_case("published_nonunistochastic_Q", Q, -R(1,16))

# Generic interior phase replay for the flat matrix: all cosines are -1/2.
LF = R(1,3)
flat_cosines = (
    sp.simplify((LF**2-LF**2-LF**2)/(2*LF*LF)),
    sp.simplify((LF**2-LF**2-LF**2)/(2*LF*LF)),
    sp.simplify((LF**2-LF**2-LF**2)/(2*LF*LF)),
)
require(flat_cosines == (-R(1,2), -R(1,2), -R(1,2)), "interior_flat: Eqs. (24)-(25) reproduce Fourier relative phase cosines")

print("RESULT: all exact transcription, completion, boundary, zero-branch, published-Q, unitary, Kraus, and ordered-product checks passed.")
