# Reproducibility guide

This package supports the numerical and symbolic checks reported in the
manuscript. The theorem itself is the analytic primal--dual proof in the paper;
solver agreement is corroboration only.

## Recorded environment

- Python 3.12.14
- CVXPY 1.9.2
- NumPy 2.5.3
- SciPy 1.18.1
- SymPy 1.14.0
- Clarabel 0.11.1
- Matplotlib 3.11.2
- TeX Live 2026 with REVTeX 4.2

The exact Python package pins are in `reproducibility/requirements.txt`.
Creating or changing an environment is left to the human author; this workflow
did not install system software.

## Regenerate the scientific checks

From the project root, using an environment with the recorded packages:

```sh
python scripts/verify_fourier_n4.py \
  --project . \
  --json-out /tmp/fourier-socp-validation.json \
  --log-out /tmp/fourier-socp-validation.log
```

Compare the regenerated files with
`evidence/research/fourier-socp-validation.json` and
`evidence/research/fourier-socp-validation.log`. The program checks the exact
Walsh identities and planar unit-vector factorization, eight named cases, 128
seeded hold-outs, the full four-vector/eight-channel SOCP, and separate
sixteen-effect parent SDPs. It rejects failed or nonoptimal solver runs.

## Regenerate the figure and manuscript

```sh
MPLCONFIGDIR=/tmp/phys-n4-mpl python manuscript/make_geometry.py
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=build manuscript/main.tex
```

The manuscript imports `manuscript/figures/geometry.pdf`. The figure is a
deterministic schematic generated from the source script, not a data plot or
AI-generated raster image.

## Evidence and redistribution scope

The handoff bundle includes only authored manuscript/figure sources and the
project's own code and generated numerical outputs needed for the reported
checks. Versioned third-party article PDFs and internal job/audit logs are not
redistributed. The bibliography gives DOI and arXiv identifiers for the
scientific sources.
