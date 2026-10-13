# Reproducing the breathing-kagome Comment

This package supports the finite, source-raster-bound claims in the Comment.
It does not establish the unresolved general connectivity criterion or an
infinite-size phase transition.

## Environment

The accepted calculations and final figure used Python 3.12.14 with NumPy
2.3.5, SciPy 1.18.1, SymPy 1.14.0, python-flint 0.9.0, and Matplotlib 3.11.2.
Pinned Python package versions are in `requirements.txt`. The manuscript was
built with REVTeX 4.2f, pdfTeX 1.40.29, BibTeX 0.99e, and latexmk 4.88 from
TeX Live 2026.

Run reproductions in a copy of the package because the research scripts write
their named output certificates. From the package root:

```sh
python3 scripts/isolated_corner_polynomial.py \
  --output evidence/isolated-corner-polynomial.json \
  --log evidence/isolated-corner-polynomial.log

python3 scripts/replay_isolated_corner_polynomial.py \
  --certificate evidence/isolated-corner-polynomial.json \
  --log evidence/isolated-corner-replay.log
```

The first command reconstructs the 15-site graph, mirror-sector
factorization, coefficient gcd, endpoint polynomials, and three-component
N=20 decomposition using exact SymPy algebra. The second imports neither
SymPy nor the first script; it rebuilds all bivariate coefficients with exact
`fractions.Fraction` Faddeev--LeVerrier evaluations and Newton interpolation,
then checks two unused rational interpolation parameters.

The finite `t=0.1`, `t'=1` crossing certificate is reproduced by:

```sh
python3 scripts/certify_parity_crossing.py .
```

This requires `evidence/geschner-input-a.json` and
`evidence/geschner-input-b.json`. It uses exact python-flint rational inertia;
floating-point values only seed broad bisection intervals.

The accepted uniform-edge transfer diagnostic is reproduced by:

```sh
python3 scripts/edge_transfer_analysis.py .
```

This reads `evidence/finite-size-isolation.json` and imports
`scripts/finite_size_isolation.py`. Its transfer identities are analytic,
whereas the match to finite-size ratios is deliberately labeled numerical.

Regenerate the vector figure and manuscript with:

```sh
MPLCONFIGDIR=/tmp/phys-p03-mpl python3 manuscript/make_core_spectrum.py \
  --output manuscript/fig_core_spectrum.pdf

cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../build main.tex
```

The figure script reads `evidence/isolated-corner-polynomial.json`. A correct
build produces `build/main.pdf`; `pdftotext` should show two resolved
references and the exact values 13 and 39. All 15 vertices, all 17 core edges,
and the two endpoint characteristic polynomials should agree with the
certificate before scientific use.
