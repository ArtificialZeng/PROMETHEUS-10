# Reproducibility guide

Run commands from the project root. The audited scientific environment used
Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1, SymPy 1.14.0, and mpmath 1.3.0.
Matplotlib 3.11.2 was used only for the diagnostic figure. Exact conclusions
use rational/integer SymPy arithmetic; floating-point spectra are diagnostics.

The authoritative interpreter for this run was:

```text
python3
```

For replay in a clean copy of the project, activate an environment satisfying
`requirements.txt`, then run:

```sh
python3 scripts/transcribe_eq3.py
python3 scripts/derive_matrix_units.py
python3 scripts/check_reproduction.py
python3 scripts/certify_rational_counterexample.py
python3 scripts/verify_rational_counterexample_independent.py
```

The first two commands independently construct the same affine 16-by-16
Liouvillian. The primary certificate uses the matrix-unit construction,
parity blocks, and Hurwitz determinants. The independent certificate uses the
directly transcribed full matrix and a recursive Routh array without a parity
split. Expected decisive outputs are:

```text
Gamma=73/10, shift=3/2: 0 right-half-plane roots
Gamma=8, shift=1:       2 right-half-plane roots
```

To regenerate the figure and build the manuscript:

```sh
mkdir -p build
MPLCONFIGDIR=/tmp/phys-00020-p01-mpl python3 manuscript/make_figure.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build manuscript/main.tex
```

The compiled manuscript is `build/main.pdf`. The exact certificate records are
`evidence/rational-counterexample-certificate.json` and
`evidence/rational-counterexample-independent.json`. Reproduction scripts
write their named evidence outputs, so replay should be done in a clean copy
if preservation of an audited snapshot is required.
