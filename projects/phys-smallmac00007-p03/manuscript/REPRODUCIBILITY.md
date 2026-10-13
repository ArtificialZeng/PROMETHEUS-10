# Reproducing the exact split-core calculation

The central theorem is exact and has no floating-point tolerance. From the project
root, use Python 3.12 with SymPy available and run:

```sh
python3 code/derive_surgery_exact.py
python3 code/check_surgery_exact.py
```

The first command derives the four rational gaps, the one-bit specializations and
the positive-coefficient identities. Compare its structured output with
`evidence/surgery-symbolic.json`. The second independently evaluates explicit code
strings from the source formula and selected literal full-graph fundamental-matrix
inversions; compare with `evidence/surgery-exact-check.json`.

The audited write environment used CPython 3.12.14, SymPy from the project runtime,
NumPy 2.3.5 and SciPy 1.18.1. NumPy and SciPy are not used to establish the exact
central inequalities. The accepted source baseline and independent referee replay
remain in the local research dossier and are not redistributed with a submission.

No downloaded third-party paper is needed in a submission bundle. The formulas
required to interpret the computation are stated in the manuscript and attributed
to the checked arXiv:2310.08552v1 source.
