# Reproducing the local-stability draft

Run commands from the project root.  The required scientific interpreter is
`python3`.  The recorded
environment is Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1,
python-flint 0.9.0, and mpmath 1.3.0.

## Scientific calculations

The designated rigorous calculation is:

```sh
python3 evidence/certify_u16_hessian.py
```

It must finish with `certificate=PASS`, after reporting an 81-dimensional
Hessian, 81 positive interval LDL pivots for the rational shift `159/1000`,
and the exact opening-map scale `5/338`.  Its archived output is
`evidence/u16-hessian-certificate.log`.  Replays at other precisions are:

```sh
U16_ARB_BITS=256 python3 evidence/certify_u16_hessian.py
U16_ARB_BITS=384 python3 evidence/certify_u16_hessian.py
```

`evidence/analyze_u16_tangent.py` and
`evidence/verify_tangent_high_precision.py` generate independent numerical
diagnostics.  They do not replace the Arb certificate.  The baseline scripts
`evidence/reproduce_input_a.py` and `evidence/reproduce_input_b.py` reconstruct
the published one-copy spectrum and below-one signed witness in two different
representations.

## Manuscript build

The manuscript depends on `manuscript/main.tex`,
`manuscript/figure-tangent.tex`, and `manuscript/references.bib`.  Build with:

```sh
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=build manuscript/main.tex
```

The expected PDF is `build/main.pdf`; the compiler transcript is
`build/main.log`.  The local draft is for author review and is not an external
submission.
