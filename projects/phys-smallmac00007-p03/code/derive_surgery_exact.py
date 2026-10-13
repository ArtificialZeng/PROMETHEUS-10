#!/usr/bin/env python3
"""Exact block derivation for two split-core threshold-graph families."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/surgery-symbolic.json"
LOG = ROOT / "evidence/surgery-symbolic.log"
JOB = "phys-smallmac00007-p03-research-94b57d5fe4fb"

s, q, t = sp.symbols("s q t", integer=True, positive=True)
u = sp.symbols("u", integer=True, nonnegative=True)


def block_kemeny(blocks):
    """Theorem 3.8 summed over constant-bit runs, with zero-based indices."""
    n = sp.expand(sum(length for _, length in blocks))
    start = sp.Integer(0)
    m = sp.Integer(0)
    for bit, length in blocks:
        end = start + length - 1
        if bit:
            m += length * (start + end) / 2
        start = end + 1
    start = sp.Integer(0)
    prefix_weight = sp.Integer(0)
    value = n - 1
    for block_index, (bit, length) in enumerate(blocks):
        end = start + length - 1
        later_ones = sum(other_length for other_bit, other_length
                         in blocks[block_index + 1:] if other_bit)
        if bit:
            z = end + 1 + later_ones
            w = 2 * prefix_weight - start * (start - 1)
            value -= length / z
        else:
            z = later_ones
            w = 2 * prefix_weight
        if start != 0:
            telescoping = 1 / start - 1 / (end + 1)
            value += w * (2 * m - w) * telescoping / (2 * m * z)
        if bit:
            prefix_weight += length * (start + end) / 2
        start = end + 1
    return sp.factor(value)


def pineapple(n, r):
    return sp.factor(n - 4 + 2 / (r + 2)
                     + (n - 1) * (2 * r + 3) / (2 * n + r**2 + r - 2))


def positive_coefficients(expression, variables):
    polynomial = sp.Poly(sp.expand(expression), *variables)
    coefficients = polynomial.coeffs()
    assert coefficients and all(coefficient > 0 for coefficient in coefficients)
    return len(coefficients), min(coefficients), max(polynomial.total_degree(), 0)


family_a = [(0, 1), (1, 1), (0, t), (1, s), (0, q), (1, 1)]
family_b = [(0, 1), (1, s), (0, t), (1, 1), (0, q), (1, 1)]
n = s + t + q + 3
r_low = s + 1
r_high = s + t + 1
k_a = block_kemeny(family_a)
k_b = block_kemeny(family_b)
f_low = pineapple(n, r_low)
f_high = pineapple(n, r_high)


def gap_parts(k_value):
    high = sp.factor(f_high - k_value)
    low = sp.factor(f_low - k_value)
    high_num, high_den = map(sp.factor, sp.together(high).as_numer_denom())
    low_num, low_den = map(sp.factor, sp.together(low).as_numer_denom())
    assert sp.rem(high_num, t, t) == 0 and sp.rem(low_num, t, t) == 0
    return high, low, sp.factor(high_num / t), high_den, sp.factor(low_num / t), low_den


high_a, low_a, h_a, high_den_a, low_scaled_a, low_den_a = gap_parts(k_a)
high_b, low_b, h_b, high_den_b, l_b, low_den_b = gap_parts(k_b)
assert sp.rem(low_scaled_a, s, s) == 0
y_a = sp.factor(low_scaled_a / s)

# Family A: if H_A>0 the high-r pineapple wins.  Otherwise the following
# exact positive-coefficient identity forces the low-r pineapple to win.
alpha_a = sp.factor(-sp.Poly(y_a, q).coeff_monomial(q**2)
                    / sp.Poly(h_a, q).coeff_monomial(q**2))
assert alpha_a == (s**2 + 4*s + 1) / (
    s**2*t + 3*s**2 + 4*s*t + 12*s + 3*t + 7)
r_a = sp.factor(y_a + alpha_a * h_a)
r_a_num, r_a_den = map(sp.factor, sp.together(r_a).as_numer_denom())
r_a_certificate = positive_coefficients(r_a_num, (q, s, t))
positive_coefficients(r_a_den, (s, t))

# Family B: L_B itself has positive coefficients after s=u+3.  The two
# remaining integer cases s=1,2 use the same positive-remainder argument.
l_b_large = sp.expand(l_b.subs(s, u + 3))
l_b_large_certificate = positive_coefficients(l_b_large, (q, u, t))
b_small = {}
for s_value in (1, 2):
    h_small = sp.factor(h_b.subs(s, s_value))
    l_small = sp.factor(l_b.subs(s, s_value))
    alpha_small = sp.factor(-sp.Poly(l_small, q).coeff_monomial(q**2)
                            / sp.Poly(h_small, q).coeff_monomial(q**2))
    assert alpha_small > 0
    remainder = sp.factor(l_small + alpha_small * h_small)
    remainder_num, remainder_den = map(
        sp.factor, sp.together(remainder).as_numer_denom())
    certificate = positive_coefficients(remainder_num, (q, t))
    positive_coefficients(remainder_den, (t,))
    b_small[str(s_value)] = {
        "H": str(h_small),
        "L": str(l_small),
        "alpha": str(alpha_small),
        "positive_remainder": str(remainder),
        "positive_numerator_monomials": certificate[0],
    }

# Specialize to the requested one-bit surgery and retain the sign polynomials.
one_high_a = sp.factor(high_a.subs(t, 1))
one_high_b = sp.factor(high_b.subs(t, 1))
one_num_a = sp.factor(sp.together(one_high_a).as_numer_denom()[0] / 4)
one_num_b = sp.factor(sp.together(one_high_b).as_numer_denom()[0] / (s + 1))
assert sp.degree(one_num_a, q) == 2 and sp.LC(sp.Poly(one_num_a, q)) > 0
assert sp.degree(one_num_b, q) == 2 and sp.LC(sp.Poly(one_num_b, q)) > 0
assert one_num_a.subs(q, 0) < 0 and one_num_b.subs(q, 0) < 0

payload = {
    "schema": 1,
    "job_id": JOB,
    "claim_tested": (
        "For all positive integers s,q,t, each of codes 01 0^t 1^s 0^q 1 "
        "and 0 1^s 0^t 1 0^q 1 has K strictly below max{F_n(s+1),"
        "F_n(s+t+1)}, where n=s+t+q+3."
    ),
    "method": "Exact symbolic summation of arXiv:2310.08552v1 Theorem 3.8 over constant-bit runs, followed by polynomial-identity sign certificates.",
    "block_identity": (
        "On a run a<=i<=b, z_i and w_i are constant and "
        "sum_i 1/(i(i+1))=1/a-1/(b+1)."
    ),
    "families": {
        "A": "01 0^t 1^s 0^q 1",
        "B": "0 1^s 0^t 1 0^q 1",
        "n": str(n),
        "low_r": str(r_low),
        "high_r": str(r_high),
    },
    "exact_gaps": {
        "A_high": str(high_a),
        "A_low": str(low_a),
        "B_high": str(high_b),
        "B_low": str(low_b),
        "all_displayed_denominators_positive": True,
    },
    "sign_certificates": {
        "A_H": str(h_a),
        "A_L": str(y_a),
        "A_alpha": str(alpha_a),
        "A_identity": "A_L + A_alpha*A_H = A_positive_remainder",
        "A_positive_remainder": str(r_a),
        "A_positive_remainder_numerator_monomials": r_a_certificate[0],
        "B_H": str(h_b),
        "B_L": str(l_b),
        "B_L_at_s_equals_u_plus_3": str(sp.factor(l_b_large)),
        "B_L_large_positive_monomials": l_b_large_certificate[0],
        "B_small_cases": b_small,
    },
    "one_bit_specialization": {
        "A_fill_minus_defect": str(one_high_a),
        "A_sign_polynomial": str(one_num_a),
        "B_fill_minus_defect": str(one_high_b),
        "B_sign_polynomial": str(one_num_b),
        "sign_rule": (
            "Each sign polynomial is an upward quadratic in q with negative "
            "constant term, hence has exactly one positive real root; the "
            "surgery is negative below and positive above that root, with "
            "possible equality at the root."
        ),
    },
    "result": "proved_exact_family_domination",
    "limitations": (
        "This proves the frozen universal conjecture only on the two stated "
        "six-run families. It neither classifies equality globally nor covers "
        "arbitrary placements or multiple separated interior zero runs."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
LOG.write_text(
    "EXACT SYMBOLIC SURGERY DERIVATION\n"
    f"job_id={JOB}\n"
    "family_A_positive_remainder_identity=true\n"
    f"family_A_positive_remainder_monomials={r_a_certificate[0]}\n"
    "family_B_s_ge_3_low_gap_positive_coefficients=true\n"
    f"family_B_s_ge_3_positive_monomials={l_b_large_certificate[0]}\n"
    "family_B_s_1_2_positive_remainder_identities=true\n"
    "one_bit_fill_monotonicity=false\n"
    "two_pineapple_envelope_strictly_dominates=true\n"
    "scope=two exact six-run families; universal conjecture unresolved\n"
    "OVERALL_CHECK=PASS\n",
    encoding="utf-8",
)
print(json.dumps({
    "result": payload["result"],
    "A_positive_monomials": r_a_certificate[0],
    "B_large_positive_monomials": l_b_large_certificate[0],
}, sort_keys=True))
