#!/usr/bin/env python3
"""Regenerate the manuscript figure from the frozen GADC equations.

Panel (a) evaluates the published one-use optimum and independently computes
the ergotropy of the corresponding two-copy product output.  The theorem in
the manuscript identifies this product value with the unrestricted two-use
optimum.  Panel (b) applies all sixteen product Kraus operators to the
phase-sensitive pair of equal-population inputs used in the proof dossier.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from evidence.method_a_kraus import apply_one, apply_two, ergotropy  # noqa: E402


def one_use_optimum(e: float, gamma: float, eta: float) -> tuple[float, float]:
    """Return the optimizing excitation x and W1 for budget e."""
    if gamma == 0.0:
        x_star = 1.0
    else:
        radicand = 1.0 - 4.0 * gamma * eta * (1.0 - eta)
        x_star = min(1.0, eta + np.sqrt(radicand) / (2.0 * np.sqrt(gamma)))
    x = min(e, x_star)
    q = 1.0 - gamma
    gap = np.sqrt(
        (1.0 - 2.0 * eta * gamma) ** 2
        + 4.0 * gamma * q * (2.0 * eta - x) * x
    )
    return x, q * x + eta * gamma - 0.5 + 0.5 * gap


def write_csv(path: Path, header: list[str], rows: list[list[float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def build(output: Path, curve_data: Path, phase_data: Path) -> dict[str, float]:
    gamma, eta = 0.55, 0.20
    energies = np.linspace(0.0, 1.0, 401)
    curve_rows: list[list[float]] = []
    product_errors: list[float] = []

    for e in energies:
        x, w1 = one_use_optimum(float(e), gamma, eta)
        vector = np.array([np.sqrt(1.0 - x), np.sqrt(x)], dtype=np.complex128)
        rho = np.outer(vector, vector.conj())
        sigma = apply_one(rho, gamma, eta)
        product_half = 0.5 * ergotropy(
            np.kron(sigma, sigma), np.array([0.0, 1.0, 1.0, 2.0])
        )
        product_errors.append(abs(product_half - w1))
        curve_rows.append([float(e), x, w1, product_half])

    phases = np.linspace(0.0, 2.0 * np.pi, 361)
    phase_rows: list[list[float]] = []
    purities: list[float] = []
    for delta in phases:
        vector = np.array([1.0, 1.0, 1.0, np.exp(1j * delta)]) / 2.0
        rho = np.outer(vector, vector.conj())
        sigma = apply_two(rho, 0.5, 0.25)
        purity = float(np.real(np.trace(sigma @ sigma)))
        purities.append(purity)
        phase_rows.append([float(delta), purity])

    output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        curve_data,
        ["budget_e", "one_use_optimizer_x", "W1_analytic", "product_W2_over_2"],
        curve_rows,
    )
    write_csv(phase_data, ["invariant_phase_delta", "output_purity"], phase_rows)

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "pdf.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75), constrained_layout=True)

    ax = axes[0]
    w1_values = np.array([row[2] for row in curve_rows])
    product_values = np.array([row[3] for row in curve_rows])
    ax.plot(energies, w1_values, color="#1f77b4", lw=1.8, label=r"$W_1(e)$")
    ax.plot(
        energies[::32],
        product_values[::32],
        linestyle="none",
        marker="o",
        markersize=3.2,
        markerfacecolor="white",
        markeredgecolor="#d62728",
        label=r"${\cal W}(\sigma_*^{\otimes2},H_2)/2$",
    )
    ax.set_xlabel(r"per-cell input budget $e$")
    ax.set_ylabel(r"ergotropy per cell")
    ax.set_title(r"$\gamma=0.55,\ \eta=0.20$")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(bottom=0.0)
    ax.grid(alpha=0.22, linewidth=0.6)
    ax.legend(frameon=False, loc="lower right")
    ax.text(
        0.04,
        0.94,
        r"theorem: $W_2(e)/2=W_1(e)$",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
    )

    ax = axes[1]
    ax.plot(phases / np.pi, purities, color="#2ca02c", lw=1.8)
    ax.scatter(
        [0.0, 1.0],
        [625.0 / 1024.0, 417.0 / 1024.0],
        color=["#1f77b4", "#d62728"],
        s=18,
        zorder=3,
    )
    ax.annotate(r"$625/1024$", (0.0, 625.0 / 1024.0), xytext=(8, -4),
                textcoords="offset points", fontsize=8)
    ax.annotate(r"$417/1024$", (1.0, 417.0 / 1024.0), xytext=(7, 4),
                textcoords="offset points", fontsize=8)
    ax.set_xlabel(r"invariant phase $\delta/\pi$")
    ax.set_ylabel(r"two-use output purity $\mathrm{Tr}\,\sigma^2$")
    ax.set_title(r"$\gamma=1/2,\ \eta=1/4$; equal populations")
    ax.set_xlim(0.0, 2.0)
    ax.grid(alpha=0.22, linewidth=0.6)

    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)

    diagnostics = {
        "max_product_identity_error": float(max(product_errors)),
        "purity_delta_0_error": float(abs(purities[0] - 625.0 / 1024.0)),
        "purity_delta_pi_error": float(abs(purities[180] - 417.0 / 1024.0)),
    }
    return diagnostics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_DIR / "manuscript/figures/gadc_two_use_summary.pdf",
    )
    parser.add_argument(
        "--curve-data",
        type=Path,
        default=PROJECT_DIR / "reproducibility/figure_curve.csv",
    )
    parser.add_argument(
        "--phase-data",
        type=Path,
        default=PROJECT_DIR / "reproducibility/figure_phase.csv",
    )
    args = parser.parse_args()
    diagnostics = build(args.output, args.curve_data, args.phase_data)
    for key, value in diagnostics.items():
        print(f"{key}={value:.17g}")


if __name__ == "__main__":
    main()
