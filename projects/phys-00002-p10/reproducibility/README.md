# Reproduce the quarter-order beam-splitter counterexample

The input is exactly (20|0>+|2>)/sqrt401 on each independently prepared mode.
The comparison uses [x,p]=i, hbar=1, natural logarithms, the full dx dp plane,
lossless balanced mixing and a partial trace. This is a finite-support physical
state, not a truncation of an infinite-support input. No external data are needed.

All certificate programs use Python's standard library only. From the package
root, run:

```sh
python3 reproducibility/run_all.py --output build/reproduction
```

The output directory must not exist already. Choose another new directory under
build/ for a subsequent replay, for example build/reproduction-2. The runner
copies the programs into that scratch directory before execution and leaves
all supplied reference outputs untouched. It creates environment.json,
exact.log, decimal.log, integer.log, computed JSON outputs and comparison.json.
Typical execution in the checked environment takes under a minute; this is
an observation, not a runtime guarantee.

## Programs and reference outputs

1. evidence/alpha-quarter-witness-exact.py reconstructs the Wigner polynomial
   with exact Fraction arithmetic in Q(sqrt2). It compares creation-map,
   partial-trace and Laguerre expressions with Hermite/Fourier moments and
   verifies normalization. Its reference output is
   evidence/alpha-quarter-witness-exact.json.
2. evidence/alpha-quarter-jensen-enclosure.py imports the directed Decimal
   arithmetic in evidence/alpha-quarter-enclosure.py. It computes analytic
   polar-cell moments, absolute-value chords and weighted Cauchy bounds on
   800x64 and 1600x128 grids through R=100, including an analytic exterior
   tail. Its reference output is evidence/alpha-quarter-jensen-enclosures.json.
3. reproducibility/independent_replay.py separately reconstructs the partial
   trace in coordinate space and uses integer fixed-point outward intervals
   with denominator 10^35 for the 1600x128 grid and a separately looser tail.
   Its reference output is reproducibility/independent-enclosure.json.

Do not run the original evidence scripts in place if preserving reference
outputs is desired: their historical interfaces write JSON alongside their
sources. The scratch runner handles this automatically. A program's comparison
with supplied reference outputs checks reproducibility; it does not establish
independence. The two calculations share the stated mathematical cell inequality
and grid, but use distinct physical reconstruction paths and arithmetic backends.

## Expected scientific checks

- Exact normalization one and identical W=e^(-R) Q^2/pi coefficients.
- Decimal full-plane uppers 9.437261993640953 and 9.437179016856389, rounded up.
- Integer full-plane upper 9.437179021478335, rounded up.
- Vacuum lower greater than 9.4389219696587875.
- 621 sign-straddling cells on the fine grid, with no omitted nodal cells.

All quoted values are upper bounds on the physical integral, except the stated
vacuum lower. Lower endpoints of intervals for the evaluated upper-bound
expressions are not lower bounds on the physical integral. A two-sided entropy
estimate is unnecessary: the strict integral ordering proves the entropy
ordering because log is increasing and 1-alpha is positive.

The exact derivation, tail control and scope are given in manuscript/main.tex;
reproducibility/SOURCE_MAP.md maps its formulas and data to the supplied programs.
No optimizer, empirical screen or finite-plane quadrature is required for the
conclusion. Python integer/Fraction arithmetic and Decimal elementary functions
remain the software trust base; no formal proof-assistant or experiment is claimed.

## Build the manuscript

With TeX and BibTeX installed, from the package root:

```sh
mkdir -p build/manuscript
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/manuscript main.tex
cd ../build/manuscript
env BIBINPUTS=../../manuscript: bibtex main
cd ../../manuscript
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/manuscript main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/manuscript main.tex
```

The local package contains authored code, data and manuscript sources only;
third-party full papers and internal job/audit logs are not redistributed.
Bibliographic primary-source links are provided in manuscript/references.bib.
Human scientific review, authorship and journal-policy decisions remain pending.
