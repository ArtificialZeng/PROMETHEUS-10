# Reproducing the local response-stability result

Paper: *Local stability of a sharp q-deformed commutator response for
conditional quantum operations*. Draft author: Xiaojian Zeng, PBC School of
Finance, Tsinghua University, Beijing 100190, China;
xiaojianzeng@foxmail.com. Author confirmation is pending.
Proposed journal: Quantum Information Processing, Regular Article.

This is an exact finite-dimensional local result. The original global
all-matrix, all-real-q bound is unresolved by this work. The theorem
excludes q=-1,1, provides no explicit radius, and asserts no uniform
large-n or parameter limit. The physical observable is success-weighted;
normalized postselection introduces a separate success-probability factor.

## Environment

The actual checked environment was Python 3.12.14 with SymPy 1.14.0.
The verification programs require only SymPy and Python's standard
library. The package includes requirements.txt as an environment record;
no installation was performed by this job. A TeX Live installation with
pdflatex, latexmk, BibTeX and the standard packages used in main.tex
builds the manuscript. No nonstandard style or proprietary data is needed.

From the root of the handoff bundle, with that environment active:

    python reproducibility/run_checks.py --output build/reproduction

The wrapper runs each supplied certificate using the current Python,
saves its actual output, and compares it byte-for-byte with the supplied
scientific output. It does not read a checkpoint, state file, audit,
job metadata, cached Hessian, network source, or acceptance verdict.
Its optional output path must remain in the bundle root. A timeout or
failed comparison exits unsuccessfully.

The three checks are:

- evidence/research/n2_equality_symbolic.py: the complete q=1/2
  two-dimensional equality determinant identity in a canonical form.
- evidence/research/equality_geometry_certificate.py: the equality
  Schur pair, equality curvature and full real-coordinate Hessians at
  n=3,4 for q=1/2.
- evidence/research/general_q_local_certificate.py: the Schur pair
  and the two active-spectator blocks for symbolic signed b, using
  exact polynomial reduction by u^2-b^2-2ub+2=0.

The supplied matching logs have the same basenames shown by the wrapper.
These finite calculations support the explicit algebra. They do not
replace the manuscript's every-n support argument, sign hypotheses,
simple-branch proof or tubular Taylor remainder. A byte match verifies
reproduction of an output, not independent scientific correctness.

## Building the article

Run from the bundle root:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder -outdir=build/author manuscript/main.tex

The main source uses manuscript/references.bib and system unsrtnat.bst.
The paper has no external figure files: the complete susceptibility
spectrum is given analytically in its equation table. The PDF is
build/author/main.pdf. Preserve the build log and inspect the rendered
pages after any edits. The supplied source layout must remain intact.

## Provenance and rights

The supplied code, source and scientific output were generated for
this project. Full third-party papers, screenshots, literature caches,
raw search observations and private workflow logs are excluded from
submission_files. The four references identify the primary papers
needed to check the cited known results. Retrieve those sources from
their rights-holders; the local handoff is not a license to redistribute
them. Any public code license and archival destination must be chosen
by the human author before distribution.

The local author handoff is not an external submission. The journal's
current LLM policy requires substantive use to be disclosed and human
accountability; this draft accurately records pending human review.
