# Finite-chain passivity: reproduction resource

The core calculation uses Python 3.10 or newer and only the standard library.
It was executed with CPython 3.14.7. No package installation is required for
the exact certificate. Work in a copy of this resource when regenerating outputs.

```sh
python3 certify.py
```

The script reads only `eigenvector-proposals.json`, encloses the exact open-chain
occupied sine projector and physical energies, verifies every proposed
eigenvalue by a Hermitian residual inequality, and sorts all Fock states at
N = 4, 8, 12, 16, 20, 24. It checks the positive N12 swap and quartic gains
and the strict N8 occupation-order inequality. Successful completion prints
`All exact certificate checks completed` and writes `certificate.json` beside
the script. The proposals are rational guesses that are checked, not trusted
eigenvalue answers. The supplied certificate is the reference output.

Each interval `[a,b]` in the certificate means the inclusive rational interval
`[a/10^90,b/10^90]`; integers are stored as strings. Decimal displays are
outward-rounded for readability. The strict manuscript bounds lie outside
the much narrower stored intervals. Small zero-containing computed intervals
at N4 and N8 alone do not prove exact equality; the analytic excitation-order
argument in the article establishes it.

The optional direct N12 density check uses NumPy and SciPy:

```sh
python3 fock-replay.py
```

That program imports none of the exact checker or proposal data. It constructs
the 924-dimensional half-filled spin/Jordan-Wigner Hamiltonian, partially
traces its ground vector to the 64-dimensional site-Fock marginal, constructs
the orbital alignment and the physical swap/quartic gate, and evaluates their
energy traces. It writes `fock-replay.json`. This floating calculation is
corroboration, not a substitute for the exact certificate. Small roundoff-negative
density eigenvalues are retained, not clipped. The archived reference run used
NumPy 2.5.3 and SciPy 1.18.1 under CPython 3.12.14; other environments can
give slightly different residuals and last digits. Its assertions use the
program's stated floating tolerances.

Energies are in hopping units J=1. The physical model has open ends, zero
chemical potential and pairing, and the unique half-filled full-chain ground
state. The subsystem is the left half; no number sector is discarded or
renormalized. The results establish a finite counterexample and the listed
finite comparisons, without a thermodynamic extrapolation or local-control
implementation claim.

These files are copies of project-authored code and generated data. No
third-party paper or downloaded source PDF is included. AI assistance in
the scientific reasoning, code, computations, and writing must accompany
any reuse of the draft's claims. Human scientific review remains necessary.
