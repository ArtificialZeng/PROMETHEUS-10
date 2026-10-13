#!/usr/bin/env python3
"""Direct, exact enumeration of OSASMs from row/column partial sums.

This route does not use the BFK Pfaffian.  Symmetry means that validating every
row also validates every column, so the backtrack fills one upper-triangular
row at a time and mirrors it immediately.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def enumerate_osasm(order: int) -> Counter[tuple[int, int]]:
    if order < 1:
        raise ValueError("order must be positive")

    matrix = [[0] * order for _ in range(order)]
    # Sum of the already fixed prefix in each not-yet-processed row.
    prefix_sum = [0] * order
    wanted_nonzero_diagonal = order & 1
    counts: Counter[tuple[int, int]] = Counter()

    def visit(row: int, nonzero_diagonal: int, upper_nonzeros: int, top_one: int) -> None:
        if row == order:
            if nonzero_diagonal == wanted_nonzero_diagonal:
                counts[(upper_nonzeros, top_one)] += 1
            return

        before = prefix_sum[row]
        if before not in (0, 1):
            return

        # q_c is the row partial sum after column c.  Each q_c is binary and
        # q_{order-1}=1.  For even OSASMs the diagonal transition is fixed to 0.
        if order % 2 == 0:
            diagonal_states = (before,)
        else:
            diagonal_states = (0, 1)

        middle_length = max(0, order - row - 2)
        for diagonal_state in diagonal_states:
            if row == order - 1 and diagonal_state != 1:
                continue
            diagonal_entry = diagonal_state - before
            new_nonzero_diagonal = nonzero_diagonal + (diagonal_entry != 0)
            if new_nonzero_diagonal > wanted_nonzero_diagonal:
                continue

            for middle in itertools.product((0, 1), repeat=middle_length):
                states = ((diagonal_state,) if row == order - 1 else
                          (diagonal_state,) + middle + (1,))
                previous = before
                upper_entries: list[int] = []
                for offset, state in enumerate(states):
                    column = row + offset
                    entry = state - previous
                    previous = state
                    matrix[row][column] = entry
                    matrix[column][row] = entry
                    if column > row:
                        upper_entries.append(entry)

                affected: list[int] = []
                viable = True
                for offset, entry in enumerate(upper_entries, start=1):
                    future_row = row + offset
                    prefix_sum[future_row] += entry
                    affected.append(future_row)
                    if prefix_sum[future_row] not in (0, 1):
                        viable = False

                if viable:
                    next_top = top_one
                    if row == 0:
                        ones = [j + 1 for j, value in enumerate(matrix[0]) if value == 1]
                        # A completed first row of an ASM has exactly one 1.
                        if len(ones) != 1:
                            viable = False
                        else:
                            next_top = ones[0]
                    if viable:
                        visit(
                            row + 1,
                            new_nonzero_diagonal,
                            upper_nonzeros + sum(abs(x) for x in upper_entries),
                            next_top,
                        )

                for future_row in affected:
                    prefix_sum[future_row] -= matrix[future_row][row]

    visit(0, 0, 0, 0)
    return counts


def encode_counts(counts: Counter[tuple[int, int]]) -> dict[str, object]:
    terms = [
        {"R": rho, "T": tau, "count": count}
        for (rho, tau), count in sorted(counts.items())
    ]
    return {"terms": terms, "total": sum(counts.values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    results: dict[str, object] = {}
    for order in range(1, args.max_order + 1):
        results[str(order)] = encode_counts(enumerate_osasm(order))
        print(f"enumeration order={order} total={results[str(order)]['total']}", flush=True)

    payload = {
        "route": "A_direct_upper_triangle_backtracking",
        "definition": "symmetric ASM; zero diagonal for even order, exactly one nonzero diagonal for odd order",
        "statistics": {"R": "sum_{i<j}|A_ij|", "T": "one-based column of first-row 1"},
        "arithmetic": "exact integer counts",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "orders": results,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
