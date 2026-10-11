# Reproducibility guide

## Scientific scope

The calculation certifies one finite-radius local statement at the
`a=1/2` stationary point in an explicit canonical rank-at-most-two
single-qubit Kossakowski chart. It does not test or certify rank-three
dissipation, distant charts, a global restricted minimum, unbounded
rate/time tails, or the boundary of `Q2`.

The decisive machine-readable record is
`evidence/interval-rank-two-neighborhood.json`; its 320-bit replay and the
independent complex matrix-unit diagnostic are
`evidence/interval-rank-two-neighborhood-320.json` and
`evidence/interval-rank-two-neighborhood-verification.json`.

## Recorded environment

- Python with NumPy.
- `python-flint` 0.9.0 backed by Arb ball arithmetic.
- Arb precision 256 bits for the primary certificate and 320 bits for the
  precision replay.
- SciPy is used only by the independent finite-difference/fixed-constraint
  diagnostic, not by the interval proof.
- Matplotlib is used only to regenerate the presentation figure.

The archived research scripts contain the task-local absolute path used to
load the isolated `python-flint` wheel. On another machine, set the
`ARB_PATH` constant in `evidence/research_interval_kkt.py` to a compatible
python-flint 0.9.0 installation before running. This portability edit changes
only dependency discovery; compare regenerated JSON fields and numerical
records rather than treating a successful import as a scientific check.

## Regeneration commands

Run from the project root with a Python interpreter compatible with the
recorded python-flint wheel. Write replays to new files so the frozen records
are not overwritten.

```sh
python3 evidence/research_interval_rank_two_neighborhood.py \
  --precision 256 \
  --json /tmp/rank-two-256.json \
  --log /tmp/rank-two-256.log

python3 evidence/research_interval_rank_two_neighborhood.py \
  --precision 320 \
  --json /tmp/rank-two-320.json \
  --log /tmp/rank-two-320.log

python3 evidence/verify_interval_rank_two_neighborhood.py \
  --json /tmp/rank-two-independent.json \
  --log /tmp/rank-two-independent.log
```

The primary script imports
`evidence/research_interval_kkt.py` and
`evidence/research_interval_second_variation.py`, and the KKT script reads
`evidence/second-variation-verification.json` for the independently obtained
starting center. The integrity-only source check reads `source.md`; the
physics calculation is described in the manuscript and scripts.

Regenerate the figure with:

```sh
MPLCONFIGDIR=/tmp/phys-00002-mpl \
python3 manuscript/make_figure.py \
  --input evidence/interval-rank-two-neighborhood.json \
  --output manuscript/figures/certificate-radii.pdf
```

Build the paper from a clean output directory with:

```sh
latexmk -C -cd -outdir=../build manuscript/main.tex
latexmk -pdf -cd -interaction=nonstopmode -halt-on-error \
  -outdir=../build manuscript/main.tex
```

## Expected decisive checks

- all eight coordinates of the interval-Newton image lie strictly inside
  their input box;
- the selected coordinate-cube radius is `1e-4` at both 256 and 320 bits;
- the smallest directed Gershgorin lower endpoint for the whitened interval
  Hessian is greater than `0.033388632850592175`;
- the resulting fixed-section coefficient `0.0165` is below half of the
  certified Hessian bound;
- the independent matrix-unit diagnostic reports a positive numerical
  Hessian, exact-chart orthogonality within its stated tolerance, normalized
  probability columns, and all corrected fixed-`a` holdouts above the root.

The larger-radius negative Gershgorin endpoints are failures of this direct
enclosure test, not counterexamples or physical instabilities.
