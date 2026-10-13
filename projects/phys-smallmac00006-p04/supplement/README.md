# Online Resource 1: reproducible weak-focus certificates

Article: **Four nested limit cycles in a planar power-law reaction system**.
Draft author: Xiaojian Zeng, PBC School of Finance, Tsinghua University, 100190;
xiaojianzeng@foxmail.com. Proposed journal: Journal of Dynamics and Differential
Equations. Author details and submission suitability require human confirmation.

The manuscript proves an existential statement for the original analytic ODE.
This resource reproduces the finite coefficient/root/sign/rank calculations;
it does not substitute a truncated ODE for that equation and does not output
a finite-amplitude four-cycle parameter set.

## Reproduce the two certificates

From the directory containing `supplement`, use:

```sh
python3 -S supplement/replay.py
```

Python 3.9 or later, with its standard library, is sufficient. No installation,
network access, numerical library, Mathematica, external solver, or long-time
integrator is needed. The driver runs the two ordinary Python programs
sequentially in the foreground and fails if either exits unsuccessfully.

The default output is `build/certificate-replay/`. It must be empty or absent.
For another replay use an explicit new directory, for example:

```sh
python3 -S supplement/replay.py --output build/replay-second
```

The driver verifies `input-hashes.json`, copies the unchanged programs and
input into the new directory, and captures actual outputs there. It checks
all certificate booleans and compares every scientific JSON field with the
reference output. Only elapsed time, peak memory, Python and platform fields
may differ. It never rewrites the reference output or accepted source inputs.

## Files and mathematical conventions

- `code/research_normal_form.py`: direct original-ODE Taylor coefficients,
  complex homological conjugacy through degree nine, and parameter derivatives.
- `code/dyadic_interval.py`: integer endpoints on the 2^(-384) grid, with
  explicit outward floor/ceiling arithmetic.
- `code/research_certificate.py`: fixed rational center and preconditioner,
  contraction inclusion, negative fourth radial coefficient, and restricted rank.
- `evidence/research/certificate-input.json`: exact finite-decimal rational
  proposals; their accuracy is established by the certificate, not assumed.
- `code/independent_lyapunov.py`: independently reconstructed real homogeneous
  scalar Lyapunov equations through degree ten, using a degree-nine field jet.
- `code/independent_certificate.py`: 90-digit directed Decimal intervals,
  its own rational inverse, independent root/sign/rank certification, and exact
  Fraction checks of both published benchmarks.
- `reference/complex-certificate.json` and `reference/scalar-certificate.json`:
  archived full enclosures. They are comparison data, never generator inputs.

The four radial coefficients in the manuscript are the real parts of the
resonant complex coefficients with resonant coordinate changes set to zero.
The independent scalar constants have a triangular gauge conversion. In the
first-nonzero position, c_(k+1)=2 F_k/w^k. At the common lower zero,
det D(c3,c4)=4 w^(-5) det D(F2,F3) and F4=w^4 c5/2.
Do not compare arbitrary off-zero high-order constants by this leading formula.

## Exact expected conclusions

Both methods isolate the same root in the a,h box of half-width 10^(-20)
printed in the article. Both certify F4<0 and a nonzero unfolding determinant.
The scalar certificate also exactly checks the source calibration
F3=-4375/884736 and the target endpoint F3=-18125/2404233216.
The two generators, arithmetic backends, and inverse constructions differ.
They are both AI-generated implementations; human code review remains necessary.

All reported time is the original dimensionless time. The model has real
reaction orders, no empirical input, and no claim of integer chemical realization.
There is no stochastic, mesh, or time-step error. Rounding is controlled by
directed endpoints; the analytic state-space remainder is handled separately
in the manuscript by a uniform C1 argument. Precision and resource limits
are recorded in `ENVIRONMENT.md`.

Full downloaded literature, browser captures, credentials, internal audit
reports and conversation logs are excluded. The code is supplied for local
author review; a public license and any external deposit require author approval.
