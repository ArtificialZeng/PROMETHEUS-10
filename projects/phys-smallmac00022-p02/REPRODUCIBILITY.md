# Reproducing the exact certificate and manuscript

## Exact scientific replay

Run the following from the project root with Python 3.12 and NumPy 2.3.5:

```sh
python3 evidence/verify_exact_sos_independent.py
```

The write-phase environment used Python 3.12.14 and NumPy 2.3.5. SciPy 1.18.1
was installed but is not required by the independent verifier. The verifier
loads `evidence/exact-sos-certificate.json`, reconstructs all 35 words, checks
the complete coefficient dictionary for
`W^dagger conjugate(Y) W = 4*1-I3`, and repeats the pivoted exact
`LDL^dagger` test. The accepting checks use `fractions.Fraction` arithmetic;
NumPy is used only for a non-certifying floating-point eigenvalue diagnostic.

A successful replay reports:

- zero coefficient mismatches;
- 16 strictly positive rational pivots;
- an identically zero 19-dimensional Schur remainder; and
- Gram rank 16 and trace 4.

The script writes its deterministic report to
`evidence/exact-sos-independent.log`. No numerical tolerance is used to accept
the operator identity or positive semidefiniteness.

## Building the manuscript

The PDF was built with `latexmk` and a TeX Live installation from the project
root:

```sh
latexmk -C -outdir=build manuscript/main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=build manuscript/main.tex
```

The output is `build/main.pdf`; the retained compilation record is
`build/main.log`. The bibliography is generated from
`manuscript/references.bib`. The exact certificate and its verifier are
supplemental files and are not executed during TeX compilation.

## File roles and scope

- `manuscript/main.tex`: article source.
- `manuscript/references.bib`: bibliography database.
- `manuscript/requirements.txt`: Python diagnostic dependency.
- `evidence/exact-sos-certificate.json`: exact cyclotomic Gram matrix,
  permutation, and pivot data.
- `evidence/verify_exact_sos_independent.py`: certificate-only exact replay.

The replay establishes the exact value of the stated `d=3` Bell functional.
It does not establish equality rigidity, self-testing, robustness, behavior
uniqueness, randomness certification, or the conjectured values for `d>3`.
