# Reproducing the analytic checks

The central result is an exact pen-and-paper variational argument. The supplied
script is a secondary algebra check, not a numerical premise of the theorem.

Authoritative environment used for the accepted calculation:

- Python 3.12.14
- NumPy 2.3.5
- SciPy 1.18.1
- SymPy 1.14.0 (used by the exact symbolic replay)
- executable during the research job:
  `python3`

From the project root, run:

```sh
python3 evidence/verify-variational-identities.py
```

Compare the complete standard output with
`evidence/variational-identity-check.log`. The script checks the radial operator
identities, boundary derivatives at `b=2`, elementary Rayleigh quotients, moment
ranges, and the two exact sign factorizations. The analytic proof in
`manuscript/main.tex` uses only exact identities and `0 < rho_+/- < 1`; its
continuum field quantifier does not depend on floating-point samples.

The project-local environment record is
`evidence/research-python-environment.txt`. The downloaded primary-source PDFs
used during research are intentionally excluded from the submission bundle;
the bibliography gives their public DOI records.
