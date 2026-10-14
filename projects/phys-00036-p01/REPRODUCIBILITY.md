# Reproducibility record

The central result is the exact all-order proof in `manuscript/main.tex`; finite
calculations test transcription, signs, factorials, finite-size conventions and the
local-gradient equations. They do not establish the universal quantifiers by sampling.

## Environment

- Recorded interpreter: CPython 3.14.7.
- Core calculations use only Python standard-library integers and
  `fractions.Fraction`; no numerical tolerance or third-party package is required.
- TeX build used `latexmk`/pdfLaTeX and BibTeX from the local TeX distribution.

## Bound calculation files

- Known XXX reconstruction: `evidence/reproduce-input-a.py`,
  `evidence/reproduce-input-b.py`, `evidence/reproduce-compare.py`, with actual output
  in `evidence/reproduce-baseline.log` and `evidence/reproduce-comparison.json`.
- Nonlinear spectral reparametrization: `evidence/research-reparam-test.py`, with actual
  output in `evidence/research-reparam-test.log` and
  `evidence/research-reparam-comparison.json`.
- Rooted-support and legal spectral-gauge attacks:
  `evidence/research-structural-tests.py`, with actual output in
  `evidence/research-structural-tests.log` and
  `evidence/research-structural-comparison.json`.

The saved logs contain the commands' real completion records and exact zero-residual
fields. The complete accepted evidence snapshot is hash-bound in `audit/snapshot.json`.

## Safe replay

The scripts write their named JSON/log outputs. To preserve the accepted snapshot, do
not rerun them in this frozen project. Copy the submission files to a separate scratch
directory, retain their relative paths, and run from that scratch root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/reproduce-input-a.py
PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/reproduce-input-b.py
PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/reproduce-compare.py
PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/research-reparam-test.py
PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/research-structural-tests.py
```

Compare the regenerated JSON/log summaries to the bundled records. The independent
referee replay is retained in the internal audit dossier but is intentionally excluded
from the distributable submission bundle because audit runtime files are not publication
inputs.

## Manuscript build

From `manuscript/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

The resulting draft is `build/main.pdf`; `build/main.log` is the compiler log.
