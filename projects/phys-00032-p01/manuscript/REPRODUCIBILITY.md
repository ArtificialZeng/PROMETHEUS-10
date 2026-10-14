# Reproducing the computer-assisted part

The paper's analytic argument is in `manuscript/main.tex`. The finite certificate is represented by rational boxes and can be checked without optimization or sampling.

## Included central files

- `evidence/research/certify_cycle.py`: directed `mpmath` interval generator.
- `evidence/research/cycle-certificate.json`: complete 3,782-leaf rational cover and generator enclosures.
- `evidence/research/check_certificate_integer.py`: separate standard-library fixed-point replay.
- `evidence/research/integer-replay-data.json`: successful replay summary and exact integer endpoints.
- `evidence/research/structural_checks.py` and `structural-check-data.json`: noncertifying convention diagnostics for generic unitaries and signed mixtures.

The accepted records were produced with Python 3.14.7 and mpmath 1.3.0 on macOS arm64. The generator uses one CPU and normally completes in a few seconds. The integer replay uses only the Python standard library.

## Commands

Run the following from the root of an extracted copy of the project or submission bundle:

```sh
python3 evidence/research/certify_cycle.py
python3 evidence/research/check_certificate_integer.py
```

The first command regenerates `cycle-certificate.json`; the second reads it, reconstructs the exact rational bisection tree, and rewrites `integer-replay-data.json`. Run in a disposable extracted copy if the archived evidence files must remain byte-identical.

Successful output reports 7,563 visited nodes and 3,782 leaves: 3,393 interval-positive leaves, 388 analytic-small-current leaves, and one leaf outside the half-domain. The fixed-point scale is `2^128`; the logarithm uses 40 terms after range reduction and an explicit positive remainder. The minimum rigorous leaf-margin lower endpoint must remain positive.

The analytic boundary arguments are necessary: the finite cover alone proves only the compact-domain portion identified in the manuscript. Discovery scans and floating-point structural fixtures are not part of the proof certificate.
