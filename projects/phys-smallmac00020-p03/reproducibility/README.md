# Reproducibility instructions

This package regenerates the numerical checks and figure for the manuscript
“Two-scale finite-size edge splitting at a repeated root of an extended
Su–Schrieffer–Heeger chain.” No random inputs or external data are used.

## Recorded environment

- Python 3.12.14
- NumPy 2.3.5
- SciPy 1.18.1
- mpmath 1.3.0
- Matplotlib 3.11.2
- TeX Live 2026 with REVTeX 4.2f and latexmk 4.88

The scientific run used
`python3`. A portable environment
can instead be created from `reproducibility/requirements.txt` with any
compatible Python 3.12 installation.

## Regenerate numerical evidence

Run from the project root:

```sh
python3 evidence/confluent_analysis.py
python3 evidence/check_confluent_exact.py
python3 reproducibility/generate_figure.py
```

The first program prints the high-precision validation table and the exact
rational endpoint inequalities. The second checks the finite Gram matrix,
projected Hamiltonian, inverse transformation, and triangular-tail identity in
40 exact-fraction cases. The third writes
`reproducibility/edge_splittings.csv` and
`manuscript/edge_splittings.pdf`. It evaluates the full-chain energies from the
two largest singular values of the rescaled inverse matrix, which avoids the
loss of relative precision incurred by directly diagonalizing exponentially
small eigenvalues in ordinary double precision.

## Build the manuscript

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -outdir=../build manuscript/main.tex
```

The expected output is `build/main.pdf`. The downloaded primary-source PDF is
not required to compile or reproduce the calculation and is intentionally
excluded from the handoff bundle.

## Scope

The programs evaluate the finite, open, Hermitian single-particle model with
`u0=r^2`, `u1=2r`, and `u2=1`. They do not model disorder, interactions,
non-Hermitian hopping, experimental noise, or a thermodynamic limit at fixed
physical length.
