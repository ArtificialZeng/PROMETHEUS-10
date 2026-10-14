"""Evaluate the accepted k=1 formulas and render their risk curves.

This is a figure generator, not an optimizer or an independent certificate.
Run from any directory; outputs are written alongside this script.
"""
from pathlib import Path
import csv
import os

HERE = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(HERE / ".matplotlib-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp

mp.mp.dps = 60
C = mp.mpf(1) / 2 + 3 / mp.pi - 24 / mp.pi**3
q = 3 / (2 * mp.pi) - 12 / mp.pi**3
prior = mp.pi**2 / 80
rows = []
for j in range(201):
    noise = mp.mpf(j) / 200
    A = (1 - noise) * C + noise / 4
    B = (1 - noise) * (1 - C) / 3 + noise / 4
    Q = (1 - noise) * q
    optimal = prior - 4 * Q**2
    sld = prior - 4 * Q**2 / (A + B)
    gap = 8 * B * Q**2 / (A + B)
    assert abs(A + 3 * B - 1) < mp.mpf("1e-55")
    assert abs(optimal - sld - gap) < mp.mpf("1e-55")
    rows.append([noise, optimal, sld, prior, gap])

with (HERE / "risk-data.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["lambda", "R1_equals_CNH", "CSLD", "prior_risk", "incompatibility_gap"])
    for row in rows:
        writer.writerow([mp.nstr(v, 50) for v in row])

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.labelsize": 10, "legend.fontsize": 8,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})
fig, ax = plt.subplots(figsize=(3.45, 2.55), layout="constrained")
x, optimum, lower, baseline, gap = map(list, zip(*[[float(v) for v in r] for r in rows]))
ax.fill_between(x, lower, optimum, color="#dde8f1", label="Incompatibility cost")
ax.plot(x, optimum, color="#205a85", linewidth=1.8, label=r"$R_1=C_{\mathrm{NH}}$")
ax.plot(x, lower, color="#af5424", linewidth=1.5, linestyle="--", label=r"$C_{\mathrm{SLD}}$")
ax.plot(x, baseline, color="#555555", linewidth=1.2, linestyle=":", label="Prior risk")
ax.set(xlabel=r"Known depolarization $\lambda$", ylabel="Bayes risk", xlim=(0, 1), ylim=(0.077, 0.126))
ax.set_xticks([0, .25, .5, .75, 1])
ax.set_yticks([.08, .09, .10, .11, .12])
ax.legend(loc="lower right", frameon=False, handlelength=2.4)
fig.savefig(HERE / "figures" / "risk.pdf", metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)
print("Formula evaluations: 201 noise values, 60 decimal-digit arithmetic; CSV prints 50 significant digits.")
print("R1(0) =", mp.nstr(rows[0][1], 30))
print("CSLD(0) =", mp.nstr(rows[0][2], 30))
print("ratio(0) =", mp.nstr(rows[0][1] / rows[0][2], 30))
print("R1(1) =", mp.nstr(rows[-1][1], 30))
