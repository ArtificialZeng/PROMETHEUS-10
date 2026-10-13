#!/usr/bin/env python3
"""Direct coordinate transcription of Patra--Taoutioui--Vertesi Eqs. (29)--(32).

This implementation deliberately uses only four-component columns in the frozen
computational-basis order.  It does not import or read input B.
"""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "input-a.json"


def sx(value):
    return sp.sstr(sp.simplify(value))


def vector_payload(vector):
    return [sx(entry) for entry in vector]


def matrix_payload(matrix):
    return [[sx(matrix[row, col]) for col in range(matrix.cols)]
            for row in range(matrix.rows)]


def main():
    r2 = sp.sqrt(2)
    r6 = sp.sqrt(6)
    r7 = sp.sqrt(7)

    # Directly keyed from the displayed four-component columns in Eqs. (29), (31),
    # and (32), in the order |00>, |01>, |10>, |11>.
    kets = [
        sp.Matrix([1, 0, 0, 0]),
        sp.Matrix([1 / r2, 1 / r2, 0, 0]),
        sp.Matrix([1 / r2, 0, 1 / r2, 0]),
        sp.Matrix([1 / r2, 0, 0, 1 / r2]),
        sp.Matrix([0, 1 / r6, -r6 / 3, 1 / r6]),
        sp.Matrix([0, 1 / r2, 0, -1 / r2]),
        sp.Matrix([
            sp.sqrt((7 - 2 * r7) / 14),
            -sp.sqrt((7 + 2 * r7) / 42),
            -sp.sqrt((7 + 2 * r7) / 42),
            -sp.sqrt((7 + 2 * r7) / 42),
        ]),
    ]
    weights = [
        1 / (6 + 2 * r7),
        1 / (6 + 2 * r7),
        1 / (6 + 2 * r7),
        1 / (6 + 2 * r7),
        (r7 - 1) / 8,
        (r7 - 1) / 8,
        (3 * r7 - 7) / 4,
    ]

    projectors = [sp.simplify(v * v.conjugate().T) for v in kets]
    norms = [sp.simplify((v.conjugate().T * v)[0]) for v in kets]
    frame = sp.simplify(sum((a * p for a, p in zip(weights, projectors)),
                            sp.zeros(4)))
    gram2 = sp.Matrix(7, 7, lambda i, j: sp.simplify(
        (kets[i].conjugate().T * kets[j])[0]
        * (kets[j].conjugate().T * kets[i])[0]))

    pair_records = []
    witness = sp.Integer(0)
    for i in range(7):
        for j in range(i):
            overlap2 = sp.simplify(gram2[i, j])
            spectral_square = sp.simplify(1 - overlap2)
            delta = sp.simplify(projectors[i] - projectors[j])
            # For two normalized rays, Delta^3=(1-|<i|j>|^2)Delta.
            cubic_residual = sp.simplify(delta**3 - spectral_square * delta)
            assert cubic_residual == sp.zeros(4)
            assert spectral_square > 0
            s = sp.sqrt(spectral_square)
            effect = sp.simplify((delta**2 + s * delta) / (2 * spectral_square))
            assert sp.simplify(effect**2 - effect) == sp.zeros(4)
            assert sp.simplify(effect.conjugate().T - effect) == sp.zeros(4)
            helstrom_term = sp.simplify(sp.trace(delta * effect))
            contribution = sp.simplify(
                weights[i] * weights[j] * (2 * s) * helstrom_term)
            witness += contribution
            pair_records.append({
                "pair": [i + 1, j + 1],
                "overlap_squared": sx(overlap2),
                "positive_eigenvalue_squared": sx(spectral_square),
                "helstrom_difference": sx(helstrom_term),
                "witness_contribution": sx(contribution),
                "effect_check": "Hermitian rank-one projector (E^2=E) exactly",
            })

    witness_residual = sp.simplify(witness - sp.Rational(3, 4))
    assert witness_residual == 0
    payload = {
        "schema_version": 1,
        "source_locator": "arXiv:2609.13075v1, Sec. VI.D, Eqs. (29)-(32), PDF pp. 18-19",
        "representation": "direct coordinate columns",
        "independence_boundary": "This script neither imports nor reads input B or its generator.",
        "basis_order": ["|00>", "|01>", "|10>", "|11>"],
        "state_order": [f"psi_{i}" for i in range(1, 8)],
        "kets": {f"psi_{i + 1}": vector_payload(v) for i, v in enumerate(kets)},
        "weights": {f"alpha_{i + 1}": sx(a) for i, a in enumerate(weights)},
        "exact_checks": {
            "state_norms": [sx(value) for value in norms],
            "weights_positive": [bool(value > 0) for value in weights],
            "weight_sum": sx(sum(weights)),
            "weighted_frame_operator": matrix_payload(frame),
            "weighted_frame_target": matrix_payload(sp.eye(4) / 4),
            "target_witness_with_helstrom_effects": "3/4",
            "target_witness_minus_three_quarters": sx(witness_residual),
            "all_21_effects_legal": all(
                item["effect_check"].startswith("Hermitian") for item in pair_records),
        },
        "pair_checks": pair_records,
    }

    assert all(value == 1 for value in norms)
    assert all(value > 0 for value in weights)
    assert sp.simplify(sum(weights) - 1) == 0
    assert sp.simplify(frame - sp.eye(4) / 4) == sp.zeros(4)
    assert len(pair_records) == 21
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print("input A exact checks: PASS")
    print("unrestricted target witness = 3/4")


if __name__ == "__main__":
    main()
