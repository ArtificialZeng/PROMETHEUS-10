# Reproducing the local manuscript calculations

Run from the project root with Python 3.12 or later. The exact rational bounds use only the Python standard library. The local checks used Python 3.12.14:

```sh
python3 evidence/weak_feedback_bounds.py
```

This writes `evidence/weak-feedback-bounds.json`. The script checks the rational lower bounds on each $S_i/a_i$, rational upper bounds on each $K_i$, and the common $0<|\epsilon|\leq1/2000$ interval. The coefficient decimals in Table 1 arise from the absolutely convergent bivariate-Poisson series in the manuscript, evaluated by the separate `evidence/weak_feedback_check.py` script. That optional diagnostic requires NumPy and SciPy (locally tested with versions 2.3.5 and 1.18.1) and builds reflected finite generators for a *cross-check only*:

```sh
python3 evidence/weak_feedback_check.py --caps 8 10 12 14
```

It writes `evidence/weak-feedback-check.json`. The finite-box stationary Fano values do not certify the infinite-state sign; the proof uses the analytic series and resolvent remainder. See `evidence/research-pass3.md` for the full scientific derivation and `audit/science.md` for the independent AI audit. These audit records are local evidence, not external peer review.

The manuscript builds with TeX Live 2026, RevTeX 4.2 and BibTeX:

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The submitted source set would consist of `manuscript/main.tex`, `manuscript/references.bib`, this reproducibility file, and the explicitly listed code/data in `publication.json`. Downloaded primary PDFs in `literature/` are verification copies and are excluded from any redistribution package.
