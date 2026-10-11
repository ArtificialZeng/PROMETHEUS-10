#!/usr/bin/env python3
"""Portable high-precision reproduction of the four-level cooling witness."""
from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "manuscript" / "witness-data.json"
PAIRS = ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3))
TRIPLETS = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


def maxabs(values):
    return max((abs(value) for value in values), default=mp.mpf("0"))


def column_generator(energies, downward):
    matrix = mp.matrix(4)
    for rate, (i, j) in zip(downward, PAIRS):
        matrix[i, j] = rate
        matrix[j, i] = rate * mp.exp(-(energies[j] - energies[i]))
    for j in range(4):
        matrix[j, j] = -mp.fsum(matrix[i, j] for i in range(4) if i != j)
    return matrix


def mapped_reversed_row_generator(energies, downward):
    order = (3, 2, 1, 0)
    position = {state: index for index, state in enumerate(order)}
    rates = {pair: rate for pair, rate in zip(PAIRS, downward)}
    row = mp.matrix(4)
    for origin in range(4):
        for destination in range(4):
            if origin == destination:
                continue
            if destination < origin:
                rate = rates[(destination, origin)]
            else:
                rate = rates[(origin, destination)] * mp.exp(
                    -(energies[destination] - energies[origin])
                )
            oi, di = position[origin], position[destination]
            row[oi, di] += rate
            row[oi, oi] -= rate
    reversal = mp.matrix(4)
    for i in range(4):
        reversal[i, 3 - i] = 1
    return row, reversal * row.T * reversal


def modal_data(matrix, energies):
    weights = mp.matrix([mp.exp(-energy) for energy in energies])
    pi = weights / mp.fsum(weights)
    root = mp.matrix([mp.sqrt(value) for value in pi])
    symmetric = mp.matrix(4)
    for i in range(4):
        for j in range(4):
            symmetric[i, j] = matrix[i, j] * root[j] / root[i]
    eigenvalues, eigenvectors = mp.eigsy(symmetric)
    u2 = eigenvectors[:, 2]
    ell2 = mp.matrix([u2[i] / root[i] for i in range(4)])
    v2 = mp.matrix([u2[i] * root[i] for i in range(4)])
    if ell2[3] < 0:
        u2, ell2, v2 = -u2, -ell2, -v2
    lam2 = eigenvalues[2]
    residuals = {
        "similarity_symmetry": maxabs(
            symmetric[i, j] - symmetric[j, i]
            for i in range(4) for j in range(4)
        ),
        "right_eigenpair": maxabs(matrix * v2 - lam2 * v2),
        "left_eigenpair": maxabs(matrix.T * ell2 - lam2 * ell2),
        "biorthogonal_normalization": abs(mp.fdot(ell2, v2) - 1),
        "stationary_orthogonality": abs(mp.fdot(ell2, pi)),
    }
    return eigenvalues, ell2, pi, residuals


def triplet_data(energies, downward):
    rates = {pair: rate for pair, rate in zip(PAIRS, downward)}
    rows = []
    for i, j, k in TRIPLETS:
        a, b, c = rates[(i, k)], rates[(j, k)], rates[(i, j)]
        q = mp.exp(-(energies[j] - energies[i]))
        r = mp.exp(-(energies[k] - energies[j]))
        kappa = (a + b) / (c * (1 + q))
        high = a * (1 + q * r / 2) - b * (1 + r / 2) - c * (1 - q)
        low = a * q - b
        branch = "high" if kappa >= 1 else "low"
        applicable = high if branch == "high" else low
        rows.append({
            "triplet": "".join(str(index + 1) for index in (i, j, k)),
            "kappa": kappa,
            "branch": branch,
            "F_high": high,
            "F_low": low,
            "applicable_value": applicable,
            "exclusion_margin_over_rate_sum": -applicable / (a + b + c),
        })
    return rows


def gibbs(beta, energies):
    weights = mp.matrix([mp.exp(-beta * energy) for energy in energies])
    return weights / mp.fsum(weights)


def relative_entropy(population, equilibrium):
    return mp.fsum(
        population[i] * mp.log(population[i] / equilibrium[i]) for i in range(4)
    )


