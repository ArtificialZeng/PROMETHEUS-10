"""Plot saved, accepted numerical outputs; do not rerun or alter research.

Run from the project root with Python and Matplotlib. No numerical curve is
an interval certificate. The all-amplitude result is analytic.
"""
from pathlib import Path
import hashlib
import json
import math
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "matplotlib-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INPUT = ROOT / "evidence/research/general-variation-check.json"
OUTPUT = ROOT / "manuscript/figures/sensitivity-ripple.pdf"
EXPECTED_HASH = "91c5e5eab1f2990df09d1f34d13f0f8d6055c78486426f11970da773744af5f0"


def main():
    (ROOT / "build").mkdir(parents=True, exist_ok=True)
    (ROOT / "evidence/write").mkdir(parents=True, exist_ok=True)
    raw = INPUT.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_HASH:
        raise RuntimeError("Figure input differs from the accepted scientific data")
    data = json.loads(raw)
    rows = data["cases"]
    sine = {strength: sorted(
        [r for r in rows if r["profile"] == "sine" and r["epsilon"] == strength],
        key=lambda r: r["t"])
        for strength in (0.005, -0.02)}
    if any(len(r) != 17 for r in sine.values()):
        raise RuntimeError("Expected 17 saved phases per strength")
    plt.rcParams.update({"font.size": 8, "axes.labelsize": 8,
                         "legend.fontsize": 7, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(3.35, 2.3), layout="constrained")
    for strength, color, marker in ((0.005, "#205f9d", "o"),
                                     (-0.02, "#d77521", "s")):
        sample = sine[strength]
        ax.plot([r["t"] for r in sample],
                     [1e3*(r["qfi_density_sld"]-4/math.e) for r in sample],
                     marker=marker, markersize=2.5, linewidth=1,
                     color=color, label=rf"$\epsilon={strength}$")
    ax.set_ylabel(r"$10^3(F_Q-4/e)$")
    ax.set_xlabel(r"Amplitude phase $t=\sqrt{2}\kappa\alpha$")
    ax.set_ylim(-6, 5.3)
    ax.legend(loc="upper right", frameon=False)
    ax.axhline(0, color="0.5", linewidth=0.6, linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(direction="out", length=3)
    ax.set_xlim(0, 2*math.pi)
    ax.set_xticks([0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi],
                       ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, metadata={"Title": "Saved coherent-state qubit sensitivity ripple",
                                 "Creator": "Matplotlib; reproducibility/make_figure.py",
                                 "CreationDate": None, "ModDate": None})
    fig.savefig(ROOT / "build" / "sensitivity-ripple-preview.png", dpi=180)
    plt.close(fig)
    summary = {
        "input": str(INPUT.relative_to(ROOT)), "input_sha256": actual,
        "output": str(OUTPUT.relative_to(ROOT)),
        "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "profile": "g(x)=sin(0.7*x)", "phase_count_per_strength": 17,
        "strengths": [0.005, -0.02],
        "source_data_unmodified": True,
        "interpretation": "Saved ordinary-float consistency data; lines guide the eye. Analytic proof supplies continuum coverage."
    }
    (ROOT / "evidence/write/figure-provenance.json").write_text(
        json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
