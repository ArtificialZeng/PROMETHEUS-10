#!/usr/bin/env python3
"""Independent full-matrix Routh replay of the rational gap counterexample.

Unlike certify_rational_counterexample.py, this checker uses input A, never
splits into parity blocks, forms the full degree-16 characteristic polynomial
at each rational rate, removes its single zero factor, and constructs the
Routh array recursively rather than through Hurwitz determinants.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


PROJECT = Path(__file__).resolve().parents[1]
GAMMA, LAMBDA, S = sp.symbols("Gamma lambda s")


def decode(rows: list[list[str]]) -> sp.Matrix:
    return sp.Matrix(
        [[sp.sympify(item, locals={"I": sp.I}) for item in row] for row in rows]
    )


def primitive_integer_polynomial(expression: sp.Expr) -> sp.Poly:
    polynomial = sp.Poly(expression, S).clear_denoms()[1].primitive()[1]
    if polynomial.LC() < 0:
        polynomial = -polynomial
    return polynomial


def routh_first_column(polynomial: sp.Poly) -> list[sp.Expr]:
    coefficients = polynomial.all_coeffs()
    degree = polynomial.degree()
    columns = (degree + 2) // 2
    table = [[sp.Integer(0) for _ in range(columns)] for _ in range(degree + 1)]
    table[0][: len(coefficients[0::2])] = coefficients[0::2]
    table[1][: len(coefficients[1::2])] = coefficients[1::2]
    for row in range(2, degree + 1):
        if table[row - 1][0] == 0:
            raise AssertionError("zero Routh pivot requires a special-case construction")
        for column in range(columns - 1):
            table[row][column] = sp.cancel(
                (
                    table[row - 1][0] * table[row - 2][column + 1]
                    - table[row - 2][0] * table[row - 1][column + 1]
                )
                / table[row - 1][0]
            )
    return [row[0] for row in table]


input_a = json.loads((PROJECT / "evidence/input-a.json").read_text(encoding="utf-8"))
generator = decode(input_a["coherent_matrix"]) + GAMMA * decode(input_a["dissipator_matrix"])

records = []
for gamma, threshold, expected_count in [
    (sp.Rational(73, 10), sp.Rational(3, 2), 0),
    (sp.Integer(8), sp.Integer(1), 2),
]:
    characteristic = generator.subs(GAMMA, gamma).charpoly(LAMBDA).as_poly()
    zero_multiplicity = min(power[0] for power in characteristic.as_dict())
    if zero_multiplicity != 1:
        raise AssertionError("the full generator must have exactly one zero root")
    nonzero = sp.Poly.from_list(
        characteristic.all_coeffs()[:-1],
        gens=characteristic.gens[0],
        domain=characteristic.domain,
    )
    shifted = primitive_integer_polynomial(
        nonzero.as_expr().subs(characteristic.gens[0], S - threshold)
    )
    first_column = routh_first_column(shifted)
    signs = [int(sp.sign(item)) for item in first_column]
    if any(sign == 0 for sign in signs):
        raise AssertionError("unexpected zero Routh entry")
    changes = sum(signs[index] != signs[index - 1] for index in range(1, len(signs)))
    if changes != expected_count:
        raise AssertionError(f"expected {expected_count} RHP roots, obtained {changes}")
    records.append(
        {
            "Gamma": str(gamma),
            "shift_r": str(threshold),
            "full_characteristic_degree": characteristic.degree(),
            "zero_root_algebraic_multiplicity": zero_multiplicity,
            "shifted_nonzero_degree": shifted.degree(),
            "shifted_nonzero_coefficients_descending": [
                str(item) for item in shifted.all_coeffs()
            ],
            "routh_first_column": [str(item) for item in first_column],
            "routh_first_column_signs": signs,
            "right_half_plane_root_count": changes,
        }
    )

payload = {
    "status": "pass",
    "method": "Independent exact full-16x16 characteristic polynomial and recursive Routh array from source-transcription input A; no parity split and no Hurwitz-determinant code are shared with the primary certificate.",
    "claim_checked": "g(73/10)>3/2 and g(8)<1",
    "records": records,
    "conclusion": "The full nonstationary spectrum has zero roots to the right of Re(lambda)=-3/2 at Gamma=73/10 and two roots to the right of Re(lambda)=-1 at Gamma=8.",
    "software": {"Python": sys.version.split()[0], "SymPy": sp.__version__},
}

output = PROJECT / "evidence/rational-counterexample-independent.json"
output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
digest = hashlib.sha256(output.read_bytes()).hexdigest()
lines = [
    "Independent exact replay of the rational counterexample",
    "Input A; full 16x16 characteristic polynomial; recursive Routh array; no parity decomposition.",
    "Gamma=73/10, shift 3/2: first-column signs " + str(records[0]["routh_first_column_signs"]),
    "Right-half-plane roots: 0; therefore g(73/10)>3/2.",
    "Gamma=8, shift 1: first-column signs " + str(records[1]["routh_first_column_signs"]),
    "Right-half-plane roots: 2; therefore g(8)<1.",
    f"Independent evidence SHA-256: {digest}",
]
(PROJECT / "evidence/rational-counterexample-independent.log").write_text(
    "\n".join(lines) + "\n", encoding="utf-8"
)
print(json.dumps({"ok": True, "sha256": digest}))
