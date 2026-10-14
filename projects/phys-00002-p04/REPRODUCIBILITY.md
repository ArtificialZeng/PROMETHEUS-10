# Reproduce the thermal heat-cumulant counterexample

Run from this directory:

```sh
python3 code/reproduce_manuscript.py
```

This performs exact Fraction arithmetic with Python's standard library. No package
installation is needed. It constructs the three-state model from symmetric thermal
factors, solves normalized eigenvector derivative equations, and compares with an
independently transcribed determinant implementation and saved exact answers. It
checks the scalar coefficient table, stationary probabilities, all four cumulants,
and determinant residuals. It prints results without writing frozen evidence.
The tested environment is recorded in evidence/write/environment.json.

Units: rates in tau^-1, energies in epsilon, beta in epsilon^-1, k_B=1.
The output dimensionless c_m represents c_m*tau/epsilon^m. A counting-field Taylor
series to degree four computes four derivatives exactly, with no finite-difference
or temperature-bias truncation error. The time limit is taken at fixed three states.

Inputs: evidence/witness-frozen.json and evidence/witness-check.json. Implementations:
code/thermal_search.py (calculate function only), code/check_witness.py (characteristic
function only), code/reproduce_manuscript.py (read-only replay). The original discovery
and checker entry points write research files; use the wrapper above for clean replay.
The original search is preserved locally but not rerun by this wrapper.

Build the paper from a clean output directory, with REVTeX 4.2, pdfLaTeX and BibTeX:

```sh
mkdir -p build/local
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/local main.tex
cd ../build/local
BIBINPUTS=../../manuscript: bibtex main
cd ../../manuscript
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/local main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build/local main.tex
```

For BibTeX run from build/local, set BIBINPUTS to the absolute manuscript directory
if references.bib cannot be located by the local TeX configuration. System REVTeX,
AMS and hyperref packages are dependencies, not bundled copies. main.tex and
references.bib are the complete authored typesetting inputs; there are no figures
or custom styles. All exact coefficient and integer data appear in the article.

Third-party full papers, primary website captures, referee reports and private job
logs are excluded from the proposed public submission package. The paper is a local
draft pending author review, fresh release audits and the human decisions
described in AUTHOR_HANDOFF.md. No public data deposit is asserted.
