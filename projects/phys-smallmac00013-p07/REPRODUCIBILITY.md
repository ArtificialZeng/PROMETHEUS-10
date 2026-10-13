# Reproducibility guide

## Scope

The all-size result is proved analytically in manuscript/main.tex. The code
provides exact diagnostic reconstruction and finite-size checks; finite data
are not used as a substitute for the proof.

## Recorded environment

- Python 3.12.14
- NumPy 2.3.5
- SciPy 1.18.1
- SymPy 1.14.0

The authoritative runtime used for the recorded calculations was
python3. On another system,
use Python 3.12 with SymPy 1.14.0; NumPy and SciPy are recorded for environment
provenance but the exact checkers do not use floating-point numerics.

## Core exact check

From the project root:

    python3 code/verify_all_n_reduction.py \
      --output evidence/all-n-reduction-check.log

Expected final line:

    OVERALL: PASS

This checks the rational binomial transform, index-parity rule, low-Laurent
coefficients, scalar reduction and symbolic instances through n=8.

## Independent source reproduction

Route A starts only from the ASM definition; route B transcribes the BFK
Pfaffians:

    python3 code/enumerate_osasm.py \
      --max-order 12 \
      --output evidence/input-a-enumeration.json

    python3 code/pfaffian_osasm.py \
      --max-order 10 \
      --output evidence/input-b-pfaffian.json

    python3 code/compare_reproduction.py \
      --input-a evidence/input-a-enumeration.json \
      --input-b evidence/input-b-pfaffian.json \
      --output evidence/input-comparison.log

The comparison must finish with OVERALL: PASS.

## Reserved order-16 comparison

The definition-only boundary transfer and independent low-t Pfaffian routes
can be replayed with:

    python3 code/osasm_boundary_dp.py \
      --order 16 \
      --top-one 3 \
      --rhs-order 14 \
      --output evidence/order16-transfer.json

    python3 code/pfaffian_third_column.py \
      --order 16 \
      --output evidence/order16-pfaffian.json

    python3 code/compare_order16.py \
      --transfer evidence/order16-transfer.json \
      --pfaffian evidence/order16-pfaffian.json \
      --output evidence/order16-comparison.log

The recorded comparison contains eight passing exact-integer checks and no
tolerance.

## Manuscript build

The draft uses only standard TeX Live packages:

    latexmk -cd -pdf -interaction=nonstopmode \
      -halt-on-error -outdir=../build manuscript/main.tex

The expected output is build/main.pdf. No downloaded paper or third-party
figure is needed to build or reproduce the manuscript.
