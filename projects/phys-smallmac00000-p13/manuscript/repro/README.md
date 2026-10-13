# Reproducing the stationary-covariance illustration

The calculation uses an odd open XX chain with kappa/J=4, mu=1/2,
eta/J=5 and a centered dephasing defect. Dimensionless q is gamma_0/J;
c is fixed and dimensionless. Stationarity precedes the size limit.
Natural occupations and IPR are dimensionless. None of these quantities
is a Liouvillian decay rate or a Hamiltonian energy.

`data.json` contains the 24 finite-chain values used for the article's
figure and table: N=81,161,321,641,1281,2561, c=1/2,2, with q=c/N and
q=c/(N-1). It includes the evaluated finite analytic bounds. The PDF
figure shows the q=c/N subset. No fit or random sampling is used.

From the directory containing this README, with the listed Python
packages already available, run:

```sh
python3 reproduce.py --verify --out reproduced
```

Use a fresh output directory on subsequent runs. This command writes
`reproduction.json`, `convergence.pdf`, `convergence.png`, and
`finite-size-table.tex` to that directory. The existing reference data
are read only. Omitting `--verify` regenerates the figure and table from
the supplied values without recomputing eigenpairs.

The eigensolver stores a real tridiagonal matrix and requests its zero
and first positive eigenpairs. The zero-vector residual and comparisons
with the supplied values are saved. The four N=2561 cases additionally
use an 80-digit boundary recurrence for IPR and the alternate LAPACK
QR eigenvalue driver. Acceptance tolerance for these numerical
reproduction diagnostics is 2e-12. The tested reproduction's maximum
spacing and IPR differences from the reference data were respectively
2.92e-16 and 7.22e-16. This is agreement between implementations and
precision choices, not an interval-certified error bound.

One process and one numerical thread are used, with O(N) matrix storage
and N at most 2561. The measured eigenvalue/recurrence portion took
approximately 0.41 seconds in the recorded environment; plotting and
font initialization are additional. The analytic proof, rather than
these finite data or diagnostic tolerances, establishes the limits.
The stored upper bounds illustrate the inequalities in the article;
their floating-point evaluation is not a substitute for the proof.

`environment.json` records the actual writing-phase environment.
`requirements.txt` records package versions, without vendoring any
third-party package. No system installation is part of this package.

To build the article from its parent `manuscript` directory, run:

```sh
python3 build.py --out build-local
```

This requires an existing TeX installation with latexmk, pdfLaTeX,
BibTeX, and the standard packages imported in `main.tex`. It creates a
clean output directory and retains compiler and bibliography logs.
The included `main.bbl` is the generated bibliography for portable
handoff; `references.bib` is its source. To check a regenerated figure
or table, compare its numbers and rendering before replacing anything
in an already reviewed manuscript.
