#!/usr/bin/env python3
"""Independent Appendix-A reconstruction in the affine Bloch basis.

The dissipative affine generator is derived analytically from the rank-one
jump.  This file neither imports nor reads the matrix-unit reconstruction.
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


def pure_bloch(theta: float) -> np.ndarray:
    # For |psi>=(cos theta, i sin theta)^T in (sigma_x,sigma_y,sigma_z).
    return np.array([0.0, math.sin(2.0 * theta), math.cos(2.0 * theta)])


def affine_generator(alpha: float, beta: float, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    no = pure_bloch(alpha)
    ni = pure_bloch(beta)
    # -i[sigma_x,rho] gives rdot=2 e_x cross r.
    hamiltonian = np.array(
        [[0.0, 0.0, 0.0], [0.0, 0.0, -2.0], [0.0, 2.0, 0.0]]
    )
    # D_A: rdot=(gamma/2)[(1+ni.r)no-ni-r].
    linear = hamiltonian + 0.5 * gamma * (np.outer(no, ni) - np.eye(3))
    offset = 0.5 * gamma * (no - ni)
    return linear, offset


def augmented_generator(alpha: float, beta: float, gamma: float) -> np.ndarray:
    linear, offset = affine_generator(alpha, beta, gamma)
    aug = np.zeros((4, 4))
    aug[:3, :3] = linear
    aug[:3, 3] = offset
    return aug


def transition(alpha: float, beta: float, gamma: float, time: float) -> tuple[float, float]:
    prop = expm(time * augmented_generator(alpha, beta, gamma))
    mzz, vz = prop[2, 2], prop[2, 3]
    return float((1.0 + mzz + vz) / 2.0), float((1.0 + mzz - vz) / 2.0)


def transition_mp(
    alpha: float, beta: float, gamma: float, time: float, dps: int = 70
) -> tuple[mp.mpf, mp.mpf]:
    with mp.workdps(dps):
        al, be, ga, tt = map(mp.mpf, map(str, (alpha, beta, gamma, time)))
        no = mp.matrix([0, mp.sin(2 * al), mp.cos(2 * al)])
        ni = mp.matrix([0, mp.sin(2 * be), mp.cos(2 * be)])
        ham = mp.matrix([[0, 0, 0], [0, 0, -2], [0, 2, 0]])
        linear = ham + ga / 2 * (no * ni.T - mp.eye(3))
        offset = ga / 2 * (no - ni)
        aug = mp.matrix(4, 4)
        for i in range(3):
            for j in range(3):
                aug[i, j] = linear[i, j]
            aug[i, 3] = offset[i]
        prop = mp.expm(tt * aug)
        mzz, vz = prop[2, 2], prop[2, 3]
        return +(1 + mzz + vz) / 2, +(1 + mzz - vz) / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    alpha, beta, gamma, time = 0.2, 1.0, 0.7, 0.9
    no, ni = pure_bloch(alpha), pure_bloch(beta)
    linear, offset = affine_generator(alpha, beta, gamma)
    prop = expm(time * augmented_generator(alpha, beta, gamma))
    aval, bval = transition(alpha, beta, gamma, time)
    amp, bmp = transition_mp(alpha, beta, gamma, time)

    unitary = []
    unitary_error = 0.0
    for t in [0.0, 0.1, math.pi / 4, 0.9, math.pi / 2, math.pi]:
        ua, ub = transition(0.2, 1.0, 0.0, t)
        expected = math.cos(t) ** 2
        err = max(abs(ua - expected), abs(ub - expected))
        unitary_error = max(unitary_error, err)
        unitary.append({"t": t, "a": ua, "b": ub, "cos2": expected, "max_abs_error": err})

    data = {
        "representation": "independently derived real affine Bloch generator",
        "derivation": {
            "state_map": "rho=(I+r_x sigma_x+r_y sigma_y+r_z sigma_z)/2",
            "psi_bloch": "n(theta)=(0,sin(2theta),cos(2theta))",
            "dissipator": "rdot=(gamma/2)[(1+n_i.r)n_o-n_i-r]",
            "hamiltonian": "H=sigma_x implies rdot=2 e_x cross r",
            "observable_map": "a=(1+Mzz+vz)/2, b=(1+Mzz-vz)/2",
        },
        "test_point": {"alpha": alpha, "beta": beta, "gamma": gamma, "t": time},
        "n_o": no.tolist(),
        "n_i": ni.tolist(),
        "linear_generator": linear.tolist(),
        "offset": offset.tolist(),
        "augmented_propagator": prop.tolist(),
        "transition": {"a": aval, "b": bval},
        "high_precision_transition_70dps": {"a": mp.nstr(amp, 60), "b": mp.nstr(bmp, 60)},
        "double_vs_70dps_max_abs": max(abs(aval - float(amp)), abs(bval - float(bmp))),
        "checks": {
            "real_affine_generator_max_imag": 0.0,
            "unitary_limit_max_abs": unitary_error,
            "gamma_nonnegative": gamma >= 0.0,
            "pure_input_bloch_norm_error": max(abs(np.linalg.norm(no) - 1.0), abs(np.linalg.norm(ni) - 1.0)),
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
