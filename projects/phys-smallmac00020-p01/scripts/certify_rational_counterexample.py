#!/usr/bin/env python3
"""Exact Routh--Hurwitz certificate that Gamma=8 is not gap-optimal.

The proof uses only rational arithmetic.  It reconstructs the two parity-block
characteristic polynomials from the independently derived matrix-unit input B.
For Gamma=73/10 it proves that every nonstationary eigenvalue lies strictly to
the left of Re(lambda)=-3/2.  For Gamma=8 it proves that the Sigma-minus block
has exactly two eigenvalues to the right of Re(lambda)=-1.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
import sympy as sp


PROJECT = Path(__file__).resolve().parents[1]
EVIDENCE = PROJECT / "evidence"
GAMMA, LAMBDA, S = sp.symbols("Gamma lambda s")


def decode(rows: list[list[str]]) -> sp.Matrix:
    return sp.Matrix(
        [[sp.sympify(item, locals={"I": sp.I}) for item in row] for row in rows]
    )


def primitive_integer_polynomial(expression: sp.Expr, variable: sp.Symbol) -> sp.Poly:
    polynomial = sp.Poly(sp.cancel(expression), variable).clear_denoms()[1].primitive()[1]
    if polynomial.LC() < 0:
        polynomial = -polynomial
    return polynomial


def hurwitz_determinants(polynomial: sp.Poly) -> list[sp.Integer]:
    """Return the leading principal minors of the Hurwitz matrix."""

    coefficients = polynomial.all_coeffs()
    degree = polynomial.degree()
    matrix = sp.zeros(degree)
    # With coefficients a_0,...,a_n in descending powers, rows begin
    # (a_1,a_3,...), (a_0,a_2,...), (0,a_1,...), ... .
    for row in range(degree):
        for column in range(degree):
            index = 2 * column - row + 1
            if 0 <= index <= degree:
                matrix[row, column] = coefficients[index]
    return [sp.factor(matrix[:size, :size].det()) for size in range(1, degree + 1)]


def certificate_record(polynomial: sp.Poly) -> dict:
    determinants = hurwitz_determinants(polynomial)
    determinant_signs = [int(sp.sign(item)) for item in determinants]
    first_column_signs = [int(sp.sign(polynomial.LC())), determinant_signs[0]]
    first_column_signs.extend(
        int(sp.sign(determinants[index] / determinants[index - 1]))
        for index in range(1, len(determinants))
    )
    sign_changes = sum(
        first_column_signs[index] != first_column_signs[index - 1]
        for index in range(1, len(first_column_signs))
    )
    return {
        "degree": polynomial.degree(),
        "primitive_integer_polynomial": sp.sstr(polynomial.as_expr()),
        "coefficients_descending": [str(item) for item in polynomial.all_coeffs()],
        "hurwitz_determinants": [str(item) for item in determinants],
        "hurwitz_determinant_signs": determinant_signs,
        "routh_first_column_signs": first_column_signs,
        "routh_right_half_plane_root_count": sign_changes,
        "no_zero_first_column_entries": all(item != 0 for item in first_column_signs),
    }


def sha256(relative: str) -> str:
    return hashlib.sha256((PROJECT / relative).read_bytes()).hexdigest()


def mp_eigenvalues(matrix: sp.Matrix, gamma: mp.mpf) -> list[mp.mpc]:
    numeric = mp.matrix(matrix.rows, matrix.cols)
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            value = matrix[row, column].subs(GAMMA, sp.Float(str(gamma), 110))
            numeric[row, column] = mp.mpc(
                str(sp.N(sp.re(value), 105)), str(sp.N(sp.im(value), 105))
            )
    values, _ = mp.eig(numeric, left=False, right=True)
    return list(values)


def replay_record(matrix: sp.Matrix, gamma_text: str) -> dict:
    gamma = mp.mpf(gamma_text)
    values = mp_eigenvalues(matrix, gamma)
    nonzero = [item for item in values if abs(item) > mp.mpf("1e-70")]
    gap = min(-mp.re(item) for item in nonzero)
    leading = sorted(nonzero, key=lambda item: mp.re(item), reverse=True)[:4]
    return {
        "Gamma": gamma_text,
        "gap_100_digit_replay": mp.nstr(gap, 70),
        "leading_nonzero_eigenvalues": [
            {"real": mp.nstr(mp.re(item), 60), "imag": mp.nstr(mp.im(item), 60)}
            for item in leading
        ],
    }


input_b = json.loads((EVIDENCE / "input-b.json").read_text(encoding="utf-8"))
coherent_b = decode(input_b["coherent_matrix"])
dissipator_b = decode(input_b["dissipator_matrix"])
generator_b = coherent_b + GAMMA * dissipator_b

sz = sp.diag(1, -1)
parity = sp.kronecker_product(
    sp.kronecker_product(sz, sz), sp.kronecker_product(sz, sz)
)
plus_indices = [index for index in range(16) if parity[index, index] == 1]
minus_indices = [index for index in range(16) if parity[index, index] == -1]
off_block = generator_b.extract(plus_indices, minus_indices)
off_block_reverse = generator_b.extract(minus_indices, plus_indices)
assert off_block.is_zero_matrix and off_block_reverse.is_zero_matrix

plus_b = generator_b.extract(plus_indices, plus_indices)
minus_b = generator_b.extract(minus_indices, minus_indices)


def fixed_block_polynomials(gamma: sp.Rational) -> tuple[sp.Poly, sp.Poly]:
    plus = plus_b.subs(GAMMA, gamma)
    minus = minus_b.subs(GAMMA, gamma)
    return plus.charpoly(LAMBDA).as_poly(), minus.charpoly(LAMBDA).as_poly()


gamma_test = sp.Rational(73, 10)
threshold_test = sp.Rational(3, 2)
plus_test, minus_test = fixed_block_polynomials(gamma_test)
plus_stationary_multiplicity = min(power[0] for power in plus_test.as_dict())
minus_at_zero = minus_test.eval(0)
assert plus_stationary_multiplicity == 1
assert minus_at_zero != 0
plus_nonzero_test = sp.Poly.from_list(
    plus_test.all_coeffs()[:-1], gens=LAMBDA, domain=plus_test.domain
)
plus_shift_test = primitive_integer_polynomial(
    plus_nonzero_test.as_expr().subs(LAMBDA, S - threshold_test), S
)
minus_shift_test = primitive_integer_polynomial(
    minus_test.as_expr().subs(LAMBDA, S - threshold_test), S
)
plus_test_certificate = certificate_record(plus_shift_test)
minus_test_certificate = certificate_record(minus_shift_test)
assert plus_test_certificate["routh_right_half_plane_root_count"] == 0
assert minus_test_certificate["routh_right_half_plane_root_count"] == 0
assert all(sign > 0 for sign in plus_test_certificate["hurwitz_determinant_signs"])
assert all(sign > 0 for sign in minus_test_certificate["hurwitz_determinant_signs"])

gamma_ep = sp.Integer(8)
threshold_ep = sp.Integer(1)
plus_ep, minus_ep = fixed_block_polynomials(gamma_ep)
assert min(power[0] for power in plus_ep.as_dict()) == 1
assert minus_ep.eval(0) != 0
minus_shift_ep = primitive_integer_polynomial(
    minus_ep.as_expr().subs(LAMBDA, S - threshold_ep), S
)
minus_ep_certificate = certificate_record(minus_shift_ep)
assert minus_ep_certificate["no_zero_first_column_entries"]
assert minus_ep_certificate["routh_right_half_plane_root_count"] == 2

# Independent high-precision replay uses the separately transcribed input A.
input_a = json.loads((EVIDENCE / "input-a.json").read_text(encoding="utf-8"))
generator_a = decode(input_a["coherent_matrix"]) + GAMMA * decode(
    input_a["dissipator_matrix"]
)
mp.mp.dps = 105
replay = [replay_record(generator_a, "7.3"), replay_record(generator_a, "8")]

payload = {
    "scope": "Exact rational counterexample to Gamma=8 being a global spectral-gap maximizer; the actual global maximizer remains unresolved.",
    "model": "Fixed two-qubit XYZ GKSL generator in problem.md with gamma=3/5, Delta=2/5, Gamma>0, Jx=hbar=1.",
    "statement_certified": "g(73/10)>3/2>1>g(8), while the reproduced largest Liouvillian exceptional point is Gamma_cr=8.",
    "exact_method": "Routh-Hurwitz stability of the shifted exact parity-block characteristic polynomials q(s)=p(s-r), all over Q. Positive Hurwitz determinants put every shifted root in Re(s)<0; the nonzero Routh first column at Gamma=8 has two sign changes and therefore exactly two roots in Re(s)>0.",
    "matrix_source_for_exact_certificate": "evidence/input-b.json (independent matrix-unit action construction)",
    "parity_block_check": {
        "plus_dimension": len(plus_indices),
        "minus_dimension": len(minus_indices),
        "both_off_diagonal_blocks_exactly_zero": True,
    },
    "Gamma_73_over_10": {
        "Gamma": "73/10",
        "shift_r": "3/2",
        "zero_mode": {
            "Sigma_plus_algebraic_multiplicity": int(plus_stationary_multiplicity),
            "Sigma_minus_characteristic_value_at_zero": str(minus_at_zero),
            "conclusion": "The stationary eigenvalue is unique, and it is removed before the Sigma-plus Hurwitz test.",
        },
        "Sigma_plus_nonzero_shifted": plus_test_certificate,
        "Sigma_minus_shifted": minus_test_certificate,
        "exact_conclusion": "Every nonzero full-Liouvillian eigenvalue satisfies Re(lambda)<-3/2, hence g(73/10)>3/2.",
    },
    "Gamma_8": {
        "Gamma": "8",
        "shift_r": "1",
        "Sigma_minus_shifted": minus_ep_certificate,
        "exact_conclusion": "Exactly two Sigma-minus eigenvalues satisfy Re(lambda)>-1, hence g(8)<1.",
    },
    "logical_conclusion": "Because 73/10>0 and g(73/10)>3/2>1>g(8), Gamma=8 cannot belong to the set of global maximizers of g. This does not identify the maximizer.",
    "independent_high_precision_replay": replay,
    "error_control": "The central inequalities and Routh root counts use exact SymPy rational/integer arithmetic; no floating-point value enters the proof. The 105-digit eigenspectra are noncertifying cross-checks only.",
    "physical_domain": "Both tested rates are strictly positive and use the same fixed Hamiltonian, jump operator, normalization, and complete 16-dimensional Liouville space as the reproduced source model.",
    "limitations": [
        "The exact counterexample does not prove existence, uniqueness, or the location of the global maximizer.",
        "It compares asymptotic spectral gaps, not finite-time Hilbert-Schmidt relaxation for every state or quench.",
        "Novelty is subject to the bounded successor/literature comparison recorded separately.",
    ],
    "software": {
        "Python": sys.version.split()[0],
        "NumPy": np.__version__,
        "SciPy": scipy.__version__,
        "SymPy": sp.__version__,
        "mpmath": mp.__version__,
        "mpmath_replay_digits": mp.mp.dps,
    },
    "integrity": {
        "source.md": sha256("source.md"),
        "evidence/input-a.json": sha256("evidence/input-a.json"),
        "evidence/input-b.json": sha256("evidence/input-b.json"),
        "intake-evidence/primary-sources/phys-00020-p01-01-2412.13674v2.pdf": sha256(
            "intake-evidence/primary-sources/phys-00020-p01-01-2412.13674v2.pdf"
        ),
    },
}

output = EVIDENCE / "rational-counterexample-certificate.json"
output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
digest = hashlib.sha256(output.read_bytes()).hexdigest()

log_lines = [
    "Research pass 3: exact rational Routh-Hurwitz counterexample",
    "Exact input: independently derived matrix-unit generator in evidence/input-b.json.",
    "At Gamma=73/10 and shift r=3/2, all 7 Sigma-plus nonzero and all 8 Sigma-minus Hurwitz determinants are strictly positive.",
    "Therefore every nonstationary eigenvalue has Re(lambda)<-3/2 and g(73/10)>3/2.",
    "At Gamma=8 and shift r=1, the Sigma-minus Routh first-column signs are "
    + str(minus_ep_certificate["routh_first_column_signs"])
    + ", with exactly two sign changes and no zero entry.",
    "Therefore two eigenvalues have Re(lambda)>-1 and g(8)<1.",
    "Exact conclusion: g(73/10)>3/2>1>g(8), so the largest LEP Gamma_cr=8 is not a global gap maximizer.",
    "Scope limitation: the actual global maximizer remains unresolved.",
    f"Certificate SHA-256: {digest}",
]
(EVIDENCE / "rational-counterexample-certificate.log").write_text(
    "\n".join(log_lines) + "\n", encoding="utf-8"
)
print(json.dumps({"ok": True, "certificate": str(output.relative_to(PROJECT)), "sha256": digest}))
