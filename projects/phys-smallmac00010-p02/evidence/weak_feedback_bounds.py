"""Exact rational inequalities supporting the concrete infinite-state epsilon range."""
from fractions import Fraction as Q
import json
from pathlib import Path


tau = [Q(1), Q(2), Q(3, 2)]
a = [Q(1), Q(1, 2), Q(2, 3)]
gamma = [1 / x for x in tau]
lam = [a[i] * tau[i] for i in range(3)]
assert lam == [1, 1, 1]

# e < 87/32 < 11/4: sum_{n=0}^3 1/n! = 8/3,
# and sum_{n>=4} 1/n! <= (1/4!)/(1-1/5)=5/96.
assert Q(8, 3) + Q(5, 96) == Q(87, 32) < Q(11, 4)
lower = []
upper_k = []
for i in range(3):
    j = (i - 1) % 3
    c = Q(4) if i == 1 else Q(1)
    s_lower = (Q(4, 11) ** (4 if i == 1 else 2)) * c / (gamma[i] + gamma[j])
    coefficient_lower = s_lower / a[i]
    ci = 2 / (gamma[i] + gamma[j])
    ai = 4 * tau[i] * tau[j] + ci * tau[i]
    bi = 2 * ci * sum((1 / (gamma[i] + gamma[k]) for k in range(3) if k != i), Q(0))
    mi = ai + Q(5, 2) * lam[i] * bi
    di = 2 * tau[i] * tau[j]
    # S_i <= Var(h_i)*tau_i <= tau_i since |h_i|<=1.
    kup = 2 * tau[i] / (a[i] ** 2) + 2 * (mi + di) / a[i]
    assert coefficient_lower > Q(3, 40)
    assert kup < 120
    lower.append(str(coefficient_lower))
    upper_k.append(str(kup))

epsilon_max = Q(1, 2000)
strict_margin_coefficient = Q(3, 40) - 120 * epsilon_max
assert strict_margin_coefficient == Q(3, 200) > 0

result = {
    "scope": "Exact rational comparison bounds for the infinite-state analytic remainder; not a finite-box certificate",
    "e_upper_rational": "87/32 < 11/4",
    "coefficient_S_over_a_strict_lower_by_species": lower,
    "K_strict_upper_by_species": upper_k,
    "uniform_coefficient_lower": "3/40",
    "uniform_remainder_K_upper": "120",
    "legal_epsilon_range": "0<|epsilon|<=1/2000",
    "F_i_minus_1_strict_lower": "epsilon^2*(3/200) for all i in the stated range",
}
Path("evidence/weak-feedback-bounds.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
