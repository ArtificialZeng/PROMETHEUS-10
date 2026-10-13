#!/usr/bin/env python3
"""Exact independent implementation of BFK v2 Eqs. (8.10) and (8.11)."""

from __future__ import annotations

import argparse
import functools
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp

r, t = sp.symbols("r t")


def pfaffian(entries: list[list[sp.Expr]]) -> sp.Expr:
    size = len(entries)
    if size % 2:
        raise ValueError("Pfaffian dimension must be even")

    @functools.lru_cache(maxsize=None)
    def rec(indices: tuple[int, ...]) -> sp.Expr:
        if not indices:
            return sp.Integer(1)
        first = indices[0]
        total = sp.Integer(0)
        for position in range(1, len(indices)):
            partner = indices[position]
            remainder = indices[1:position] + indices[position + 1 :]
            total += (-1) ** (position + 1) * entries[first][partner] * rec(remainder)
        return sp.expand(total)

    return rec(tuple(range(size)))


class BFKSeries:
    def __init__(self, max_index: int):
        # H=1/(1-r*u-r*v+(r**2-1)*u*v), derived coefficientwise.
        self.h: dict[tuple[int, int], sp.Expr] = {}
        for i in range(max_index + 1):
            for j in range(max_index + 1):
                if i == 0 and j == 0:
                    value = sp.Integer(1)
                else:
                    value = r * self.get_h(i - 1, j) + r * self.get_h(i, j - 1)
                    value -= (r**2 - 1) * self.get_h(i - 1, j - 1)
                self.h[(i, j)] = sp.expand(value)

        # G=H/(1-u*v).
        self.g: dict[tuple[int, int], sp.Expr] = {}
        for i in range(max_index + 1):
            for j in range(max_index + 1):
                self.g[(i, j)] = sp.expand(
                    sum(self.get_h(i - k, j - k) for k in range(min(i, j) + 1))
                )

    def get_h(self, i: int, j: int) -> sp.Expr:
        return self.h.get((i, j), sp.Integer(0)) if i >= 0 and j >= 0 else sp.Integer(0)

    def get_g(self, i: int, j: int) -> sp.Expr:
        return self.g.get((i, j), sp.Integer(0)) if i >= 0 and j >= 0 else sp.Integer(0)

    def a(self, i: int, j: int) -> sp.Expr:
        # Multiply G by (v-u)(1+u)(1+v)
        value = self.get_g(i, j - 1) - self.get_g(i - 1, j)
        value += self.get_g(i, j - 2) - self.get_g(i - 2, j)
        value += self.get_g(i - 1, j - 2) - self.get_g(i - 2, j - 1)
        return sp.expand(value)


def pf_for_indices(indices: list[int], entry) -> sp.Expr:
    size = len(indices)
    matrix = [[sp.Integer(0) for _ in range(size)] for _ in range(size)]
    for p in range(size):
        for q in range(p + 1, size):
            value = entry(indices[p], indices[q])
            matrix[p][q] = value
            matrix[q][p] = -value
    return pfaffian(matrix)


def x_at_one(order: int, series: BFKSeries) -> sp.Expr:
    if order == 0:
        return sp.Integer(1)
    start = order & 1
    indices = list(range(start, order))
    return sp.expand(r ** (order // 2) * pf_for_indices(indices, series.a))


def last_column(i: int) -> sp.Expr:
    # [u^i] of the last-column rational function in BFK Eq. (8.11),
    # expanded from its two geometric-series factors.
    numerator = (t - 1, t - 1 - r * t, -r * t)
    total = sp.Integer(0)
    for degree, coefficient in enumerate(numerator):
        remaining = i - degree
        if remaining < 0:
            continue
        inner = sp.Integer(0)
        for a in range(remaining + 1):
            b = remaining - a
            inner += (t - 1) ** a * (t - 1 + r**2) ** b / (r ** (a + b) * t**a)
        total += coefficient * inner / (r**2 * t)
    return sp.cancel(total)


def x_refined(order: int, series: BFKSeries) -> sp.Expr:
    if order == 1:
        return t
    start = order & 1
    indices = list(range(start, order))

    def entry(i: int, j: int) -> sp.Expr:
        if j == order - 1:
            return last_column(i)
        return series.a(i, j)

    pf = pf_for_indices(indices, entry)
    numerator = r ** ((3 * order) // 2) * t ** (order + 1) * pf
    if order & 1:
        correction = t * sum(
            (r * t) ** i * (1 - t) ** (order - i - 1) for i in range(order)
        ) * x_at_one(order - 1, series)
        numerator += correction
    quotient = sp.cancel(numerator / (t - 1) ** (order - 1))
    num, den = sp.fraction(quotient)
    if sp.expand(den) != 1:
        raise ArithmeticError(f"Eq. (8.11) did not divide exactly at order {order}: {den}")
    return sp.expand(num)


def encode_polynomial(poly: sp.Expr) -> dict[str, object]:
    p = sp.Poly(sp.expand(poly), r, t)
    terms = [
        {"R": int(rho), "T": int(tau), "count": int(coefficient)}
        for (rho, tau), coefficient in sorted(p.terms(), key=lambda item: item[0])
    ]
    # Normalize to the same ascending key order as route A.
    terms.sort(key=lambda item: (item["R"], item["T"]))
    return {"terms": terms, "total": int(poly.subs({r: 1, t: 1}))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    series = BFKSeries(args.max_order)
    results: dict[str, object] = {}
    unrefined: dict[str, str] = {"0": "1"}
    for order in range(1, args.max_order + 1):
        x1 = x_at_one(order, series)
        xt = x_refined(order, series)
        if sp.expand(xt.subs(t, 1) - x1) != 0:
            raise AssertionError(f"refined/unrefined mismatch at order {order}")
        results[str(order)] = encode_polynomial(xt)
        unrefined[str(order)] = str(x1)
        print(f"pfaffian order={order} total={results[str(order)]['total']}", flush=True)

    payload = {
        "route": "B_BFK_v2_equations_8_10_and_8_11",
        "coefficient_basis": "ascending monomials r^R t^T with exact integer coefficients",
        "coefficient_extraction": "formal bivariate recurrence plus exact symbolic Pfaffian",
        "arithmetic": "SymPy exact rational/polynomial arithmetic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "orders": results,
        "unrefined_X_order_r_1": unrefined,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
