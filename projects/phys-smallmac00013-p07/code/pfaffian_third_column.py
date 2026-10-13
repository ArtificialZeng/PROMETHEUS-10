#!/usr/bin/env python3
"""Exact low-t extraction from BFK Eq. (8.11), without full X(r,t).

This is independent of the definition-only OSASM transfer code.  Polynomials
in r are tuples of Python integers, and the Pfaffians use a subset recurrence.
"""

from __future__ import annotations

import argparse
import functools
import json
from datetime import datetime, timezone
from pathlib import Path


Poly = tuple[int, ...]
ZERO: Poly = ()
ONE: Poly = (1,)


def trim(poly: list[int] | tuple[int, ...]) -> Poly:
    values = list(poly)
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    values = [0] * max(len(left), len(right))
    for degree, coefficient in enumerate(left):
        values[degree] += coefficient
    for degree, coefficient in enumerate(right):
        values[degree] += scale * coefficient
    return trim(values)


def shift(poly: Poly, degree: int, scale: int = 1) -> Poly:
    if not poly or scale == 0:
        return ZERO
    return (0,) * degree + tuple(scale * coefficient for coefficient in poly)


def multiply(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return ZERO
    values = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            values[i + j] += a * b
    return trim(values)


class KernelCoefficients:
    """Coefficients of the skew kernel in BFK Eq. (8.10)."""

    def __init__(self, max_index: int):
        self.h: dict[tuple[int, int], Poly] = {}
        for i in range(max_index + 1):
            for j in range(max_index + 1):
                if i == 0 and j == 0:
                    value = ONE
                else:
                    value = add(shift(self.get_h(i - 1, j), 1), shift(self.get_h(i, j - 1), 1))
                    # -(r^2-1)h = h-r^2 h.
                    diagonal = self.get_h(i - 1, j - 1)
                    value = add(value, diagonal)
                    value = add(value, shift(diagonal, 2), scale=-1)
                self.h[(i, j)] = value

        self.g: dict[tuple[int, int], Poly] = {}
        for i in range(max_index + 1):
            for j in range(max_index + 1):
                value = ZERO
                for k in range(min(i, j) + 1):
                    value = add(value, self.get_h(i - k, j - k))
                self.g[(i, j)] = value

    def get_h(self, i: int, j: int) -> Poly:
        return self.h.get((i, j), ZERO) if i >= 0 and j >= 0 else ZERO

    def get_g(self, i: int, j: int) -> Poly:
        return self.g.get((i, j), ZERO) if i >= 0 and j >= 0 else ZERO

    def a(self, i: int, j: int) -> Poly:
        # [u^i v^j] (v-u)(1+u)(1+v) G(u,v).
        value = add(self.get_g(i, j - 1), self.get_g(i - 1, j), scale=-1)
        value = add(value, self.get_g(i, j - 2))
        value = add(value, self.get_g(i - 2, j), scale=-1)
        value = add(value, self.get_g(i - 1, j - 2))
        value = add(value, self.get_g(i - 2, j - 1), scale=-1)
        return value


def pfaffian(indices: tuple[int, ...], kernel: KernelCoefficients) -> tuple[Poly, int]:
    calls = 0

    @functools.lru_cache(maxsize=None)
    def rec(active: tuple[int, ...]) -> Poly:
        nonlocal calls
        calls += 1
        if not active:
            return ONE
        first = active[0]
        total = ZERO
        for position in range(1, len(active)):
            partner = active[position]
            remainder = active[1:position] + active[position + 1 :]
            term = multiply(kernel.a(first, partner), rec(remainder))
            total = add(total, term, scale=1 if position % 2 else -1)
        return total

    return rec(indices), calls


def encode(poly: Poly) -> dict[str, object]:
    return {
        "coefficients": [
            {"R": degree, "count": coefficient}
            for degree, coefficient in enumerate(poly)
            if coefficient
        ],
        "total_at_r_1": sum(poly),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    order = args.order
    if order < 4 or order % 2:
        raise ValueError("target order must be even and at least four")
    n = order // 2

    kernel = KernelCoefficients(order)
    # C0 is the Eq. (8.10) Pfaffian for matrix order order-2.  C1 replaces
    # its final index order-3 by order-2.
    c0, calls0 = pfaffian(tuple(range(order - 2)), kernel)
    c1, calls1 = pfaffian(tuple(range(order - 3)) + (order - 2,), kernel)

    # Laurent extraction from the last column of Eq. (8.11): for i>=1,
    # [t^(-i-1)]b_i=(-1)^(i+1)r^(-i-2), and
    # [t^(-i)]b_i=(-1)^i(i+r+r^2)r^(-i-2).
    # Only i=order-2 and i=order-3 can reach [t^3].
    factor0 = add(add(ONE, shift(ONE, 1), scale=-1), shift(ONE, 2), scale=-1)
    lhs = shift(add(multiply(factor0, c0), shift(c1, 1)), n)
    rhs_factor = add(ONE, shift(ONE, 2, n - 2))
    rhs = shift(multiply(rhs_factor, c0), n)
    difference = add(lhs, rhs, scale=-1)
    minor_expected = multiply(add(ONE, shift(ONE, 1, n - 1)), c0)
    minor_difference = add(c1, minor_expected, scale=-1)
    unrefined_order_minus_two = shift(c0, n - 1)

    payload = {
        "route": "B_BFK_8_10_8_11_low_t_manual_integer_polynomials",
        "arithmetic": "exact Python-integer coefficient arrays",
        "matrix_order": order,
        "n_in_target": n,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "low_t_derivation": {
            "contributing_last_column_indices": [order - 3, order - 2],
            "laurent_coefficients": "for i>=1: [t^(-i-1)]b_i=(-1)^(i+1)r^(-i-2); [t^(-i)]b_i=(-1)^i(i+r+r^2)r^(-i-2)",
            "formula": "[t^3]X_order=r^n((1-r-r^2)C0+r*C1)",
        },
        "c0": encode(c0),
        "c1": encode(c1),
        "unrefined_order_minus_two": encode(unrefined_order_minus_two),
        "lhs_t3": encode(lhs),
        "predicted_rhs": encode(rhs),
        "difference": encode(difference),
        "difference_is_zero": not difference,
        "minor_relation": {
            "statement": "C1=(1+(n-1)r)C0 at the tested order",
            "difference": encode(minor_difference),
            "difference_is_zero": not minor_difference,
        },
        "pfaffian_subproblems": {"c0": calls0, "c1": calls1},
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"order={order} D_zero={not difference} minor_zero={not minor_difference} "
        f"pfaffian_subproblems={calls0}+{calls1}",
        flush=True,
    )


if __name__ == "__main__":
    main()