def evaluate(decimal_digits):
    mp.mp.dps = decimal_digits
    energies = [mp.mpf(0), mp.mpf(1) / 200, mp.mpf(7) / 20, mp.mpf(14)]
    downward = [
        mp.mpf(1) / 10, mp.mpf(1), mp.mpf(13),
        mp.mpf(99) / 100, mp.mpf(1), mp.mpf(3) / 4,
    ]
    beta_hot, beta_cool = mp.mpf(1) / 50, mp.mpf(1) / 20
    direct = column_generator(energies, downward)
    reversed_row, mapped = mapped_reversed_row_generator(energies, downward)
    eigenvalues, ell2, pi, residuals = modal_data(direct, energies)
    mapped_eigenvalues, mapped_ell2, mapped_pi, mapped_residuals = modal_data(
        mapped, energies
    )
    g_hot, g_cool = gibbs(beta_hot, energies), gibbs(beta_cool, energies)
    b_hot = mp.fdot(ell2, g_hot - pi)
    b_cool = mp.fdot(ell2, g_cool - pi)
    mapped_hot = mp.fdot(mapped_ell2, g_hot - mapped_pi)
    mapped_cool = mp.fdot(mapped_ell2, g_cool - mapped_pi)
    triples = triplet_data(energies, downward)
    times = (0, 1, 2, 4, 6, 8, 10)
    evolution = []
    for time_value in times:
        time = mp.mpf(time_value)
        hot = mp.expm(direct * time) * g_hot
        cool = mp.expm(direct * time) * g_cool
        d_hot = relative_entropy(hot, pi)
        d_cool = relative_entropy(cool, pi)
        evolution.append({
            "time": time,
            "D_hot": d_hot,
            "D_cool": d_cool,
            "D_hot_minus_D_cool": d_hot - d_cool,
            "minimum_probability": min(min(hot), min(cool)),
            "hot_probability_sum_error": abs(mp.fsum(hot) - 1),
            "cool_probability_sum_error": abs(mp.fsum(cool) - 1),
        })
    matrix_checks = {
        "direct_vs_reversed_map": maxabs(
            direct[i, j] - mapped[i, j] for i in range(4) for j in range(4)
        ),
        "direct_column_sums": maxabs(
            mp.fsum(direct[i, j] for i in range(4)) for j in range(4)
        ),
        "reversed_row_sums": maxabs(
            mp.fsum(reversed_row[i, j] for j in range(4)) for i in range(4)
        ),
        "stationarity": maxabs(direct * pi),
        "detailed_balance": maxabs(
            direct[i, j] * pi[j] - direct[j, i] * pi[i]
            for i in range(4) for j in range(4)
        ),
        "mapped_eigenvalues": maxabs(
            eigenvalues[i] - mapped_eigenvalues[i] for i in range(4)
        ),
        "mapped_amplitudes": max(
            abs(abs(b_hot) - abs(mapped_hot)),
            abs(abs(b_cool) - abs(mapped_cool)),
        ),
    }
    return {
        "precision": decimal_digits,
        "energies": energies,
        "downward_rates": downward,
        "beta_hot": beta_hot,
        "beta_cool": beta_cool,
        "triplets": triples,
        "eigenvalues": list(eigenvalues),
        "relative_slow_gap": (eigenvalues[2] - eigenvalues[1]) / (-eigenvalues[0]),
        "amplitude_hot": abs(b_hot),
        "amplitude_cool": abs(b_cool),
        "amplitude_reversal": abs(b_cool) - abs(b_hot),
        "initial_KL_hot": relative_entropy(g_hot, pi),
        "initial_KL_cool": relative_entropy(g_cool, pi),
        "time_evolution": evolution,
        "matrix_checks": matrix_checks,
        "modal_residuals": residuals,
        "mapped_modal_residuals": mapped_residuals,
    }


def serialize(value):
    if isinstance(value, mp.mpf):
        return mp.nstr(value, 70)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def main() -> None:
    low = evaluate(100)
    high = evaluate(180)
    stability = {
        name: abs(low[name] - high[name])
        for name in (
            "amplitude_hot", "amplitude_cool", "amplitude_reversal",
            "relative_slow_gap",
        )
    }
    residuals = list(high["matrix_checks"].values())
    residuals += list(high["modal_residuals"].values())
    residuals += list(high["mapped_modal_residuals"].values())
    checks = {
        "all_four_applicable_predicates_negative": all(
            row["applicable_value"] < 0 for row in high["triplets"]
        ),
        "minimum_normalized_margin_above_1e_3": min(
            row["exclusion_margin_over_rate_sum"] for row in high["triplets"]
        ) > mp.mpf("1e-3"),
        "simple_slow_mode": high["relative_slow_gap"] > mp.mpf("1e-2"),
        "amplitude_reversal_above_2e_4": high["amplitude_reversal"] > mp.mpf("2e-4"),
        "hotter_state_initially_farther": high["initial_KL_hot"] > high["initial_KL_cool"],
        "late_time_order_reversed": high["time_evolution"][-1]["D_hot_minus_D_cool"] < 0,
        "matrix_and_modal_residuals_below_1e_170": max(residuals) < mp.mpf("1e-170"),
        "precision_stability_below_1e_90": max(stability.values()) < mp.mpf("1e-90"),
    }
    if not all(checks.values()):
        raise SystemExit("one or more reproduction checks failed")
    record = {
        "scope": (
            "One controlled-numerical four-level finite-bath cooling witness; "
            "not a directed-rounding proof, heating classification, or all-N theorem."
        ),
        "precision_decimal_digits": [100, 180],
        "checks": checks,
        "precision_stability": stability,
        "high_precision_result": high,
    }
    OUTPUT.write_text(json.dumps(serialize(record), indent=2) + "\n", encoding="utf-8")
    for name in checks:
        print(f"PASS {name}")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
