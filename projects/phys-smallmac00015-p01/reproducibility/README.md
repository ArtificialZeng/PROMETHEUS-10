# Reproducing the analytic checks

The central result is the analytic proof in `manuscript/main.tex`. The programs below
provide independent-representation and exact finite-instance checks; finite tests do
not replace the all-parameter proof.

## Environment

The accepted calculations were run with Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1,
and SymPy 1.14.0. Install the pinned packages from `reproducibility/requirements.txt`
in an isolated environment. The standard library supplies exact `Fraction` arithmetic.

## Commands

Run from the project root with the `evidence` directory on the import path:

```sh
python3 evidence/reproduce_response.py
python3 evidence/test_spectral_gap.py
PYTHONPATH=evidence python3 evidence/check_spectral_proof.py
```

Expected terminal markers are, respectively, `RESPONSE_COMPARISON_STATUS=PASS` plus
`BASELINE_STATUS=PASS`, `status=PASS_NO_COUNTEREXAMPLE_IN_TESTED_FAMILIES`, and
`status=PASS`.

`reproduce_response.py` compares the direct probability-basis response with the
detailed-balance spectral representation and reproduces the symmetric two-state
baseline with nonlinear convergence checks. `test_spectral_gap.py` uses floating
eigenvalues only as diagnostics and exact rational LDL factorizations for each listed
finite case. `check_spectral_proof.py` verifies the secular determinant and strict
superadditivity algebra symbolically and checks exact boundary eigenpairs.

No downloaded article PDF, private runtime log, credential, or generated audit record
is required or included in the handoff bundle.
