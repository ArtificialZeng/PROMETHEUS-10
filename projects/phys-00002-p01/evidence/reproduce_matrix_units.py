#!/usr/bin/env python3
"""Direct Appendix-A reconstruction in the matrix-unit basis.

This implementation transcribes H and the rank-one jump directly and applies
Eq. (3) to each matrix unit.  It does not use the Bloch implementation or any
matrix produced by it.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import expm


SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def jump(alpha: float, beta: float, gamma: float) -> np.ndarray:
    """A=sqrt(gamma)|psi_o(alpha)><psi_i(beta)|, source Appendix A."""
    psi_o = np.array([math.cos(alpha), 1j * math.sin(alpha)], dtype=complex)
    psi_i = np.array([math.cos(beta), 1j * math.sin(beta)], dtype=complex)
    return math.sqrt(gamma) * np.outer(psi_o, psi_i.conj())


def action(rho: np.ndarray, alpha: float, beta: float, gamma: float) -> np.ndarray:
    h = SIGMA_X
    a = jump(alpha, beta, gamma)
    adag_a = a.conj().T @ a
    return -1j * (h @ rho - rho @ h) + a @ rho @ a.conj().T - 0.5 * (
        adag_a @ rho + rho @ adag_a
    )


def liouvillian(alpha: float, beta: float, gamma: float) -> np.ndarray:
    """Column-vectorized L in order (E00,E10,E01,E11)."""
    columns = []
    for j in range(2):
        for i in range(2):
            eij = np.zeros((2, 2), dtype=complex)
            eij[i, j] = 1.0
            columns.append(action(eij, alpha, beta, gamma).reshape(4, order="F"))
    return np.column_stack(columns)


def transition(alpha: float, beta: float, gamma: float, time: float) -> tuple[float, float]:
    channel = expm(time * liouvillian(alpha, beta, gamma))
    return float(channel[0, 0].real), float(channel[3, 3].real)


def transition_mp(
    alpha: float, beta: float, gamma: float, time: float, dps: int = 70
) -> tuple[mp.mpf, mp.mpf]:
    """High-precision replay, independently evaluating Eq. (3) on E_ij."""
    with mp.workdps(dps):
        al, be, ga, tt = map(mp.mpf, map(str, (alpha, beta, gamma, time)))
        h = mp.matrix([[0, 1], [1, 0]])
        po = mp.matrix([[mp.cos(al)], [1j * mp.sin(al)]])
        pi = mp.matrix([[mp.cos(be)], [1j * mp.sin(be)]])
        a = mp.sqrt(ga) * po * pi.transpose_conj()
        q = a.transpose_conj() * a

        def act(rho: mp.matrix) -> mp.matrix:
            return -1j * (h * rho - rho * h) + a * rho * a.transpose_conj() - (
                q * rho + rho * q
            ) / 2

        lm = mp.matrix(4, 4)
        col = 0
        for j in range(2):
            for i in range(2):
                eij = mp.matrix(2, 2)
                eij[i, j] = 1
                out = act(eij)
                lm[:, col] = mp.matrix([out[0, 0], out[1, 0], out[0, 1], out[1, 1]])
                col += 1
        channel = mp.expm(tt * lm)
        return +mp.re(channel[0, 0]), +mp.re(channel[3, 3])


def carray(x: np.ndarray) -> list:
    return [[[float(z.real), float(z.imag)] for z in row] for row in x]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    alpha, beta, gamma, time = 0.2, 1.0, 0.7, 0.9
    amat = jump(alpha, beta, gamma)
    lmat = liouvillian(alpha, beta, gamma)
    channel = expm(time * lmat)
    aval, bval = transition(alpha, beta, gamma, time)
    amp, bmp = transition_mp(alpha, beta, gamma, time)

    trace_residual = 0.0
    hermiticity_residual = 0.0
    for j in range(2):
        for i in range(2):
            eij = np.zeros((2, 2), dtype=complex)
            eij[i, j] = 1.0
            trace_residual = max(trace_residual, abs(np.trace(action(eij, alpha, beta, gamma))))
            partner = np.zeros((2, 2), dtype=complex)
            partner[j, i] = 1.0
            hermiticity_residual = max(
                hermiticity_residual,
                float(np.max(np.abs(action(eij, alpha, beta, gamma).conj().T - action(partner, alpha, beta, gamma)))),
            )

    unitary = []
    unitary_error = 0.0
    for t in [0.0, 0.1, math.pi / 4, 0.9, math.pi / 2, math.pi]:
        ua, ub = transition(0.2, 1.0, 0.0, t)
        expected = math.cos(t) ** 2
        err = max(abs(ua - expected), abs(ub - expected))
        unitary_error = max(unitary_error, err)
        unitary.append({"t": t, "a": ua, "b": ub, "cos2": expected, "max_abs_error": err})

    data = {
        "representation": "direct matrix-unit action of Eq. (3)",
        "source_transcription": {
            "H": [[[0.0, 0.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 0.0]]],
            "psi": "(cos(theta), i sin(theta))^T",
            "jump": "sqrt(gamma)|psi_o(alpha)><psi_i(beta)|",
            "vectorization": "column-major (E00,E10,E01,E11)",
        },
        "test_point": {"alpha": alpha, "beta": beta, "gamma": gamma, "t": time},
        "A": carray(amat),
        "L": carray(lmat),
        "channel": carray(channel),
        "transition": {"a": aval, "b": bval},
        "high_precision_transition_70dps": {"a": mp.nstr(amp, 60), "b": mp.nstr(bmp, 60)},
        "double_vs_70dps_max_abs": max(abs(aval - float(amp)), abs(bval - float(bmp))),
        "checks": {
            "trace_preservation_generator_max_abs": float(trace_residual),
            "hermiticity_preservation_max_abs": hermiticity_residual,
            "column_probability_sum_max_abs": float(
                max(abs(channel[0, 0].real + channel[3, 0].real - 1.0), abs(channel[0, 3].real + channel[3, 3].real - 1.0))
            ),
            "unitary_limit_max_abs": unitary_error,
        },
        "unitary_limit": unitary,
        "software": {"numpy": np.__version__, "scipy": scipy.__version__, "mpmath": mp.__version__},
    }
    Path(args.json).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "input": args.json,
        "transition": data["transition"],
        "double_vs_70dps_max_abs": data["double_vs_70dps_max_abs"],
        "checks": data["checks"],
    }, indent=2))


if __name__ == "__main__":
    main()
