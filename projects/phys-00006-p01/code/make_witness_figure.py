#!/usr/bin/env python3
"""Generate the manuscript's comparison figure from the exact witness values."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

e_input = (3 * sp.sqrt(1489) - 101) / 202
e_bound = sp.Rational(3, 4) * e_input
e_output = (3 * sp.sqrt(41) - 13) / 101
margin = sp.simplify(e_output - e_bound)

assert margin == (199 + 24 * sp.sqrt(41) - 9 * sp.sqrt(1489)) / 808
assert margin > 0

records = [
    ("input_E2", e_input),
    ("alpha_ceiling", e_bound),
    ("actual_output_E2", e_output),
    ("violation_margin", margin),
    ("actual_output_error", (1 - e_output) / 3),
    ("alpha_implied_error_floor", (1 - e_bound) / 3),
]

with (FIGURE_DIR / "witness_values.csv").open("w", newline="", encoding="utf-8") as stream:
    writer = csv.writer(stream)
    writer.writerow(["quantity", "exact_sympy", "decimal_15_digits"])
    for name, value in records:
        writer.writerow([name, sp.sstr(value), f"{float(sp.N(value, 17)):.15f}"])

values = [float(e_input), float(e_bound), float(e_output)]
labels = [
    r"Input $E_2$",
    "Proposed ceiling\n" + r"$(1-\alpha)E_2$",
    r"Actual output $E_2$",
]
colors = ["#6B7280", "#3B82F6", "#E76F51"]

fig, ax = plt.subplots(figsize=(7.1, 3.8), constrained_layout=True)
bars = ax.bar(range(3), values, width=0.62, color=colors, edgecolor="#1F2937", linewidth=0.8)
ax.set_ylabel(r"Hockey-stick divergence $E_2$")
ax.set_xticks(range(3), labels)
ax.set_ylim(0, 0.083)
ax.grid(axis="y", color="#D1D5DB", linewidth=0.7, alpha=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.0012,
        f"{value:.6f}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

x_bound, x_output = 1, 2
y_arrow = values[2] - 0.0004
ax.annotate(
    "",
    xy=(x_output - 0.10, y_arrow),
    xytext=(x_bound + 0.10, y_arrow),
    arrowprops={"arrowstyle": "<->", "color": "#111827", "linewidth": 1.0},
)
ax.text(
    1.5,
    y_arrow + 0.0011,
    rf"$\Delta={float(margin):.6f}>0$",
    ha="center",
    va="bottom",
    fontsize=9,
)

ax.text(
    0.02,
    0.97,
    r"$\alpha=1/4,\quad \alpha_+=0,\quad \gamma=2$",
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=9.5,
)

metadata = {
    "Title": "Exact qubit-memory hockey-stick counterexample",
    "Author": "Generated from exact values in code/make_witness_figure.py",
    "Subject": "Comparison of input, proposed output ceiling, and actual output divergence",
}
pdf_metadata = {
    **metadata,
    "CreationDate": datetime(2026, 9, 13, tzinfo=timezone.utc),
    "ModDate": datetime(2026, 9, 13, tzinfo=timezone.utc),
}
fig.savefig(FIGURE_DIR / "witness_comparison.pdf", metadata=pdf_metadata)
fig.savefig(FIGURE_DIR / "witness_comparison.png", dpi=240, metadata=metadata)
plt.close(fig)

print(f"INPUT_E2={sp.sstr(e_input)}")
print(f"PROPOSED_CEILING={sp.sstr(e_bound)}")
print(f"ACTUAL_OUTPUT_E2={sp.sstr(e_output)}")
print(f"STRICT_MARGIN={sp.sstr(margin)}")
print("RESULT=PASS; figure and CSV generated from exact expressions")
