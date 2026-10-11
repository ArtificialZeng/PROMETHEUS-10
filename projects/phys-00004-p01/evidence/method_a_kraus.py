#!/usr/bin/env python3
"""Independent reconstruction A: direct GADC Kraus sums.

The one-cell Kraus matrices are transcribed from the immutable ``source.md``.
The two-cell channel is evaluated from all sixteen products in the ordered
computational basis |00>, |01>, |10>, |11>.  This module contains no
Liouville-superoperator implementation and does not read method B's output.
"""

from __future__ import annotations

import json
from typing import Iterable

import numpy as np


COMPLEX = np.complex128


def kraus_operators(gamma: float, eta: float) -> tuple[np.ndarray, ...]:
    """Return K0,...,K3 in the |0>,|1> energy basis."""
    q = 1.0 - gamma
    return (
        np.sqrt(1.0 - eta)
        * np.array([[1.0, 0.0], [0.0, np.sqrt(q)]], dtype=COMPLEX),
        np.sqrt((1.0 - eta) * gamma)
        * np.array([[0.0, 1.0], [0.0, 0.0]], dtype=COMPLEX),
        np.sqrt(eta)
        * np.array([[np.sqrt(q), 0.0], [0.0, 1.0]], dtype=COMPLEX),
        np.sqrt(eta * gamma)
        * np.array([[0.0, 0.0], [1.0, 0.0]], dtype=COMPLEX),
    )


def apply_one(rho: np.ndarray, gamma: float, eta: float) -> np.ndarray:
    out = np.zeros((2, 2), dtype=COMPLEX)
    for operator in kraus_operators(gamma, eta):
        out += operator @ rho @ operator.conj().T
    return out


def product_kraus(gamma: float, eta: float) -> Iterable[np.ndarray]:
    local = kraus_operators(gamma, eta)
    for left in local:
        for right in local:
            yield np.kron(left, right)


def apply_two(rho: np.ndarray, gamma: float, eta: float) -> np.ndarray:
    out = np.zeros((4, 4), dtype=COMPLEX)
    for operator in product_kraus(gamma, eta):
        out += operator @ rho @ operator.conj().T
    return out


def completeness_residual(gamma: float, eta: float, uses: int = 1) -> float:
    dimension = 2**uses
    total = np.zeros((dimension, dimension), dtype=COMPLEX)
    operators = (
        kraus_operators(gamma, eta) if uses == 1 else product_kraus(gamma, eta)
    )
    for operator in operators:
        total += operator.conj().T @ operator
    return float(np.max(np.abs(total - np.eye(dimension))))


def ergotropy(state: np.ndarray, energies: np.ndarray) -> float:
    """Ergotropy using descending state spectrum and ascending energies."""
    hermitian = 0.5 * (state + state.conj().T)
    eigenvalues = np.linalg.eigvalsh(hermitian)[::-1]
    passive_energy = float(np.dot(eigenvalues, np.sort(energies)))
    mean_energy = float(np.real(np.trace(hermitian @ np.diag(energies))))
    return mean_energy - passive_energy


def _complex_matrix_payload(matrix: np.ndarray) -> dict[str, list[list[float]]]:
    return {
        "real": np.real(matrix).tolist(),
        "imag": np.imag(matrix).tolist(),
    }


def diagnostic_report() -> dict[str, object]:
    gamma, eta = 0.37, 0.21
    vector = np.array(
        [np.sqrt(0.61), np.exp(0.73j) * np.sqrt(0.39)], dtype=COMPLEX
    )
    rho = np.outer(vector, vector.conj())
    return {
        "method": "A_direct_four_Kraus_and_sixteen_product_Kraus",
        "basis": ["|0>", "|1>"],
        "two_use_basis": ["|00>", "|01>", "|10>", "|11>"],
        "parameters": {"gamma": gamma, "eta": eta},
        "one_use_completeness_residual": completeness_residual(gamma, eta, 1),
        "two_use_completeness_residual": completeness_residual(gamma, eta, 2),
        "sample_input": _complex_matrix_payload(rho),
        "sample_output": _complex_matrix_payload(apply_one(rho, gamma, eta)),
    }


if __name__ == "__main__":
    print(json.dumps(diagnostic_report(), indent=2, sort_keys=True))
