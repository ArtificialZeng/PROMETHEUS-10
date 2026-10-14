# Reproduce the three-state envelope checks

The proof is evidence/research/spectral-envelope-proof.md. Manuscript: manuscript/main.tex. This package contains project-authored sources, not third-party full papers or private workflow logs. Claims remain restricted to positive finite rates, N=3, finite A>=log64 and large thresholds.

## Environment

Checks were produced with Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0, already present in the local environment. Standard-library determinant and renewal modules have no external dependencies. requirements.txt records dependencies; this job installed no software. Scientific evidence remains hash-bound and must not be overwritten when replaying.

## Safe replay in a separate project-shaped copy

From the package/project root, use an empty scratch directory of your choice:

```sh
mkdir -p /tmp/fpt-envelope-replay/evidence/research
mkdir -p /tmp/fpt-envelope-replay/evidence/reproduction
cp source.md /tmp/fpt-envelope-replay/
cp evidence/research/spectral-envelope-check.py /tmp/fpt-envelope-replay/evidence/research/
cp evidence/reproduction/determinant_a.py /tmp/fpt-envelope-replay/evidence/reproduction/
cp evidence/reproduction/renewal_b.py /tmp/fpt-envelope-replay/evidence/reproduction/
cd /tmp/fpt-envelope-replay
python3 evidence/research/spectral-envelope-check.py > replay.log 2>&1
```

Use an interpreter with the recorded libraries (locally, python3). The script imports the two independent passage modules, checks symbolic identities and rational samples, evaluates optimizing rates at 90/170 digits, checks the preserved source hash, and writes evidence/research/spectral-envelope-values.json in the scratch copy. Expected output includes PASS messages ending with the immutable source check. No installed optimizer or scientific literature download is needed. Decimal residuals are corroborative, not certified interval errors.

## Clean manuscript build

From the package root, with a TeX installation providing latexmk, pdfLaTeX and BibTeX:

```sh
mkdir -p /tmp/fpt-manuscript-clean
cp manuscript/main.tex manuscript/references.bib /tmp/fpt-manuscript-clean/
cd /tmp/fpt-manuscript-clean
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

No external figures or custom styles are needed. System TeX packages are listed by the source; build dependencies are main.tex and references.bib. DOI/arXiv references identify the consulted scientific literature. A fresh citation/build/every-page visual release audit and human scientific review are still required before local release activation and any separately authorized submission.
