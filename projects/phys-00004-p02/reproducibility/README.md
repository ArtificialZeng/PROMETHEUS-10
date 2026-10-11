# Reproducing the exact counterexample

The manuscript's conclusion requires no floating-point optimizer. The tuple is
stored in `certificate.json`, and `verify_counterexample.py` checks it using
Python's standard-library `fractions.Fraction` class.

From the root of the unpacked source bundle, run:

```sh
python3 reproducibility/verify_counterexample.py
```

The command requires Python 3.9 or later, no third-party packages, and no
network access. It exits nonzero if a check fails and otherwise prints a JSON
object with `"status": "PASS"`.

The spectral check is deliberately independent of evaluating the quadratic
radical in the paper. For `G=C^T C`, it restricts `(2/3)I-G` to the sum-zero
basis `(1,-1,0)` and `(1,1,-2)`. The resulting symmetric quadratic form has
positive leading principal minor `2602/5625` and positive determinant
`292/16875`. Hence it is positive definite on the full nonuniform subspace,
which proves that every nontrivial eigenvalue of `G` is strictly below `2/3`.
The norm excess is then checked by the positive integer

```text
3*519655217^3 - 15^12*1341^4
= 1409896381134395295169314.
```

To build the paper from the project root with REVTeX 4.2 and BibTeX available:

```sh
mkdir -p build
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

The expected output is `build/main.pdf`. The manuscript does not claim that
the supplied witness is a global maximizer; its strict feasible value alone
disproves the universal identity.
