# Reproducibility guide

This directory contains the LaTeX source and the script for the plotted exact
crossing sequence. The scientific certificate scripts remain in `../evidence/`
and are included explicitly in the handoff manifest; downloaded papers and
runtime audit logs are intentionally excluded from the submission bundle.

## Required interpreter

The accepted calculations used Python 3.12.14 with NumPy 2.3.5, SciPy 1.18.1,
SymPy 1.14.0, python-flint 0.9.0, and Matplotlib 3.11.2. In this project the
authorized interpreter is the value of `PHYSICS_PYTHON`.

## Regenerate the figure

From the project root:

```sh
MPLCONFIGDIR=/tmp/phys-00021-mpl "$PHYSICS_PYTHON" manuscript/generate_figures.py
```

This rewrites `manuscript/data/crossing_data.csv` and both renderings in
`manuscript/figures/`. The PDF rendering is the manuscript dependency; the PNG
is a convenience preview and is not required for compilation.

## Replay the central certificates

The following commands regenerate or check the exact `k=5` factorization, the
signed Schur recurrence, and the all-depth crossing specialization. They can be
computationally expensive at the direct depth-six steps.

```sh
"$PHYSICS_PYTHON" evidence/exact_k5_degeneracy.py
"$PHYSICS_PYTHON" evidence/check_exact_k5.py
"$PHYSICS_PYTHON" evidence/cycle_schur_pass3.py
"$PHYSICS_PYTHON" evidence/check_cycle_schur_pass3.py
"$PHYSICS_PYTHON" evidence/flat_crossing_scaling_pass4.py
"$PHYSICS_PYTHON" evidence/check_flat_crossing_scaling_pass4.py
```

The fixed-window bound is analytic and stated in
`evidence/fixed-interval-gap-salvage-result.md`. The fresh scientific review
also independently replayed its coefficient arithmetic. Floating-point spectra
are corroborative; the all-depth claim rests on the polynomial identities and
induction in the manuscript.

## Clean build

Copy `main.tex`, `references.bib`, and `figures/crossing_scale.pdf` into a clean
build tree while preserving the `figures/` subdirectory, then run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The project build log records the actual clean invocation used for this draft.
