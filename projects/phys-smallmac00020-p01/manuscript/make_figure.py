#!/usr/bin/env python3
"""Regenerate the manuscript's diagnostic gap-comparison figure."""

from __future__ import annotations

import json
import os
from decimal import Decimal
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/phys-00020-p01-matplotlib")

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "evidence/rational-counterexample-certificate.json"
OUTPUT = PROJECT / "manuscript/figure-gap-comparison.pdf"


def main() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    diagnostic = {
        record["Gamma"]: Decimal(record["gap_100_digit_replay"])
        for record in data["independent_high_precision_replay"]
    }
    x = [0, 1]
    y = [float(diagnostic["7.3"]), float(diagnostic["8"])]

    plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.8})
    fig, ax = plt.subplots(figsize=(3.25, 2.35), constrained_layout=True)
    lower_color = "#0072B2"
    upper_color = "#D55E00"
    ax.scatter([x[0]], [y[0]], marker="o", s=46, facecolors="white",
               edgecolors="#222222", zorder=4)
    ax.scatter([x[1]], [y[1]], marker="s", s=42, facecolors="white",
               edgecolors="#222222", zorder=4)
    ax.vlines(0, 1.5, y[0], color=lower_color, linewidth=3, zorder=3)
    ax.vlines(1, y[1], 1.0, color=upper_color, linewidth=3, zorder=3)
    ax.axhline(1.5, color=lower_color, linestyle="--", linewidth=1)
    ax.axhline(1.0, color=upper_color, linestyle="-.", linewidth=1)
    ax.text(0.03, 1.505, r"exact: $g>3/2$", color=lower_color, va="bottom")
    ax.text(0.97, 0.992, r"exact: $g<1$", color=upper_color, ha="right", va="top")
    ax.annotate(f"{y[0]:.10f}", (0, y[0]), xytext=(7, 3), textcoords="offset points")
    ax.annotate(f"{y[1]:.10f}", (1, y[1]), xytext=(-7, -13),
                textcoords="offset points", ha="right")
    ax.set_xticks(x, [r"$73/10$", r"$8=\Gamma_{\rm cr}$"])
    ax.set_xlabel(r"dissipation strength $\Gamma$")
    ax.set_ylabel(r"spectral gap $g(\Gamma)$")
    ax.set_xlim(-0.32, 1.32)
    ax.set_ylim(0.84, 1.68)
    ax.spines[["top", "right"]].set_visible(False)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, metadata={"Creator": "manuscript/make_figure.py"})
    plt.close(fig)
    print(json.dumps({"ok": True, "output": str(OUTPUT.relative_to(PROJECT)),
                      "diagnostic_gaps": {key: str(value) for key, value in diagnostic.items()}}))


if __name__ == "__main__":
    main()
