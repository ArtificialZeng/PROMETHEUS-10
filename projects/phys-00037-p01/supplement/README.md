# Reproduction of the three-mode entropy Hessian certificate

Article: Second-order entropy stability of a three-mode fermionic product channel.
Draft author: Xiaojian Zeng, PBC School of Finance, Tsinghua University, Beijing
100190, China; xiaojianzeng@foxmail.com. Author details require confirmation.

This is the computational supplement (Online Resource 1) for the exact
second-order statement. It does not prove a global entropy minimum, higher-mode
stability or entropy differentiability at b1=1. The analytic resolvent reduction
and inequalities are in the manuscript. Numeric diagnostics in the CP checker
are supplementary convention checks, not the continuous-parameter proof.

## Run

Use Python 3.12 with NumPy 2.5.3 and SymPy 1.14.0, the versions tested here.
The code needs no network access or third-party paper files. From the bundle root:

```sh
python3 supplement/run_checks.py --output-dir replay-output
```

Do not use `python -O`. The programs reject optimized assertion removal.
The output directory must be outside the source supplement directory. All new
data go there; the shipped witness and source files are read-only inputs.
The run finishes with `replay-output/summary.json` and actual stage output on
stdout. Return code zero is required; an interrupted run is not a pass.

1. `generate_polynomials.py` expands the four resolvent numerator coefficients
   symbolically in the six squared attenuations.
2. `generate_certificate.py` imposes the analytic worst case f=e, maps the
   ordered chamber to the five-dimensional ratio cube, and computes every
   Bernstein coefficient by exact integer tensor conversion. NumPy object
   arrays carry Python arbitrary-precision integers, not machine-width floats.
3. `verify_monomials.py` rebuilds the full Jordan-Wigner monomial channel,
   verifies its 192 reference/normal/coherence matrix entries and Gaussian
   tangent rank, rebuilds polynomials with sparse integer dictionary operations,
   and verifies the witness by inverse finite differences.
4. `verify_cp.py` independently within the algorithm reconstructs the CP-factor
   channel, source output and coherence entries, tangent/support identities,
   and a fresh Fraction-valued Bernstein expansion. It then compares each
   freshly computed value with the supplied witness. It also replays the known
   one-/two-mode rational spectra and 29 floating full-Hessian diagnostics.

The wrapper requires the freshly generated certificate to agree in full with
`certificate.json`. Expected counts: 37,320 rational coefficients, 192 source
matrix identities in each representation, tangent rank 12, 384 CP support
identities. The witness records common positive denominators and flattened
arrays in Python C order, last index fastest. For each k=0,1,2,3,
coefficient = all_scaled_coefficients[index]/common_denominator; tensor shape
is ratio_degrees+1. The x0-index-1 slice at k=0 is identically 4/5.

## Compilation

From the bundle root, with a standard TeX installation:

```sh
python3 manuscript/build.py --output-dir manuscript-build
```

This runs pdflatex, BibTeX and two further pdflatex passes with shell escape
disabled, and retains stage logs. No publisher-specific class is required.

## Scope and provenance

The witness is a byte-identical copy of the accepted scientific evidence.
The scripts are path-only adaptations of the reviewed generating/checking
implementations. Running these ports is a portability check; it is not a new
independent scientific referee. Generic exact arithmetic libraries and common
primary-source conventions are shared. The author must review the argument,
code, literature priority and extensive AI involvement before submission.

Only original manuscript/code and the project's exact rational witness are
included. Downloaded primary papers, private records and process logs are
excluded. No assertion of human authorship approval or third-party licensing
is made by this source selection.
