#!/usr/bin/env python3
"""Independent exact matrix audit of the frozen D-cert candidate.

This checker does not import or read the discovery/certificate script.  It
starts from the explicit density matrices and the independently reproduced
closed-form channel action.
"""

import sympy as sp


def trace_second(matrix):
    return sp.Matrix(2, 2, lambda r, rp: sum(
        matrix[2 * r + a, 2 * rp + a] for a in range(2)
    ))


def apply_reproduced_channel(matrix):
    # Independently use N([[a,b],[c,d]])=[[a+3d/4,b/2],[c/2,d/4]]
    # on every 2x2 A block, rather than the Kraus implementation.
    result = sp.zeros(4)
    for r in range(2):
        for rp in range(2):
            a = matrix[2 * r, 2 * rp]
            b = matrix[2 * r, 2 * rp + 1]
            c = matrix[2 * r + 1, 2 * rp]
            d = matrix[2 * r + 1, 2 * rp + 1]
            block = sp.Matrix([
                [a + sp.Rational(3, 4) * d, b / 2],
                [c / 2, d / 4],
            ])
            for i in range(2):
                for j in range(2):
                    result[2 * r + i, 2 * rp + j] = block[i, j]
    return result


rho = sp.Matrix([
    [1, 0, 0, 10],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [10, 0, 0, 100],
]) / 101
sigma = sp.Matrix([
    [1, 0, 0, -10],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-10, 0, 0, 100],
]) / 101

expected_rho_output = sp.Matrix([
    [1, 0, 0, 5],
    [0, 0, 0, 0],
    [0, 0, 75, 0],
    [5, 0, 0, 25],
]) / 101
expected_sigma_output = sp.Matrix([
    [1, 0, 0, -5],
    [0, 0, 0, 0],
    [0, 0, 75, 0],
    [-5, 0, 0, 25],
]) / 101

assert rho == sp.Matrix([1, 0, 0, 10]) * sp.Matrix([1, 0, 0, 10]).T / 101
assert sigma == sp.Matrix([1, 0, 0, -10]) * sp.Matrix([1, 0, 0, -10]).T / 101
assert trace_second(rho) == trace_second(sigma) == sp.diag(sp.Rational(1, 101), sp.Rational(100, 101))
assert apply_reproduced_channel(rho) == expected_rho_output
assert apply_reproduced_channel(sigma) == expected_sigma_output

input_difference = rho - 2 * sigma
output_difference = expected_rho_output - 2 * expected_sigma_output
assert input_difference == sp.Matrix([
    [-1, 0, 0, 30], [0, 0, 0, 0], [0, 0, 0, 0], [30, 0, 0, -100]
]) / 101
assert output_difference == sp.Matrix([
    [-1, 0, 0, 15], [0, 0, 0, 0], [0, 0, -75, 0], [15, 0, 0, -25]
]) / 101

# The nonzero input block has characteristic polynomial
# lambda^2+lambda-800/10201; direct exact eigenvalue checks avoid any
# numerical diagonalization.
input_positive = (3 * sp.sqrt(1489) - 101) / 202
output_positive = (3 * sp.sqrt(41) - 13) / 101
assert sp.det(input_difference.extract([0, 3], [0, 3]) - input_positive * sp.eye(2)) == 0
assert sp.det(output_difference.extract([0, 3], [0, 3]) - output_positive * sp.eye(2)) == 0
assert input_positive > 0 and output_positive > 0

sqrt41 = sp.sqrt(41)
effect = sp.zeros(4)
effect[0, 0] = (4 + sqrt41) / (2 * sqrt41)
effect[0, 3] = effect[3, 0] = 5 / (2 * sqrt41)
effect[3, 3] = (sqrt41 - 4) / (2 * sqrt41)
assert effect.T == effect
assert sp.simplify(effect ** 2 - effect) == sp.zeros(4)
assert sp.simplify(sp.trace(effect) - 1) == 0
assert sp.simplify(sp.trace(effect * output_difference)) == output_positive

# Recheck the feasible alpha primal slack through an exact Gram decomposition.
h = sp.diag(sp.Rational(1, 2), -sp.Rational(1, 4))
choi = sp.Matrix([
    [1, 0, 0, sp.Rational(1, 2)], [0, 0, 0, 0],
    [0, 0, sp.Rational(3, 4), 0], [sp.Rational(1, 2), 0, 0, sp.Rational(1, 4)],
])
slack = choi - sp.kronecker_product(sp.eye(2), h)
gram = (sp.Matrix([1, 0, 0, 1]) * sp.Matrix([1, 0, 0, 1]).T) / 2
gram += sp.diag(0, sp.Rational(1, 4), sp.Rational(1, 4), 0)
assert slack == gram

margin_numerator = 199 + 24 * sp.sqrt(41) - 9 * sp.sqrt(1489)
assert sp.expand((199 + 24 * sp.sqrt(41)) ** 2 - (9 * sp.sqrt(1489)) ** 2) == -57392 + 9552 * sp.sqrt(41)
assert -57392 + sp.Rational(9552 * 32, 5) == sp.Rational(18704, 5)
assert 41 > sp.Rational(32 * 32, 25)
assert margin_numerator > 0

print("INDEPENDENCE=explicit rational states plus blockwise reproduced channel action; no import/read of discovery script")
print("STATE_PSD=rank-one Gram forms with unit trace")
print("COMMON_R_MARGINAL=diag(1/101,100/101)")
print("INPUT_POSITIVE_EIGENVALUE=(3*sqrt(1489)-101)/202")
print("OUTPUT_EFFECT=rank-one orthogonal projector")
print("OUTPUT_WITNESS=(3*sqrt(41)-13)/101")
print("ALPHA_PRIMAL_SLACK=explicit Gram sum; Tr(H)=1/4")
print("STRICT_MARGIN_NUMERATOR=199+24*sqrt(41)-9*sqrt(1489)>0")
print("SIGN_PROOF_LOWER_BOUND=18704/5>0 after legal squaring")
print("RESULT=PASS; independent exact audit confirms strict D-cert violation")
