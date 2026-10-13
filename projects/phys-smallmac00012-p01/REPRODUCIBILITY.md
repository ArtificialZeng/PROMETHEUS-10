# Reproducibility guide

The central result is an analytic exact proof. The programs below audit its
algebraic identities and exact examples; no finite scan is used to infer the
universal claim.

## Environment used

- macOS, Python 3.9.6
- SymPy 1.14.0
- TeX Live 2026 / RevTeX 4.2
- `latexmk`, `bibtex`, `pdfinfo`, and `pdftotext`

Install the only Python package needed by the central exact scripts with:

```sh
python3 -m pip install -r reproducibility/requirements.txt
```

## Source reproduction and exact proof checks

Run these commands from the project root:

```sh
python3 -B code/compare_inputs.py
python3 -B code/reproduce_baseline.py
python3 -B code/exterior_triangle_orthostochastic.py
python3 -B code/exact_qutrit_monoid_proof.py
```

Reference outputs are, respectively:

- `evidence/input-comparison.log`
- `evidence/baseline.log`
- `evidence/exterior-triangle-orthostochastic.log`
- `evidence/qutrit-unistochastic-monoid-proof.log`

The two central proof scripts use exact SymPy expressions. They verify the
exterior Lagrange/Gram certificate, CKM affine chord, four-coordinate Heron
identity, negative-semidefinite concavity form, exact endpoint realizers, a
fully interior example, a unitary completion, and a collapsed singular
chart. Any floating-point searches elsewhere in the project are diagnostic
history and are not required to reproduce the proof.

## Manuscript build

From the project root, build in the dedicated output directory:

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=../build main.tex
```

The expected manuscript is `build/main.pdf`. The retained final compiler and
BibTeX transcripts are `build/main.log` and `build/main.blg` in the local draft
dossier.

## Redistribution boundary

The handoff list contains authored manuscript files, this guide, the pinned
requirement, project-generated exact code, and project-generated outputs. It
does not contain the local primary-source excerpts or any third-party full
paper. The author must choose a license before publicly redistributing code or
data and must recheck journal supplementary-material requirements.
