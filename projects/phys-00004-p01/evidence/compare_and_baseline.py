#!/usr/bin/env python3
"""Cross-compare the two reconstructions and reproduce Eqs. (53), (56)-(60).

No two-use encoding optimization is performed here.  Two-use calculations are
restricted to representation/basis tests for the published channel input.
"""

from __future__ import annotations

import argparse
import json
from typing import Callable

import mpmath as mp
import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar

import method_a_kraus as method_a
import method_b_liouville as method_b


ENERGIES_ONE = np.array([0.0, 1.0])
ENERGIES_TWO = np.array([0.0, 1.0, 1.0, 2.0])


def density_matrix(x: float, coherence_fraction: float, phase: float) -> np.ndarray:
    """All qubit states at excited population x, including complex mixed states."""
    radius = np.sqrt(max(0.0, x * (1.0 - x)))
    off_diagonal = coherence_fraction * radius * np.exp(-1j * phase)
    return np.array(
        [[1.0 - x, off_diagonal], [np.conj(off_diagonal), x]],
        dtype=np.complex128,
    )


def pure_density(x: float, phase: float = 0.0) -> np.ndarray:
    return density_matrix(x, 1.0, phase)


def eq53_reference(rho: np.ndarray, gamma: float, eta: float) -> np.ndarray:
    """Eq. (53) as printed, applicable here to normalized density matrices."""
    rho11 = rho[1, 1]
    coherence = np.sqrt(1.0 - gamma)
    return np.array(
        [
            [
                1.0 - gamma * eta - (1.0 - gamma) * rho11,
                coherence * rho[0, 1],
            ],
            [coherence * rho[1, 0], gamma * eta + (1.0 - gamma) * rho11],
        ],
        dtype=np.complex128,
    )


def eq56_eigenvalues(gamma: float, eta: float, x: float) -> np.ndarray:
    radicand = (1.0 - 2.0 * eta * gamma) ** 2 + 4.0 * gamma * (
        1.0 - gamma
    ) * (2.0 * eta - x) * x
    root = np.sqrt(max(0.0, radicand))
    return np.array([(1.0 - root) / 2.0, (1.0 + root) / 2.0])


def eq57_fixed_ergotropy(gamma: float, eta: float, x: float) -> float:
    radicand = (1.0 - 2.0 * eta * gamma) ** 2 + 4.0 * gamma * (
        1.0 - gamma
    ) * (2.0 * eta - x) * x
    return (
        (1.0 - gamma) * x
        + eta * gamma
        - 0.5
        + 0.5 * np.sqrt(max(0.0, radicand))
    )


def eq58_unconstrained_energy(gamma: float, eta: float) -> float:
    if gamma == 0.0:
        return 1.0
    radicand = max(0.0, 1.0 - 4.0 * gamma * eta * (1.0 - eta))
    return min(1.0, eta + np.sqrt(radicand) / (2.0 * np.sqrt(gamma)))


def eq59_budgeted_energy(gamma: float, eta: float, budget: float) -> float:
    return min(budget, eq58_unconstrained_energy(gamma, eta))


def eq60_ball_ergotropy(gamma: float, eta: float, budget: float) -> float:
    return eq57_fixed_ergotropy(
        gamma, eta, eq59_budgeted_energy(gamma, eta, budget)
    )


def fixed_density_optimization(gamma: float, eta: float, x: float) -> dict[str, float]:
    """Optimize over the complete complex coherence disk at fixed population."""
    if x in (0.0, 1.0):
        value = method_a.ergotropy(method_a.apply_one(pure_density(x), gamma, eta), ENERGIES_ONE)
        return {"value": value, "coherence_fraction": 1.0, "phase": 0.0}

    def objective(variables: np.ndarray) -> float:
        state = density_matrix(x, variables[0], variables[1])
        output = method_a.apply_one(state, gamma, eta)
        return -method_a.ergotropy(output, ENERGIES_ONE)

    result = differential_evolution(
        objective,
        bounds=[(0.0, 1.0), (0.0, 2.0 * np.pi)],
        seed=20260912,
        tol=1e-11,
        atol=1e-13,
        popsize=12,
        maxiter=300,
        polish=True,
        workers=1,
    )
    return {
        "value": float(-result.fun),
        "coherence_fraction": float(result.x[0]),
        "phase": float(result.x[1]),
    }


