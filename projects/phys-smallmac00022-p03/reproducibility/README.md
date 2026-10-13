# Reproducing the finite subdivided-star result

The central claim is the exact finite-range statement

`Delta(T_q,s) > 1-s^2` for `q=1,...,6` and every real `0<s<1`.

The proof for `q=1` is given symbolically in the manuscript and in
`evidence/path4-exact-analysis.md`. For `q=2,...,6`, use the following files:

- `evidence/certify_subdivided_star_continuum.py`: exact block, resultant,
  real-root-isolation and rational-enclosure generator;
- `evidence/subdivided-star-continuum.json`: saved exact certificate;
- `evidence/verify_subdivided_star_continuum.py`: independent direct
  computational-basis checker of every saved rational inequality and selected
  full spectra;
- `source.md`: immutable model statement used by the independent checker.

## Environment

The validated environment used Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5 and
SciPy 1.18.1. Install the exact Python dependencies from
`reproducibility/requirements.txt`. No proprietary solver is required.

## Commands

From the project root, regenerate an exact packet with

```sh
python3 evidence/certify_subdivided_star_continuum.py \
  --min-q 2 --max-q 6 --resultant-epsilon-power 24 \
  --output reproduced-continuum.json
```

Then check either the frozen packet or the regenerated packet with

```sh
python3 evidence/verify_subdivided_star_continuum.py \
  --packet evidence/subdivided-star-continuum.json --source source.md
```

The exact rational endpoints returned by real-root isolation need not be
byte-identical between otherwise valid runs. Compare the polynomial invariants,
root counts, exact inequalities and conclusions, rather than requiring a
particular noncanonical isolating interval.

The direct-basis diagonalizations in the checker are corroborative. The
continuous-parameter proof rests on exact rational polynomial arithmetic,
complete block enumeration, exact real-root isolation and the saved Weyl
enclosures.
