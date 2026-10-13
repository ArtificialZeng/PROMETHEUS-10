# Reproducibility guide

The central result is the exact proof in `main.tex`; it does not depend on a
numerical spectrum.  The supplementary checker
`scripts/check_universal_annulus_ordering.py` independently verifies the new
symbolic identities and rational endpoint inequalities used in the proof.

From the project root, with the project scientific environment active, run:

```sh
python3 scripts/check_universal_annulus_ordering.py
```

The expected terminal record has `"ok": true`; the detailed JSON record is
written to `evidence/universal-annulus-ordering-check.log`.  The checker also
verifies that the immutable problem source has the expected content digest.
It uses exact SymPy algebra and Python rational arithmetic.  NumPy and SciPy
are imported only to bind and report the tested scientific environment; no
floating spectral calculation contributes to the theorem.

The write-phase environment probe, performed before any Python computation,
found the required executable and recorded Python 3.12.14, NumPy 2.3.5, and
SciPy 1.18.1 in `manuscript/write-environment.log`.  The accepted checker log
also records SymPy 1.14.0.

To rebuild the article from a clean project-local directory, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=build-release manuscript/main.tex
```

The expected output is `build-release/main.pdf`; the compiler transcript is
retained as `build-release/main.log`.
