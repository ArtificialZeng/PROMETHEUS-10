#!/usr/bin/env python3
"""Input A: exact transcription of source Eq. (3), in row-vectorization."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def encode_matrix(matrix: sp.Matrix) -> list[list[str]]:
    return [[sp.sstr(sp.expand(matrix[r, c])) for c in range(matrix.cols)] for r in range(matrix.rows)]


def main() -> None:
    ii = sp.I
    half = sp.Rational(1, 2)
    gamma = sp.Rational(3, 5)
    delta = sp.Rational(2, 5)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -ii], [ii, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    identity2 = sp.eye(2)
    identity4 = sp.eye(4)
    sigma_plus = (sx + ii * sy) / 2

    hamiltonian = (
        sp.kronecker_product(sx, sx)
        + gamma * sp.kronecker_product(sy, sy)
        + delta * sp.kronecker_product(sz, sz)
    )
    jump = sp.kronecker_product(sigma_plus, identity2)
    jump_dag_jump = jump.conjugate().T * jump

    # Source Eq. (3), using its row-major vec convention from footnote [23].
    coherent = -ii * sp.kronecker_product(hamiltonian, identity4) + ii * sp.kronecker_product(
        identity4, hamiltonian.T
    )
    dissipator = (
        sp.kronecker_product(jump, jump.conjugate())
        - half * sp.kronecker_product(jump_dag_jump, identity4)
        - half * sp.kronecker_product(identity4, jump_dag_jump.T)
    )

    payload = {
        "input_id": "A",
        "method": "Direct exact transcription of primary-source Eq. (3)",
        "source_locator": "main-text Eq. (3) and footnote [23]",
        "parameters": {"gamma": "3/5", "Delta": "2/5", "Gamma_domain": "Gamma>0", "Jx": "1", "hbar": "1"},
        "vectorization": "row-major vec(E_ab) index 4*a+b",
        "basis": [f"E_{a}{b}" for a in range(4) for b in range(4)],
        "formula": "L(Gamma)=coherent_matrix+Gamma*dissipator_matrix",
        "hamiltonian": encode_matrix(hamiltonian),
        "jump": encode_matrix(jump),
        "coherent_matrix": encode_matrix(coherent),
        "dissipator_matrix": encode_matrix(dissipator),
    }
    output = Path("evidence/input-a.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
