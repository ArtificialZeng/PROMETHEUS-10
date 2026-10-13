#!/usr/bin/env python3
"""Generate the exact finite-depth crossing figure and its tabulated data.

The plotted quantities are closed-form consequences of the accepted recurrence;
no fit or digitized source data enter this figure.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"
DATA = ROOT / "data"


def crossing_row(k: int) -> dict[str, object]:
    n = k - 3
    j_abs = 3.0 ** (-n / 2.0)
    multiplicity = (3 ** (k - 2) + 1) // 2
    numerator = 5 ** (n + 1) - 6 * 3**n + 1
    denominator = 5 ** (n + 1) + 6 * 3**n + 1
    slope = numerator / denominator
    separation = 12 * 3**n / denominator
    return {
        "k": k,
        "J_abs": j_abs,
        "source_lambda": j_abs / 2.0,
        "crossing_multiplicity_per_eigenvalue_sign": multiplicity,
        "dispersive_slope_numerator": numerator,
        "dispersive_slope_denominator": denominator,
        "dispersive_slope": slope,
        "x_separation_coefficient": separation,
    }


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if expected and Path(os.sys.executable).resolve() != Path(expected).resolve():
        raise RuntimeError(f"wrong interpreter: {os.sys.executable}; expected {expected}")

    FIGURES.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    rows = [crossing_row(k) for k in range(3, 13)]
    data_path = DATA / "crossing_data.csv"
    with data_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.figsize": (7.15, 3.0),
            "savefig.bbox": "tight",
        }
    )
    fig, (ax0, ax1) = plt.subplots(1, 2)

    ks = [int(row["k"]) for row in rows]
    js = [float(row["J_abs"]) for row in rows]
    lambdas = [float(row["source_lambda"]) for row in rows]
    slopes = [float(row["dispersive_slope"]) for row in rows]
    separations = [float(row["x_separation_coefficient"]) for row in rows]

    ax0.axhspan(0.25, 0.5, color="#d9d9d9", alpha=0.75, label=r"fixed $I_+$")
    ax0.semilogy(ks, js, "o-", color="#0072B2", label=r"$|J_k|$")
    ax0.semilogy(ks, lambdas, "s--", color="#D55E00", label=r"$\lambda_k$")
    ax0.scatter([5], [1 / 3], s=72, facecolors="none", edgecolors="black", zorder=5)
    ax0.set_xlabel(r"depth $k$")
    ax0.set_ylabel("crossing location")
    ax0.set_xticks(ks[::2])
    ax0.grid(True, which="both", alpha=0.25)
    ax0.legend(frameon=False, loc="upper right")

    ax1.plot(ks, slopes, "o-", color="#009E73", label=r"$dx_{\rm disp}/dJ$")
    ax1.plot(ks, separations, "s--", color="#CC79A7", label="linear separation")
    ax1.axhline(1.0, color="black", linewidth=0.8, alpha=0.6, label="flat-band slope")
    ax1.set_xlabel(r"depth $k$")
    ax1.set_ylabel("dimensionless coefficient")
    ax1.set_xticks(ks[::2])
    ax1.set_ylim(-0.04, 1.04)
    ax1.grid(True, alpha=0.25)
    ax1.legend(frameon=False, loc="center right")

    fig.tight_layout(w_pad=2.0)
    fig.savefig(FIGURES / "crossing_scale.pdf")
    fig.savefig(FIGURES / "crossing_scale.png", dpi=220)
    plt.close(fig)

    if not math.isclose(rows[2]["J_abs"], 1 / 3, rel_tol=0.0, abs_tol=1e-15):
        raise RuntimeError("k=5 landmark regression")
    if rows[3]["crossing_multiplicity_per_eigenvalue_sign"] != 41:
        raise RuntimeError("k=6 multiplicity regression")
    print(f"wrote {data_path.relative_to(ROOT.parent)}")
    print(f"wrote {(FIGURES / 'crossing_scale.pdf').relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
