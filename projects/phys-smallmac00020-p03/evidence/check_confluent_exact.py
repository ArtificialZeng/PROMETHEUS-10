#!/usr/bin/env python3
"""Exact-rational implementation checks for the confluent derivation."""

from fractions import Fraction as F


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def matvec(T, x):
    return [dot(row, x) for row in T]


def check_case(N, r):
    z = -r
    T = [[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        T[i][i] = r * r
        if i + 1 < N:
            T[i][i + 1] = 2 * r
        if i + 2 < N:
            T[i][i + 2] = 1
    u = [z**i for i in range(N)]
    w = [F(0) if i == 0 else i * z ** (i - 1) for i in range(N)]
    Ru, Rw = list(reversed(u)), list(reversed(w))
    Tu, Tw = matvec(T, u), matvec(T, w)
    q = r * r
    A = sum((q**i for i in range(N)), F(0))
    B = sum((i * q**i for i in range(N)), F(0))
    D = sum((i * i * q**i for i in range(N)), F(0))
    gram_ok = [[dot(u, u), dot(u, w)], [dot(w, u), dot(w, w)]] == [
        [A, -B / r], [-B / r, D / (r * r)]
    ]
    cross_ok = [[dot(Tu, Ru), dot(Tu, Rw)], [dot(Tw, Ru), dot(Tw, Rw)]] == [
        [F(0), -(z**N)], [-(z**N), -N * z ** (N - 1)]
    ]

    # Closed nilpotent inverse, followed by the reversal/sign equivalence.
    inv = [[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for k in range(i, N):
            d = k - i
            inv[i][k] = (-1) ** d * (d + 1) * r ** (-d - 2)
    transformed = [[F(0) for _ in range(N)] for _ in range(N)]
    target = [[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for ell in range(N):
            transformed[i][ell] = (
                (-1) ** (N - 1 + i + ell) * r ** (N + 1) * inv[i][N - 1 - ell]
            )
            if i + ell <= N - 1:
                target[i][ell] = (N - i - ell) * r ** (i + ell)
    inverse_ok = transformed == target

    Fmat = [[(N - i - ell) * r ** (i + ell) for ell in range(N)] for i in range(N)]
    tail_sq = sum(
        ((target[i][ell] - Fmat[i][ell]) ** 2 for i in range(N) for ell in range(N)),
        F(0),
    )
    tail_formula = sum(
        ((N - 1 - t) * t * t * q ** (N + t) for t in range(1, N - 1)), F(0)
    )
    return gram_ok, cross_ok, inverse_ok, tail_sq == tail_formula


def main():
    cases = 0
    failures = []
    for N in range(3, 11):
        for r in (F(1, 5), F(1, 3), F(1, 2), F(3, 4), F(4, 5)):
            cases += 1
            checks = check_case(N, r)
            if not all(checks):
                failures.append((N, str(r), checks))
    print(f"exact_rational_cases={cases}")
    print(f"failure_count={len(failures)}")
    print(f"failures={failures}")
    print("checks=finite_Gram,cross_Hamiltonian,rescaled_inverse_equivalence,tail_Frobenius_sum")


if __name__ == "__main__":
    main()
