"""Independent finite-field Schrödinger replay of a sampled 11-qubit circuit.

Each Pauli rotation is synthesized into H/S/CX, one T or T-dagger, then
H/S/CX. The final stabilizer readout is implemented by an explicit inverse
Clifford. All 2048 terminal outcomes are retained. No postselection occurs.
"""

import argparse
import json
from pathlib import Path

import numpy as np


P = 1009
SQRT2 = next(x for x in range(P) if x * x % P == 2)
INVROOT2 = pow(SQRT2, -1, P)
IROOT = next(x for x in range(P) if x * x % P == P - 1)


def inverse_gate(gate):
    kind, i, j = gate
    if kind in ("h", "cx"):
        return gate
    if kind == "s":
        return ("sdg", i, j)
    if kind == "sdg":
        return ("s", i, j)
    raise ValueError(gate)


def rotation_gates(label, direction, N):
    x, z = label
    support = [i for i in range(N) if ((x | z) >> i) & 1]
    assert support
    pivot = support[0]
    C = [("cx", i, pivot) for i in support[1:]]
    L = []
    for i in support:
        xi, zi = (x >> i) & 1, (z >> i) & 1
        if xi:
            L.append(("h", i, -1))
            if zi:
                L.append(("s", i, -1))
    D = C + L  # Chronological D = (local L) (parity C).
    return ([inverse_gate(g) for g in reversed(D)] +
            [("t" if direction == 1 else "tdg", pivot, -1)] + D)


def explicit_gates(instance, N):
    gates = []
    for label, direction in instance["rotation_axes_xz_and_direction"]:
        gates.extend(rotation_gates(label, direction, N))
    gates.extend(inverse_gate(tuple(g)) for g in reversed(
        instance["measurement_clifford_ops"]))
    return gates


def state_matrix(gates, n, m, iroot):
    N = n + m
    dim = 1 << N
    data_dim = 1 << n
    A = np.zeros((dim, data_dim), dtype=np.int64)
    for a in range(data_dim):
        A[a << m, a] = 1
    indices = np.arange(dim, dtype=np.int64)
    for kind, i, j in gates:
        bit = 1 << (N - 1 - i)
        if kind == "h":
            lo = indices[(indices & bit) == 0]
            hi = lo | bit
            old_lo = A[lo].copy()
            old_hi = A[hi].copy()
            A[lo] = (old_lo + old_hi) * INVROOT2 % P
            A[hi] = (old_lo - old_hi) * INVROOT2 % P
        elif kind == "cx":
            control = bit
            target = 1 << (N - 1 - j)
            flip = ((indices & control) != 0) * target
            A = A[indices ^ flip]
        else:
            selected = (indices & bit) != 0
            if kind == "s":
                factor = iroot
            elif kind == "sdg":
                factor = -iroot
            elif kind == "t":
                factor = (1 + iroot) * INVROOT2
            elif kind == "tdg":
                factor = (1 - iroot) * INVROOT2
            else:
                raise ValueError(kind)
            A[selected] = A[selected] * (factor % P) % P
    return A


def modular_rank(matrix):
    pivots = {}
    pivot_rows = []
    pivot_cols = []
    for row_index, original in enumerate(matrix):
        row = original.copy()
        while True:
            nonzero = np.flatnonzero(row)
            if len(nonzero) == 0:
                break
            col = int(nonzero[0])
            if col in pivots:
                row = (row - int(row[col]) * pivots[col]) % P
            else:
                pivots[col] = row * pow(int(row[col]), -1, P) % P
                pivot_rows.append(row_index)
                pivot_cols.append(col)
                break
    return len(pivots), pivot_rows, pivot_cols


def modular_determinant(square):
    A = square.copy()
    r = len(A)
    determinant = 1
    for j in range(r):
        nz = np.flatnonzero(A[j:, j])
        if len(nz) == 0:
            return 0
        k = j + int(nz[0])
        if k != j:
            A[[j, k]] = A[[k, j]]
            determinant = -determinant
        pivot = int(A[j, j])
        determinant = determinant * pivot % P
        if j + 1 < r:
            factors = A[j + 1:, j] * pow(pivot, -1, P) % P
            A[j + 1:, j:] = (A[j + 1:, j:] -
                              factors[:, None] * A[j, j:]) % P
    return determinant % P


def replay(instance, n=4, m=7):
    N = n + m
    gates = explicit_gates(instance, N)
    assert sum(g[0] in ("t", "tdg") for g in gates) == len(
        instance["rotation_axes_xz_and_direction"])
    A = state_matrix(gates, n, m, IROOT)
    Abar = state_matrix(gates, n, m, -IROOT % P)
    gram = Abar.T @ A % P
    assert np.array_equal(gram, np.eye(1 << n, dtype=np.int64)), gram
    # The b-th row is vec(E_b) = vec(A_b^dagger A_b). Evaluating i at
    # IROOT and conjugate i at -IROOT preserves all algebraic identities.
    effects = (Abar[:, :, None] * A[:, None, :]).reshape(1 << N, -1) % P
    assert np.array_equal(effects.sum(axis=0).reshape(1 << n, 1 << n) % P,
                          np.eye(1 << n, dtype=np.int64))
    rank, pivot_rows, pivot_cols = modular_rank(effects)
    minor = effects[np.ix_(pivot_rows, pivot_cols)]
    minor_det = modular_determinant(minor)
    assert minor_det != 0
    return {
        "field": "F_1009, sqrt(2)=%d, i=%d" % (SQRT2, IROOT),
        "rank_mod_1009": rank,
        "gate_count": len(gates),
        "t_count": sum(g[0] in ("t", "tdg") for g in gates),
        "outcomes": len(effects),
        "data_dimension": 1 << n,
        "ancilla_dimension": 1 << m,
        "isometry_gram_identity": True,
        "povm_sum_identity": True,
        "pivot_outcome_rows": pivot_rows,
        "pivot_matrix_columns": pivot_cols,
        "pivot_minor_determinant_mod_1009": minor_det,
        "circuit_chronological_gates": gates,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    record = json.loads(args.input.read_text())
    instance = record.get("best_instances", [record])[args.index]
    result = replay(instance)
    result["source_instance_file"] = str(args.input)
    result["source_instance_index"] = args.index
    result["heisenberg_rank_mod_1009"] = instance["rank_mod_1009"]
    assert result["rank_mod_1009"] == result["heisenberg_rank_mod_1009"]
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "rank_mod_1009", "gate_count", "t_count", "outcomes",
        "isometry_gram_identity", "povm_sum_identity")}, indent=2))


if __name__ == "__main__":
    main()
