# Reproduce the local result-note

The manuscript's universal result is analytic. Its finite checks use exact
Hermitian 2-by-2 matrices, algebraic numbers and symbolic coefficients. They do
not rely on an optimizer, numerical rank threshold, statistical error bar or
perturbative truncation. Every mathematical and physical hypothesis is stated
in manuscript/main.tex, Sections 2–3.

The original exact checker is evidence/n4k2_exact_checks.py. It reconstructs the
complete target coefficient slack space and checks every empty, singleton and
pair active-label set on two extremal reference measurements: the tetrahedron
and an unequal-weight target. There are eleven sets per model. Every replacement
is checked for positivity, completeness, matched diagonal exclusions, unchanged
active preparations and an exactly unchanged symbolic score. The general claim
follows from the manuscript proof, not the finite checks.

The checker also preserves historical tangent-curve and target-only-spoof
diagnostics. Those diagnostics are outside the article's central argument.
Its historical phrases about proposer status belong to the unchanged original
checker; rerunning it is not a new scientific or release acceptance.

Use an existing Python environment with the dependencies in requirements.txt.
The actual local run used Python 3.12.14 and SymPy 1.14.0. No software was
installed for this draft. The tested command from the project root is:

```sh
python3 reproducibility/run_exact_checks.py
```

On another machine, use its existing compatible interpreter:

```sh
python3 reproducibility/run_exact_checks.py --output-dir reproducibility/runs/new-check
```

The wrapper runs the unchanged checker in a new directory and captures stdout,
the generated exact summary and a run record there. It refuses an existing
nonempty directory, so it does not replace scientific evidence. The actual
local replay completed with exit code zero; its log and record are under
reproducibility/runs/exact/. Repeating a check uses a fresh output path.

Build the article with an already installed TeX distribution, latexmk, BibTeX,
and standard packages (article, geometry, Latin Modern, AMS mathematics,
mathtools, microtype, natbib, hyperref and enumitem). No custom styles or figures
are needed. From the project/bundle root run:

```sh
python3 reproducibility/build_manuscript.py --output-dir build/new-draft
```

The build script requires a new directory and records the actual command,
compiler output and return code. It runs LaTeX/BibTeX until references settle.
The complete authored TeX dependencies are manuscript/main.tex and
manuscript/references.bib; generated .bbl/.aux files are build outputs.

The actual draft is build/final/main.pdf, with compiler-output.log, main.log,
main.blg and build-record.json in the same directory. Formal citation, clean-build
and every-page visual release audits require a separate release job. This packet
does not claim those audits, human approval, external peer review or submission.

The handoff selection contains original TeX/Bib, code, instructions, the local
run output and AUTHOR_HANDOFF.md. It excludes full third-party papers, source
renderings, raw web caches, workflow job logs and private material. Reference
papers are identified by DOI/versioned URL in the bibliography and author handoff.
System libraries and TeX packages are dependencies, not redistributed copies.
