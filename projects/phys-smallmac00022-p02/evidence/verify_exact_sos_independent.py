#!/usr/bin/env python3
"""Independent, certificate-only exact replay of the I3 SOS identity.

This checker deliberately does not import the reconstruction script, the NPA
baseline, or its word algebra.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ZERO = Fraction(0), Fraction(0)
ONE = Fraction(1), Fraction(0)
OMEGA = Fraction(0), Fraction(1)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def scale(x, value):
    value = Fraction(value)
    return value * x[0], value * x[1]


def conj(x):
    a, b = x
    return a - b, -b


def power(x, exponent):
    exponent %= 3 if x == OMEGA else 10**18
    out, base = ONE, x
    while exponent:
        if exponent & 1:
            out = mul(out, base)
        base = mul(base, base)
        exponent //= 2
    return out


def reduce_seq(seq):
    stack = []
    for setting, exponent in seq:
        exponent %= 3
        if not exponent:
            continue
        if stack and stack[-1][0] == setting:
            setting0, previous = stack.pop()
            combined = (previous + exponent) % 3
            if combined:
                stack.append((setting0, combined))
        else:
            stack.append((setting, exponent))
    return tuple(stack)


def product(u, v):
    return reduce_seq(u[0] + v[0]), reduce_seq(u[1] + v[1])


def adjoint(word):
    return (
        reduce_seq(tuple((x, -k) for x, k in reversed(word[0]))),
        reduce_seq(tuple((y, -k) for y, k in reversed(word[1]))),
    )


def words_1ab():
    words = [((), ())]
    words += [(((x, k),), ()) for x in range(2) for k in (1, 2)]
    words += [((), ((y, k),)) for y in range(3) for k in (1, 2)]
    words += [(((x, k),), ((y, ell),)) for x in range(2) for k in (1, 2) for y in range(3) for ell in (1, 2)]
    assert len(words) == 35 and len(set(words)) == 35
    return words


def word_text(word):
    if word == ((), ()):
        return "1"
    return " ".join(
        [f"A{x}^{k}" for x, k in word[0]] + [f"B{y}^{k}" for y, k in word[1]]
    )


def parse_matrix(raw):
    return [[(Fraction(x[0]), Fraction(x[1])) for x in row] for row in raw]


def coefficient_map(y, words):
    result = {}
    for i, wi in enumerate(words):
        for j, wj in enumerate(words):
            key = product(adjoint(wi), wj)
            result[key] = add(result.get(key, ZERO), conj(y[i][j]))
    return {key: value for key, value in result.items() if value != ZERO}


def target_map():
    result = {((), ()): (Fraction(4), Fraction(0))}
    for x in range(2):
        for y in range(3):
            alpha = ONE if x == 0 else power(OMEGA, y)
            key = (((x, 1),), ((y, 1),))
            key_star = adjoint(key)
            result[key] = add(result.get(key, ZERO), scale(alpha, Fraction(-1, 2)))
            result[key_star] = add(result.get(key_star, ZERO), scale(conj(alpha), Fraction(-1, 2)))
    return result


def exact_ldl(y):
    a = [[x for x in row] for row in y]
    n, pivots = len(a), []
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][i][0] > 0 and a[i][i][1] == 0), None)
        if pivot is None:
            assert all(a[i][i] == ZERO for i in range(k, n))
            assert all(a[i][j] == ZERO for i in range(k, n) for j in range(k, n))
            return pivots, n - k
        assert all(a[i][i][1] == 0 and a[i][i][0] >= 0 for i in range(k, n))
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            for row in a:
                row[k], row[pivot] = row[pivot], row[k]
        d = a[k][k][0]
        pivots.append(d)
        ell = [scale(a[i][k], Fraction(1, 1) / d) for i in range(k + 1, n)]
        for ii, i in enumerate(range(k + 1, n)):
            for jj, j in enumerate(range(k + 1, n)):
                a[i][j] = sub(a[i][j], scale(mul(ell[ii], conj(ell[jj])), d))
        for i in range(k + 1, n):
            a[i][k] = a[k][i] = ZERO
    return pivots, 0


def main():
    raw = json.loads((HERE / "exact-sos-certificate.json").read_text(encoding="utf-8"))
    words = words_1ab()
    assert raw["word_order"] == [word_text(word) for word in words]
    y = parse_matrix(raw["gram_matrix"])
    assert all(y[j][i] == conj(y[i][j]) for i in range(35) for j in range(35))
    trace = sum((y[i][i][0] for i in range(35)), Fraction(0))
    assert trace == 4 and all(y[i][i][1] == 0 for i in range(35))
    actual, expected = coefficient_map(y, words), target_map()
    assert actual == expected
    pivots, zero_dimension = exact_ldl(y)
    assert len(pivots) == 16 and zero_dimension == 19 and all(x > 0 for x in pivots)

    omega = np.exp(2j * np.pi / 3)
    numeric = np.array([[float(a) + float(b) * omega for a, b in row] for row in y])
    eigenvalues = np.linalg.eigvalsh(numeric)
    positive = eigenvalues[eigenvalues > 1e-9]
    lines = [
        "Independent certificate-only replay (no reconstruction/NPA imports)",
        "word_count=35",
        "hermitian_exact=True trace_exact=4",
        "coefficient_identity_exact=True mismatches=0",
        f"ldl_positive_pivots={len(pivots)} zero_remainder_dimension={zero_dimension}",
        f"numeric_crosscheck_positive_rank={len(positive)} smallest_positive_eigenvalue={positive[0]:.12g}",
        "relations_used=order-three reduction within each setting plus Alice/Bob commutation",
        "status=pass",
    ]
    (HERE / "exact-sos-independent.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
