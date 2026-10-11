#!/usr/bin/env python3
"""Independent structural/numerical reconstruction of the n=16 witness."""

from __future__ import annotations

import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

import argparse
import json
from pathlib import Path

import numpy as np


N = 16
STEPS = (2, 3, 4, 6)
DELETED_EDGES = ((0, 13), (5, 8))


def structural_edges() -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for vertex in range(N):
        for step in STEPS:
            neighbor = (vertex + step) % N
            edges.add(tuple(sorted((vertex, neighbor))))
    for edge in DELETED_EDGES:
        edges.remove(tuple(sorted(edge)))
    return sorted(edges)


def laplacian(edges: list[tuple[int, int]]) -> np.ndarray:
    result = np.zeros((N, N), dtype=np.float64)
    for u, v in edges:
        result[u, u] += 1.0
        result[v, v] += 1.0
        result[u, v] -= 1.0
        result[v, u] -= 1.0
    return result


def grouped_projectors(
    eigenvalues: np.ndarray, eigenvectors: np.ndarray, relative_tolerance: float
) -> tuple[list[np.ndarray], list[list[int]]]:
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    threshold = relative_tolerance * scale
    groups: list[list[int]] = [[0]]
    for index in range(1, len(eigenvalues)):
        if float(eigenvalues[index] - eigenvalues[index - 1]) > threshold:
            groups.append([])
        groups[-1].append(index)
    projectors = [
        eigenvectors[:, group] @ eigenvectors[:, group].T for group in groups
    ]
    return projectors, groups


def connected_and_degrees(edges: list[tuple[int, int]]) -> tuple[bool, list[int]]:
    adjacency = [[] for _ in range(N)]
    degrees = [0] * N
    for u, v in edges:
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
    edges = structural_edges()
    if len(edges) != 62 or len(set(edges)) != len(edges):
        raise AssertionError("structural edge construction failed")
    L = laplacian(edges)
    if not np.array_equal(L, L.T) or np.max(np.abs(np.sum(L, axis=1))) != 0.0:
        raise AssertionError("invalid structural Laplacian")
    eigenvalues, eigenvectors = np.linalg.eigh(L)
    strict_projectors, strict_groups = grouped_projectors(eigenvalues, eigenvectors, 2.0e-10)
    loose_projectors, loose_groups = grouped_projectors(eigenvalues, eigenvectors, 2.0e-8)

    def trace_from(projectors: list[np.ndarray]) -> float:
        return float(sum(np.dot(np.diag(projector), np.diag(projector)) for projector in projectors))

    strict_tau = trace_from(strict_projectors)
    loose_tau = trace_from(loose_projectors)
    residual = float(np.max(np.abs(L @ eigenvectors - eigenvectors * eigenvalues)))
    orthogonality = float(np.max(np.abs(eigenvectors.T @ eigenvectors - np.eye(N))))
    completeness = float(np.max(np.abs(sum(strict_projectors) - np.eye(N))))
    projector_idempotence = max(
        float(np.max(np.abs(projector @ projector - projector))) for projector in strict_projectors
    )
    projector_orthogonality = max(
        [
            float(np.max(np.abs(strict_projectors[i] @ strict_projectors[j])))
            for i in range(len(strict_projectors))
            for j in range(i)
        ]
        or [0.0]
    )
    connected, degrees = connected_and_degrees(edges)
    output = {
        "construction": {
            "deleted_edges_zero_based": [list(edge) for edge in DELETED_EDGES],
            "description": "C_16({+/-2,+/-3,+/-4,+/-6}) with the antipodal step-3 edges {0,13} and {5,8} deleted",
            "steps_mod_16": list(STEPS),
        },
        "edges_zero_based": [list(edge) for edge in edges],
        "graph_checks": {
            "connected": connected,
            "degree_sequence": sorted(degrees, reverse=True),
            "edge_count": len(edges),
            "simple_undirected_unweighted_loopless": True,
        },
        "laplacian": L.astype(int).tolist(),
        "method": "NumPy symmetric eigendecomposition grouped into full eigenspace projectors, independently from the literal exact input",
        "n": N,
        "numerical_checks": {
            "eigensolver_residual_max_abs": residual,
            "loose_group_count": len(loose_groups),
            "orthogonality_max_abs": orthogonality,
            "projector_completeness_max_abs": completeness,
            "projector_idempotence_max_abs": projector_idempotence,
            "projector_orthogonality_max_abs": projector_orthogonality,
            "strict_group_count": len(strict_groups),
        },
        "path_tau_float": 23.0 / 16.0,
        "tau_loose": loose_tau,
        "tau_strict": strict_tau,
    }
    Path(args.output).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.log).write_text(
        "\n".join(
            [
                "COUNTEREXAMPLE METHOD A: STRUCTURAL FULL-EIGENSPACE SCREEN",
                f"n={N} edges={len(edges)} connected={connected} degree_sequence={sorted(degrees, reverse=True)}",
                f"strict_groups={len(strict_groups)} loose_groups={len(loose_groups)}",
                f"tau_strict={strict_tau:.17g} tau_loose={loose_tau:.17g} path_tau={23.0/16.0:.17g}",
                f"residual={residual:.17g} orthogonality={orthogonality:.17g} completeness={completeness:.17g}",
                "Scope: numerical candidate generation only; the sign is not certified by this method.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"edges": len(edges), "groups": len(strict_groups), "tau": strict_tau}, sort_keys=True))


if __name__ == "__main__":
    main()
