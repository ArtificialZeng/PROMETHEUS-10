# Reproducing the noisy two-qubit result

The universal claim is analytical. The manuscript follows the stable accepted
argument in evidence/noisy-unitary-proof.md. Finite checks are diagnostics and
special-case certificates, not universal quantifier proofs.

Python uses only the standard library; no pip dependencies are required.
Original environment: Python 3.14.7, macOS 26.5 arm64.
TeX: pdfTeX 1.40.29 / TeX Live 2026 and latexmk 4.88.

Run from the root of an extracted copy of the submission source package:

~~~sh
python3 evidence/input-a.py
python3 evidence/input-b.py
python3 evidence/replay.py
python3 evidence/research-check.py
~~~

The first two independently transcribed scripts produce input-a.json and
input-b.json with 12 Choi matrices each. replay.py compares 3072 rational
entries after factor permutation, checks marginals and positivity, and writes
input-comparison.log and baseline.log. It checks nine gate/noise objectives
and two KRS published state limits. Its manifest dependency is
input-manifest.json's source_sha256 field.
The final script prints 32 exact complex-rational primal/dual/TP certificates
for eight gates, with 128 correlated sign invariances, and checks the original
source.md hash. Source and manifest are included; full third-party papers are not.

These programs write generated inputs/logs. Run in an extracted copy, not
in a frozen project, so accepted evidence remains untouched. Gaussian rational
arithmetic has no roundoff tolerance. Historical script phrases about awaiting
a referee describe their creation phase, not the current audit status.

## Build

Use an empty build directory. From manuscript/:

~~~sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
~~~

Standard TeX inputs: article, fontenc, inputenc, lmodern, geometry, amsmath,
amssymb, amsthm, booktabs, hyperref and unsrt bibliography style.
No custom style, plot, image or external executable is imported by TeX.
The authored inputs are main.tex and references.bib; BibTeX generates the bbl.

## Exact result and limits

For X=RA A,Y=RB B and normalized Omega, compute rho_U from the pure unitary
Choi vector, L=Tr sqrt(rho_U), and kappa=L^2. Both objectives are
(1-p)kappa+p/4; channel entropy is minus the base-two logarithm minus one.
Do not use the noisy reduction for rho_U. The dual support-complement term
is necessary at deficient Schmidt rank.
Scope: one use, all U(4), p in [0,1], maximally mixed replacer, qubit ports
and trivial-Hamiltonian interpretation.

## Primary source map

1. Badhani/Das, arXiv:2604.01217v2, VI.1 Proposition 10, Figure 2 and
   following open extension; Appendix D Lemma 9.
2. Das/Goswami/Pandey, arXiv:2410.01740v2, Corollary 4 Eq.87:
   Gamma=4Omega, M=4Q gives objective 2t and the channel offset.
3. König/Renner/Schaffner, DOI 10.1109/TIT.2009.2025545, Definition 1 and
   pure-state formula: state entropy definition and baseline.

Sources are linked in the BibTeX database. Cached full PDFs stay in the local
dossier and are excluded from submission files.
