#!/usr/bin/env python3
"""Independent exact replay of the split-core family result."""

from fractions import Fraction
import json
from pathlib import Path

from flint import fmpq, fmpq_mat


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/surgery-exact-check.json"
LOG = ROOT / "evidence/surgery-exact-check.log"
JOB = "phys-smallmac00007-p03-research-94b57d5fe4fb"


def theorem_3_8(code_text):
    code = [int(character) for character in code_text]
    n = len(code)
    m = sum(index * code[index] for index in range(1, n))
    prefix_weight = 0
    suffix_ones = sum(code[1:])
    value = Fraction(n - 1)
    for index in range(1, n):
        bit = code[index]
        z_value = (index + 1) * bit + suffix_ones - bit
        w_value = 2 * prefix_weight - index * (index - 1) * bit
        value -= Fraction(bit, z_value)
        value += Fraction(w_value * (2 * m - w_value),
                          2 * m * index * (index + 1) * z_value)
        prefix_weight += index * bit
        suffix_ones -= bit
    return value


def pineapple(n, r):
    return (Fraction(n - 4) + Fraction(2, r + 2)
            + Fraction((n - 1) * (2 * r + 3), 2 * n + r * r + r - 2))


def full_graph_fundamental(code_text):
    code = [int(character) for character in code_text]
    n = len(code)
    adjacency = [[0 if i == j else code[max(i, j)] for j in range(n)]
                 for i in range(n)]
    degrees = [sum(row) for row in adjacency]
    if min(degrees) <= 0:
        raise AssertionError("disconnected input")
    two_m = sum(degrees)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            entry = fmpq(1 if i == j else 0)
            entry -= fmpq(adjacency[i][j], degrees[i])
            entry += fmpq(degrees[j], two_m)
            row.append(entry)
        matrix.append(row)
    inverse = fmpq_mat(matrix).inv()
    return sum((Fraction(str(inverse[i, i])) for i in range(n)), Fraction()) - 1


def codes(s_value, q_value, t_value):
    family_a = "01" + "0" * t_value + "1" * s_value + "0" * q_value + "1"
    family_b = "0" + "1" * s_value + "0" * t_value + "1" + "0" * q_value + "1"
    filled = "0" + "1" * (s_value + t_value + 1) + "0" * q_value + "1"
    return family_a, family_b, filled


grid_checked = 0
minimum_gap = None
minimum_location = None
for t_value in range(1, 6):
    for s_value in range(1, 13):
        for q_value in range(1, 31):
            n = s_value + t_value + q_value + 3
            low = pineapple(n, s_value + 1)
            high = pineapple(n, s_value + t_value + 1)
            for family, code in zip(("A", "B"), codes(s_value, q_value, t_value)[:2]):
                value = theorem_3_8(code)
                gap = max(low, high) - value
                if gap <= 0:
                    raise AssertionError((family, s_value, q_value, t_value, gap))
                if minimum_gap is None or gap < minimum_gap:
                    minimum_gap = gap
                    minimum_location = [family, s_value, q_value, t_value]
                grid_checked += 1

selected_parameters = [(1, 1, 1), (1, 4, 1), (3, 5, 2), (2, 7, 4), (12, 48, 1)]
selected = []
for s_value, q_value, t_value in selected_parameters:
    n = s_value + t_value + q_value + 3
    low = pineapple(n, s_value + 1)
    high = pineapple(n, s_value + t_value + 1)
    for family, code in zip(("A", "B"), codes(s_value, q_value, t_value)[:2]):
        formula_value = theorem_3_8(code)
        graph_value = full_graph_fundamental(code)
        if formula_value != graph_value:
            raise AssertionError("literal full-graph replay mismatch")
        selected.append({
            "family": family,
            "s": s_value,
            "q": q_value,
            "t": t_value,
            "n": n,
            "code": code,
            "theorem_3_8_value": str(formula_value),
            "literal_full_graph_value": str(graph_value),
            "F_low": str(low),
            "F_high": str(high),
            "two_pineapple_gap": str(max(low, high) - formula_value),
        })

a_111, b_111, p_111 = codes(1, 1, 1)
a_141, b_141, p_141 = codes(1, 4, 1)
if a_111 != b_111 or a_141 != b_141:
    raise AssertionError("s=1 families should coincide")
negative_reversal = theorem_3_8(p_111) - theorem_3_8(a_111)
positive_reversal = theorem_3_8(p_141) - theorem_3_8(a_141)
if negative_reversal != Fraction(-229, 1980):
    raise AssertionError(negative_reversal)
if positive_reversal != Fraction(11, 840):
    raise AssertionError(positive_reversal)
_, b_equal, p_equal = codes(12, 48, 1)
if theorem_3_8(p_equal) != theorem_3_8(b_equal) != Fraction(1055, 16):
    raise AssertionError("one-bit equality case failed")
equality_low_gap = pineapple(64, 13) - theorem_3_8(b_equal)
if equality_low_gap != Fraction(337, 2640):
    raise AssertionError(equality_low_gap)

payload = {
    "schema": 1,
    "job_id": JOB,
    "claim_tested": (
        "Exact replay of strict domination by max{F_n(s+1),F_n(s+t+1)} "
        "for the two stated split-core families, plus literal full-graph checks."
    ),
    "method": (
        "Independent direct implementation of Theorem 3.8 on explicit bit strings; "
        "selected cases are separately reconstructed by exact rational inversion of "
        "the literal full-graph fundamental matrix."
    ),
    "coverage": {
        "exact_formula_grid": "1<=t<=5, 1<=s<=12, 1<=q<=30, both families",
        "grid_codes_checked": grid_checked,
        "literal_full_graph_codes_checked": len(selected),
        "selected_parameters": [list(item) for item in selected_parameters],
    },
    "error_control": "All comparisons use Python Fraction or python-flint fmpq arithmetic; tolerance is exactly zero.",
    "minimum_grid_gap": str(minimum_gap),
    "minimum_grid_gap_location_family_s_q_t": minimum_location,
    "one_bit_edge_cases": {
        "s1_q1_fill_minus_defect": str(negative_reversal),
        "s1_q4_fill_minus_defect": str(positive_reversal),
        "family_B_s12_q48_fill_minus_defect": "0",
        "family_B_s12_q48_low_pineapple_gap": str(equality_low_gap),
    },
    "selected_full_graph_records": selected,
    "result": "pass",
    "limitations": (
        "The finite replay is not the proof of the all-parameter statement; that proof "
        "is the exact symbolic identity in evidence/surgery-symbolic.json. Neither "
        "record resolves threshold codes outside the two families."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
LOG.write_text(
    "INDEPENDENT EXACT SURGERY CHECK\n"
    f"job_id={JOB}\n"
    f"exact_formula_grid_codes={grid_checked}\n"
    f"literal_full_graph_codes={len(selected)}\n"
    f"minimum_grid_gap={minimum_gap}\n"
    f"minimum_grid_gap_location={minimum_location}\n"
    f"one_bit_negative_reversal={negative_reversal}\n"
    f"one_bit_positive_reversal={positive_reversal}\n"
    "one_bit_exact_equality_B_s12_q48=true\n"
    "all_selected_formula_equals_literal_full_graph=true\n"
    "OVERALL_CHECK=PASS\n",
    encoding="utf-8",
)
print(json.dumps({
    "grid_codes": grid_checked,
    "full_graph_codes": len(selected),
    "minimum_gap": str(minimum_gap),
    "result": "pass",
}, sort_keys=True))
