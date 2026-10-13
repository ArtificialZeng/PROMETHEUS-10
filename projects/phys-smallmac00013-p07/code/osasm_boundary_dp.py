#!/usr/bin/env python3
"""Exact definition-only transfer calculation for even OSASM boundary data.

The state is the vector of partial column sums in the unprocessed rows.  It is
independent of the BFK Pfaffian representation.  Polynomial coefficients are
stored as integer Counters keyed by R.
"""

from __future__ import annotations

import argparse
import functools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


Polynomial = Counter[int]


def add_shifted(target: Polynomial, source: Polynomial, shift: int) -> None:
    for degree, coefficient in source.items():
        target[degree + shift] += coefficient


def fixed_boundary_polynomial(order: int, top_one: int) -> tuple[Polynomial, dict[str, int]]:
    """Return sum r^R over OSASM(order) with one-based T=top_one.

    Only even order is used here, so the diagonal is forced to zero.  The first
    row is installed explicitly; every later row is generated from binary row
    partial sums and mirrored column partial sums.
    """
    if order < 2 or order % 2:
        raise ValueError("this transfer calculation requires positive even order")
    if not 2 <= top_one <= order:
        raise ValueError("top_one must lie in 2..order")

    # After fixing row zero, the only nonzero upper-triangular entry is the 1
    # in column top_one (one-based).
    initial = [0] * (order - 1)
    initial[top_one - 2] = 1
    transition_count = 0

    @functools.lru_cache(maxsize=None)
    def finish(row: int, state: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
        nonlocal transition_count
        if len(state) != order - row:
            raise AssertionError("state length mismatch")
        if any(value not in (0, 1) for value in state):
            raise AssertionError("non-binary incoming partial sum")
        if row == order - 1:
            return ((0, 1),) if state[0] == 1 else ()

        before = state[0]
        future = state[1:]
        result: Polynomial = Counter()
        # q_j denotes the row partial sum after column j.  q_row=before,
        # q_{order-1}=1; enumerate only the still-free intermediate states.
        middle_count = order - row - 2
        for mask in range(1 << middle_count):
            q = [before]
            q.extend((mask >> bit) & 1 for bit in range(middle_count))
            q.append(1)
            next_state: list[int] = []
            delta_r = 0
            viable = True
            for offset, old in enumerate(future, start=1):
                entry = q[offset] - q[offset - 1]
                updated = old + entry
                if updated not in (0, 1):
                    viable = False
                    break
                next_state.append(updated)
                delta_r += abs(entry)
            if not viable:
                continue
            transition_count += 1
            child = Counter(dict(finish(row + 1, tuple(next_state))))
            add_shifted(result, child, delta_r)
        return tuple(sorted(result.items()))

    tail = Counter(dict(finish(1, tuple(initial))))
    polynomial: Polynomial = Counter()
    add_shifted(polynomial, tail, 1)
    stats = {
        "cached_states": finish.cache_info().currsize,
        "cache_hits": finish.cache_info().hits,
        "transitions": transition_count,
    }
    return polynomial, stats


def unrefined_polynomial(order: int) -> tuple[Polynomial, dict[str, int]]:
    result: Polynomial = Counter()
    aggregate = {"cached_states": 0, "cache_hits": 0, "transitions": 0}
    for top_one in range(2, order + 1):
        poly, stats = fixed_boundary_polynomial(order, top_one)
        add_shifted(result, poly, 0)
        for key in aggregate:
            aggregate[key] += stats[key]
    return result, aggregate


def encode(poly: Polynomial) -> dict[str, object]:
    return {
        "coefficients": [
            {"R": degree, "count": coefficient}
            for degree, coefficient in sorted(poly.items())
            if coefficient
        ],
        "total_at_r_1": sum(poly.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--top-one", type=int, default=3)
    parser.add_argument("--rhs-order", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    lhs, lhs_stats = fixed_boundary_polynomial(args.order, args.top_one)
    rhs_order = args.rhs_order if args.rhs_order is not None else args.order - 2
    unrefined, rhs_stats = unrefined_polynomial(rhs_order)
    n = args.order // 2
    predicted: Polynomial = Counter()
    add_shifted(predicted, unrefined, 1)
    add_shifted(predicted, unrefined, 3)
    if n - 2 != 1:
        for degree in list(predicted):
            # Undo the unit coefficient just added at shift 3 and replace it
            # by (n-2).  This keeps the construction manifestly integral.
            base = unrefined.get(degree - 3, 0)
            predicted[degree] += (n - 3) * base
    difference = lhs.copy()
    for degree, coefficient in predicted.items():
        difference[degree] -= coefficient
    difference = Counter({degree: coefficient for degree, coefficient in difference.items() if coefficient})

    payload = {
        "route": "A_definition_only_binary_partial_sum_transfer",
        "arithmetic": "exact Python integers",
        "matrix_order": args.order,
        "n_in_target": n,
        "top_one": args.top_one,
        "rhs_matrix_order": rhs_order,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lhs_t_coefficient": encode(lhs),
        "rhs_unrefined": encode(unrefined),
        "predicted_rhs": encode(predicted),
        "difference": encode(difference),
        "difference_is_zero": not difference,
        "state_statistics": {"lhs": lhs_stats, "rhs": rhs_stats},
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"order={args.order} T={args.top_one} lhs_total={sum(lhs.values())} "
        f"rhs_total={sum(predicted.values())} D_zero={not difference}",
        flush=True,
    )


if __name__ == "__main__":
    main()
