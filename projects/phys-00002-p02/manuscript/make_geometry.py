#!/usr/bin/env python3
"""Generate the manuscript's deterministic two-panel geometry schematic."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUT = HERE / "figures" / "geometry.pdf"


def unit(theta: np.ndarray | float) -> np.ndarray:
    theta = np.asarray(theta)
    return np.stack((np.cos(theta), np.sin(theta)), axis=-1)


def arrow(ax, vector, color, label=None, width=0.010, alpha=1.0, zorder=4):
    ax.arrow(
        0,
        0,
        vector[0],
        vector[1],
        width=width,
        head_width=0.075,
        head_length=0.09,
        length_includes_head=True,
        color=color,
        alpha=alpha,
        zorder=zorder,
    )
    if label:
        ax.text(
            1.10 * vector[0],
            1.10 * vector[1],
            label,
            color=color,
            ha="center",
            va="center",
            fontsize=9,
            zorder=zorder + 1,
        )


def prepare_axis(ax, title):
    t = np.linspace(0, 2 * np.pi, 500)
    circle = unit(t)
    ax.plot(circle[:, 0], circle[:, 1], color="#8c8c8c", lw=0.9, ls="--")
    ax.axhline(0, color="#c5c5c5", lw=0.6, zorder=0)
    ax.axvline(0, color="#c5c5c5", lw=0.6, zorder=0)
    ax.set_aspect("equal")
    ax.set_xlim(-1.23, 1.23)
    ax.set_ylim(-1.23, 1.23)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, fontsize=10, pad=2)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
        }
    )
    blue = "#0072B2"
    orange = "#D55E00"
    green = "#009E73"
    purple = "#7B3294"

    angles = np.asarray([0.0, 0.55, 1.45, 2.55])
    n = unit(angles)
    polygon = np.vstack((n, -n, n[0]))

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25), constrained_layout=True)

    ax = axes[0]
    prepare_axis(ax, "(a) Ordered measurement axes")
    ax.fill(polygon[:, 0], polygon[:, 1], color=blue, alpha=0.08, zorder=1)
    ax.plot(polygon[:, 0], polygon[:, 1], color="#666666", lw=1.0, zorder=2)
    half_path = np.vstack((n, -n[0]))
    ax.plot(half_path[:, 0], half_path[:, 1], color=orange, lw=2.5, zorder=3)
    for j, vector in enumerate(n, start=1):
        arrow(ax, 0.90 * vector, blue, rf"$\mathbf{{n}}_{j}$", width=0.007)
        ax.plot(vector[0], vector[1], "o", color=blue, ms=4, zorder=5)
        ax.plot(-vector[0], -vector[1], "o", mfc="white", mec="#666666", ms=3.6, zorder=3)
    ax.text(-0.43, 0.77, r"highlighted length $2D$", color=orange, fontsize=8.5)

    dvec = [n[0] - n[1], n[1] - n[2], n[2] - n[3], n[0] + n[3]]
    u = np.asarray([v / np.linalg.norm(v) for v in dvec])
    beta = np.unwrap(np.arctan2(u[:, 1], u[:, 0]))

    ax = axes[1]
    prepare_axis(ax, "(b) Ordered dual directions")
    arc = unit(np.linspace(beta[0], beta[-1], 250))
    ax.plot(arc[:, 0], arc[:, 1], color=green, lw=3.0, alpha=0.60, zorder=2)
    for j, vector in enumerate(u, start=1):
        arrow(ax, 0.95 * vector, green, rf"$\mathbf{{u}}_{j}$", width=0.007)
        ax.plot(vector[0], vector[1], "o", color=green, ms=4, zorder=5)

    witness = u[0] + u[3] - u[2]
    arrow(ax, witness, purple, r"$\mathbf{u}_1+\mathbf{u}_4-\mathbf{u}_3$", width=0.009, zorder=6)
    ax.text(0.10, -1.10, r"arc span $<\pi$", color=green, fontsize=8.5)
    ax.text(-1.14, 1.06, r"resultant lies in unit disk", color=purple, fontsize=8.2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUT,
        bbox_inches="tight",
        metadata={"Creator": "Matplotlib 3.11.2", "CreationDate": None, "ModDate": None},
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
