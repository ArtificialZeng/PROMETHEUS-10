# Reproducing the exact non-saturation certificate

## Scope

The replay establishes only the equality obstruction used in the manuscript:
no seven two-qubit product rays have all 21 transition probabilities of the
fixed target. It then prints the negative Bloch-Gram determinant for the sole
algebraic survivor. It does not compute `Q_SEP`, reproduce the published
floating-point see-saw point, or produce an explicit numerical gap.

## Tested environment

- Python 3.12.14
- SymPy 1.14.0
- NumPy 2.3.5
- SciPy 1.18.1

The authoritative project interpreter was
`python3`; the environment probe
is recorded in `evidence/write-python-environment.txt`. The exact checker uses
SymPy and the Python standard library; NumPy and SciPy are recorded to make the
scientific environment complete.

## Files

- `scripts/reproduce_input_a.py`: generates the coordinate transcription,
  exact state/frame checks, 21 transition probabilities, and the unrestricted
  `3/4` baseline.
- `evidence/input-a.json`: frozen machine-readable output used by the checker.
- `scripts/check_product_saturation.py`: exact parity enumeration, polynomial
  construction, Groebner checks, and final Gram calculation.
- `evidence/product-saturation-exact.log`: expected exact output.

The downloaded primary paper is intentionally excluded from the submission
bundle. The seven states, weights, and full transition matrix needed for the
calculation appear in the manuscript and scripts.

## Commands

From the project root, in an environment satisfying `requirements.txt`:

```sh
python3 scripts/check_product_saturation.py
```

Compare its standard output byte-for-byte with
`evidence/product-saturation-exact.log`. To regenerate the coordinate input
from the displayed formulas before replaying the checker:

```sh
python3 scripts/reproduce_input_a.py
python3 scripts/check_product_saturation.py
```

The input generator intentionally overwrites `evidence/input-a.json`; run it in
a copy of the handoff directory if preservation of the frozen file is needed.

## Exactness boundary

All decisive zero tests and ideal computations use rational arithmetic in the
algebraic extension `Q(sqrt(7))`. The rejected classes have unit Groebner ideal.
The survivor's determinant is exactly `-27/16`, with eigenvalues
`{-1/2, 3/2, 3/2, 3/2}`. No floating-point tolerance enters the conclusion.
