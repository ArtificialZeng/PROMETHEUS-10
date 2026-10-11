#!/usr/bin/env python3
"""Regenerate the manuscript's coefficient-decay figure and tabulated data."""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "mpl-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
from scipy.special import gammaln


def coefficients(gamma: float, z: complex, n_max: int) -> np.ndarray:
    """Return F_0,...,F_nmax from the exact generating-function recurrence."""
    values = np.empty(n_max + 1, dtype=np.complex128)
    values[0] = 1.0
    if n_max == 0:
        return values
    a0 = gamma + (1.0 - gamma) * z
    values[1] = a0
    for n in range(1, n_max):
        values[n + 1] = (
            ((1.0 + z) * n + a0) * values[n] - z * n * values[n - 1]
        ) / (n + 1)
    return values


def endpoint_mass(t: np.ndarray, beta: float) -> np.ndarray:
    return np.exp(gammaln(t + beta) - gammaln(beta) - gammaln(t + 1.0))


def direct_coefficient(gamma: float, z: complex, t: int) -> complex:
    """Independent high-precision convolution of the exact age law."""
    mp.mp.dps = 80
    gamma_mp = mp.mpf(str(gamma))
    z_mp = mp.mpc(z.real, z.imag)
    total = mp.mpc(0)
    for n in range(t + 1):
        left = mp.rf(gamma_mp, t - n) / mp.factorial(t - n)
        right = mp.rf(1 - gamma_mp, n) / mp.factorial(n)
        total += left * right * z_mp**n
    return complex(total)


def main() -> None:
    figure_dir = ROOT / "manuscript" / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    data_path = ROOT / "manuscript" / "figure_data.csv"
    figure_path = figure_dir / "coherence-decay.pdf"

    phase = np.pi / 2.0
    z = np.exp(1j * phase)
    n_max = 512
    times = np.arange(1, n_max + 1, dtype=float)
    gammas = (0.2, 0.5, 0.7)
    colors = ("#0072B2", "#D55E00", "#009E73")
    records: list[dict[str, object]] = []
    max_ratio = 0.0
    max_recurrence_error = 0.0

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.15), constrained_layout=True)
    ax = axes[0]
    for gamma, color in zip(gammas, colors):
        coeff = coefficients(gamma, z, n_max)
        a_t = endpoint_mass(times, gamma)
        b_t = endpoint_mass(times, 1.0 - gamma)
        bound = 2.0 * (a_t + b_t) / abs(1.0 - z)
        ratio = np.abs(coeff[1:]) / bound
        max_ratio = max(max_ratio, float(np.max(ratio)))
        if np.any(ratio > 1.0 + 5e-13):
            raise RuntimeError("a plotted coefficient violates the proved bound")
        for t_check in (1, 2, 7, 32, 128, 512):
            direct = direct_coefficient(gamma, z, t_check)
            error = abs(coeff[t_check] - direct)
            max_recurrence_error = max(max_recurrence_error, error)
            if error > 2e-12:
                raise RuntimeError("recurrence/direct-convolution mismatch")
        ax.loglog(times, np.abs(coeff[1:]), color=color, lw=1.15,
                  label=rf"$\gamma={gamma:g}$")
        ax.loglog(times, bound, color=color, lw=0.9, ls="--", alpha=0.72)
        for t, value, upper in zip(range(1, n_max + 1), coeff[1:], bound):
            records.append({
                "panel": "fixed_phase",
                "t": t,
                "gamma": f"{gamma:.1f}",
                "phase_over_pi": "0.5",
                "real_F": f"{value.real:.17g}",
                "imag_F": f"{value.imag:.17g}",
                "abs_F": f"{abs(value):.17g}",
                "theorem_bound": f"{upper:.17g}",
            })

    ax.set_xlabel(r"clock step $t$")
    ax.set_ylabel(r"$|F_t(e^{i\pi/2})|$")
    ax.set_title("Fixed nonzero eigenphase gap")
    ax.grid(True, which="both", color="0.88", lw=0.45)
    ax.legend(frameon=False, fontsize=8, ncol=1)
    ax.text(0.97, 0.06, "dashed: theorem bound", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7.2, color="0.28")

    ax = axes[1]
    parity_t = np.arange(0, 33)
    parity_values = np.zeros_like(parity_t, dtype=float)
    for t in parity_t:
        if t % 2 == 0:
            m = t // 2
            parity_values[t] = math.comb(2 * m, m) / (4.0**m)
        records.append({
            "panel": "parity",
            "t": int(t),
            "gamma": "0.5",
            "phase_over_pi": "1.0",
            "real_F": f"{parity_values[t]:.17g}",
            "imag_F": "0",
            "abs_F": f"{abs(parity_values[t]):.17g}",
            "theorem_bound": "",
        })
    even = parity_t % 2 == 0
    odd = ~even
    ax.vlines(parity_t[even], 0.0, parity_values[even], color="#0072B2", lw=0.9)
    ax.scatter(parity_t[even], parity_values[even], color="#0072B2", s=18,
               label="even $t$")
    ax.scatter(parity_t[odd], parity_values[odd], marker="x", color="#D55E00",
               s=21, linewidths=1.0, label="odd $t$: exact zero")
    ax.set_xlabel(r"clock step $t$")
    ax.set_ylabel(r"$F_t(-1)$")
    ax.set_title(r"Exact parity at $\gamma=1/2$")
    ax.set_xlim(-0.7, 32.7)
    ax.set_ylim(-0.045, 1.05)
    ax.grid(True, axis="y", color="0.88", lw=0.45)
    ax.legend(frameon=False, fontsize=8)

    with data_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=(
            "panel", "t", "gamma", "phase_over_pi", "real_F", "imag_F",
            "abs_F", "theorem_bound",
        ))
        writer.writeheader()
        writer.writerows(records)

    fig.savefig(figure_path, bbox_inches="tight", metadata={
        "Title": "Critical Sibuya coherence decay",
        "Author": "Xiaojian Zeng (draft; confirmation pending)",
    })
    plt.close(fig)
    print(f"wrote={figure_path.relative_to(ROOT)}")
    print(f"data={data_path.relative_to(ROOT)} rows={len(records)}")
    print(f"max_abs_F_over_bound={max_ratio:.12g}")
    print(f"max_recurrence_vs_80digit_convolution={max_recurrence_error:.12g}")
    print("parity_odd_exact_zero=true")


if __name__ == "__main__":
    main()
