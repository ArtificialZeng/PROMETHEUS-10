# Reproducing the exact spectral-locus result

Run all commands from the project root. The scientific interpreter used for the
accepted calculations was:

`python3`

Its recorded versions are Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1, SymPy
1.14.0, and Matplotlib 3.11.2. The declarative package list is in
`reproducibility/requirements.txt`; no installation step is performed by this
project.

## Exact calculations

1. `python3 scripts/reproduce_baseline.py all`
   independently constructs the Hamiltonian in two ways and reproduces the
   published all-equal spectrum.
2. `python3 scripts/research_characteristic.py`
   computes the exact general characteristic polynomial and factors the sole
   signed-sum obstruction.
3. `python3 scripts/verify_spectral_locus.py`
   checks the chiral Pauli symmetry, the universal real-spectrum factorization,
   every irreducible branch, representative intersections, and exact off-locus
   witnesses.
4. `python3 audit/referee_replay.py` is an independently implemented replay based
   on Pauli-group traces and Newton identities. It belongs to the audit dossier,
   not the submission bundle.

The decisive operations in steps 1--3 use SymPy exact integer and symbolic
arithmetic. Floating-point eigenspectra are diagnostics and are not used as the
classification certificate.

## Figure

Set a writable Matplotlib cache directory, then regenerate the authored PDF:

`MPLCONFIGDIR=/private/tmp/phys-00019-p01-mpl python3 scripts/plot_locus_slices.py --output manuscript/figures/locus-slices.pdf`

The figure is a direct visualization of the accepted exact factorization; it
contains no fitted or external data.

## Manuscript build

From `manuscript/`, run:

`latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build main.tex`

The expected manuscript output is `build/main.pdf`. The bibliography uses BibTeX
through `latexmk`. A release reviewer must repeat the clean build and citation and
page-by-page visual checks before local activation.
