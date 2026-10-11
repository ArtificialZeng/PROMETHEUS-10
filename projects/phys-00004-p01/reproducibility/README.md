# Reproducibility guide

This directory contains the deterministic data and plotting code for
Fig. 1 of the manuscript. The frozen central proof and its independent
channel checks are in the project-level `evidence/` files listed in
`claim.json`; the plot is an illustration and is not the universal proof.

## Environment

The figure was generated with Python 3.12.14 and the versions pinned in
`requirements.txt`:

- NumPy 2.5.3
- SymPy 1.14.0
- Matplotlib 3.11.2
- SciPy 1.18.1
- mpmath 1.3.0

Create an isolated environment, install `requirements.txt`, and run from the
project root:

```sh
python reproducibility/generate_figure.py
```

The script imports `evidence/method_a_kraus.py`, applies the explicit GADC
Kraus operators, and writes:

- `manuscript/figures/gadc_two_use_summary.pdf`;
- `reproducibility/figure_curve.csv`; and
- `reproducibility/figure_phase.csv`.

Optional command-line arguments `--output`, `--curve-data`, and
`--phase-data` can redirect those three outputs. A headless run may set
`MPLCONFIGDIR` and `XDG_CACHE_HOME` to writable temporary directories.

## What is checked

For panel (a), the script evaluates the analytic one-use optimum at
`gamma=0.55`, `eta=0.20` and independently computes half of the ergotropy of
the corresponding two-copy output by a direct Kraus sum. Their maximum
sampled difference was `2.7755575615628914e-16`. The theorem, rather than the
plotting calculation, identifies that product value with the unrestricted
two-use optimum.

For panel (b), the script varies the invariant phase in the equal-population
input at `gamma=1/2`, `eta=1/4`. It reproduces the exact endpoint purities
`625/1024` at phase zero and `417/1024` at phase pi with zero reported
floating-point difference. The actual command and stdout are retained in
`figure-generation.log`.

## Exact proof checks

The central algebra can be replayed with the frozen scripts, in particular:

```sh
python evidence/verify_gadc_coefficients.py
python evidence/verify_gadc_quadratic_proof.py
```

Their captured outputs are
`evidence/gadc-coefficient-verification.log` and
`evidence/gadc-quadratic-proof-verification.log`. These exact symbolic checks,
not the sampled figure data, support the quantified result.
