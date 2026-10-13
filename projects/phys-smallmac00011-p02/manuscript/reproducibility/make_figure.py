#!/usr/bin/env python3
"""Regenerate the representative fixed-ray capacity data and Figure 1.

The positive-overlap example mixes the reverse-depolarizing endpoint with
the pure replacement channel rho -> |0><0| Tr(rho).  Axial symmetry and
concavity reduce C_E to a one-dimensional input optimization; the two axial
pure inputs attain the Holevo capacity for this shifted-sphere channel.

The zero-overlap example uses Q=diag(0.6,0.3,0.1), for which the exact Pauli
capacity formulas apply.  The calculations are diagnostics of the analytic
proof, not interval certificates.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar


I2 = np.eye(2, dtype=complex)
X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
P0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
P1 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)


def h2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


CHI_D = 1.0 - h2(2.0 / 3.0)
CE_D = 2.0 - math.log2(3.0)
K_STAR = CE_D / CHI_D


def entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2.0)
    vals = np.clip(vals.real, 0.0, 1.0)
    nz = vals[vals > 1.0e-15]
    return float(-np.sum(nz * np.log2(nz)))


def state_z(z: float) -> np.ndarray:
    return (I2 + z * Z) / 2.0


def choi_from_kraus(kraus: list[np.ndarray]) -> np.ndarray:
    omega = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex)
    out = np.zeros((4, 4), dtype=complex)
    for operator in kraus:
        vec = np.kron(I2, operator) @ omega
        out += np.outer(vec, vec.conj())
    return out


J_D = choi_from_kraus([X / math.sqrt(3.0), Y / math.sqrt(3.0), Z / math.sqrt(3.0)])
J_REPLACEMENT = np.kron(I2, P0)


def output_from_choi(choi: np.ndarray, rho: np.ndarray) -> np.ndarray:
    blocks = choi.reshape(2, 2, 2, 2)
    return np.einsum("ij,ikjl->kl", rho, blocks)


def canonical_joint_output(choi: np.ndarray, rho: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh(rho.T)
    root = (vecs * np.sqrt(np.clip(2.0 * vals, 0.0, None))) @ vecs.conj().T
    transform = np.kron(root, I2)
    return transform @ (choi / 2.0) @ transform.conj().T


def mutual_information(choi: np.ndarray, z: float) -> float:
    rho = state_z(z)
    return entropy(rho) + entropy(output_from_choi(choi, rho)) - entropy(
        canonical_joint_output(choi, rho)
    )


def replacement_ray_capacities(epsilon: float) -> tuple[float, float, float]:
    choi = (1.0 - epsilon) * J_D + epsilon * J_REPLACEMENT
    ce_fit = minimize_scalar(
        lambda z: -mutual_information(choi, z),
        bounds=(-0.999999999, 0.999999999),
        method="bounded",
        options={"xatol": 2.0e-13, "maxiter": 1000},
    )
    ce = -float(ce_fit.fun)

    out_plus = output_from_choi(choi, P0)
    out_minus = output_from_choi(choi, P1)
    ent_plus = entropy(out_plus)
    ent_minus = entropy(out_minus)
    chi_fit = minimize_scalar(
        lambda weight: -(
            entropy(weight * out_plus + (1.0 - weight) * out_minus)
            - weight * ent_plus
            - (1.0 - weight) * ent_minus
        ),
        bounds=(0.0, 1.0),
        method="bounded",
        options={"xatol": 2.0e-14, "maxiter": 1000},
    )
    chi = -float(chi_fit.fun)
    return ce, chi, float(ce_fit.x)


def zero_face_capacities(epsilon: float) -> tuple[float, float]:
    q = np.array([0.6, 0.3, 0.1], dtype=float)
    a = (1.0 - epsilon) / 3.0 + epsilon * q
    probabilities = (1.0 - a) / 2.0
    ce = 2.0 + float(np.sum(probabilities * np.log2(probabilities)))
    chi = 1.0 - h2((1.0 + float(np.max(a))) / 2.0)
    return ce, chi


def main() -> None:
    manuscript_dir = Path(__file__).resolve().parents[1]
    figure_dir = manuscript_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    data_path = Path(__file__).resolve().parent / "two_regime_scaling.csv"

    epsilons = np.logspace(-6.0, -2.0, 25)
    rows: list[dict[str, float]] = []
    for epsilon in epsilons:
        ce_pos, chi_pos, z_opt = replacement_ray_capacities(float(epsilon))
        ce_zero, chi_zero = zero_face_capacities(float(epsilon))
        gap_pos = K_STAR * chi_pos - ce_pos
        gap_zero = K_STAR * chi_zero - ce_zero
        rows.append(
            {
                "epsilon": float(epsilon),
                "ce_positive": ce_pos,
                "chi_positive": chi_pos,
                "z_opt_positive": z_opt,
                "gap_positive": gap_pos,
                "gap_positive_normalized": gap_pos
                / (epsilon * math.log2(1.0 / epsilon)),
                "ce_zero": ce_zero,
                "chi_zero": chi_zero,
                "gap_zero": gap_zero,
                "gap_zero_normalized": gap_zero / epsilon,
            }
        )

    with data_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75), constrained_layout=True)
    x = np.array([row["epsilon"] for row in rows])
    y_pos = np.array([row["gap_positive_normalized"] for row in rows])
    y_zero = np.array([row["gap_zero_normalized"] for row in rows])
    zero_limit = K_STAR * (0.6 - 1.0 / 3.0) / 2.0

    axes[0].semilogx(x, y_pos, "o-", color="#1f77b4", ms=3.0, lw=1.0)
    axes[0].axhline(0.25, color="black", ls="--", lw=1.0, label=r"$c_\Psi=1/4$")
    axes[0].set_xlabel(r"mixture weight $\epsilon$")
    axes[0].set_ylabel(r"$G/[\epsilon\log_2(1/\epsilon)]$")
    axes[0].set_title("(a) positive Bell overlap")
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].semilogx(x, y_zero, "s-", color="#d62728", ms=3.0, lw=1.0)
    axes[1].axhline(
        zero_limit,
        color="black",
        ls="--",
        lw=1.0,
        label=rf"$K_*(0.6-1/3)/2={zero_limit:.4f}$",
    )
    axes[1].set_xlabel(r"mixture weight $\epsilon$")
    axes[1].set_ylabel(r"$G/\epsilon$")
    axes[1].set_title("(b) zero-overlap face")
    axes[1].legend(frameon=False, fontsize=8)
    for axis in axes:
        axis.grid(alpha=0.22, linewidth=0.5)

    pdf_path = figure_dir / "two_regime_scaling.pdf"
    png_path = figure_dir / "two_regime_scaling.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=220)
    plt.close(fig)

    print(f"endpoint chi={CHI_D:.15f}")
    print(f"endpoint CE={CE_D:.15f}")
    print(f"K_star={K_STAR:.15f}")
    print(f"positive normalized at epsilon={rows[0]['epsilon']:.1e}: "
          f"{rows[0]['gap_positive_normalized']:.12f} (limit 0.25)")
    print(f"zero-face normalized at epsilon={rows[0]['epsilon']:.1e}: "
          f"{rows[0]['gap_zero_normalized']:.12f} (limit {zero_limit:.12f})")
    print(f"wrote {data_path.relative_to(manuscript_dir)}")
    print(f"wrote {pdf_path.relative_to(manuscript_dir)}")
    print(f"wrote {png_path.relative_to(manuscript_dir)}")


if __name__ == "__main__":
    main()
