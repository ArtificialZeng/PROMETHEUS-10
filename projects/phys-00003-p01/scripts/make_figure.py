#!/usr/bin/env python3
"""Regenerate the thermally normalized quotient-spectrum figure and CSV data.

The plotted grid is illustrative only.  Positivity in the paper follows from
the exact rational-function certificate in ``verify_quotient.py``.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"


def components(a: np.ndarray, u: np.ndarray):
    """Return A, B, C, Delta, and G from the exact quotient formula."""
    h = 16 * a**2 + 32 * a * u + 24 * a + 16 * u**2 + 40 * u + 9
    p0 = (
        448 * a**5
        + 2944 * a**4 * u
        + 1700 * a**4
        + 5568 * a**3 * u**2
        + 8220 * a**3 * u
        + 2683 * a**3
        + 4096 * a**2 * u**3
        + 12480 * a**2 * u**2
        + 8432 * a**2 * u
        + 1872 * a**2
        + 1024 * a * u**4
        + 6144 * a * u**3
        + 8256 * a * u**2
        + 3424 * a * u
        + 432 * a
        + 768 * u**4
        + 2304 * u**3
        + 1440 * u**2
        + 336 * u
        + 27
    )
    p2 = (
        10496 * a**7
        + 60928 * a**6 * u
        + 41024 * a**6
        + 147200 * a**5 * u**2
        + 235488 * a**5 * u
        + 70512 * a**5
        + 189440 * a**4 * u**3
        + 529920 * a**4 * u**2
        + 359932 * a**4 * u
        + 65772 * a**4
        + 136960 * a**3 * u**4
        + 591680 * a**3 * u**3
        + 702445 * a**3 * u**2
        + 278523 * a**3 * u
        + 28404 * a**3
        + 52736 * a**2 * u**5
        + 335040 * a**2 * u**4
        + 633102 * a**2 * u**3
        + 458033 * a**2 * u**2
        + 105507 * a**2 * u
        + 3564 * a**2
        + 8448 * a * u**6
        + 83424 * a * u**5
        + 251037 * a * u**4
        + 299256 * a * u**3
        + 142527 * a * u**2
        + 19332 * a * u
        + 4608 * u**6
        + 30960 * u**5
        + 61749 * u**4
        + 50670 * u**3
        + 16893 * u**2
        + 1620 * u
    )
    kval = (
        16 * a**2 + 32 * a * u + 12 * a + 16 * u**2 - 13 * u
    ) ** 2 + 4 * u * (20 * a + 20 * u + 3) ** 2
    aa = 2 * u * (5 * a + 4 * u + 1) / a**3
    bb = 16 * u * (4 * a + 4 * u + 1) / a**4
    delta = 32 * u**2 * p0 / (a**8 * (4 * a + 3) * h)
    cc = (delta + bb**2) / aa
    gg = 16 * u * p2 / (
        a**3
        * (4 * a + 3)
        * (4 * a + 3 * u + 3)
        * ((a + u) ** 2 + u)
        * kval
    )
    return aa, bb, cc, delta, gg


def normalized_spectrum(a: np.ndarray, u: np.ndarray):
    """Spectrum after c=(c0,a*c1,a*c2,a*c3)."""
    aa, bb, cc, delta, gg = components(a, u)
    trace_iso = aa + a**2 * cc / 2
    discriminant = np.sqrt((aa - a**2 * cc / 2) ** 2 + 2 * (a * bb) ** 2)
    lambda_iso_max = (trace_iso + discriminant) / 2
    # det of this orthonormal isotropic block is a^2*delta/2.  The
    # determinant-over-largest formula avoids subtractive cancellation.
    lambda_iso_min = (a**2 * delta / 2) / lambda_iso_max
    lambda_angular_min = a**2 * gg / 4
    lambda_angular_max = a**2 * gg / 2
    lambda_min = np.minimum(lambda_iso_min, lambda_angular_min)
    lambda_max = np.maximum(lambda_iso_max, lambda_angular_max)
    return lambda_min, lambda_max, lambda_max / lambda_min


def main():
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    grid = np.logspace(-2, 2, 81)
    a, u = np.meshgrid(grid, grid, indexing="xy")
    lambda_min, lambda_max, condition = normalized_spectrum(a, u)
    if not np.all(np.isfinite(lambda_min)) or not np.all(lambda_min > 0):
        raise RuntimeError("nonpositive or nonfinite plotted eigenvalue")

    csv_path = FIGURE_DIR / "quotient_spectrum.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("a", "u", "lambda_min", "lambda_max", "condition_number"))
        for av, uv, lo, hi, cond in zip(
            a.ravel(), u.ravel(), lambda_min.ravel(), lambda_max.ravel(), condition.ravel()
        ):
            writer.writerow((f"{av:.17g}", f"{uv:.17g}", f"{lo:.17g}", f"{hi:.17g}", f"{cond:.17g}"))

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.85), constrained_layout=True)
    extent = (-2, 2, -2, 2)
    image0 = axes[0].imshow(
        np.log10(lambda_min), origin="lower", extent=extent, aspect="auto", cmap="viridis"
    )
    axes[0].set_title(r"Smallest eigenvalue of $\widetilde Q_\Delta$")
    axes[0].set_xlabel(r"$\log_{10} a$")
    axes[0].set_ylabel(r"$\log_{10} u$")
    color0 = fig.colorbar(image0, ax=axes[0], pad=0.02)
    color0.set_label(r"$\log_{10}\lambda_{\min}$")

    image1 = axes[1].imshow(
        np.log10(condition), origin="lower", extent=extent, aspect="auto", cmap="magma"
    )
    axes[1].set_title(r"Condition number of $\widetilde Q_\Delta$")
    axes[1].set_xlabel(r"$\log_{10} a$")
    axes[1].set_ylabel(r"$\log_{10} u$")
    color1 = fig.colorbar(image1, ax=axes[1], pad=0.02)
    color1.set_label(r"$\log_{10}\kappa_2$")

    metadata = {
        "Title": "Thermally normalized quotient spectrum",
        "Author": "Xiaojian Zeng (draft; confirmation pending)",
        "Subject": "Numerical visualization of an exact positivity certificate",
    }
    fig.savefig(FIGURE_DIR / "quotient_spectrum.pdf", metadata=metadata)
    fig.savefig(FIGURE_DIR / "quotient_spectrum.png", dpi=240, metadata=metadata)
    plt.close(fig)
    print(f"grid_points={grid.size * grid.size}")
    print(f"lambda_min_range=({lambda_min.min():.17g},{lambda_min.max():.17g})")
    print(f"condition_range=({condition.min():.17g},{condition.max():.17g})")
    print("status=PASS")


if __name__ == "__main__":
    main()
