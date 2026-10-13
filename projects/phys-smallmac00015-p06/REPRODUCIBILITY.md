# Reproducibility guide

## Central exact check

Use the project-bound scientific Python environment:

```text
python3 scripts/verify_gad_global_bound.py
```

The write-job preflight recorded Python 3.12.14, NumPy 2.3.5, and SciPy 1.18.1 in
`evidence/write-runtime-versions.txt`. The verifier uses NumPy together with Python's
standard library. Its immutable scientific inputs are documented in
`evidence/gad-global-input.json`; the previously accepted replay output is
`evidence/gad-global-bound-check.log`.

The script checks exact Kraus completeness and rank data, reconstructs the two
coarse instrument operations, evaluates the history witness both by all 16 hidden
fine paths and by coarse Liouville composition, and evaluates the rational
trace-norm/Frobenius upper certificate. Floating-point values are diagnostic replays;
the manuscript's logical bounds are exact rational/radical statements.

## Manuscript build

From the project root, run:

```text
(cd manuscript && latexmk -C -outdir=../build main.tex && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex)
```

The bibliography is `manuscript/references.bib`. No downloaded third-party paper or
private runtime log is required or included in the handoff bundle.
