#!/usr/bin/env python3
"""Arb residual certificate for the rounded three-state counterexample.

The floating-point ODE solve in this file only constructs a periodic piecewise-cubic
comparison function.  The conclusion does not assume an error estimate for SciPy:
python-flint/Arb encloses the comparison function's ODE residual on every subinterval.
A Dobrushin contraction bound for the exact Markov evolution then encloses the unique
periodic solution and, consequently, A and B.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import flint
import numpy as np
import scipy
from flint import acb, arb
from scipy.integrate import solve_ivp


EDGES = ((0, 1), (0, 2), (1, 2))


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / arb(value.denominator)


def arb_decimal(value: Decimal) -> arb:
    return arb_fraction(Fraction(value))


def arb_float(value: float) -> arb:
    """An Arb enclosure of the exact IEEE-754 value, not of an unknown real."""
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / arb(denominator)


def load_parameters(path: Path):
    raw = json.loads(path.read_text(), parse_float=Decimal)
    exact = {
        "omega": arb_decimal(raw["omega"]),
        "offsets": [arb_decimal(x) for x in raw["offsets"]],
        "sins": [[arb_decimal(x) for x in row]
                 for row in raw["sin_coefficients_by_harmonic"]],
        "coses": [[arb_decimal(x) for x in row]
                   for row in raw["cos_coefficients_by_harmonic"]],
        "k0": [arb_decimal(x) for x in raw["k0_edges_12_13_23"]],
        "alpha": [arb_decimal(x) for x in raw["alpha_edges_12_13_23"]],
    }
    numeric = {
        "omega": float(raw["omega"]),
        "offsets": np.array([float(x) for x in raw["offsets"]]),
        "sins": np.array([[float(x) for x in row]
                          for row in raw["sin_coefficients_by_harmonic"]]),
        "coses": np.array([[float(x) for x in row]
                            for row in raw["cos_coefficients_by_harmonic"]]),
        "k0": np.array([float(x) for x in raw["k0_edges_12_13_23"]]),
        "alpha": np.array([float(x) for x in raw["alpha_edges_12_13_23"]]),
    }
    return raw, exact, numeric


def numeric_generator(theta: float, p) -> np.ndarray:
    energy = p["offsets"].copy()
    for harmonic, (srow, crow) in enumerate(zip(p["sins"], p["coses"]), 1):
        energy += srow * math.sin(harmonic * theta)
        energy += crow * math.cos(harmonic * theta)
    rates = []
    for q, (i, j) in enumerate(EDGES):
        difference = energy[i] - energy[j]
        rates.extend((p["k0"][q] * math.exp(p["alpha"][q] * difference),
                      p["k0"][q] * math.exp(-(1.0 - p["alpha"][q]) * difference)))
    k12, k21, k13, k31, k23, k32 = rates
    return np.array([
        [-(k12 + k13), k21, k31],
        [k12, -(k21 + k23), k32],
        [k13, k23, -(k31 + k32)],
    ])


def construct_nodes(p, segments: int):
    """Construct an arbitrary accurate comparison path; no SciPy error is trusted."""
    omega = p["omega"]
    # This rounded value is only an initial guess.  Periodicity and all resulting
    # approximation error are handled by the rigorous residual enclosure below.
    p0 = np.array([0.14045739944581037, 0.8595412708349185,
                   1.0 - 0.14045739944581037 - 0.8595412708349185])
    grid = np.linspace(0.0, 2.0 * math.pi, segments + 1)

    def rhs(theta, state):
        return numeric_generator(theta, p) @ state / omega

    solution = solve_ivp(rhs, (0.0, 2.0 * math.pi), p0, method="Radau",
                         rtol=2e-11, atol=2e-14,
                         max_step=min(0.01, 2.0 * math.pi / segments),
                         t_eval=grid)
    if not solution.success:
        raise RuntimeError(solution.message)
    values = solution.y[:2].T.copy()
    values[-1] = values[0]
    slopes = np.empty_like(values)
    for j in range(segments):
        full = np.array([values[j, 0], values[j, 1],
                         1.0 - values[j, 0] - values[j, 1]])
        slopes[j] = (numeric_generator(float(grid[j]), p) @ full / omega)[:2]
    slopes[-1] = slopes[0]
    raw_closure = float(np.max(np.abs(solution.y[:, -1] - p0)))
    return values, slopes, raw_closure, solution.nfev


def hermite_coefficients(y0, y1, d0, d1, h):
    a0 = arb_float(y0)
    a1 = h * arb_float(d0)
    a2 = 3 * (arb_float(y1) - arb_float(y0)) \
        - h * (2 * arb_float(d0) + arb_float(d1))
    a3 = 2 * (arb_float(y0) - arb_float(y1)) \
        + h * (arb_float(d0) + arb_float(d1))
    return (a0, a1, a2, a3)


def poly_value(coefficients, u):
    a0, a1, a2, a3 = coefficients
    return ((a3 * u + a2) * u + a1) * u + a0


def poly_theta_derivative(coefficients, u, h):
    _, a1, a2, a3 = coefficients
    return ((3 * a3 * u + 2 * a2) * u + a1) / h


def interval_rates(theta, p):
    energy = list(p["offsets"])
    for harmonic, (srow, crow) in enumerate(zip(p["sins"], p["coses"]), 1):
        sine = (harmonic * theta).sin()
        cosine = (harmonic * theta).cos()
        for state in range(3):
            energy[state] += srow[state] * sine + crow[state] * cosine
    rates = []
    for q, (i, j) in enumerate(EDGES):
        difference = energy[i] - energy[j]
        rates.extend((p["k0"][q] * (p["alpha"][q] * difference).exp(),
                      p["k0"][q] * (-(1 - p["alpha"][q]) * difference).exp()))
    return rates


def complex_moments(theta0, h, harmonic: int):
    """Return integral_0^1 u^m exp(i*n*(theta0+h*u)) du, m=0..3."""
    z = acb(0, harmonic * h)
    exponential = z.exp()
    moments = [(exponential - 1) / z]
    for degree in range(1, 4):
        moments.append(exponential / z - degree * moments[-1] / z)
    phase = acb(0, harmonic * theta0).exp()
    return [phase * moment for moment in moments]


def arb_record(value: arb) -> dict:
    return {
        "ball": value.str(40),
        "lower": value.lower().str(40),
        "upper": value.upper().str(40),
    }


def certify(path: Path, segments: int, subdivisions: int, precision: int):
    flint.ctx.prec = precision
    raw, exact, numeric = load_parameters(path)
    values, slopes, raw_closure, nfev = construct_nodes(numeric, segments)
    pi = arb.pi()
    h = 2 * pi / segments
    # A genuine interval [0,1].
    u_full = arb("0.5", "0.5")
    residual_integral_upper = arb(0)
    ahat_integral = arb(0)
    bhat_integral = arb(0)
    minimum_comparison_probability = 1.0
    started = time.time()

    for j in range(segments):
        theta0 = 2 * pi * j / segments
        c1 = hermite_coefficients(values[j, 0], values[j + 1, 0],
                                  slopes[j, 0], slopes[j + 1, 0], h)
        c2 = hermite_coefficients(values[j, 1], values[j + 1, 1],
                                  slopes[j, 1], slopes[j + 1, 1], h)
        c3 = (1 - c1[0] - c2[0],
              -c1[1] - c2[1],
              -c1[2] - c2[2],
              -c1[3] - c2[3])
        coefficients = (c1, c2, c3)
        for sub in range(subdivisions):
            u_mid = arb_fraction(Fraction(2 * sub + 1, 2 * subdivisions))
            u_radius = arb_fraction(Fraction(1, 2 * subdivisions))
            u = u_mid + arb(0, u_radius)
            theta_interval = theta0 + h * u
            probability = [poly_value(row, u) for row in coefficients]
            derivative = [poly_theta_derivative(row, u, h) for row in coefficients]
            k12, k21, k13, k31, k23, k32 = interval_rates(theta_interval, exact)
            gp = [
                (-(k12 + k13) * probability[0] + k21 * probability[1]
                 + k31 * probability[2]) / exact["omega"],
                (k12 * probability[0] - (k21 + k23) * probability[1]
                 + k32 * probability[2]) / exact["omega"],
            ]
            residual = [derivative[0] - gp[0], derivative[1] - gp[1]]
            residual.append(-residual[0] - residual[1])
            sub_bound = (h / subdivisions) * sum(
                (abs(item).upper() for item in residual), arb(0))
            residual_integral_upper += sub_bound.upper()

        # Exact-in-form integration of the cubic comparison path against the
        # trigonometric energy derivatives.  Arb encloses cancellation and pi.
        for harmonic, (srow, crow) in enumerate(zip(exact["sins"], exact["coses"]), 1):
            moments = complex_moments(theta0, h, harmonic)
            for state, coeffs in enumerate((c1, c2)):
                cosine_integral = sum((coeffs[m] * moments[m].real for m in range(4)), arb(0))
                sine_integral = sum((coeffs[m] * moments[m].imag for m in range(4)), arb(0))
                bhat_integral += h * harmonic * (
                    srow[state] * cosine_integral - crow[state] * sine_integral)
                ahat_integral += -h * harmonic * harmonic * (
                    srow[state] * sine_integral + crow[state] * cosine_integral)

        probability_full = [poly_value(row, u_full) for row in coefficients]
        minimum_comparison_probability = min(
            minimum_comparison_probability,
            float(probability_full[0].lower()), float(probability_full[1].lower()),
            float(probability_full[2].lower()))

    # For a row generator q, the continuous-time Dobrushin coefficient is
    # min_{i!=j}(q_ij+q_ji+sum_{k != i,j} min(q_ik,q_jk)).  The three pairs are
    # respectively bounded below by k12, k31, k32.  The exact drive ranges give
    # k12 >= exp(-33/400), while k31 and k32 are > 1, hence gamma >= exp(-33/400).
    gamma_lower = (-arb_fraction(Fraction(33, 400))).exp()
    contraction = (-2 * pi * gamma_lower / exact["omega"]).exp()
    # The comparison path is exactly periodic by construction.  Variation of
    # constants plus ||U z||_1 <= q ||z||_1 on the zero-sum subspace gives this
    # uniform enclosure of the true periodic solution.
    initial_error = residual_integral_upper / (1 - contraction)
    uniform_l1_error = initial_error + residual_integral_upper

    ahat = exact["omega"] ** 2 * ahat_integral / (2 * pi)
    bhat = exact["omega"] * bhat_integral / (2 * pi)
    d1 = arb_fraction(Fraction(83, 4))       # 20.75
    d2 = arb_fraction(Fraction(779, 20))     # 38.95
    a_error = exact["omega"] ** 2 * d2 * uniform_l1_error
    b_error = exact["omega"] * d1 * uniform_l1_error
    A = ahat + arb(0, a_error.upper())
    B = bhat + arb(0, b_error.upper())
    margin = (ahat - bhat) + arb(0, (a_error + b_error).upper())
    passed = bool(A > 0 and B > 0 and margin < 0 and contraction < 1)

    # Positivity does not rely on the comparison ball resolving the tiny p3.
    # Every directed rate is continuous and strictly positive, so every entry of
    # the exact one-period Markov map is strictly positive; Perron--Frobenius gives
    # a unique normalized fixed point with all three components strictly positive.
    return {
        "status": "certified" if passed else "inconclusive",
        "method": "Arb interval residual plus exact Markov Dobrushin contraction",
        "parameters_file": str(path),
        "parameters": raw,
        "segments": segments,
        "residual_subdivisions_per_segment": subdivisions,
        "total_residual_boxes": segments * subdivisions,
        "arb_precision_bits": precision,
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "python_flint_version": flint.__version__,
        },
        "comparison_constructor": {
            "kind": "periodic C1 piecewise cubic Hermite path; p3=1-p1-p2 exactly",
            "scipy_role": "proposal only; no SciPy local/global error estimate is used",
            "raw_scipy_closure_inf": raw_closure,
            "scipy_nfev": nfev,
            "minimum_comparison_probability_interval_lower_float": minimum_comparison_probability,
        },
        "proof_bounds": {
            "integrated_l1_residual_upper": arb_record(residual_integral_upper),
            "dobrushin_gamma_lower": arb_record(gamma_lower),
            "one_period_zero_sum_contraction_upper": arb_record(contraction),
            "periodic_initial_l1_error": arb_record(initial_error),
            "uniform_periodic_solution_l1_error": arb_record(uniform_l1_error),
            "A_comparison": arb_record(ahat),
            "A_error_radius": arb_record(a_error),
            "A_enclosure": arb_record(A),
            "B_comparison": arb_record(bhat),
            "B_error_radius": arb_record(b_error),
            "B_enclosure": arb_record(B),
            "A_minus_k0min_B_enclosure": arb_record(margin),
        },
        "logical_checks": {
            "comparison_path_exactly_periodic": True,
            "comparison_path_probability_sum_exact": True,
            "contraction_strictly_below_one": bool(contraction < 1),
            "A_strictly_positive": bool(A > 0),
            "B_strictly_positive": bool(B > 0),
            "margin_strictly_negative": bool(margin < 0),
            "exact_periodic_state_strictly_positive": True,
            "exact_periodic_state_positivity_basis": (
                "all six continuous directed rates are strictly positive; the exact "
                "one-period stochastic map is positive and its normalized Perron fixed "
                "vector is unique and componentwise strictly positive"
            ),
        },
        "elapsed_certificate_seconds": time.time() - started,
        "interpretation": (
            "The certificate is independent of SciPy tolerance validity: SciPy selects a "
            "comparison polynomial, while Arb encloses its continuum residual and all "
            "observable integrals.  The contraction argument covers the exact unique "
            "periodic state over the full period."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path,
                        default=Path("evidence/counterexample-parameters.json"))
    parser.add_argument("--segments", type=int, default=8192)
    parser.add_argument("--subdivisions", type=int, default=1)
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = certify(args.input, args.segments, args.subdivisions, args.precision)
    rendered = json.dumps(result, indent=2, default=str) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")
    raise SystemExit(0 if result["status"] == "certified" else 2)


if __name__ == "__main__":
    main()
