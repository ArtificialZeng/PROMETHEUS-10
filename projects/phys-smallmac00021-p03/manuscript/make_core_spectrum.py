#!/usr/bin/env python3
"""Render the accepted 15-site corner core and its mirror-resolved spectrum."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "evidence" / "isolated-corner-polynomial.json"


def load_certificate() -> dict:
    with CERTIFICATE.open(encoding="utf-8") as stream:
        return json.load(stream)


def hamiltonian(data: dict, lam: float) -> np.ndarray:
    size = len(data["vertices"])
    matrix = np.zeros((size, size), dtype=float)
    weights = {
        "lambda": lam,
        "one_minus_lambda": 1.0 - lam,
        "one": 1.0,
    }
    for edge in data["edges"]:
        value = -weights[edge["kind"]]
        i, j = edge["i"], edge["j"]
        matrix[i, j] = value
        matrix[j, i] = value
    return matrix


def reflection_bases(reflection: list[int]) -> tuple[np.ndarray, np.ndarray]:
    size = len(reflection)
    even_columns: list[np.ndarray] = []
    odd_columns: list[np.ndarray] = []
    for i, partner in enumerate(reflection):
        if i > partner:
            continue
        if i == partner:
            vector = np.zeros(size)
            vector[i] = 1.0
            even_columns.append(vector)
        else:
            even = np.zeros(size)
            odd = np.zeros(size)
            even[i] = even[partner] = 1.0 / np.sqrt(2.0)
            odd[i] = 1.0 / np.sqrt(2.0)
            odd[partner] = -1.0 / np.sqrt(2.0)
            even_columns.append(even)
            odd_columns.append(odd)
    return np.column_stack(even_columns), np.column_stack(odd_columns)


def render(output: Path) -> None:
    data = load_certificate()
    figure, (graph_axis, spectrum_axis) = plt.subplots(
        1, 2, figsize=(7.2, 3.35), gridspec_kw={"width_ratios": [1.02, 1.35]}
    )

    positions = {
        vertex["index"]: np.array(
            [vertex["plot_coordinate"][0], np.sqrt(3.0) * vertex["plot_coordinate"][1]],
            dtype=float,
        )
        for vertex in data["vertices"]
    }
    styles = {
        "lambda": ("#2c7fb8", r"weight $\lambda$", "-"),
        "one_minus_lambda": ("#d95f0e", r"weight $1-\lambda$", "-"),
        "one": ("#303030", "fixed unit weight", "-"),
    }
    shown: set[str] = set()
    for edge in data["edges"]:
        kind = edge["kind"]
        color, label, line_style = styles[kind]
        left, right = positions[edge["i"]], positions[edge["j"]]
        graph_axis.plot(
            [left[0], right[0]],
            [left[1], right[1]],
            color=color,
            linestyle=line_style,
            linewidth=2.1,
            solid_capstyle="round",
            label=label if kind not in shown else None,
            zorder=1,
        )
        shown.add(kind)
    coordinates = np.array(list(positions.values()))
    graph_axis.scatter(
        coordinates[:, 0], coordinates[:, 1], s=29, facecolor="white",
        edgecolor="black", linewidth=0.8, zorder=3
    )
    for index, point in positions.items():
        graph_axis.annotate(
            str(index), point, xytext=(0, 5), textcoords="offset points",
            ha="center", va="bottom", fontsize=6.1
        )
    axis_x = np.linspace(0.0, 16.0, 100)
    graph_axis.plot(axis_x, axis_x / np.sqrt(3.0), "--", color="#777777", linewidth=0.8)
    graph_axis.set_aspect("equal")
    graph_axis.axis("off")
    graph_axis.set_title("(a) Raster-defined corner core", loc="left", fontsize=9)
    graph_axis.legend(loc="upper left", fontsize=6.4, frameon=False, handlelength=2.1)

    even_basis, odd_basis = reflection_bases(data["reflection"])
    lambdas = np.linspace(0.0, 1.0, 501)
    even_levels = []
    odd_levels = []
    for lam in lambdas:
        matrix = hamiltonian(data, float(lam))
        even_levels.append(np.linalg.eigvalsh(even_basis.T @ matrix @ even_basis))
        odd_levels.append(np.linalg.eigvalsh(odd_basis.T @ matrix @ odd_basis))
    even_levels = np.asarray(even_levels)
    odd_levels = np.asarray(odd_levels)
    for column in range(even_levels.shape[1]):
        spectrum_axis.plot(
            lambdas, even_levels[:, column], color="#2166ac", linewidth=0.9,
            alpha=0.92, label="mirror even" if column == 0 else None
        )
    for column in range(odd_levels.shape[1]):
        spectrum_axis.plot(
            lambdas, odd_levels[:, column], color="#b2182b", linewidth=0.9,
            alpha=0.88, label="mirror odd" if column == 0 else None
        )
    spectrum_axis.axhline(1.0, color="#222222", linestyle="--", linewidth=0.75)
    spectrum_axis.annotate(
        "two fixed roots at $E=1$",
        xy=(0.63, 1.0), xytext=(0.43, 1.62), fontsize=7.0,
        arrowprops={"arrowstyle": "->", "lw": 0.65, "color": "#333333"},
    )
    spectrum_axis.set_xlim(0.0, 1.0)
    spectrum_axis.set_ylim(-2.45, 2.45)
    spectrum_axis.set_xlabel(r"interpolation $\lambda$")
    spectrum_axis.set_ylabel(r"energy $E/t'$", labelpad=2)
    spectrum_axis.set_title("(b) Mirror-resolved core spectrum", loc="left", fontsize=9)
    spectrum_axis.grid(color="#dddddd", linewidth=0.45, alpha=0.8)
    spectrum_axis.legend(loc="lower right", fontsize=6.6, frameon=False)
    spectrum_axis.tick_params(labelsize=7)

    figure.tight_layout(pad=0.7, w_pad=0.8)
    output.parent.mkdir(parents=True, exist_ok=True)
    fixed_time = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
    figure.savefig(
        output,
        bbox_inches="tight",
        metadata={
            "Creator": "Matplotlib 3.11.2",
            "CreationDate": fixed_time,
            "ModDate": fixed_time,
        },
    )
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "manuscript" / "fig_core_spectrum.pdf",
    )
    arguments = parser.parse_args()
    render(arguments.output.resolve())


if __name__ == "__main__":
    main()
