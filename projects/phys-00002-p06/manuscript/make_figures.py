#!/usr/bin/env python3
"""Render the manuscript figure from the frozen machine-readable verifier output."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "build" / "mpl-cache"
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def panel_label(axis, label: str) -> None:
    axis.text(-0.16, 1.04, label, transform=axis.transAxes,
              fontsize=10, fontweight="bold", va="bottom")


def main() -> None:
    source = ROOT / "manuscript" / "witness-data.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = payload["high_precision_result"]

    plt.rcParams.update({
        "font.size": 8.0,
        "axes.labelsize": 8.5,
        "axes.titlesize": 8.5,
        "legend.fontsize": 7.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.2,
        "lines.markersize": 4.5,
    })
    blue = "#0072B2"
    orange = "#D55E00"
    green = "#009E73"

    fig, axes = plt.subplots(1, 3, figsize=(7.05, 2.25), constrained_layout=True)

    triples = result["triplets"]
    labels = [row["triplet"] for row in triples]
    margins = [float(row["exclusion_margin_over_rate_sum"]) for row in triples]
    axes[0].bar(labels, margins, color=green, width=0.62, edgecolor="black", linewidth=0.45)
    axes[0].set_yscale("log")
    axes[0].set_ylim(1.8e-3, 1.8)
    axes[0].set_xlabel("triplet")
    axes[0].set_ylabel(r"exclusion margin $m_{ijk}$")
    axes[0].grid(axis="y", which="both", alpha=0.22, linewidth=0.5)
    panel_label(axes[0], "(a)")

    beta = [float(result["beta_hot"]), float(result["beta_cool"])]
    amplitude = [float(result["amplitude_hot"]), float(result["amplitude_cool"])]
    axes[1].plot(beta, [1e3 * x for x in amplitude], color="0.3", zorder=1)
    axes[1].scatter(beta[0], 1e3 * amplitude[0], color=orange, label="hotter", zorder=2)
    axes[1].scatter(beta[1], 1e3 * amplitude[1], color=blue, label="cooler", zorder=2)
    axes[1].set_xlim(0.015, 0.055)
    axes[1].set_ylim(62.77, 63.12)
    axes[1].set_xlabel(r"preparation $\beta/\beta_b$")
    axes[1].set_ylabel(r"$10^3\mathcal{A}(\beta)$")
    axes[1].legend(frameon=False, loc="upper left")
    axes[1].grid(alpha=0.22, linewidth=0.5)
    panel_label(axes[1], "(b)")

    evolution = result["time_evolution"]
    times = [float(row["time"]) for row in evolution]
    delta = [float(row["D_hot_minus_D_cool"]) for row in evolution]
    axes[2].plot(times, delta, color="0.35", zorder=1)
    positive_t = [t for t, d in zip(times, delta) if d >= 0]
    positive_d = [d for d in delta if d >= 0]
    negative_t = [t for t, d in zip(times, delta) if d < 0]
    negative_d = [d for d in delta if d < 0]
    axes[2].scatter(positive_t, positive_d, color=blue, label=r"$D_h>D_c$", zorder=2)
    axes[2].scatter(negative_t, negative_d, color=orange, label=r"$D_h<D_c$", zorder=2)
    axes[2].axhline(0.0, color="black", linewidth=0.6)
    axes[2].set_yscale("symlog", linthresh=1e-13, linscale=0.8)
    axes[2].set_xlabel(r"dimensionless time $\gamma t$")
    axes[2].set_ylabel(r"$D_h-D_c$")
    axes[2].legend(frameon=False, loc="upper right")
    axes[2].grid(alpha=0.22, linewidth=0.5)
    panel_label(axes[2], "(c)")

    output = ROOT / "manuscript" / "fig-counterexample.pdf"
    fig.savefig(output, metadata={
        "Title": "Controlled numerical four-level Mpemba witness",
        "Creator": "Matplotlib script reading witness-data.json",
        "CreationDate": datetime(2026, 9, 12, tzinfo=timezone.utc),
        "ModDate": datetime(2026, 9, 12, tzinfo=timezone.utc),
    })
    plt.close(fig)
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
