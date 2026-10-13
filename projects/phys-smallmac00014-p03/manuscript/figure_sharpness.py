#!/usr/bin/env python3
"""Generate the exact sharpness-family figure and its tabulated data."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
H_MARKERS = np.array([0.0, 2.0, 8.0, 16.0, 32.0])


def ratio(h: np.ndarray) -> np.ndarray:
    """Exact A_2/(k_0 B_2) for the antisymmetric sharpness mode."""
    return 2.0 + np.exp(-h / 2.0)


def main() -> None:
    h = np.linspace(0.0, 32.0, 641)
    y = ratio(h)
    marker_y = ratio(H_MARKERS)

    with (OUT / "sharpness-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["H", "A2_over_k0_B2", "strict_margin"])
        for hh, yy in zip(H_MARKERS, marker_y, strict=True):
            writer.writerow([f"{hh:.1f}", f"{yy:.15g}", f"{yy - 2.0:.15g}"])

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9.0,
        "axes.labelsize": 9.0,
        "legend.fontsize": 8.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "pdf.fonttype": 42,
    })
    fig, ax = plt.subplots(figsize=(5.55, 3.35), constrained_layout=True)
    ax.plot(h, y, color="#1f5a99", linewidth=2.0, label=r"$2+\exp(-H/2)$")
    ax.scatter(H_MARKERS, marker_y, color="#b33b2e", s=24, zorder=3,
               label="tabulated exact values")
    ax.axhline(2.0, color="black", linewidth=1.0, linestyle="--",
               label="sharp infimum")
    ax.set_xlim(0.0, 32.0)
    ax.set_ylim(1.97, 3.04)
    ax.set_xlabel(r"third-state offset $H$")
    ax.set_ylabel(r"$A_2/(k_0 B_2)$")
    ax.grid(True, alpha=0.22, linewidth=0.6)
    ax.legend(loc="upper right", frameon=False)

    inset = ax.inset_axes([0.51, 0.36, 0.43, 0.36])
    inset.semilogy(h, y - 2.0, color="#1f5a99", linewidth=1.4)
    inset.scatter(H_MARKERS, marker_y - 2.0, color="#b33b2e", s=12, zorder=3)
    inset.set_xlim(0.0, 32.0)
    inset.set_ylim(5e-8, 2.0)
    inset.set_xlabel(r"$H$", labelpad=0)
    inset.set_ylabel(r"ratio $-2$", labelpad=1)
    inset.grid(True, which="both", alpha=0.18, linewidth=0.45)

    fig.savefig(OUT / "sharpness.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()

