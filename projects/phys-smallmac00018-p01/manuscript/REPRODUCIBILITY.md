# Reproducing the exact checks and manuscript figure

The scientific claim is established by the exact-arithmetic scripts in `scripts/`.
Run them from the project root with the recorded scientific Python:

```sh
python3 scripts/reproduce_baseline.py
python3 scripts/verify_extrema_reduction.py
python3 scripts/verify_gap_factorization.py
python3 scripts/certify_global_boundary.py
python3 scripts/verify_laurent_reconstruction.py
```

The first script includes converged numerical Chern checks. The decisive boundary
identities, resultants, Sturm counts, and sector exclusions in the latter scripts use
SymPy exact rational arithmetic (and the explicit quadratic field at the cusp).
Floating-point optimizers and plotted samples are corroboration or visualization only.

Regenerate the submitted figure and its data table with:

```sh
python3 manuscript/generate_phase_diagram.py
```

The write-stage environment was Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1,
SymPy 1.14.0, and Matplotlib 3.11.2. The plotting script asserts four accepted
boundary values before reporting success. `data/phase_boundary.csv` records the
plotted parametric samples; `figures/phase_diagram.pdf` is the vector figure used by
the manuscript. The exact formulas, rather than the CSV samples, define the boundary.
