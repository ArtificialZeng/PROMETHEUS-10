# Reproducibility guide

This package reproduces the exact quotient certificate, the independent
two-time covariance/Wick check, the published zero-field work-current
benchmark, and the figure used in the manuscript. Run all commands from the
project/package root with Python 3.12 or later.

The reference environment used for this draft is recorded in
`reproducibility/environment.txt`. The scripts require NumPy, SciPy, SymPy,
Matplotlib, and (for the numerical Wick quadrature) their standard compiled
dependencies. No random seed is needed: all calculations are deterministic.

## Central exact certificate

```sh
python scripts/quotient_symbolic.py
python scripts/verify_quotient.py
```

The first command constructs the complete rotation-invariant and angular-two
polynomial sectors, solves the centered Poisson equations, and asserts exact
zero residuals. The second audits the positive-coefficient polynomials and
compares the closed formula to complete 69-unknown rational Poisson solves at
three hold-out points. A successful run ends with `status=PASS`.

## Independent numerical representation

```sh
python scripts/quotient_wick.py
python scripts/compare_quotient_methods.py
```

These commands reconstruct two-time covariances in complex coordinates,
integrate symmetrized Wick contractions, and compare the resulting matrices to
the real polynomial-Poisson implementation. The accepted reference tolerances
and values are summarized in `reproducibility/verification-summary.csv`.

## Published work-current benchmark

```sh
python scripts/baseline_poisson.py
python scripts/baseline_wick.py
python scripts/compare_inputs.py
```

The two reconstructions use different coordinate orders and computational
representations. They reproduce

\[
\langle\dot W\rangle=\frac{2\kappa^2T}{\gamma k_*},\qquad
D_W=\frac{2\kappa^2T^2}{\gamma k_*^3}
\left(k^2+\kappa^2+\frac{3mk\kappa^2}{\gamma^2}\right).
\]

## Figure

```sh
MPLCONFIGDIR=/tmp/phys-quotient-mpl python scripts/make_figure.py
```

This writes `figures/quotient_spectrum.csv`,
`figures/quotient_spectrum.pdf`, and `figures/quotient_spectrum.png`. The grid
is only a visualization; it is not used to certify positivity.

## Expected interpretation

- The exact proof is the rational-function identity plus its positive-domain
  certificate, not the numerical grid or finite hold-outs.
- Strict stability requires `kstar > 0`; no boundary or unstable point is
  admitted.
- The comparison preserves `m`, `gamma`, and `T` and uses equilibrium stiffness
  `kstar`, not the driven spring parameter `k`.
- Diffusion means `lim Var/(2t)`. Gradient currents are stationary boundary
  increments and vanish only after taking this long-time rate.

The package contains no experimental or proprietary data. Third-party source
papers are intentionally excluded from the submission-file list.
