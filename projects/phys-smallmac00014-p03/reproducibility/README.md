# Reproducing the checks and figure

The central result in the manuscript is analytic. The supplied calculations check the
rate convention, the modal coefficients, perturbative convergence, periodic closure,
probability positivity, and agreement of two numerical representations.

## Environment

The archived run used Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1, and Matplotlib
3.11.2. `requirements.txt` records the Python-package versions. Use a local virtual
environment; no network access is required after those packages are available.

## Linear-response and nonlinear checks

From the project root, run

```sh
python3 evidence/verify_k3_linear_response.py
```

The checker imports `evidence/search_k3_phase.py`. It prints the exact modal values,
full nonlinear periodic-propagator values at four amplitudes, eliminated-coordinate
Fourier-collocation comparisons, probability/normalization/periodicity diagnostics, and
a finite spectral-grid sanity check. The finite scan is not used as a proof.

The two rows quoted in the manuscript correspond to the labelled cases
`generic_two_harmonic` and `near_effective_two_state`. Their accepted captured output is
summarized without workflow metadata in `reproducibility/check-results.txt`; the scripts
regenerate it from the stated inputs rather than reading saved trajectories. The fuller
project evidence log remains in the research dossier and is not needed in the handoff.

## Exact sharpness figure

From the project root, run

```sh
MPLCONFIGDIR=/tmp/phys-00014-mpl python3 manuscript/figure_sharpness.py
```

This writes `manuscript/sharpness.pdf` and `manuscript/sharpness-data.csv` from the exact
formula `2 + exp(-H/2)`. The figure contains no fitted or externally sourced data.

## Scope

These scripts support the leading-order weak-driving result only. They do not certify
the unresolved finite-amplitude inequality, a uniform radius in amplitude, different
graph topologies, heterogeneous kinetic prefactors, asymmetric rate splittings, or more
than three states.
