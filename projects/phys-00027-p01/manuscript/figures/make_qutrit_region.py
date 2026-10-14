#!/usr/bin/env python3
"""Render the accepted exact qutrit criterion; sampling is only for display.

No scientific input or accepted snapshot file is rewritten.  Boundary
coordinates are rational because s=t^3, a=t (gamma_s=0) or a=t^5
(gamma_a=0) with rational t.  Endpoint t=0,1 is shown only as a limit.
"""
from __future__ import annotations

import csv
import json
import os
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "mpl-cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from matplotlib.lines import Line2D


def xy(s: F, a: F) -> tuple[F, F]:
    return (2 - 5*s + 3*a)/6, (2 + s - 3*a)/3


def sectors(x: F, y: F) -> tuple[F, F]:
    return 1-F(3, 2)*x-F(3, 4)*y, 1-F(1, 2)*x-F(5, 4)*y


def embedded(x: F, y: F) -> bool:
    s, a = sectors(x, y)
    return x > 0 and y > 0 and x+y <= 1 and s > 0 and a > 0 and s**5 <= a**3 <= s


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    points = {"gamma_s_zero": [], "gamma_a_zero": []}
    for label, power in (("gamma_s_zero", 1), ("gamma_a_zero", 5)):
        for k in range(1001):
            t = F(k, 1000)
            s, a = t**3, t**power
            x, y = xy(s, a)
            assert sectors(x, y) == (s, a)
            if 0 < k < 1000:
                assert embedded(x, y)
            rows.append([label, str(t), str(x), str(y), str(s), str(a)])
            points[label].append((float(x), float(y)))
    with (OUT / "qutrit-boundaries.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["boundary", "t", "x", "y", "s", "a"])
        w.writerows(rows)
    assert embedded(F(1,4), F(1,4))
    assert not embedded(F(1,2), F(1,10))

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.labelsize": 12, "pdf.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    ax.add_patch(Polygon([(0,0),(1,0),(0,1)], facecolor="#f1dfd7", edgecolor="#7d6c65", linewidth=1.1))
    ax.add_patch(Polygon([(0,0),(2/3,0),(1/3,2/3),(0,4/5)],
                        facecolor="#e9ecef", edgecolor="none"))
    lens = points["gamma_s_zero"] + list(reversed(points["gamma_a_zero"]))
    ax.add_patch(Polygon(lens, facecolor="#a6d7da", edgecolor="none"))
    for label, color in (("gamma_s_zero","#176c8a"),("gamma_a_zero","#bd5e2f")):
        ax.plot(*zip(*points[label]), color=color, linewidth=1.7)
    ax.plot([0, 1/3], [0, 2/3], color="#44515b", linestyle=":", linewidth=1.1)
    ax.plot([2/3,1/3,0], [0,2/3,4/5], color="#8b9399", linestyle="--", linewidth=0.9)
    ax.scatter([0,1/3], [0,2/3], s=34, facecolor="white", edgecolor="#44515b", zorder=5)
    ax.scatter([1/4], [1/4], color="#172f37", s=30, zorder=6)
    ax.annotate(r"$(1/4,1/4)$", (1/4,1/4), xytext=(0.28,0.34),
                fontsize=10, arrowprops={"arrowstyle":"-","lw":0.7})
    ax.scatter([1/2], [1/10], color="#a13c37", marker="x", s=45, linewidth=1.7, zorder=6)
    ax.annotate(r"$(1/2,1/10)$", (1/2,1/10), xytext=(0.57,0.12),
                fontsize=10, color="#843029", arrowprops={"arrowstyle":"-","lw":0.7,"color":"#843029"})
    ax.annotate(r"$\gamma_{\rm s}=0$", xy=points["gamma_s_zero"][500],
                xytext=(0.57,0.31), color="#176c8a",
                arrowprops={"arrowstyle":"-","lw":0.8,"color":"#176c8a"})
    ax.annotate(r"$\gamma_{\rm a}=0$", xy=points["gamma_a_zero"][700],
                xytext=(0.015,0.49), color="#a94f23",
                arrowprops={"arrowstyle":"-","lw":0.8,"color":"#a94f23"})
    ax.set_xlim(-0.025,1.02); ax.set_ylim(-0.025,1.02)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$  (antisymmetric noise weight)")
    ax.set_ylabel(r"$y$  (symmetric noise weight)")
    handles = [
        Patch(facecolor="#a6d7da",label="Homogeneous embedding"),
        Patch(facecolor="#e9ecef",label="Positive spectrum, excluded"),
        Patch(facecolor="#f1dfd7",label="Zero/negative spectrum, excluded"),
    ]
    ax.legend(handles=handles,loc="upper right",bbox_to_anchor=(1.015,1.18),
              fontsize=10,frameon=False)
    fig.subplots_adjust(left=0.14,right=0.98,bottom=0.14,top=0.83)
    fig.savefig(OUT / "qutrit-region.pdf", bbox_inches="tight", pad_inches=0.04, metadata={
        "Title":"Exact qutrit homogeneous-embedding region",
        "Creator":"make_qutrit_region.py", "CreationDate":None, "ModDate":None})
    fig.savefig(OUT / "qutrit-region.png", dpi=170, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    report = {
        "boundary_rows":len(rows),
        "coordinates":"Exact Fraction values; s=t^3, a=t or t^5",
        "classification":"Analytic accepted criterion, not a numerical discovery",
        "boundary_interior_assertions":"All 1998 nonendpoint samples satisfy the exact domain and criterion",
        "benchmark":{"x":"1/4","y":"1/4","s":"7/16","a":"9/16","embeddable":True},
        "outside":{"x":"1/2","y":"1/10","s":"7/40","a":"5/8","embeddable":False},
        "excluded_limits":["t=0: singular s=a=0","t=1: x=y=0, outside the frozen domain"],
    }
    (OUT / "figure-data.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
