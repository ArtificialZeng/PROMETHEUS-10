#!/usr/bin/env python3
"""Reproduce the finite-chain illustration using O(N) tridiagonal storage.

The supplied data are numerical illustrations; the analytic limits follow from
the proof in the article. No interval certificate is asserted by this program.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import os
import platform
import time

# Set these before importing numerical libraries. A single process is sufficient.
for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[name] = "1"


def calculate(row):
    import numpy as np
    from scipy.linalg import eigh_tridiagonal, eigvalsh_tridiagonal
    import mpmath as mp

    n = row["N"]
    half = (n - 1) // 2
    c = Fraction(row["c"])
    qexact = c / (n if row["denominator"] == "N" else n - 1)
    q = float(qexact)
    sites = np.arange(-half, half + 1)
    diagonal = q * sites + 2.5 * np.sign(sites)
    diagonal[0] -= 1
    diagonal[-1] += 1
    offdiagonal = np.ones(n - 1)
    eigenvalues, vectors = eigh_tridiagonal(
        diagonal, offdiagonal, select="i", select_range=(half, half + 1),
        lapack_driver="stebz", tol=1e-14)
    orbital = vectors[:, 0]
    residual = diagonal * orbital
    residual[1:] += orbital[:-1]
    residual[:-1] += orbital[1:]
    resistance = 18 + 2 * (n - 1) * q
    result = {
        "N": n, "c": str(c), "denominator": row["denominator"],
        "occupation_spacing": float(eigenvalues[1] / resistance),
        "IPR": float(np.sum(orbital ** 4)),
        "zero_residual_inf": float(np.max(np.abs(residual))),
    }
    if n == 2561:
        # An alternate QR eigenvalue method and an 80-digit boundary recurrence.
        qr = eigvalsh_tridiagonal(diagonal, offdiagonal, lapack_driver="sterf")
        result["QR_spacing_difference"] = float(abs(qr[half + 1] - eigenvalues[1]) / resistance)
        with mp.workdps(80):
            qm = mp.mpf(qexact.numerator) / qexact.denominator
            left_diagonal = [qm * j - mp.mpf("2.5") - (1 if j == -half else 0)
                             for j in range(-half, 0)]
            left = [mp.mpf(1), -left_diagonal[0]]
            for j in range(1, half):
                left.append(-left_diagonal[j] * left[-1] - left[-2])
            full = left + [(-1) ** j * left[half - j] for j in range(1, half + 1)]
            norm2 = sum(x * x for x in full)
            ipr = sum(x ** 4 for x in full) / norm2 ** 2
            result["IPR_80_digits"] = mp.nstr(ipr, 45)
            result["IPR_precision_difference"] = float(abs(ipr - result["IPR"]))
    return result


def plot(data, out):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    plt.rcParams.update({"font.size": 10, "axes.labelsize": 11,
                         "font.family": "DejaVu Sans", "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.15), layout="constrained")
    colors = {"1/2": "#1764ab", "2": "#b34424"}
    for c, color in colors.items():
        rows = [r for r in data["cases"] if r["c"] == c and r["denominator"] == "N"]
        rows.sort(key=lambda r: r["N"])
        sizes = np.array([r["N"] for r in rows])
        gap_error = [r["occupation_spacing"] - r["occupation_spacing_limit"] for r in rows]
        gap_bound = [r["B_spacing_upper_bound"] / r["R"] - r["occupation_spacing_limit"] for r in rows]
        ipr_error = [abs(r["IPR"] - r["IPR_limit"]) for r in rows]
        ipr_bound = [r["IPR_error_upper_bound"] for r in rows]
        for ax, errors, bounds in zip(axes, [gap_error, ipr_error], [gap_bound, ipr_bound]):
            ax.loglog(sizes, errors, "o-", color=color, markersize=4, linewidth=1.3)
            ax.loglog(sizes, bounds, "--", color=color, linewidth=1.2)
    for label, ax in zip(["(a)", "(b)"], axes):
        ax.set_xlabel("Chain length $N$")
        ax.set_xticks([81, 321, 1281, 2561], labels=["81", "321", "1281", "2561"])
        ax.grid(which="major", color="0.90", linewidth=0.6)
        ax.text(0.02, 1.02, label, transform=ax.transAxes, va="bottom", fontweight="bold")
    axes[0].set_ylabel(r"$\delta\nu_N-(36+4c)^{-1}$")
    axes[1].set_ylabel(r"$|\mathrm{IPR}(u_N)-51/125|$")
    handles = [Line2D([0], [0], color=colors[c], marker="o", label="$c=" + c + "$")
               for c in colors]
    handles += [Line2D([0], [0], color="0.25", linestyle="--", label="Finite upper bound")]
    axes[0].legend(handles=handles, frameon=False, loc="upper right", fontsize=8)
    fig.savefig(out / "convergence.pdf", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(out / "convergence.png", dpi=180)
    plt.close(fig)


def table(data, out):
    rows = [r for r in data["cases"] if r["N"] == 2561]
    lines = [r"\begin{tabular}{ccccc}", r"\toprule",
             r"$c$ & $q_N$ & $\delta\nu_N$ & $(36+4c)^{-1}$ & $\IPR(u_N)$\\",
             r"\midrule"]
    for row in rows:
        rate = "c/N" if row["denominator"] == "N" else "c/(N-1)"
        c = row["c"]
        lines.append(f"${c}$ & ${rate}$ & {row['occupation_spacing']:.9f} & "
                     f"{row['occupation_spacing_limit']:.9f} & {row['IPR']:.9f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (out / "finite-size-table.tex").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.json"))
    parser.add_argument("--out", type=Path, required=True, help="Separate output directory")
    parser.add_argument("--verify", action="store_true", help="Recompute all 24 supplied cases")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.out.resolve() == args.data.parent.resolve():
        parser.error("Use a separate output directory to preserve the reference data.")
    os.environ["MPLCONFIGDIR"] = str(args.out.resolve() / ".matplotlib")
    data = json.loads(args.data.read_text())
    if args.verify:
        import numpy as np
        import scipy
        import mpmath as mp
        start = time.monotonic()
        results = [calculate(row) for row in data["cases"]]
        differences = {key: max(abs(a[key] - b[key]) for a, b in zip(results, data["cases"]))
                       for key in ("occupation_spacing", "IPR")}
        max_residual = max(r["zero_residual_inf"] for r in results)
        passed = max(differences.values()) < 2e-12 and max_residual < 2e-12
        passed = passed and all(r.get("IPR_precision_difference", 0) < 2e-12 and
                                r.get("QR_spacing_difference", 0) < 2e-12 for r in results)
        report = {"pass": passed, "cases": results, "max_reference_differences": differences,
                  "max_zero_residual_inf": max_residual,
                  "elapsed_seconds": time.monotonic() - start,
                  "environment": {"python": platform.python_version(), "numpy": np.__version__,
                                  "scipy": scipy.__version__, "mpmath": mp.__version__},
                  "limits": "Floating-point diagnostics, not interval enclosures or proof of the size limit."}
        (args.out / "reproduction.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({k: v for k, v in report.items() if k != "cases"}, indent=2))
        if not passed:
            raise SystemExit("Numerical reproduction failed; inspect reproduction.json.")
    plot(data, args.out)
    table(data, args.out)


if __name__ == "__main__":
    main()
