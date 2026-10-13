#!/usr/bin/env python3
"""Input B: derive the generator by applying the master equation to all E_ab."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def encode_matrix(matrix: sp.Matrix) -> list[list[str]]:
    return [[sp.sstr(sp.expand(matrix[r, c])) for c in range(matrix.cols)] for r in range(matrix.rows)]


def main() -> None:
    # This implementation never constructs or imports the Eq. (3) Kronecker superoperator.
    imaginary = sp.I
    gamma = sp.Rational(3, 5)
    delta = sp.Rational(2, 5)
    pauli_x = sp.Matrix(((0, 1), (1, 0)))
    pauli_y = sp.Matrix(((0, -imaginary), (imaginary, 0)))
    pauli_z = sp.diag(1, -1)
    one_qubit_identity = sp.eye(2)
    raising = sp.Matrix(((0, 1), (0, 0)))

    h = (
        sp.kronecker_product(pauli_x, pauli_x)
        + gamma * sp.kronecker_product(pauli_y, pauli_y)
        + delta * sp.kronecker_product(pauli_z, pauli_z)
    )
    ell = sp.kronecker_product(raising, one_qubit_identity)
    ell_dag = ell.conjugate().T
    number = ell_dag * ell

    coherent = sp.zeros(16)
    dissipator = sp.zeros(16)
    for a in range(4):
        for b in range(4):
            unit = sp.zeros(4)
            unit[a, b] = 1
            image_h = -imaginary * (h * unit - unit * h)
            image_d = ell * unit * ell_dag - (number * unit + unit * number) / 2
            column = 4 * a + b
            # Directly read each output coefficient in the independently enumerated E_cd basis.
            for c in range(4):
                for d in range(4):
                    row = 4 * c + d
                    coherent[row, column] = sp.expand(image_h[c, d])
                    dissipator[row, column] = sp.expand(image_d[c, d])

    payload = {
        "input_id": "B",
        "method": "Master-equation action independently evaluated on all sixteen matrix units",
        "source_locator": "main-text Eqs. (1)-(2)",
        "parameters": {"gamma": "3/5", "Delta": "2/5", "Gamma_domain": "Gamma>0", "Jx": "1", "hbar": "1"},
        "vectorization": "coefficient of E_cd in L(E_ab) is row 4*c+d, column 4*a+b",
        "basis": [f"E_{a}{b}" for a in range(4) for b in range(4)],
        "formula": "L(Gamma)=coherent_matrix+Gamma*dissipator_matrix",
        "hamiltonian": encode_matrix(h),
        "jump": encode_matrix(ell),
        "coherent_matrix": encode_matrix(coherent),
        "dissipator_matrix": encode_matrix(dissipator),
    }
    output = Path("evidence/input-b.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
