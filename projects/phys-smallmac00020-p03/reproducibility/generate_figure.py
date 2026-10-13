#!/usr/bin/env python3
"""Regenerate the numerical data and figure used in the manuscript.

The full-chain edge energies are evaluated stably from the two largest
singular values of the rescaled inverse matrix M_N derived in the paper.
No random data or fitted parameters are used.
"""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "phys-00020-p03-matplotlib")
)

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "reproducibility" / "edge_splittings.csv"
FIGURE_PATH = ROOT / "manuscript" / "edge_splittings.pdf"


def finite_sums(n: int, r: float) -> tuple[float, float, float]:
    indices = np.arange(n, dtype=float)
    weights = r ** (2.0 * indices)
    return (
        float(np.sum(weights)),
        float(np.sum(indices * weights)),
        float(np.sum(indices * indices * weights)),
    )


def comparison_quantities(n: int, r: float) -> dict[str, float]:
    i = np.arange(n)[:, None]
    ell = np.arange(n)[None, :]
    degree = i + ell
    matrix = np.where(degree <= n - 1, (n - degree) * r**degree, 0.0)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    mu1, mu2 = singular_values[:2]

    a_n, b_n, d_n = finite_sums(n, r)
    delta_n = a_n * d_n - b_n * b_n
    m_n = n * a_n - 2.0 * b_n
    discriminant = np.sqrt(m_n * m_n + 4.0 * delta_n)
    phi1 = 0.5 * (discriminant + m_n)
    phi2 = 0.5 * (discriminant - m_n)

    t = np.arange(1, n - 1, dtype=float)
    epsilon_sq = np.sum((n - 1.0 - t) * t * t * r ** (2.0 * n + 2.0 * t))
    epsilon = float(np.sqrt(epsilon_sq))
    scale = r ** (n + 1)
    eta = (
        150.0
        * n
        * (4.0 / 5.0) ** (n + 1)
        * np.sqrt((n - 1.0) * (41.0 / 25.0) / (9.0 / 25.0) ** 3)
    )
    return {
        "E1_exact": scale / mu1,
        "E2_exact": scale / mu2,
        "E1_ritz": scale / phi1,
        "E2_ritz": scale / phi2,
        "E1_leading": (1.0 - r * r) * scale / n,
        "E2_leading": n * (1.0 - r * r) ** 3 * r ** (n - 1),
        "epsilon_over_phi1": epsilon / phi1,
        "epsilon_over_phi2": epsilon / phi2,
        "eta_uniform": eta,
    }


def main() -> None:
    r_values = (1.0 / 3.0, 1.0 / 2.0, 3.0 / 4.0, 4.0 / 5.0)
    rows: list[dict[str, float | int]] = []
    for r in r_values:
        for n in range(8, 101):
            row: dict[str, float | int] = {"N": n, "r": r}
            row.update(comparison_quantities(n, r))
            rows.append(row)

    fieldnames = ["N", "r", *comparison_quantities(8, 0.5).keys()]
    with DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    plt.rcParams.update(
        {
            "font.size": 8.2,
            "axes.labelsize": 8.5,
            "legend.fontsize": 7.3,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "lines.linewidth": 1.15,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75), constrained_layout=True)

    ns = np.arange(8, 81)
    half = [comparison_quantities(int(n), 0.5) for n in ns]
    axes[0].semilogy(ns, [x["E1_exact"] for x in half], color="#204a87", label=r"$E_{N,1}$")
    axes[0].semilogy(ns, [x["E2_exact"] for x in half], color="#a40000", label=r"$E_{N,2}$")
    axes[0].semilogy(
        ns,
        [x["E1_leading"] for x in half],
        "--",
        color="#729fcf",
        label=r"leading $E_{N,1}$",
    )
    axes[0].semilogy(
        ns,
        [x["E2_leading"] for x in half],
        "--",
        color="#ef2929",
        label=r"leading $E_{N,2}$",
    )
    axes[0].set_xlabel(r"chain length $N$")
    axes[0].set_ylabel(r"positive edge energy ($u_2=1$)")
    axes[0].set_title(r"(a) Two splitting scales at $r=1/2$")
    axes[0].legend(frameon=False, ncol=2, loc="upper right")
    axes[0].grid(alpha=0.2, which="both")

    colors = ("#4e9a06", "#204a87", "#75507b", "#a40000")
    bound_ns = np.arange(8, 101)
    for r, color in zip(r_values, colors):
        values = [comparison_quantities(int(n), r)["epsilon_over_phi2"] for n in bound_ns]
        axes[1].semilogy(bound_ns, values, color=color, label=rf"$r={r:.3g}$")
    theorem_ns = np.arange(61, 101)
    eta_values = [comparison_quantities(int(n), 0.5)["eta_uniform"] for n in theorem_ns]
    axes[1].semilogy(
        theorem_ns,
        eta_values,
        "k--",
        linewidth=1.4,
        label=r"uniform $eta_N$",
    )
    axes[1].axvline(61, color="0.5", linestyle=":", linewidth=0.8)
    axes[1].set_xlabel(r"chain length $N$")
    axes[1].set_ylabel(r"relative enclosure factor $epsilon_N/\phi_{2,N}$")
    axes[1].set_title("(b) Explicit inverse-tail control")
    axes[1].set_xlim(8, 100)
    axes[1].set_ylim(1e-20, 3.0)
    axes[1].legend(frameon=False, ncol=2, loc="lower left")
    axes[1].grid(alpha=0.2, which="both")

    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    print(f"wrote {DATA_PATH.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"wrote {FIGURE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
