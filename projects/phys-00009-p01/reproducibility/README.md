# Reproducibility and manuscript build

This package concerns exactly two particles on each finite Boolean cube
with homogeneous parameter a>0 and equal edge conductance c>0. The exact
gap formula, crossover, recurrence and threshold limit are proved in the
manuscript and in evidence/hypercube-result.md. The original all-graph,
all-alpha, all-particle-number conjecture remains unresolved.

Use Python 3.12 with the versions in reproducibility/requirements.txt.
The author's environment actually used Python 3.12.14; exact package
versions are reproducibility/environment.json. No package installation
is performed by the provided scripts. Compilation needs an existing
LaTeX distribution, latexmk, pdflatex and bibtex. PDF inspection used
existing Poppler pdfinfo, pdftotext and pdftoppm.

Run from the top-level package directory. Always use a disposable exported
copy when replaying scripts: the historical checkers write into evidence/
and must not overwrite a hash-bound accepted dossier. The supplied saved
outputs are evidence from the recorded executions, not a promise of
byte-identical output across platforms or library versions.

## Exact central checks

```sh
python3 -u evidence/research_hypercube_check.py
```

This imports evidence/reconstruct_a.py and assembles a second matrix
separately by a reversible incidence construction. It checks full occupation
inputs, character/radial intertwiners, exact root intervals at D=3 and D=4,
and determinant/Green/integral/recurrence threshold identities through D=16.
It writes research-hypercube-checks.json and
research-hypercube-symbolic-checks.json under evidence/. The saved actual
output is evidence/research-hypercube-check.log. The finite list supports,
and does not replace, the analytic proof for every finite D and a,c>0.

## Published baselines and source conventions

The occupation jump formula, reversible form, mass and sign/basis convention
map are in evidence/reconstruction-map.md. To replay the published finite
path and complete-graph baselines in a disposable copy:

```sh
python3 evidence/reconstruct_a.py
python3 evidence/reconstruct_b.py
python3 evidence/compare_inputs.py
python3 evidence/reproduce_baseline.py
```

The independently obtained inputs read only
evidence/reproduction-cases.json. Their saved inputs, comparison and baseline
outputs are included. Units are dimensionless a and occupations, with c in
inverse time; c multiplies every displayed gap. The ordered generator has
no factor 1/2, while the ordered Dirichlet form has one.

## Figure

```sh
python3 reproducibility/make_figure.py
```

This writes manuscript/figures/crossover.pdf and a preview PNG, plus
reproducibility/illustration-data.json and environment.json. The left panel
uses the symmetric reversible distance-chain matrix at 80 decimal working
precision and checks three sentinel values at 120 digits. A separately
assembled SciPy tridiagonal calculation is a numerical comparison. The
right panel is the exact rational threshold recurrence. Data fields record
observed residuals and discrepancies. The numerical curve is an illustration;
these checks are not rigorous interval enclosures or independent scientific
acceptance. The all-D proof and exact 1/35 crossing do not rely on the plot.

## Clean LaTeX build

```sh
python3 reproducibility/build_manuscript.py --output build/author-rebuild
```

The output directory must be empty; existing files are preserved. The helper
runs latexmk, including BibTeX and all required LaTeX reruns. It retains a
command transcript, the final compiler log, the resolved .bbl and the
dependency recorder .fls. Initial-pass unresolved references in a transcript
are expected before BibTeX/reruns; the final main.log and extracted PDF must
be checked separately. Compilation reads manuscript/main.tex,
manuscript/references.bib and manuscript/figures/crossover.pdf plus installed
system TeX packages. No local custom style or additional TeX input is used.

The fresh release build is build/release-clean/main.pdf, recorded in
publication.json; earlier writer builds remain in the local dossier.
The release reviewer checked the final TeX/BibTeX logs, complete authored
dependencies, four primary citations and all seven rendered pages.
Final audit reports and workflow records are in the local audit/ directory
and intentionally excluded from the submission archive. The supervisor
must pass the release gate before local activation and bundle creation.
Author scientific, authorship and policy approval remain pending.

## Redistribution scope

The explicit submission list contains only authored TeX/Bib/figure sources,
authored reproducibility scripts/data/proof material and this handoff. It
excludes third-party article PDFs/full text, raw web returns, supervisor or
job logs, mutable handoffs and audit reports. Primary sources are cited by
identifier/DOI/URL; full papers must be obtained from their original hosts.
Rights clearance here is a scope check, not a choice of public software
license or authorization to submit externally. The human author must choose
any final distribution license and repository.
