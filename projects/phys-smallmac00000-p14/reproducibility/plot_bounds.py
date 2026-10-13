"""Regenerate the manuscript figure from the accompanying certificate records."""
import json
import os
from pathlib import Path
from decimal import Decimal

HERE = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(HERE / "output" / "matplotlib-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def endpoint(text, lower):
    # Include the recorded Arb radius, then round outwards at 10 decimal places.
    s = text.strip("[]").split(" +/- ")
    center = Decimal(s[0]); radius = Decimal(s[1]) if len(s) > 1 else Decimal(0)
    value = center - radius if lower else center + radius
    from decimal import ROUND_FLOOR, ROUND_CEILING
    return float(value.quantize(Decimal("0.0000000001"), rounding=ROUND_FLOOR if lower else ROUND_CEILING))

def main():
    records = [json.loads((HERE / "reference" / f"certificate{n}.json").read_text()) for n in [96,80]]
    data = {"bands": [[28/25,52/25],[52/25,68/25]],
            "forcing_intervals": [[endpoint(r["infinite_real_lower"], True),
                                    endpoint(r["infinite_real_upper"], False)] for r in records],
            "meaning": "Outward-rounded certified enclosures; not statistical errors or an L extrapolation"}
    out = HERE.parent / "manuscript" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    (out / "certified-bounds-data.json").write_text(json.dumps(data, indent=2)+"\n")
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":9, "axes.spines.top":False,
                         "axes.spines.right":False, "pdf.fonttype":42})
    fig, axes = plt.subplots(1, 2, figsize=(6.35,2.4), gridspec_kw={"width_ratios":[1,1.25]})
    colors = ["#16618a", "#bc5b22"]
    for row, (lo,hi) in enumerate(data["bands"]):
        axes[0].plot([lo,hi],[1-row]*2, lw=5, solid_capstyle="butt", color=colors[row])
        axes[0].scatter([lo,hi],[1-row]*2, s=18, color=colors[row], zorder=3)
    axes[0].set(yticks=[1,0], yticklabels=["A", "B"], ylim=(-.7,1.7), xlim=(0,3),
                xlabel=r"$\mathrm{Re}\,\omega/t$", title="(a) Positive continuum bands")
    axes[0].axvline(0,color="#777777",lw=.8)
    for row,(lo,hi) in enumerate(data["forcing_intervals"]):
        axes[1].plot([lo*1e4,hi*1e4],[1-row]*2,lw=4,color=colors[row],solid_capstyle="butt")
        axes[1].plot([lo*1e4,hi*1e4],[1-row]*2,"|",color=colors[row],ms=12,mew=1.4)
    axes[1].axvline(0,color="#777777",lw=.8)
    axes[1].axvline(1,color="#555555",ls="--",lw=1)
    axes[1].set(yticks=[1,0],yticklabels=["96 sites", "80 sites"],ylim=(-.7,1.7),xlim=(-.12,1.95),
                xlabel=r"$10^4\,\mathrm{Re}\,\Phi/t$",title="(b) Infinite forcing enclosures")
    for ax in axes:
        ax.grid(axis="x",color="#dddddd",lw=.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y",length=0)
    fig.tight_layout(w_pad=2)
    fig.savefig(out / "certified-bounds.pdf", metadata={"Title":"Certified half-line bounds", "CreationDate":None, "ModDate":None})
    fig.savefig(out / "certified-bounds.png", dpi=180)
    plt.close(fig)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
