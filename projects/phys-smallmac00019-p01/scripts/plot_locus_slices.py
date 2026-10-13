"""Regenerate the two exact obstruction slices used in the manuscript.

The plotted quantity is derived directly from
R = -64 c^2 d^2 (a^2-f^2) (b^2-e^2).  The plot is illustrative;
no sampled or fitted data enter the spectral-locus proof.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def signed_log(value: np.ndarray) -> np.ndarray:
    """A dimensionless, odd, monotone transform that preserves the zero set."""

    return np.sign(value) * np.log10(1.0 + np.abs(value))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="manuscript/figures/locus-slices.pdf",
        help="Project-relative or absolute output PDF path",
    )
    args = parser.parse_args()

    coordinate = np.linspace(-6.0, 6.0, 601)
    horizontal, vertical = np.meshgrid(coordinate, coordinate, indexing="xy")
    values = signed_log(horizontal**2 - vertical**2)
    vmax = float(np.max(np.abs(values)))

    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.15), constrained_layout=True)
    labels = (
        (r"$a/E_0$", r"$f/E_0$", r"(a) $a=\pm f$ slice"),
        (r"$b/E_0$", r"$e/E_0$", r"(b) $b=\pm e$ slice"),
    )
    image = None
    for axis, (xlabel, ylabel, title) in zip(axes, labels, strict=True):
        image = axis.pcolormesh(
            coordinate,
            coordinate,
            values,
            shading="auto",
            cmap="coolwarm",
            vmin=-vmax,
            vmax=vmax,
            rasterized=True,
        )
        axis.plot(coordinate, coordinate, "k--", linewidth=1.15)
        axis.plot(coordinate, -coordinate, "k--", linewidth=1.15)
        axis.set_aspect("equal")
        axis.set_xlim(-6.0, 6.0)
        axis.set_ylim(-6.0, 6.0)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_title(title, fontsize=10)
        axis.tick_params(direction="in", top=True, right=True)

    assert image is not None
    colorbar = fig.colorbar(image, ax=axes, shrink=0.88, pad=0.03)
    colorbar.set_label(r"$\operatorname{sgn}(r)\log_{10}(1+|r|)$")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output,
        format="pdf",
        dpi=300,
        metadata={
            "Title": "Exact obstruction slices",
            "Author": "Xiaojian Zeng",
            "Creator": "Matplotlib 3.11.2",
        },
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
