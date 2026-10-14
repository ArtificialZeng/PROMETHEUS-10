#!/usr/bin/env python3
"""Plot only the accepted analytic family; strictness is checked rationally."""
from __future__ import annotations
import csv
import json
import math
import os
import platform
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "matplotlib-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def family(m: int, q: float, alpha: float) -> tuple[float, float, float]:
    u, v = math.cos(alpha), math.sin(alpha)
    f = 1 - math.sin(2 * alpha) ** 2 / 4
    cross = u * u * ((1 + u**4) / 2) ** m
    cross += v * v * ((1 + v**4) / 2) ** m
    parent = (1-q)**2 + q*q*f**m + 2*q*(1-q)*cross
    return parent, f, cross


def main() -> None:
    out = ROOT / "manuscript" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    q, p, m = Fraction(1, 4), Fraction(3, 4), 8
    fp = p*p + q*q*Fraction(3, 4)**m + 2*p*q*Fraction(5, 8)**m
    branch = Fraction(3, 4)**m
    ratio = fp / Fraction(3, 4)**2
    assert fp == Fraction(77509155, 134217728)
    assert branch == Fraction(6561, 65536)
    assert ratio == Fraction(25836385, 25165824) and ratio > 1
    x = ratio-1
    rows = []
    angles = [("pi/12", math.pi/12), ("pi/8", math.pi/8), ("pi/4", math.pi/4)]
    for label, alpha in angles:
        for blocks in range(1, 33):
            parent, f, cross = family(blocks, float(q), alpha)
            if label == "pi/4":
                exact = p*p + q*q*Fraction(3, 4)**blocks
                exact += 2*p*q*Fraction(5, 8)**blocks
                assert abs(parent-float(exact)) < 5e-16
                parent = float(exact)
            pin = -math.log(parent)
            average = -float(q)*blocks*math.log(f)
            rows.append([label, blocks, 4*blocks+2, parent, f**blocks,
                         pin, average, average-pin, cross])
    with (out / "recorded_measurement.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["alpha", "m", "N", "F_parent", "F_branch1",
                         "P_parent", "mean_output_P", "Delta", "K_m"])
        writer.writerows(rows)
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":9,
                         "axes.spines.top":False, "axes.spines.right":False,
                         "pdf.fonttype":42, "ps.fonttype":42})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), layout="constrained")
    mid = [r for r in rows if r[0] == "pi/4"]
    ms = [r[1] for r in mid]
    axes[0].plot(ms, [r[5] for r in mid], "o-", ms=2.7, lw=1.4,
                 color="#285f91", label="Input")
    axes[0].plot(ms, [r[6] for r in mid], "s-", ms=2.5, lw=1.4,
                 color="#c05139", label="Mean output")
    axes[0].axhline(-2*math.log(float(p)), ls="--", lw=1, color="#666666",
                   label=r"Input bound $-2\ln p$")
    axes[0].plot(8, -math.log(float(fp)), "o", ms=5, color="#285f91")
    axes[0].plot(8, -float(q)*8*math.log(3/4), "s", ms=5, color="#c05139")
    axes[0].annotate(r"Exact $m=8$ witness", xy=(8, 0.576), xytext=(15, 0.80),
                     fontsize=8, arrowprops={"arrowstyle":"->","lw":0.8})
    axes[0].set(xlabel=r"Four-mode blocks $m$", ylabel="Entropy (natural logs)",
                title=r"(a) $\alpha=\pi/4$", xlim=(1,32), ylim=(0,2.4))
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    colors = ["#23846d", "#a86b18", "#67478d"]
    labels = [r"$\pi/12$", r"$\pi/8$", r"$\pi/4$"]
    for (label, _), color, legend in zip(angles, colors, labels):
        subset = [r for r in rows if r[0] == label]
        axes[1].plot([r[1] for r in subset], [r[7] for r in subset],
                     "o-", ms=2.5, lw=1.4, color=color, label=legend)
    axes[1].axhline(0, color="#666666", lw=0.8, ls="--")
    axes[1].set(xlabel=r"Four-mode blocks $m$", ylabel=r"Average increase $\Delta$",
                title=r"(b) Fixed interior angles", xlim=(1,32))
    axes[1].legend(title=r"$\alpha$", frameon=False, fontsize=8, title_fontsize=8)
    for ax in axes:
        ax.grid(axis="y", alpha=0.18, lw=0.6)
    fig.savefig(out / "recorded_measurement.pdf",
                metadata={"Creator":"Reproducibility make_figure.py",
                          "CreationDate":None, "ModDate":None})
    fig.savefig(out / "recorded_measurement.png", dpi=200)
    plt.close(fig)
    environment = {"python":sys.version, "platform":platform.platform(),
                   "matplotlib":matplotlib.__version__,
                   "numeric_scope":"Double precision for plots only; no sign certified numerically",
                   "exact_witness":{"F_parent":str(fp), "F_branch1":str(branch),
                                    "exp_Delta":str(ratio),
                                    "lower_Delta":str(x/(1+x)), "upper_Delta":str(x)}}
    (out / "figure-environment.json").write_text(json.dumps(environment, indent=2)+"\n")
    print(json.dumps(environment))


if __name__ == "__main__":
    main()
