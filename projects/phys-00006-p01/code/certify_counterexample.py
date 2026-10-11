#!/usr/bin/env python3
"""Exact D-cert counterexample for the frozen qubit-memory inequality."""

import sympy as sp


def partial_trace_second(matrix):
    """Trace the second qubit in R-major order |00>,|01>,|10>,|11>."""
    return sp.Matrix(2, 2, lambda r, rp: sum(
        matrix[2 * r + a, 2 * rp + a] for a in range(2)
    ))


def partial_trace_first(matrix):
    """Trace the first qubit in first-subsystem-major tensor order."""
    return sp.Matrix(2, 2, lambda a, ap: sum(
        matrix[2 * r + a, 2 * r + ap] for r in range(2)
    ))


def channel_on_second(matrix, kraus):
    output = sp.zeros(4)
    for operator in kraus:
        extended = sp.kronecker_product(sp.eye(2), operator)
        output += extended * matrix * extended.conjugate().T
    return sp.simplify(output)


sqrt3 = sp.sqrt(3)
sqrt41 = sp.sqrt(41)
sqrt1489 = sp.sqrt(1489)

# Amplitude-damping calibration channel N_{1,1/4}.
k1 = sp.diag(1, sp.Rational(1, 2))
k2 = sp.Matrix([[0, sqrt3 / 2], [0, 0]])
kraus = [k1, k2]
assert sum((k.T * k for k in kraus), sp.zeros(2)) == sp.eye(2)

# The published alpha certificate, replayed here so that the contraction
# factor used by this D-cert is self-contained.
choi = sp.Matrix([
    [1, 0, 0, sp.Rational(1, 2)],
    [0, 0, 0, 0],
    [0, 0, sp.Rational(3, 4), 0],
    [sp.Rational(1, 2), 0, 0, sp.Rational(1, 4)],
])
h = sp.diag(sp.Rational(1, 2), -sp.Rational(1, 4))
y_alpha = sp.Matrix([
    [1, 0, 0, -1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-1, 0, 0, 1],
])
alpha_slack = choi - sp.kronecker_product(sp.eye(2), h)
assert alpha_slack.is_positive_semidefinite
assert y_alpha.is_positive_semidefinite
assert partial_trace_first(y_alpha) == sp.eye(2)
assert sp.trace(h) == sp.trace(choi * y_alpha) == sp.Rational(1, 4)

# Genuinely entangled, rational-density-matrix inputs with the same R marginal.
psi_plus = sp.Matrix([1, 0, 0, 10]) / sp.sqrt(101)
psi_minus = sp.Matrix([1, 0, 0, -10]) / sp.sqrt(101)
rho = sp.simplify(psi_plus * psi_plus.T)
sigma = sp.simplify(psi_minus * psi_minus.T)
rho_r = partial_trace_second(rho)
sigma_r = partial_trace_second(sigma)
assert rho.is_positive_semidefinite and sigma.is_positive_semidefinite
assert sp.trace(rho) == sp.trace(sigma) == 1
assert rho_r == sigma_r == sp.diag(sp.Rational(1, 101), sp.Rational(100, 101))