def ball_density_optimization(
    gamma: float, eta: float, budget: float
) -> dict[str, float]:
    """Optimize over every complex qubit density matrix with rho11<=budget."""
    if budget == 0.0:
        value = method_a.ergotropy(
            method_a.apply_one(pure_density(0.0), gamma, eta), ENERGIES_ONE
        )
        return {
            "value": value,
            "excited_population": 0.0,
            "coherence_fraction": 0.0,
            "phase": 0.0,
        }

    def objective(variables: np.ndarray) -> float:
        state = density_matrix(variables[0], variables[1], variables[2])
        output = method_a.apply_one(state, gamma, eta)
        return -method_a.ergotropy(output, ENERGIES_ONE)

    result = differential_evolution(
        objective,
        bounds=[(0.0, budget), (0.0, 1.0), (0.0, 2.0 * np.pi)],
        seed=20260912,
        tol=1e-11,
        atol=1e-13,
        popsize=14,
        maxiter=400,
        polish=True,
        workers=1,
    )
    return {
        "value": float(-result.fun),
        "excited_population": float(result.x[0]),
        "coherence_fraction": float(result.x[1]),
        "phase": float(result.x[2]),
    }


def random_density(dimension: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    state = matrix @ matrix.conj().T
    return state / np.trace(state)


def matrix_units(dimension: int):
    for row in range(dimension):
        for column in range(dimension):
            unit = np.zeros((dimension, dimension), dtype=np.complex128)
            unit[row, column] = 1.0
            yield unit


def comparison_report() -> dict[str, object]:
    rng = np.random.default_rng(6305681)
    parameter_grid = [
        (float(gamma), float(eta))
        for gamma in np.linspace(0.0, 1.0, 6)
        for eta in np.linspace(0.0, 0.5, 5)
    ]
    max_one_basis_difference = 0.0
    max_two_basis_difference = 0.0
    max_random_one_difference = 0.0
    max_random_two_difference = 0.0
    max_eq53_residual = 0.0
    max_energy_law_residual = 0.0
    minimum_output_eigenvalue = 1.0
    max_one_completeness = 0.0
    max_two_completeness = 0.0
    max_permutation_residual = 0.0

    for gamma, eta in parameter_grid:
        max_one_completeness = max(
            max_one_completeness,
            method_a.completeness_residual(gamma, eta, uses=1),
        )
        max_two_completeness = max(
            max_two_completeness,
            method_a.completeness_residual(gamma, eta, uses=2),
        )
        max_permutation_residual = max(
            max_permutation_residual,
            method_b.permutation_identity_residual(gamma, eta),
        )
        for unit in matrix_units(2):
            difference = method_a.apply_one(unit, gamma, eta) - method_b.apply_one(
                unit, gamma, eta
            )
            max_one_basis_difference = max(
                max_one_basis_difference, float(np.max(np.abs(difference)))
            )
        for state in [random_density(2, rng) for _ in range(3)]:
            output_a = method_a.apply_one(state, gamma, eta)
            output_b = method_b.apply_one(state, gamma, eta)
            max_random_one_difference = max(
                max_random_one_difference,
                float(np.max(np.abs(output_a - output_b))),
            )
            max_eq53_residual = max(
                max_eq53_residual,
                float(np.max(np.abs(output_a - eq53_reference(state, gamma, eta)))),
            )
            input_energy = float(np.real(state[1, 1]))
            output_energy = float(np.real(output_a[1, 1]))
            max_energy_law_residual = max(
                max_energy_law_residual,
                abs(output_energy - ((1.0 - gamma) * input_energy + gamma * eta)),
            )
            minimum_output_eigenvalue = min(
                minimum_output_eigenvalue,
                float(np.min(np.linalg.eigvalsh(0.5 * (output_a + output_a.conj().T)))),
            )

    two_use_parameters = [(0.0, 0.0), (0.2, 0.5), (0.37, 0.21), (1.0, 0.5)]
    for gamma, eta in two_use_parameters:
        for unit in matrix_units(4):
            difference = method_a.apply_two(unit, gamma, eta) - method_b.apply_two(
                unit, gamma, eta
            )
            max_two_basis_difference = max(
                max_two_basis_difference, float(np.max(np.abs(difference)))
            )
        for state in [random_density(4, rng) for _ in range(4)]:
            output_a = method_a.apply_two(state, gamma, eta)
            output_b = method_b.apply_two(state, gamma, eta)
            max_random_two_difference = max(
                max_random_two_difference,
                float(np.max(np.abs(output_a - output_b))),
            )
            minimum_output_eigenvalue = min(
                minimum_output_eigenvalue,
                float(np.min(np.linalg.eigvalsh(0.5 * (output_a + output_a.conj().T)))),
            )

    tolerance = 2e-13
    metrics = {
        "max_one_use_operator_basis_difference": max_one_basis_difference,
        "max_two_use_operator_basis_difference": max_two_basis_difference,
        "max_random_one_use_difference": max_random_one_difference,
        "max_random_two_use_difference": max_random_two_difference,
        "max_Eq53_residual": max_eq53_residual,
        "max_Eq55_energy_law_residual": max_energy_law_residual,
        "max_one_use_Kraus_completeness_residual": max_one_completeness,
        "max_two_use_Kraus_completeness_residual": max_two_completeness,
        "max_Liouville_permutation_identity_residual": max_permutation_residual,
        "minimum_sample_output_eigenvalue": minimum_output_eigenvalue,
    }
    passed = (
        max(
            max_one_basis_difference,
            max_two_basis_difference,
            max_random_one_difference,
            max_random_two_difference,
            max_eq53_residual,
            max_energy_law_residual,
            max_one_completeness,
            max_two_completeness,
            max_permutation_residual,
        )
        <= tolerance
        and minimum_output_eigenvalue >= -tolerance
    )
    return {
        "status": "pass" if passed else "fail",
        "precision": "IEEE-754 binary64 complex arithmetic",
        "absolute_tolerance": tolerance,
        "parameter_grid_size": len(parameter_grid),
        "one_use_random_states": 3 * len(parameter_grid),
        "two_use_parameter_points": two_use_parameters,
        "two_use_random_states": 4 * len(two_use_parameters),
        "basis_map": {
            "physical_basis": ["|00>", "|01>", "|10>", "|11>"],
            "single_column_vec": ["rho00", "rho10", "rho01", "rho11"],
            "global_vec_index": "(2*i1+i2)+4*(2*j1+j2)",
            "local_tensor_index": "4*(i1+2*j1)+(i2+2*j2)",
            "identity_tested": "S2=P^T (S tensor S) P and all 16 global matrix units",
        },
        "metrics": metrics,
    }


def high_precision_value(gamma: str, eta: str, x: str) -> str:
    mp.mp.dps = 80
    g, q, energy = mp.mpf(gamma), mp.mpf(eta), mp.mpf(x)
    radicand = (1 - 2 * q * g) ** 2 + 4 * g * (1 - g) * (2 * q - energy) * energy
    value = (1 - g) * energy + q * g - mp.mpf("0.5") + mp.sqrt(radicand) / 2
    return mp.nstr(value, 70)


def baseline_report() -> dict[str, object]:
    equation_grid = [
        (float(gamma), float(eta), float(x), float(phase))
        for gamma in np.linspace(0.0, 1.0, 6)
        for eta in np.linspace(0.0, 0.5, 5)
        for x in np.linspace(0.0, 1.0, 7)
        for phase in (0.0, 0.73, 2.11)
    ]
    max_eq56_residual = 0.0
    max_eq57_direct_residual = 0.0
    for gamma, eta, x, phase in equation_grid:
        output = method_a.apply_one(pure_density(x, phase), gamma, eta)
        numerical_eigenvalues = np.linalg.eigvalsh(0.5 * (output + output.conj().T))
        max_eq56_residual = max(
            max_eq56_residual,
            float(np.max(np.abs(numerical_eigenvalues - eq56_eigenvalues(gamma, eta, x)))),
        )
        numerical_ergotropy = method_a.ergotropy(output, ENERGIES_ONE)
        max_eq57_direct_residual = max(
            max_eq57_direct_residual,
            abs(numerical_ergotropy - eq57_fixed_ergotropy(gamma, eta, x)),
        )

    fixed_cases = [
        (0.5, 0.0, 0.2),
        (0.5, 0.15, 0.6),
        (0.5, 0.25, 1.0),
        (0.5, 0.35, 0.4),
        (0.5, 0.5, 0.8),
        (0.0, 0.3, 0.6),
        (0.2, 0.3, 0.6),
        (0.4, 0.3, 0.6),
        (0.6, 0.3, 0.6),
        (0.8, 0.3, 0.6),
    ]
    fixed_optimization = []
    max_fixed_optimizer_residual = 0.0
    for gamma, eta, x in fixed_cases:
        numerical = fixed_density_optimization(gamma, eta, x)
        analytic = eq57_fixed_ergotropy(gamma, eta, x)
        residual = abs(numerical["value"] - analytic)
        max_fixed_optimizer_residual = max(max_fixed_optimizer_residual, residual)
        fixed_optimization.append(
            {
                "gamma": gamma,
                "eta": eta,
                "fixed_energy": x,
                "density_matrix_optimum": numerical,
                "Eq57": analytic,
                "absolute_residual": residual,
            }
        )

    ball_cases = [
        (0.5, 0.3, 1.0),
        (0.8, 0.3, 1.0),
        (0.5, 0.0, 1.0),
        (0.2, 0.5, 0.7),
        (0.95, 0.1, 0.9),
        (0.01, 0.3, 0.4),
    ]
    ball_optimization = []
    max_ball_optimizer_residual = 0.0
    max_optimal_energy_residual = 0.0
    for gamma, eta, budget in ball_cases:
        numerical = ball_density_optimization(gamma, eta, budget)
        analytic_energy = eq59_budgeted_energy(gamma, eta, budget)
        analytic_value = eq60_ball_ergotropy(gamma, eta, budget)
        value_residual = abs(numerical["value"] - analytic_value)
        energy_residual = abs(numerical["excited_population"] - analytic_energy)
        max_ball_optimizer_residual = max(max_ball_optimizer_residual, value_residual)
        max_optimal_energy_residual = max(max_optimal_energy_residual, energy_residual)
        ball_optimization.append(
            {
                "gamma": gamma,
                "eta": eta,
                "energy_budget": budget,
                "density_matrix_optimum": numerical,
                "Eq59_optimal_energy": analytic_energy,
                "Eq60": analytic_value,
                "absolute_value_residual": value_residual,
                "absolute_energy_residual": energy_residual,
            }
        )

    derivative_checks = []
    max_eq58_optimizer_residual = 0.0
    # The gamma=1 limiting map is exactly input independent, so every x is a
    # maximizer and an optimizer cannot be required to return Eq. (58)'s
    # particular representative.  Localization is tested only where the
    # maximum is nondegenerate; the endpoint is checked separately below.
    for gamma, eta in [(0.2, 0.1), (0.5, 0.3), (0.8, 0.3), (0.95, 0.1)]:
        result = minimize_scalar(
            lambda x: -eq57_fixed_ergotropy(gamma, eta, float(x)),
            bounds=(0.0, 1.0),
            method="bounded",
            options={"xatol": 1e-14},
        )
        predicted = eq58_unconstrained_energy(gamma, eta)
        residual = abs(float(result.x) - predicted)
        max_eq58_optimizer_residual = max(max_eq58_optimizer_residual, residual)
        derivative_checks.append(
            {
                "gamma": gamma,
                "eta": eta,
                "scalar_optimizer_energy": float(result.x),
                "Eq58_energy": predicted,
                "absolute_residual": residual,
            }
        )

    panel_a = []
    for eta in (0.0, 0.15, 0.25, 0.35, 0.5):
        panel_a.append(
            {
                "gamma": 0.5,
                "eta": eta,
                "Eq57_at_e_0.2_0.6_1.0": [
                    eq57_fixed_ergotropy(0.5, eta, x) for x in (0.2, 0.6, 1.0)
                ],
            }
        )
    panel_b = []
    for gamma in (0.0, 0.2, 0.4, 0.6, 0.8):
        panel_b.append(
            {
                "gamma": gamma,
                "eta": 0.3,
                "Eq57_at_e_0.2_0.6_1.0": [
                    eq57_fixed_ergotropy(gamma, 0.3, x)
                    for x in (0.2, 0.6, 1.0)
                ],
            }
        )
    panel_c = [
        {
            "gamma": gamma,
            "eta": eta,
            "Eq58_optimal_energy": eq58_unconstrained_energy(gamma, eta),
        }
        for gamma, eta in ((0.2, 0.1), (0.5, 0.3), (0.8, 0.3), (1.0, 0.1))
    ]
    panel_d = [
        {
            "gamma": gamma,
            "eta": eta,
            "Eq60_W1_at_budget_1": eq60_ball_ergotropy(gamma, eta, 1.0),
        }
        for gamma, eta in ((0.2, 0.1), (0.5, 0.3), (0.8, 0.3), (1.0, 0.1))
    ]

    high_precision = []
    for gamma, eta, x in (("0.5", "0.15", "0.6"), ("0.8", "0.3", "0.6")):
        mp_value = high_precision_value(gamma, eta, x)
        double_value = eq57_fixed_ergotropy(float(gamma), float(eta), float(x))
        high_precision.append(
            {
                "gamma": gamma,
                "eta": eta,
                "x": x,
                "mpmath_dps": 80,
                "Eq57_mpmath": mp_value,
                "Eq57_binary64": double_value,
                "absolute_difference": float(abs(mp.mpf(mp_value) - double_value)),
            }
        )

    value_tolerance = 2e-9
    energy_tolerance = 1e-6
    direct_tolerance = 2e-13
    passed = (
        max_eq56_residual <= direct_tolerance
        and max_eq57_direct_residual <= direct_tolerance
        and max_fixed_optimizer_residual <= value_tolerance
        and max_ball_optimizer_residual <= value_tolerance
        and max_optimal_energy_residual <= energy_tolerance
        and max_eq58_optimizer_residual <= energy_tolerance
    )
    return {
        "status": "pass" if passed else "fail",
        "published_baseline": "arXiv:2305.16803v4 Eqs. (53), (56)-(60), representative Fig. 3 values",
        "precision": {
            "channel_and_spectrum": "IEEE-754 binary64",
            "analytic_spot_checks": "mpmath 80 decimal digits",
            "density_matrix_optimizer": "SciPy differential_evolution, fixed seed 20260912, polished",
        },
        "complete_qubit_parameterization": "rho=[[1-x,t*sqrt(x(1-x))*exp(-i phi)],[conj,x]], x in budget interval, t in [0,1], phi in [0,2pi]",
        "tolerances": {
            "direct_equations_absolute": direct_tolerance,
            "optimized_value_absolute": value_tolerance,
            "optimized_energy_absolute": energy_tolerance,
        },
        "equation_grid_points": len(equation_grid),
        "max_residuals": {
            "Eq56_output_spectrum": max_eq56_residual,
            "Eq57_direct_ergotropy": max_eq57_direct_residual,
            "Eq57_full_density_matrix_fixed_energy_optimization": max_fixed_optimizer_residual,
            "Eq58_scalar_energy_optimization": max_eq58_optimizer_residual,
            "Eq59_optimal_energy_full_density_matrix_optimization": max_optimal_energy_residual,
            "Eq60_ball_full_density_matrix_optimization": max_ball_optimizer_residual,
        },
        "fixed_energy_density_matrix_checks": fixed_optimization,
        "ball_density_matrix_checks": ball_optimization,
        "Eq58_checks": derivative_checks,
        "gamma_1_endpoint_check": {
            "interpretation": "For eta<=1/2, Eq. (58) selects x=1/2 at gamma=1, but Eq. (57) is identically zero and the maximizer is nonunique.",
            "eta": 0.1,
            "Eq58_selected_energy": eq58_unconstrained_energy(1.0, 0.1),
            "max_absolute_Eq57_on_101_point_x_grid": max(
                abs(eq57_fixed_ergotropy(1.0, 0.1, float(x)))
                for x in np.linspace(0.0, 1.0, 101)
            ),
        },
        "Fig3_representative_values": {
            "panel_a_Eq57_gamma_0.5": panel_a,
            "panel_b_Eq57_eta_0.3": panel_b,
            "panel_c_Eq58": panel_c,
            "panel_d_Eq60_budget_1": panel_d,
        },
        "high_precision_spot_checks": high_precision,
        "scope_note": "This run verifies the published one-use baseline and the two-use channel representation only; it does not optimize two-use encodings or resolve additivity.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("compare", "baseline"))
    arguments = parser.parse_args()
    report: Callable[[], dict[str, object]] = (
        comparison_report if arguments.mode == "compare" else baseline_report
    )
    print(json.dumps(report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
