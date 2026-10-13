# Reproducing the computer-assisted counterexample

Use Python 3.12.14 with the versions pinned in `requirements.txt`. From the project
root, verify the interpreter and packages first:

```sh
command -v python3
python3 -c 'import sys,numpy,scipy,flint; print(sys.executable); print(sys.version); print(numpy.__version__,scipy.__version__,flint.__version__)'
```

The environment used for the accepted calculation resolved to
`python3`, with NumPy 2.3.5, SciPy
1.18.1, and python-flint 0.9.0. The path is machine-specific; matching package versions
and a working Arb/FLINT backend are the portable requirements.

Regenerate the primary certificate:

```sh
python3 evidence/certify_counterexample.py \
  --segments 2048 --subdivisions 1024 --precision 256 \
  --output evidence/counterexample-interval-certificate.regenerated.json
```

Regenerate the changed-partition replay:

```sh
python3 evidence/certify_counterexample.py \
  --segments 4096 --subdivisions 512 --precision 320 \
  --output evidence/counterexample-interval-replay.regenerated.json
```

The decisive fields are `logical_checks.A_strictly_positive`,
`logical_checks.B_strictly_positive`, and
`logical_checks.margin_strictly_negative`. Compare all non-timing fields against the
distributed JSON records. Runtime depends on hardware; the primary accepted run used
2,097,152 residual boxes.

SciPy only proposes a periodic cubic comparison path. Its local or global numerical
error is never trusted. Arb encloses the continuum residual on every subbox, and the
analytic contraction argument converts that residual into a uniform enclosure of the
exact periodic state.

## Included scientific files

- `evidence/counterexample-parameters.json`: exact terminating-decimal witness.
- `evidence/certify_counterexample.py`: proposal construction and interval certificate.
- `evidence/counterexample-interval-certificate.json`: primary 256-bit record.
- `evidence/counterexample-interval-replay.json`: 320-bit changed-partition record.

The downloaded predecessor paper and thesis are citation sources, not redistributable
supplementary material, and are deliberately excluded from the handoff archive.
