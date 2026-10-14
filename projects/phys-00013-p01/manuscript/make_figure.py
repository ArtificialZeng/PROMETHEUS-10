"""Render accepted exact rational spectra; never overwrite frozen research data."""
from pathlib import Path
from fractions import Fraction
import csv
import json
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "mpl-cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / "build" / "font-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    out = ROOT / "manuscript" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    r_values = list(range(1, 13))
    exact = [Fraction(6, (r + 2) * (2 * r + 3)) for r in r_values]
    holdout = json.loads((ROOT / "evidence/research/sym8-holdout-result.json").read_text())
    observed = [Fraction(v) for v in holdout["observed_signed_cosines"]][1:]
    assert observed == exact[:4]
    assert exact[0] == Fraction(2, 5)
    assert all(a > b > 0 for a, b in zip(exact, exact[1:]))
    with (out / "spectrum.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["r", "exact_cosine", "degree8_exact_check"])
        for r, value in zip(r_values, exact):
            writer.writerow([r, str(value), str(observed[r-1]) if r <= 4 else ""])
    plt.rcParams.update({
        "font.size": 9,
        "axes.labelsize": 10,
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(3.45, 2.65), layout="constrained")
    ax.axhline(0.5, color="0.40", linestyle="--", linewidth=1.0)
    ax.text(12.2, 0.506, "Known group witness", ha="right", va="bottom", fontsize=8)
    ax.plot(r_values, [float(c) for c in exact], "o-", color="#0072B2",
            markersize=4, linewidth=1.0, label="Analytic state spectrum")
    ax.scatter(range(1, 5), [float(c) for c in observed], marker="s", s=43,
               facecolors="none", edgecolors="#D55E00", linewidths=1.0,
               label="Exact degree-8 check", zorder=4)
    ax.set(xlabel=r"Mode degree $r$", ylabel=r"Principal cosine $c_r$",
           xlim=(0.65, 12.4), ylim=(0, 0.55))
    ax.set_xticks([1, 2, 4, 6, 8, 10, 12])
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.grid(axis="y", color="0.9", linewidth=0.5)
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.87), frameon=False, fontsize=8)
    fig.savefig(out / "spectrum.pdf", metadata={"CreationDate": None, "ModDate": None,
                "Title": "Accepted exact pure-state principal cosines"})
    plt.close(fig)
    print(json.dumps({"figure": "manuscript/figures/spectrum.pdf",
        "data": "manuscript/figures/spectrum.csv",
        "exact_modes_rendered": r_values,
        "degree8_values_match": True,
        "arithmetic": "Fraction; floats used only for rendering",
        "scope": "Display of the accepted analytic formula, not a new scientific test"}, indent=2))


if __name__ == "__main__":
    main()
