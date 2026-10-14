# Reproduce the manuscript

The result is exact for one fixed Bell probe, known depolarization in [0,1],
the Cartesian-volume prior of radius pi/4, and risk E[||estimate-theta||^2]/3.
The paper contains the proof. Numerical integration and SDPs are diagnostic
checks and are not the argument for an all-noise equality. No experiment,
large-copy limit, other prior or optimized-probe result is represented here.

The original scripts and data are preserved under `evidence/`. They write
beside their code and must not be run there after their evidence is frozen.
The following wrapper executes byte-identical copies in a **new** directory:

```sh
python manuscript/run_reproducibility.py --output reproduction-run
```

Use Python 3.12 with the already available NumPy, SciPy, SymPy and mpmath.
`manuscript/requirements.txt` records the installed versions used for this
draft, including Matplotlib for the figure and CVXPY for optional original
SDP diagnostics. No package installation is part of this workflow. On this
workstation the existing scientific interpreter is
`python3`; elsewhere invoke the matching
environment's Python. The wrapper refuses an existing output directory.

It replays three checks:

1. Exact source Choi/Bell convention map, spherical moments and radial integrals.
2. Exact measurement/circuit identities and positive physical/NH certificates
   (2,141 symbolic entry checks in the preserved run).
3. Computational Pauli/Bell construction and direct integration of the actual
   finite measurement at five noise values and three quadrature resolutions.

`reproduction-run/reproduction-summary.json` and the three logs record the
actual run. The numerical residual is an observed floating-point difference,
not a directed-rounding error bound. PSD follows from the written Gram/projector
factorizations and the physical dual determinant. Embedded historical job labels
belong to the original scripts; replay is not an independent scientific review.
The wrapper verifies that the original inputs remain byte-identical.

For Fig. 1, copy `manuscript/make_figure.py` into a scratch directory with a
`figures/` subdirectory, then execute it there. It evaluates the accepted closed
formulas at 201 noise values with 60-digit mpmath arithmetic and prints 50
significant digits to `risk-data.csv`. The plot is ordinary Matplotlib vector
graphics. Sampling is only for drawing the analytic curves; it does not establish
their exactness. To regenerate the official figure sources before freezing a
manuscript, run `python manuscript/make_figure.py` from the project root.
After manuscript freezing, regenerate in a copy so the bound figure/data stay
unchanged.

Build from the project root, with a fresh output directory:

```sh
latexmk -pdf -pdflatex='pdflatex -no-shell-escape %O %S' \
  -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=build/reproduction-clean manuscript/main.tex
```

TeX Live 2026, REVTeX 4.2, `apsrev4-2`, BibTeX, hyperref and graphicx were
already installed. The only authored compiler dependencies are `main.tex`,
`references.bib` and `figures/risk.pdf`. Bibliography and note files in the
build output are generated from those sources; standard TeX packages are system
dependencies. No shell escape, downloaded style, external API or author code
is needed. A fresh release worker must still inspect citations, build logs
and every rendered page of the final bound PDF.

The selected submission files contain project-authored TeX, bibliography,
figure/code/data, original derivations and needed input/checker files. Downloaded
third-party papers, source-page screenshots, web-response logs, job records,
scientific audit records and operational handoffs are excluded from that bundle.
No scientific evidence or source copy needs to be redistributed to reproduce
the self-contained certificates.
