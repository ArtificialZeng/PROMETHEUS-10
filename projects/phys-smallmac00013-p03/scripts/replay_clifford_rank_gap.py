#!/usr/bin/env python3
"""Independent exterior-algebra replay of the Clifford rank-gap certificate."""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


DIM = 8
TOP = (1 << DIM) - 1
EVEN_MASKS = [m for m in range(1 << DIM) if m.bit_count() % 2 == 0]
ROW_PAIRS = list(combinations(range(2 * DIM), 2))
a, b, c = sp.symbols("a b c")


def wedge_generator(j: int, mask: int) -> tuple[int, int] | None:
    if mask & (1 << j):
        return None
    sign = -1 if (mask & ((1 << j) - 1)).bit_count() % 2 else 1
    return mask | (1 << j), sign


def contraction(j: int, mask: int) -> tuple[int, int] | None:
    if not mask & (1 << j):
        return None
    sign = -1 if (mask & ((1 << j) - 1)).bit_count() % 2 else 1
    return mask ^ (1 << j), sign


def clifford(index: int, mask: int) -> tuple[int, int]:
    """Apply epsilon_j+iota_j or epsilon_j-iota_j in a split basis."""
    j, branch = divmod(index, 2)
    term = contraction(j, mask) if mask & (1 << j) else wedge_generator(j, mask)
    assert term is not None
    out, coefficient = term
    if branch == 1 and mask & (1 << j):
        coefficient = -coefficient
    return out, coefficient


def apply_two(first: int, second: int, mask: int) -> tuple[int, int]:
    intermediate, coefficient_2 = clifford(second, mask)
    final, coefficient_1 = clifford(first, intermediate)
    return final, coefficient_1 * coefficient_2


def top_wedge_after_reversal(left: int, right: int) -> int:
    left_tuple = [j for j in range(DIM) if left & (1 << j)]
    right_tuple = [j for j in range(DIM) if right & (1 << j)]
    word = list(reversed(left_tuple)) + right_tuple
    if len(word) != DIM or len(set(word)) != DIM:
        return 0
    inversions = sum(word[p] > word[q] for p in range(DIM) for q in range(p + 1, DIM))
    return -1 if inversions % 2 else 1


def make_matrix(state: dict[int, sp.Expr | int]) -> sp.Matrix:
    data = []
    for first, second in ROW_PAIRS:
        row = []
        for ket in EVEN_MASKS:
            out, coefficient = apply_two(first, second, ket)
            value = sum(
                amplitude * coefficient * top_wedge_after_reversal(label, out)
                for label, amplitude in state.items()
            )
            row.append(value)
        data.append(row)
    return sp.Matrix(data)


def third_pure_spinor(q: int, i: int) -> dict[int, int]:
    state = {sum(1 << j for j in range(q)): 1}
    for pair_index in range(i):
        j = q + 2 * pair_index
        pair_mask = (1 << j) | (1 << (j + 1))
        additions = {mask | pair_mask: coefficient for mask, coefficient in state.items()}
        state.update(additions)
    return state


def stratum_matrix(q: int, i: int) -> sp.Matrix:
    state: dict[int, sp.Expr | int] = {0: a, TOP: b}
    for mask, coefficient in third_pure_spinor(q, i).items():
        state[mask] = state.get(mask, 0) + c * coefficient
    return make_matrix(state)


def support_components(matrix: sp.Matrix) -> list[tuple[set[int], set[int]]]:
    """Connected components of the bipartite nonzero support graph."""
    row_neighbors = [set() for _ in range(matrix.rows)]
    col_neighbors = [set() for _ in range(matrix.cols)]
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            if matrix[row, col] != 0:
                row_neighbors[row].add(col)
                col_neighbors[col].add(row)
    components = []
    visited_rows = set()
    for start in range(matrix.rows):
        if start in visited_rows or not row_neighbors[start]:
            continue
        rows, cols = set(), set()
        frontier = [(0, start)]
        while frontier:
            side, index = frontier.pop()
            if side == 0:
                if index in rows:
                    continue
                rows.add(index)
                visited_rows.add(index)
                frontier.extend((1, col) for col in row_neighbors[index])
            else:
                if index in cols:
                    continue
                cols.add(index)
                frontier.extend((0, row) for row in col_neighbors[index])
        components.append((rows, cols))
    return components


