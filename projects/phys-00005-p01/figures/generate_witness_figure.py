#!/usr/bin/env python3
"""Generate the witness-construction and return-probability figure."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    n = int(data["n"])
    edges = [tuple(map(int, edge)) for edge in data["edges_zero_based"]]
    if n != 16 or len(edges) != 62 or len(set(edges)) != 62:
        raise AssertionError("unexpected witness data")

    deleted = {(0, 13), (5, 8)}
    positions = {
        vertex: (
            math.cos(math.pi / 2 - 2 * math.pi * vertex / n),
            math.sin(math.pi / 2 - 2 * math.pi * vertex / n),
        )
        for vertex in range(n)
    }
    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1

    colors = {2: "#4477AA", 3: "#66A61E", 4: "#AA4499", 6: "#CC6677"}
    figure, axes = plt.subplots(1, 2, figsize=(9.0, 4.15), gridspec_kw={"width_ratios": [1.15, 0.85]})
    graph_axis, bar_axis = axes

    for u, v in edges:
        step = min((v - u) % n, (u - v) % n)
        x_values = [positions[u][0], positions[v][0]]
        y_values = [positions[u][1], positions[v][1]]
        graph_axis.plot(x_values, y_values, color=colors[step], alpha=0.36, linewidth=0.75, zorder=1)

    for u, v in sorted(deleted):
        graph_axis.plot(
            [positions[u][0], positions[v][0]],
            [positions[u][1], positions[v][1]],
            color="#B2182B",
            linestyle=(0, (4, 2)),
            linewidth=2.0,
            zorder=2,
        )

    for vertex in range(n):
        color = "#E69F00" if degrees[vertex] == 7 else "#F7F7F7"
        graph_axis.scatter(*positions[vertex], s=235, facecolor=color, edgecolor="#222222", linewidth=0.8, zorder=3)
        graph_axis.text(*positions[vertex], str(vertex), ha="center", va="center", fontsize=8.2, zorder=4)

    graph_axis.set_aspect("equal")
    graph_axis.set_xlim(-1.22, 1.22)
    graph_axis.set_ylim(-1.18, 1.18)
    graph_axis.axis("off")
    graph_axis.set_title("(a) 62-edge witness on $\\mathbb{Z}_{16}$", fontsize=10.5)
    graph_axis.text(
        0,
        -1.15,
        "dashed red: deleted step-3 edges; orange: degree 7",
        ha="center",
        va="top",
        fontsize=7.8,
    )

    witness_tau = Fraction(data["tau_exact"])
    path_tau = Fraction(data["path_tau_exact"])
    values = [float(witness_tau / n), float(path_tau / n)]
    bars = bar_axis.bar(["Witness $G$", "Path $P_{16}$"], values, color=["#4477AA", "#BBBBBB"], width=0.62)
    bar_axis.set_ylim(0.0, 0.10)
    bar_axis.set_ylabel("uniform-start long-time return")
    bar_axis.set_title("(b) Exact Cesàro averages", fontsize=10.5)
    bar_axis.grid(axis="y", color="#DDDDDD", linewidth=0.6)
    bar_axis.set_axisbelow(True)
    labels = [r"$1673/19072$", r"$23/256$"]
    for bar, label in zip(bars, labels):
        bar_axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0015, label, ha="center", va="bottom", fontsize=8.5)
    bar_axis.text(
        0.5,
        0.08,
        r"exact difference $=-81/38144$",
        ha="center",
        va="center",
        transform=bar_axis.transAxes,
        fontsize=8.2,
    )
    bar_axis.spines["top"].set_visible(False)
    bar_axis.spines["right"].set_visible(False)

    figure.tight_layout()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
