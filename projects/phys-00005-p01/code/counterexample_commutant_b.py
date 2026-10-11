#!/usr/bin/env python3
"""Independent literal-edge exact commutant certificate for the n=16 witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


N = 16
# Independently transcribed literal edge list.  This routine does not construct
# a circulant or read the output of method A.
EDGES = (
    (0, 2), (0, 3), (0, 4), (0, 6), (0, 10), (0, 12), (0, 14),
    (1, 3), (1, 4), (1, 5), (1, 7), (1, 11), (1, 13), (1, 14), (1, 15),
    (2, 4), (2, 5), (2, 6), (2, 8), (2, 12), (2, 14), (2, 15),
    (3, 5), (3, 6), (3, 7), (3, 9), (3, 13), (3, 15),
    (4, 6), (4, 7), (4, 8), (4, 10), (4, 14),
    (5, 7), (5, 9), (5, 11), (5, 15),
    (6, 8), (6, 9), (6, 10), (6, 12),
    (7, 9), (7, 10), (7, 11), (7, 13),
    (8, 10), (8, 11), (8, 12), (8, 14),
    (9, 11), (9, 12), (9, 13), (9, 15),
    (10, 12), (10, 13), (10, 14),
    (11, 13), (11, 14), (11, 15),
    (12, 14), (12, 15),
    (13, 15),
)


def laplacian() -> sp.Matrix:
    if len(EDGES) != len(set(EDGES)) or any(not (0 <= u < v < N) for u, v in EDGES):
        raise AssertionError("literal edge list is not a simple graph")
    result = sp.zeros(N)
    for u, v in EDGES:
        result[u, u] += 1
        result[v, v] += 1
        result[u, v] -= 1
        result[v, u] -= 1
    return result


def col_vec(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[row, column] for column in range(N) for row in range(N)])


def connected_and_degrees() -> tuple[bool, list[int]]:
    adjacency = [[] for _ in range(N)]
    degrees = [0] * N
    for u, v in EDGES:
        adjacency[u].append(v)
        adjacency[v].append(u)
        degrees[u] += 1
        degrees[v] += 1
    seen = {0}
    stack = [0]
    while stack:
        for vertex in adjacency[stack.pop()]:
            if vertex not in seen:
                seen.add(vertex)
                stack.append(vertex)
    return len(seen) == N, degrees


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()
    L = laplacian()
    if L != L.T or L * sp.ones(N, 1) != sp.zeros(N, 1):
        raise AssertionError("literal Laplacian failed exact guards")
    characteristic = sp.Poly(L.charpoly().as_expr())
    if sp.gcd(characteristic, characteristic.diff()).degree() != 0:
        raise AssertionError("witness Laplacian spectrum is not simple")

    powers = [sp.eye(N)]
    for _ in range(1, N):
        powers.append(powers[-1] * L)
    B = sp.Matrix.hstack(*(col_vec(power) for power in powers))
    C = sp.kronecker_product(sp.eye(N), L) - sp.kronecker_product(L.T, sp.eye(N))
    if C * B != sp.zeros(N * N, N):
        raise AssertionError("power basis does not lie in the commutant kernel")
    gram = B.T * B
    gram_inverse = gram.inv()
    if gram * gram_inverse != sp.eye(N):
        raise AssertionError("exact Gram inverse failed")
    diagonal_rows = [vertex + N * vertex for vertex in range(N)]
    restricted = B[diagonal_rows, :]
    restricted_projector = (restricted * gram_inverse * restricted.T).applyfunc(sp.cancel)
    if restricted_projector != restricted_projector.T:
        raise AssertionError("restricted rational projector is not symmetric")
    tau = sp.cancel(sp.trace(restricted_projector))
    path_tau = sp.Rational(23, 16)
    delta = sp.cancel(tau - path_tau)
    if not delta < 0:
        raise AssertionError("literal exact calculation did not certify a deficit")
    connected, degrees = connected_and_degrees()
    if not connected:
        raise AssertionError("witness unexpectedly disconnected")
    output = {
        "characteristic_polynomial_factorization": sp.sstr(sp.factor(characteristic.as_expr())),
        "checks": {
            "C_times_B_exact_zero": "pass",
            "Gram_inverse_exact": "pass",
            "characteristic_polynomial_square_free": "pass",
            "connected": "pass",
            "integer_symmetric_L_zero_row_sum": "pass",
            "power_basis_dimension_equals_commutant_dimension": "pass",
            "restricted_projector_symmetric": "pass",
            "simple_undirected_unweighted_loopless": "pass",
        },
        "commutant_dimension": N,
        "degree_sequence": sorted(degrees, reverse=True),
        "delta_exact": str(delta),
        "edges_zero_based": [list(edge) for edge in EDGES],
        "laplacian": [list(map(int, L.row(index))) for index in range(N)],
        "method": "Exact rational Frobenius projection Q=B(B^T B)^(-1)B^T with B=vec(I,L,...,L^15); square-free characteristic polynomial proves this is the full commutant",
        "n": N,
        "path_tau_exact": str(path_tau),
        "tau_exact": str(tau),
        "uniform_return_deficit_exact": str(sp.cancel(delta / N)),
    }
    Path(args.output).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.log).write_text(
        "\n".join(
            [
                "COUNTEREXAMPLE METHOD B: LITERAL EXACT RATIONAL COMMUTANT",
                f"n={N} edges={len(EDGES)} connected={connected} degree_sequence={sorted(degrees, reverse=True)}",
                f"characteristic_polynomial={output['characteristic_polynomial_factorization']}",
                f"commutant_dimension={N} tau={tau} path_tau={path_tau} delta={delta}",
                f"uniform_return_deficit={sp.cancel(delta/N)}",
                "PASS: exact negative rational trace difference for the stated simple unweighted graph.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"delta": str(delta), "edges": len(EDGES), "tau": str(tau)}, sort_keys=True))


if __name__ == "__main__":
    main()
