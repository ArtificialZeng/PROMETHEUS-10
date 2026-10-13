#!/usr/bin/env python3
"""Independent numerical checks of the exact K3 linear-response calculation."""
from __future__ import annotations

import json
import math
import platform
import sys

import numpy as np
import scipy

from search_k3_phase import Drive, collocation_solution, generator, propagator_solution


def equilibrium(offset: np.ndarray) -> np.ndarray:
    weights = np.exp(-offset)
    return weights / np.sum(weights)


def symmetric_relaxation(offset: np.ndarray, k0: float) -> np.ndarray:
    pi = equilibrium(offset)
    root = np.sqrt(pi)
    dminus = np.diag(1.0 / root)
    dplus = np.diag(root)
    return -dminus @ generator(offset, k0) @ dplus


def analytic_coefficients(base: Drive) -> dict[str, object]:
    pi = equilibrium(base.offset)
    root = np.sqrt(pi)
    ksym = symmetric_relaxation(base.offset, base.k0)
    evals, evecs = np.linalg.eigh(ksym)
    keep = evals > 1e-9 * base.k0
    lambdas = evals[keep]
    modes = evecs[:, keep]
    a2 = 0.0
    b2 = 0.0
    modal = []
    for n in range(1, base.sin_coeff.shape[0] + 1):
        ehat = base.cos_coeff[n - 1].astype(complex) - 1j * base.sin_coeff[n - 1]
        ehat -= np.dot(pi, ehat)
        vhat = root * ehat
        coeff = modes.T.conj() @ vhat
        freq = n * base.omega
        for lam, amp in zip(lambdas, coeff, strict=True):
            weight = 0.5 * abs(amp) ** 2 * freq**2 / (lam**2 + freq**2)
            bpiece = weight * lam
            apiece = weight * lam**2
            a2 += apiece
            b2 += bpiece
            modal.append({
                "harmonic": n,
                "lambda": float(lam),
                "abs_coefficient_squared": float(abs(amp) ** 2),
                "A2_piece": float(apiece),
                "B2_piece": float(bpiece),
            })
    return {
        "pi": pi.tolist(),
        "K_eigenvalues": evals.tolist(),
        "A2": a2,
        "B2": b2,
        "A2_minus_2k0B2": a2 - 2.0 * base.k0 * b2,
        "A2_over_k0B2": a2 / (base.k0 * b2),
        "phase_leading": math.atan2(base.omega * b2, a2),
        "modal_terms": modal,
    }


def scaled(base: Drive, epsilon: float) -> Drive:
    return Drive(
        base.offset.copy(),
        epsilon * base.sin_coeff,
        epsilon * base.cos_coeff,
        base.omega,
        base.k0,
    )


def main() -> None:
    print("ENV " + json.dumps({
        "executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }, sort_keys=True, separators=(",", ":")))
    cases = [
        (
            "generic_two_harmonic",
            Drive(
                np.array([-0.8, 0.3, 1.1]),
                np.array([[0.7, -0.4, -0.3], [0.2, 0.5, -0.7]]),
                np.array([[-0.1, 0.6, -0.5], [0.8, -0.3, -0.5]]),
                1.3,
                1.0,
            ),
        ),
        (
            "near_effective_two_state",
            Drive(
                np.array([0.0, 0.0, 7.0]),
                np.array([[0.5, -0.5, 0.0]]),
                np.array([[0.25, -0.25, 0.0]]),
                0.8,
                1.0,
            ),
        ),
    ]
    for label, base in cases:
        analytic = analytic_coefficients(base)
        print(f"CASE {label}")
        print("BASE_DRIVE " + json.dumps(base.record(), sort_keys=True, separators=(",", ":")))
        print("ANALYTIC " + json.dumps(analytic, sort_keys=True, separators=(",", ":")))
        for eps in [0.2, 0.1, 0.05, 0.025]:
            drive = scaled(base, eps)
            prop = propagator_solution(drive, rtol=2e-12, atol=2e-14, nodes=4097)
            row = {
                "epsilon": eps,
                "A_over_eps2": float(prop["A"]) / eps**2,
                "B_over_eps2": float(prop["B"]) / eps**2,
                "ratio": prop["A_over_k0B"],
                "phase": prop["phase"],
                "A2_relative_error": (float(prop["A"]) / eps**2 - float(analytic["A2"])) / float(analytic["A2"]),
                "B2_relative_error": (float(prop["B"]) / eps**2 - float(analytic["B2"])) / float(analytic["B2"]),
                "periodic_residual_inf": prop["periodic_residual_inf"],
                "normalization_residual_inf": prop["normalization_residual_inf"],
                "min_probability": prop["min_probability"],
            }
            print("NONLINEAR_TO_LR " + json.dumps(row, sort_keys=True, separators=(",", ":")))
        eps = 0.05
        drive = scaled(base, eps)
        prop = propagator_solution(drive, rtol=2e-12, atol=2e-14, nodes=4097)
        for nodes in [48, 96, 192]:
            coll = collocation_solution(drive, nodes=nodes)
            print("INDEPENDENT_CHECK " + json.dumps({
                "epsilon": eps,
                "collocation_nodes": nodes,
                "abs_A_difference": abs(float(coll["A"]) - float(prop["A"])),
                "abs_B_difference": abs(float(coll["B"]) - float(prop["B"])),
                "propagator_ratio": prop["A_over_k0B"],
                "collocation_ratio": coll["A_over_k0B"],
                "collocation_residual_inf": coll["collocation_residual_inf"],
            }, sort_keys=True, separators=(",", ":")))
    # Static offset grid checks only the exact relaxation matrix, not the nonlinear claim.
    grid_min = math.inf
    grid_arg = None
    for x in np.linspace(-8.0, 8.0, 33):
        for y in np.linspace(-8.0, 8.0, 33):
            evals = np.linalg.eigvalsh(symmetric_relaxation(np.array([x, y, 0.0]), 1.0))
            positive = evals[evals > 1e-8]
            candidate = float(np.min(positive))
            if candidate < grid_min:
                grid_min = candidate
                grid_arg = [float(x), float(y), 0.0]
    print("STATIC_SPECTRAL_GRID " + json.dumps({
        "offset_grid": "x,y in [-8,8] step 0.5; E3=0",
        "minimum_positive_lambda_over_k0": grid_min,
        "argmin_offset": grid_arg,
        "interpretation": "finite grid sanity check only; exact proof is separate",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