def expression(text: str) -> sp.Expr:
    return sp.sympify(text, locals={"a": a, "b": b, "c": c})


def zero(value: sp.Expr) -> bool:
    return sp.cancel(value) == 0


def vector_from_sparse(record: dict[str, str]) -> dict[int, sp.Expr]:
    return {int(index): expression(value) for index, value in record.items()}


def verify_nullspace(matrix: sp.Matrix, record: dict[str, object]) -> int:
    basis = [vector_from_sparse(v) for v in record["right_nullspace_basis"]]
    free = record["free_columns"]
    assert len(basis) == len(free)
    for basis_index, vector in enumerate(basis):
        for row in range(matrix.rows):
            dot = sum(matrix[row, col] * value for col, value in vector.items())
            assert zero(dot)
        for other_index, column in enumerate(free):
            expected = 1 if basis_index == other_index else 0
            assert zero(vector.get(column, 0) - expected)
    return len(basis)


def verify_minor(matrix: sp.Matrix, record: dict[str, object]) -> None:
    observed = sp.factor(matrix.extract(record["rows"], record["cols"]).det())
    assert zero(observed - expression(record["determinant"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    certificate = json.loads(raw)
    assert certificate["schema"] == "clifford-rank-gap-certificate-v1"

    target = make_matrix({0: 1, 15: 1, 240: 1, 255: 1})
    target_record = certificate["target"]
    verify_minor(target, {
        "rows": target_record["pivot_rows"],
        "cols": target_record["pivot_columns"],
        "determinant": target_record["pivot_determinant"],
    })
    target_nullity = verify_nullspace(target, target_record)
    assert len(target_record["pivot_columns"]) == 78
    assert target_nullity == 50
    assert target.rank() == 78

    low_summary = []
    for record in certificate["low_strata"]:
        q, i = record["q"], record["i"]
        matrix = stratum_matrix(q, i)
        nullity = verify_nullspace(matrix, record)
        upper_bound = matrix.cols - nullity
        assert upper_bound == record["rank_upper_bound_for_all_complex_specializations"]
        assert upper_bound <= 74
        low_summary.append((q, i, upper_bound))

    high_summary = []
    for record in certificate["high_strata"]:
        q, i = record["q"], record["i"]
        matrix = stratum_matrix(q, i)
        components = support_components(matrix)
        assert len(components) == 7
        component_total = 0
        used_components = set()
        for component in record["component_minors"]:
            component_index = component["component"]
            assert component_index not in used_components
            used_components.add(component_index)
            support_rows, support_cols = components[component_index]
            candidates = component.get("alternative_minors", [component])
            for candidate in candidates:
                assert set(candidate["rows"]).issubset(support_rows)
                assert set(candidate["cols"]).issubset(support_cols)
                verify_minor(matrix, candidate)
            sizes = {len(candidate["rows"]) for candidate in candidates}
            assert len(sizes) == 1
            component_total += sizes.pop()
        assert used_components == set(range(7))
        assert component_total == record["rank_lower_bound"] and component_total >= 83
        high_summary.append((q, i, component_total))

    special = next(x for x in certificate["high_strata"] if (x["q"], x["i"]) == (0, 4))
    alternatives = special["component_minors"][0]["alternative_minors"]
    assert expression(alternatives[0]["determinant"]) == -128*a**2*b**3*c**5*(a-b)
    assert expression(alternatives[1]["determinant"]) == 64*a**2*b**3*c**5*(a+b)

    covered = {(q, i) for q, i, _ in low_summary + high_summary}
    expected = {(q, i) for q in range(0, 9, 2) for i in range((8-q)//2 + 1)}
    assert covered == expected and len(covered) == 15

    print("certificate_sha256", hashlib.sha256(raw).hexdigest())
    print("independent_construction", "wedge/contraction and top-wedge reversal")
    print("target_pivot_determinant", target_record["pivot_determinant"])
    print("target_right_nullity", target_nullity)
    print("target_rank_exact", 78)
    print("low_upper_bounds", low_summary)
    print("high_lower_bounds", high_summary)
    print("exhaustive_strata", len(covered))
    print("independent_replay", "PASS")


if __name__ == "__main__":
    main()
