#!/usr/bin/env python3
"""Numerical/exact audit of the critical Sibuya fixed-gap coefficient bound.

This is verification evidence, not a proof engine.  It compares the closed
age law with the forward renewal recursion, checks the summation-by-parts
identity and its non-asymptotic bound, probes the two-singularity expansion,
and performs an exact rational parity test at gamma=1/2, z=-1.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import mpmath as mp


def closed_age(t: int, gamma: mp.mpf) -> list[mp.mpf]:
    """p_t(b)=(gamma)_{t-b}/(t-b)! (1-gamma)_b/b!."""
    left = [mp.mpf(1)]
    right = [mp.mpf(1)]
    for k in range(t):
        left.append(left[-1] * (k + gamma) / (k + 1))
        right.append(right[-1] * (k + 1 - gamma) / (k + 1))
    return [left[t - b] * right[b] for b in range(t + 1)]


def forward_history(t_max: int, gamma: mp.mpf) -> list[list[mp.mpf]]:
    """Independent implementation of the age recursion in problem.md."""
    history = [[mp.mpf(1)]]
    for t in range(t_max):
        old = history[-1]
        new = [mp.fsum((gamma / (n + 1)) * old[n] for n in range(t + 1))]
        new.extend((1 - gamma / (n + 1)) * old[n] for n in range(t + 1))
        history.append(new)
    return history


def transform(p: list[mp.mpf], z: mp.mpc) -> mp.mpc:
    return mp.fsum(p[b] * z**b for b in range(len(p)))


def sbp_rhs(p: list[mp.mpf], z: mp.mpc) -> mp.mpc:
    t = len(p) - 1
    return (
        p[0]
        + mp.fsum((p[b] - p[b - 1]) * z**b for b in range(1, t + 1))
        - p[t] * z ** (t + 1)
    )


def principal_power(w: mp.mpc, exponent: mp.mpf) -> mp.mpc:
    return mp.e ** (exponent * mp.log(w))


def two_singularity_lead(t: int, gamma: mp.mpf, z: mp.mpc) -> mp.mpc:
    p = closed_age(t, gamma)
    a = principal_power(1 - z, gamma - 1)
    b = principal_power(1 - 1 / z, -gamma)
    return a * p[0] + b * z**t * p[-1]


def exact_half_parity(t_max: int) -> dict[str, object]:
    coeff = [Fraction(1, 1)]
    for k in range(t_max + 1):
        if k:
            coeff.append(coeff[-1] * Fraction(2 * k - 1, 2 * k))

    failures: list[dict[str, str | int]] = []
    for t in range(t_max + 1):
        value = sum(((-1) ** b) * coeff[t - b] * coeff[b] for b in range(t + 1))
        expected = Fraction(0, 1) if t % 2 else coeff[t // 2]
        if value != expected:
            failures.append({"t": t, "value": str(value), "expected": str(expected)})
    return {
        "tested_t_max": t_max,
        "identity": "F_(2m+1)(-1)=0; F_(2m)(-1)=binom(2m,m)/4^m",
        "failure_count": len(failures),
        "failures": failures[:5],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--precision", type=int, default=80)
    args = parser.parse_args()
    mp.mp.dps = args.precision

    gammas = [mp.mpf("0.2"), mp.mpf("0.5"), mp.mpf("0.8")]
    angles = [mp.pi, mp.pi / 2, 2 * mp.pi / 3, mp.mpf("0.071")]
    recursion_t_max = 160
    bound_times = [1, 2, 3, 8, 32, 128, 512]
    asymptotic_times = [128, 512, 2048, 8192]

    max_recursion_error = mp.mpf(0)
    max_normalization_error = mp.mpf(0)
    max_sbp_error = mp.mpf(0)
    max_bound_ratio = mp.mpf(0)
    max_variation_ratio = mp.mpf(0)
    monotonicity_failures = 0
    tested_bound_cases = 0

    for gamma in gammas:
        history = forward_history(recursion_t_max, gamma)
        for t in range(recursion_t_max + 1):
            p = closed_age(t, gamma)
            max_recursion_error = max(
                max_recursion_error,
                max(abs(p[b] - history[t][b]) for b in range(t + 1)),
            )
            max_normalization_error = max(max_normalization_error, abs(mp.fsum(p) - 1))

        for angle in angles:
            z = mp.e ** (1j * angle)
            for t in bound_times:
                p = closed_age(t, gamma)
                f = transform(p, z)
                rhs = sbp_rhs(p, z)
                max_sbp_error = max(max_sbp_error, abs((1 - z) * f - rhs))

                variation = mp.fsum(abs(p[b] - p[b - 1]) for b in range(1, t + 1))
                endpoints = p[0] + p[-1]
                max_variation_ratio = max(max_variation_ratio, variation / endpoints)
                bound = 2 * endpoints / abs(1 - z)
                max_bound_ratio = max(max_bound_ratio, abs(f) / bound)
                tested_bound_cases += 1

                ratios = [p[b + 1] / p[b] for b in range(t)]
                for b, ratio in enumerate(ratios):
                    expected_sign = mp.sign((b + 1) - gamma * (t + 1))
                    actual_sign = mp.sign(ratio - 1)
                    if actual_sign != expected_sign:
                        monotonicity_failures += 1

    asymptotic_probes: list[dict[str, object]] = []
    for gamma in gammas:
        for angle in angles:
            z = mp.e ** (1j * angle)
            rows = []
            for t in asymptotic_times:
                p = closed_age(t, gamma)
                f = transform(p, z)
                lead = two_singularity_lead(t, gamma, z)
                scale = t ** (gamma - 2) + t ** (-gamma - 1)
                rows.append(
                    {
                        "t": t,
                        "abs_F": mp.nstr(abs(f), 14),
                        "abs_residual": mp.nstr(abs(f - lead), 14),
                        "residual_over_predicted_order": mp.nstr(abs(f - lead) / scale, 14),
                    }
                )
            asymptotic_probes.append(
                {
                    "gamma": mp.nstr(gamma, 4),
                    "angle_over_pi": mp.nstr(angle / mp.pi, 12),
                    "rows": rows,
                }
            )

    payload = {
        "status": "pass"
        if monotonicity_failures == 0 and exact_half_parity(128)["failure_count"] == 0
        else "fail",
        "precision_decimal_digits": args.precision,
        "closed_form": "p_t(b)=(gamma)_(t-b)/(t-b)! * (1-gamma)_b/b!",
        "tested_gamma": [mp.nstr(g, 4) for g in gammas],
        "tested_angles_over_pi": [mp.nstr(a / mp.pi, 12) for a in angles],
        "recursion_t_max": recursion_t_max,
        "max_closed_vs_forward_abs_error": mp.nstr(max_recursion_error, 16),
        "max_normalization_abs_error": mp.nstr(max_normalization_error, 16),
        "tested_bound_cases": tested_bound_cases,
        "max_summation_by_parts_abs_error": mp.nstr(max_sbp_error, 16),
        "max_total_variation_over_endpoint_sum": mp.nstr(max_variation_ratio, 16),
        "max_abs_transform_over_exact_bound": mp.nstr(max_bound_ratio, 16),
        "monotonicity_sign_failure_count": monotonicity_failures,
        "exact_half_parity": exact_half_parity(128),
        "two_singularity_residual_probes": asymptotic_probes,
        "limitations": [
            "Finite high-precision probes support but do not prove an asymptotic expansion.",
            "The non-asymptotic coefficient bound is proved separately in evidence/fixed-gap-analysis.md.",
            "Near-resonance uniformity is not tested; the smallest sampled phase is fixed at 0.071 radians.",
        ],
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "two_singularity_residual_probes"}, indent=2))


if __name__ == "__main__":
    main()
