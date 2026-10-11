#!/usr/bin/env python3
"""Plot the recorded interval-Hessian radius trials.

The plot is a presentation of frozen calculation output.  A failed
Gershgorin enclosure at a larger radius is inconclusive and is not interpreted
as a physical instability.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


NUMBER = re.compile(r"^[\[(]?\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")


def lower_endpoint(record: dict) -> float:
    match = NUMBER.search(record["lower"])
    if match is None:
        raise ValueError(f"cannot parse directed lower endpoint: {record['lower']!r}")
    return float(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="evidence/interval-rank-two-neighborhood.json",
        help="frozen interval certificate JSON",
    )
    parser.add_argument(
        "--output",
        default="manuscript/figures/certificate-radii.pdf",
        help="output figure",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = []
    for trial in data["radius_trials"]:
        margin = min(lower_endpoint(item) for item in trial["direct_gershgorin_margins"])
        rows.append(
            (
                float(trial["radius"]),
                margin,
                bool(trial["uniform_augmented_hessian_positive"]),
            )
        )
    rows.sort()

    radii = [row[0] for row in rows]
    margins = [row[1] for row in rows]
    passed = [row[2] for row in rows]

    fig, ax = plt.subplots(figsize=(5.6, 3.6), constrained_layout=True)
    ax.plot(radii, margins, color="#4c566a", linewidth=1.2, zorder=1)
    for radius, margin, success in rows:
        ax.scatter(
            [radius],
            [margin],
            s=48,
            marker="o" if success else "x",
            linewidths=1.8,
            color="#2a9d8f" if success else "#c94c4c",
            zorder=2,
        )
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.axvline(1e-4, color="#2a9d8f", linestyle="--", linewidth=1.0)
    ax.annotate(
        r"selected $r=10^{-4}$",
        xy=(1e-4, margins[radii.index(1e-4)]),
        xytext=(1.6e-5, -2.1),
        arrowprops={"arrowstyle": "->", "color": "#2a9d8f"},
        fontsize=9,
    )
    ax.set_xscale("log")
    ax.set_yscale("symlog", linthresh=0.05, linscale=1.0)
    ax.set_xlabel(r"coordinate-cube radius $r$")
    ax.set_ylabel("minimum directed Gershgorin lower endpoint")
    ax.grid(True, which="both", alpha=0.22, linewidth=0.6)
    ax.tick_params(direction="in")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", metadata={"Creator": "make_figure.py"})


if __name__ == "__main__":
    main()
