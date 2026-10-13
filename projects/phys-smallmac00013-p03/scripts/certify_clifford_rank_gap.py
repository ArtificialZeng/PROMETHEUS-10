#!/usr/bin/env python3
"""Emit an exact certificate for the Spin(16) Clifford-flattening rank gap.

All calculations are over ZZ or QQ(a,b,c).  The JSON artifact contains an
explicit right-nullspace basis for every low-rank normal form and indexed
nonzero minors for every high-rank normal form.  No finite-field or floating
point inference is used.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


N = 8
FULL = (1 << N) - 1
EVEN = [mask for mask in range(1 << N) if mask.bit_count() % 2 == 0]
PAIRS = list(combinations(range(2 * N), 2))
A, B, C = sp.symbols("a b c")


def gamma(index: int, mask: int) -> tuple[int, int]:
    """Real Witt-equivalent Majorana action; omitted i is a row rescaling."""
    mode, kind = divmod(index, 2)
    occupied = (mask >> mode) & 1
    sign = -1 if (mask & ((1 << mode) - 1)).bit_count() % 2 else 1
    if kind and occupied:
        sign = -sign
    return mask ^ (1 << mode), sign


def gamma_pair(pair: tuple[int, int], mask: int) -> tuple[int, int]:
    sign = 1
    for index in reversed(pair):
        mask, factor = gamma(index, mask)
        sign *= factor
    return mask, sign


def chevalley_pair(left: int, right: int) -> int:
    if left & right or left | right != FULL:
        return 0
    degree = left.bit_count()
    reversal = -1 if degree * (degree - 1) // 2 % 2 else 1
    inversions = sum(
        (right & ((1 << j) - 1)).bit_count()
        for j in range(N)
        if (left >> j) & 1
    )
    return reversal * (-1 if inversions % 2 else 1)


def flattening(state: dict[int, sp.Expr | int]) -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for pair in PAIRS:
        row = []
        for ket in EVEN:
            out, sign = gamma_pair(pair, ket)
            row.append(
                sp.Add(*(
                    coefficient * sign * chevalley_pair(label, out)
                    for label, coefficient in state.items()
                ))
            )
        rows.append(row)
    return sp.Matrix(rows)


def canonical_pure(q: int, i: int) -> dict[int, int]:
    """e_1...e_q product_j(1+e_(q+2j-1)e_(q+2j))."""
    base = sum(1 << j for j in range(q))
    remaining = list(range(q, N))
    state = {base: 1}
    for j in range(i):
        block = (1 << remaining[2 * j]) | (1 << remaining[2 * j + 1])
        state.update({mask | block: value for mask, value in list(state.items())})
    return state


def normal_form_matrix(q: int, i: int) -> sp.Matrix:
    state: dict[int, sp.Expr | int] = {0: A, FULL: B}
    for mask, coefficient in canonical_pure(q, i).items():
        state[mask] = state.get(mask, 0) + C * coefficient
    return flattening(state)


def connected_components(matrix: sp.Matrix) -> list[tuple[list[int], list[int]]]:
    row_to_cols = [set() for _ in range(matrix.rows)]
    col_to_rows = [set() for _ in range(matrix.cols)]
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            if matrix[row, col] != 0:
                row_to_cols[row].add(col)
                col_to_rows[col].add(row)
    seen_rows: set[int] = set()
    components: list[tuple[list[int], list[int]]] = []
    for starting_row in range(matrix.rows):
        if starting_row in seen_rows or not row_to_cols[starting_row]:
            continue
        rows: set[int] = set()
        cols: set[int] = set()
        stack = [("row", starting_row)]
        while stack:
            kind, index = stack.pop()
            if kind == "row":
                if index in rows:
                    continue
                rows.add(index)
                seen_rows.add(index)
                stack.extend(("col", col) for col in row_to_cols[index])
            else:
                if index in cols:
                    continue
                cols.add(index)
                stack.extend(("row", row) for row in col_to_rows[index])
        components.append((sorted(rows), sorted(cols)))
    return components


def sparse_vector(vector: sp.Matrix) -> dict[str, str]:
    return {
        str(index): sp.sstr(sp.factor(sp.cancel(entry)))
        for index, entry in enumerate(vector)
        if entry != 0
    }


def exact_zero(expression: sp.Expr) -> bool:
    return sp.cancel(expression) == 0


def minor(rows: list[int], cols: list[int], determinant: str) -> dict[str, object]:
    return {"rows": rows, "cols": cols, "determinant": determinant}


# Global row and column indices in PAIRS and EVEN order.  Each determinant is
# recomputed, not trusted, before the certificate is emitted.
HIGH_CERTIFICATES: dict[tuple[int, int], list[dict[str, object]]] = {
    (0, 3): [
        {"component": 0, **minor([119,65,118,55,93,94,0,54,15,105,16,116], [96,7,120,126,127,97,1,24,0,102,121,103], "256*a**3*b**4*c**5")},
        {"component": 1, **minor([32,43,42,18,31,19,44,17,20,5,3,4], [3,2,4,100,5,123,101,125,122,99,98,124], "-1024*a**4*b**4*c**4")},
        {"component": 2, **minor([47,21,34,35,8,49,48,10,46,22,9,36], [110,119,113,9,16,105,17,111,8,118,104,112], "1024*a**4*b**4*c**4")},
        {"component": 3, **minor([25,12,50,11,13,39,51,27,53,41,14,40], [88,56,33,64,32,57,95,71,62,94,63,65], "256*a**4*b**4*c**4")},
        {"component": 4, **minor([70,67,78,86,68,58,60,69,59,57,77,76], [106,114,12,107,18,108,109,115,116,10,20,117], "1024*a**4*b**4*c**4")},
        {"component": 5, **minor([74,90,83,64,80,61,71,91,81,73,89,72], [90,34,59,93,58,61,66,92,60,68,36,91], "-256*a**4*b**4*c**4")},
        {"component": 6, **minor([95,97,104,113,98,102,112,110,109,111,107,96], [54,40,41,81,55,78,47,79,72,80,87,48], "-256*a**4*b**4*c**4")},
    ],
    (2, 2): [
        {"component": 0, **minor([100,114,105,75,16,15,65,115,99,116,66], [126,1,30,121,0,24,120,102,96,6,103], "64*a**3*b**5*c**3")},
        {"component": 1, **minor([44,20,17,31,32,4,6,30,43,45,5,18], [4,125,100,122,123,3,5,99,124,98,101,2], "-256*a**4*b**4*c**4")},
        {"component": 2, **minor([49,8,23,37,21,48,10,35,7,47,9,46], [110,112,16,113,105,8,9,119,104,118,17,111], "-256*a**4*b**4*c**4")},
        {"component": 3, **minor([27,11,52,39,40,12,50,41,38,28,14,25], [95,32,64,56,62,63,65,70,71,57,94,33], "256*a**4*b**4*c**4")},
        {"component": 4, **minor([60,59,87,68,69,79,84,67,76,78,70,58], [20,114,109,10,107,108,116,115,12,106,18,117], "-1024*a**4*b**4*c**4")},
        {"component": 5, **minor([81,72,89,71,63,73,88,83,74,91,90,62], [90,61,91,59,66,58,68,92,93,36,34,60], "-256*a**4*b**4*c**4")},
        {"component": 6, **minor([111,96,103,106,102,109,107,104,112,98,95,113], [86,54,87,79,40,72,46,47,48,80,78,55], "-256*a**4*b**4*c**4")},
    ],
    (2, 3): [
        {"component": 0, **minor([1,114,56,0,54,66,94,100,92,2,117,118], [97,30,0,102,127,126,31,96,103,24,120,6], "-256*a**4*b**3*c**5")},
        {"component": 1, **minor([5,17,20,32,3,33,19,18,45,31,42,30], [29,3,5,124,4,100,125,99,98,2,123,122], "-256*a**4*b**4*c**4")},
        {"component": 2, **minor([8,37,24,47,10,34,9,46,22,49,48,7], [104,22,17,111,119,113,118,8,105,9,110,16], "-256*a**4*b**4*c**4")},
        {"component": 3, **minor([25,27,38,11,50,12,40,52,39,14,13,53], [65,62,70,63,95,94,64,56,33,89,39,32], "256*a**4*b**4*c**4")},
        {"component": 4, **minor([59,68,70,57,79,76,58,86,78,60,69,77], [107,116,10,117,18,115,12,108,20,106,109,114], "-1024*a**4*b**4*c**4")},
        {"component": 5, **minor([61,74,71,91,80,64,73,62,89,81,72,83], [59,93,60,61,58,34,36,92,91,90,68,66], "-1024*a**4*b**4*c**4")},
        {"component": 6, **minor([106,97,110,113,98,104,109,101,108,107,102,112], [47,46,86,55,40,54,80,78,48,87,79,72], "-1024*a**4*b**4*c**4")},
    ],
    (0, 4): [
        {
            "component": 0,
            "alternative_minors": [
                minor([0,119,93,54,55,117,16,15,99,115,56], [24,121,120,7,97,6,0,102,127,1,31], "-128*a**2*b**3*c**5*(a-b)"),
                minor([105,75,66,0,99,117,119,100,16,65,15], [96,24,97,0,1,120,30,121,25,31,103], "64*a**2*b**3*c**5*(a+b)"),
            ],
            "nonvanishing_reason": "For abc!=0, a-b and a+b cannot both vanish over characteristic zero.",
        },
        {"component": 1, **minor([44,4,3,30,17,32,19,5,43,6,45,31], [98,29,27,124,5,100,4,3,122,125,2,123], "-1024*a**4*b**4*c**4")},
        {"component": 2, **minor([34,7,9,48,35,24,49,8,46,21,22,10], [8,15,16,104,22,113,17,111,9,118,110,119], "1024*a**4*b**4*c**4")},
        {"component": 3, **minor([39,53,41,11,12,51,50,28,38,40,25,27], [71,32,63,70,62,94,57,56,65,95,33,64], "-1024*a**4*b**4*c**4")},
        {"component": 4, **minor([76,60,85,84,87,79,67,77,57,58,78,59], [108,21,106,18,114,117,115,107,12,109,20,10], "-1024*a**4*b**4*c**4")},
        {"component": 5, **minor([90,88,91,62,74,73,83,89,63,72,64,61], [60,36,35,66,91,59,34,68,67,93,61,69], "1024*a**4*b**4*c**4")},
        {"component": 6, **minor([110,102,95,113,98,111,107,109,97,101,96,106], [49,41,48,72,79,40,55,78,81,87,47,80], "1024*a**4*b**4*c**4")},
    ],
}


LOW_STRATA = [
    (0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (4, 0),
    (4, 1), (4, 2), (6, 0), (6, 1), (8, 0),
]


def checked_nullspace(matrix: sp.Matrix) -> tuple[list[int], list[dict[str, str]]]:
    basis = matrix.nullspace(simplify=False)
    pivots = matrix.rref(simplify=False)[1]
    free = [column for column in range(matrix.cols) if column not in pivots]
    assert len(basis) == len(free)
    for basis_index, vector in enumerate(basis):
        product = matrix * vector
        assert all(exact_zero(entry) for entry in product)
        for other_index, column in enumerate(free):
            expected = 1 if basis_index == other_index else 0
            assert exact_zero(vector[column] - expected)
    return free, [sparse_vector(vector) for vector in basis]


def verify_minor(matrix: sp.Matrix, item: dict[str, object]) -> None:
    rows = item["rows"]
    cols = item["cols"]
    assert isinstance(rows, list) and isinstance(cols, list) and len(rows) == len(cols)
    observed = sp.factor(matrix.extract(rows, cols).det())
    expected = sp.sympify(item["determinant"], locals={"a": A, "b": B, "c": C})
    assert exact_zero(observed - expected), (observed, expected)


def build_certificate() -> dict[str, object]:
    target_matrix = flattening({0: 1, 15: 1, 240: 1, 255: 1})
    target_free, target_basis = checked_nullspace(target_matrix)
    target_pivot_cols = list(target_matrix.rref()[1])
    target_pivot_rows = list(target_matrix[:, target_pivot_cols].T.rref()[1])
    target_det = target_matrix.extract(target_pivot_rows, target_pivot_cols).det()
    assert len(target_pivot_cols) == 78
    assert len(target_basis) == 50
    assert target_det == 2**71

    low_records = []
    for q, i in LOW_STRATA:
        matrix = normal_form_matrix(q, i)
        free, basis = checked_nullspace(matrix)
        generic_rank = matrix.cols - len(basis)
        assert generic_rank in (57, 74)
        low_records.append({
            "q": q,
            "i": i,
            "field": "QQ(a,b,c)",
            "generic_rank": generic_rank,
            "rank_upper_bound_for_all_complex_specializations": generic_rank,
            "free_columns": free,
            "right_nullspace_basis": basis,
        })

    high_records = []
    for q, i in ((0, 3), (0, 4), (2, 2), (2, 3)):
        matrix = normal_form_matrix(q, i)
        components = connected_components(matrix)
        records = HIGH_CERTIFICATES[(q, i)]
        total = 0
        used_components = set()
        for item in records:
            component_index = item["component"]
            assert component_index not in used_components
            used_components.add(component_index)
            component_rows, component_cols = components[component_index]
            candidates = item.get("alternative_minors", [item])
            sizes = set()
            for candidate in candidates:
                assert set(candidate["rows"]).issubset(component_rows)
                assert set(candidate["cols"]).issubset(component_cols)
                verify_minor(matrix, candidate)
                sizes.add(len(candidate["rows"]))
            assert len(sizes) == 1
            total += sizes.pop()
        expected = 83 if (q, i) in ((0, 4), (2, 2)) else 84
        assert total == expected
        assert used_components == set(range(7))
        high_records.append({
            "q": q,
            "i": i,
            "coefficient_domain": "a,b,c in C*",
            "rank_lower_bound": total,
            "component_minors": records,
        })

    covered = {(record["q"], record["i"]) for record in low_records + high_records}
    expected_strata = {
        (q, i)
        for q in range(0, 9, 2)
        for i in range((8 - q) // 2 + 1)
    }
    assert covered == expected_strata and len(covered) == 15

    return {
        "schema": "clifford-rank-gap-certificate-v1",
        "arithmetic": "Exact ZZ and QQ(a,b,c); no floating point and no finite-field inference",
        "indexing": {
            "rows": "lexicographic 2-subsets of Majorana indices 0,...,15",
            "columns": "ascending even-popcount masks 0,...,255",
        },
        "normal_form": "a*1+b*e_1...e_8+c*e_1...e_q*product_(j=1)^i(1+e_(q+2j-1)e_(q+2j))",
        "target": {
            "unnormalized_support_masks": [0, 15, 240, 255],
            "rank": 78,
            "pivot_rows": target_pivot_rows,
            "pivot_columns": target_pivot_cols,
            "pivot_determinant": str(target_det),
            "free_columns": target_free,
            "right_nullspace_basis": target_basis,
        },
        "low_strata": low_records,
        "high_strata": high_records,
        "exhaustive_stratum_count": 15,
        "rank_gap": "Every low stratum has rank <=74; every high stratum has rank >=83 for abc!=0; target rank is 78.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    payload = json.dumps(certificate, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print("certificate", args.output.as_posix())
    print("sha256", digest)
    print("target_rank", certificate["target"]["rank"])
    print("low_strata", [(x["q"], x["i"], x["generic_rank"]) for x in certificate["low_strata"]])
    print("high_strata", [(x["q"], x["i"], x["rank_lower_bound"]) for x in certificate["high_strata"]])
    print("all_exact_checks", "PASS")


if __name__ == "__main__":
    main()