# A negative partial-transpose eigenvalue -10/101 certifies that neither input
# is classical on the reference and that both are entangled.
rho_partial_transpose = sp.Matrix(4, 4, lambda i, j:
    rho[2 * (j // 2) + (i % 2), 2 * (i // 2) + (j % 2)])
assert rho_partial_transpose.eigenvals()[sp.Rational(-10, 101)] == 1

gamma = sp.Integer(2)
input_difference = sp.simplify(rho - gamma * sigma)
input_positive_eigenvalue = (3 * sqrt1489 - 101) / 202
expected_input_spectrum = {
    sp.Integer(0): 2,
    (-101 - 3 * sqrt1489) / 202: 1,
    input_positive_eigenvalue: 1,
}
assert input_difference.eigenvals() == expected_input_spectrum
assert 3 * 3 * 1489 > 101 * 101

rho_output = channel_on_second(rho, kraus)
sigma_output = channel_on_second(sigma, kraus)
output_difference = sp.simplify(rho_output - gamma * sigma_output)
output_positive_eigenvalue = (-13 + 3 * sqrt41) / 101
expected_output_spectrum = {
    sp.Integer(0): 1,
    sp.Rational(-75, 101): 1,
    (-13 - 3 * sqrt41) / 101: 1,
    output_positive_eigenvalue: 1,
}
assert output_difference.eigenvals() == expected_output_spectrum
assert 9 * 41 > 13 * 13

# Exact projector onto the positive output eigenvector, embedded in RB.
effect = sp.Matrix([
    [(4 + sqrt41) / (2 * sqrt41), 0, 0, 5 / (2 * sqrt41)],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [5 / (2 * sqrt41), 0, 0, (sqrt41 - 4) / (2 * sqrt41)],
])
assert sp.simplify(effect * effect - effect) == sp.zeros(4)
assert effect.is_positive_semidefinite
assert (sp.eye(4) - effect).is_positive_semidefinite

lhs_witness = sp.simplify(sp.trace(effect * output_difference))
input_divergence = input_positive_eigenvalue
rhs_alpha = sp.simplify((1 - sp.trace(h)) * input_divergence)
strict_margin = sp.simplify(lhs_witness - rhs_alpha)
expected_margin = (199 + 24 * sqrt41 - 9 * sqrt1489) / 808
assert lhs_witness == output_positive_eigenvalue
assert strict_margin == expected_margin

# Exact sign proof for the radical margin.  Both sides of
# 199+24 sqrt(41) > 9 sqrt(1489) are positive.  After squaring, their
# difference is -57392+9552 sqrt(41), and sqrt(41)>32/5 because
# 41>(32/5)^2.  The resulting rational lower bound is 18704/5>0.
squared_gap = sp.expand((199 + 24 * sqrt41) ** 2 - (9 * sqrt1489) ** 2)
rational_lower_bound = -57392 + sp.Rational(9552 * 32, 5)
assert squared_gap == -57392 + 9552 * sqrt41
assert 41 * 25 > 32 * 32
assert rational_lower_bound == sp.Rational(18704, 5) > 0

print("CLAIM=exact counterexample to frozen inequality (D)")
print("CHANNEL=N_{p=1,eta=1/4}; GAMMA=2; BASIS=|00>,|01>,|10>,|11>")
print("ARITHMETIC=exact SymPy rationals and radicals; no floating tolerance")
print("KRAUS_COMPLETENESS=I")
print("ALPHA_H=" + str(h.tolist()))
print("ALPHA_SLACK_EIGENVALUES=" + str(alpha_slack.eigenvals()))
print("ALPHA_DUAL_Y_EIGENVALUES=" + str(y_alpha.eigenvals()))
print("ALPHA_CERTIFIED=1/4")
print("RHO=" + str(rho.tolist()))
print("SIGMA=" + str(sigma.tolist()))
print("COMMON_R_MARGINAL=" + str(rho_r.tolist()))
print("PARTIAL_TRANSPOSE_NEGATIVE_EIGENVALUE=-10/101")
print("INPUT_DIFFERENCE=" + str(input_difference.tolist()))
print("INPUT_SPECTRUM=" + str(input_difference.eigenvals()))
print("INPUT_E_GAMMA=(3*sqrt(1489)-101)/202")
print("RHO_OUTPUT=" + str(rho_output.tolist()))
print("SIGMA_OUTPUT=" + str(sigma_output.tolist()))
print("OUTPUT_DIFFERENCE=" + str(output_difference.tolist()))
print("OUTPUT_SPECTRUM=" + str(output_difference.eigenvals()))
print("EFFECT_M=" + str(effect.tolist()))
print("EFFECT_CHECK=M^2=M; spectrum subset {0,1}")
print("LHS_WITNESS=(-13+3*sqrt(41))/101")
print("RHS_WITH_1_MINUS_ALPHA=3*(3*sqrt(1489)-101)/808")
print("STRICT_MARGIN=(199+24*sqrt(41)-9*sqrt(1489))/808")
print("MARGIN_SIGN_CERT=(199+24sqrt(41))^2-(9sqrt(1489))^2=-57392+9552sqrt(41)>18704/5>0")
print("DECIMAL_MARGIN=" + str(sp.N(strict_margin, 25)))
print("RESULT=PASS; strict exact D-cert violation")
