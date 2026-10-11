#!/usr/bin/env python3
"""Independent reconstruction B: Eq. (53) as a Liouville map.

The linear action is derived directly from Eq. (53) of arXiv:2305.16803v4.
Column vectorization is fixed as vec_F(rho)=(rho00,rho10,rho01,rho11).
For two cells, an explicit perfect-shuffle permutation maps the global matrix
vectorization to the tensor product of the two local Liouville spaces.  This
module has no Kraus matrices and does not read method A's output.
"""

from __future__ import annotations

import json

import numpy as np


COMPLEX = np.complex128


def liouville_one(gamma: float, eta: float) -> np.ndarray:
    """S such that vec_F(Phi(rho)) = S vec_F(rho)."""
    coherence = np.sqrt(1.0 - gamma)
    return np.array(
        [
            [1.0 - gamma * eta, 0.0, 0.0, gamma * (1.0 - eta)],
            [0.0, coherence, 0.0, 0.0],
            [0.0, 0.0, coherence, 0.0],
            [gamma * eta, 0.0, 0.0, 1.0 - gamma * (1.0 - eta)],
        ],
        dtype=COMPLEX,
    )


def apply_one(rho: np.ndarray, gamma: float, eta: float) -> np.ndarray:
    vector = np.asarray(rho, dtype=COMPLEX).reshape(4, order="F")
    return (liouville_one(gamma, eta) @ vector).reshape((2, 2), order="F")


def global_to_local_liouville_permutation() -> np.ndarray:
    """P with v_local=P v_global for two qubits.

    global index: (i1 i2) + 4 (j1 j2), with binary composite indices;
    local index:  (i1+2*j1)*4 + (i2+2*j2).
    """
    permutation = np.zeros((16, 16), dtype=COMPLEX)
    for i1 in range(2):
        for i2 in range(2):
            for j1 in range(2):
                for j2 in range(2):
                    ket = 2 * i1 + i2
                    bra = 2 * j1 + j2
                    global_index = ket + 4 * bra
                    local_left = i1 + 2 * j1
                    local_right = i2 + 2 * j2
                    local_index = 4 * local_left + local_right
                    permutation[local_index, global_index] = 1.0
    return permutation


def liouville_two_permuted(gamma: float, eta: float) -> np.ndarray:
    local = liouville_one(gamma, eta)
    permutation = global_to_local_liouville_permutation()
    return permutation.conj().T @ np.kron(local, local) @ permutation


def liouville_two_by_matrix_units(gamma: float, eta: float) -> np.ndarray:
    """Independently assemble the global superoperator column by column."""
    result = np.zeros((16, 16), dtype=COMPLEX)
    local_basis_outputs: dict[tuple[int, int], np.ndarray] = {}
    for i in range(2):
        for j in range(2):
            matrix_unit = np.zeros((2, 2), dtype=COMPLEX)
            matrix_unit[i, j] = 1.0
            local_basis_outputs[(i, j)] = apply_one(
                matrix_unit, gamma, eta
            )
    for i1 in range(2):
        for i2 in range(2):
            for j1 in range(2):
                for j2 in range(2):
                    ket = 2 * i1 + i2
                    bra = 2 * j1 + j2
                    column = ket + 4 * bra
                    output = np.kron(
                        local_basis_outputs[(i1, j1)],
                        local_basis_outputs[(i2, j2)],
                    )
                    result[:, column] = output.reshape(16, order="F")
    return result


def apply_two(rho: np.ndarray, gamma: float, eta: float) -> np.ndarray:
    vector = np.asarray(rho, dtype=COMPLEX).reshape(16, order="F")
    output = liouville_two_by_matrix_units(gamma, eta) @ vector
    return output.reshape((4, 4), order="F")


def permutation_identity_residual(gamma: float, eta: float) -> float:
    explicit = liouville_two_by_matrix_units(gamma, eta)
    permuted = liouville_two_permuted(gamma, eta)
    return float(np.max(np.abs(explicit - permuted)))


def _complex_matrix_payload(matrix: np.ndarray) -> dict[str, list[list[float]]]:
    return {
        "real": np.real(matrix).tolist(),
        "imag": np.imag(matrix).tolist(),
    }


def diagnostic_report() -> dict[str, object]:
    gamma, eta = 0.37, 0.21
    matrix = liouville_one(gamma, eta)
    return {
        "method": "B_Eq53_column_vectorized_Liouville",
        "vec_convention": ["rho00", "rho10", "rho01", "rho11"],
        "two_use_global_basis": ["|00>", "|01>", "|10>", "|11>"],
        "parameters": {"gamma": gamma, "eta": eta},
        "liouville_matrix": _complex_matrix_payload(matrix),
        "two_use_permutation_identity_residual": permutation_identity_residual(
            gamma, eta
        ),
    }


if __name__ == "__main__":
    print(json.dumps(diagnostic_report(), indent=2, sort_keys=True))
