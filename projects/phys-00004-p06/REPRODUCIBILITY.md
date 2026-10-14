# Reproducing the Cauchy certificates

The manuscript's units are one Cauchy scale and one jump step. Absorption is
landing strictly above a finite barrier; resetting is before the fresh jump.
All decisive signs use exact integer outward intervals, not display floats.
No random seed or third-party numerical library is needed.

Do not run scripts in the accepted evidence directory: several scripts write
their result JSON there. Instead, from the project root:

```sh
python3 reproduce_bundle.py
```

This copies the listed certificate scripts and their stable JSON inputs into
`replay-work/evidence`, runs them sequentially, and stores real stdout/stderr
and regenerated JSON there. Existing replay-work is refused so old logs are
not overwritten. The accepted scientific files are never modified. Some
finite-kernel checks take several minutes; no execution-time promise is made.

The scalar check verifies the interval engine. `finite_survival.py` verifies
the exploratory finite orders and exact infinite-order induction.
`barrier_cover.py` regenerates the complete ten-cell cover.
`antecedent_exclusion.py` checks the 191 derivative cells, 42 middle-barrier
cells and analytic large-barrier bound. `interval_survival.py` also recomputes
the compact Simpson initial sign. Two alternative-coordinate/scalar scripts
replay survival and exclusion with different grids and arithmetic choices.
The assertion exits and exact rational inequalities, not elapsed times or
rounded decimals, are decisive. The analytical argument is in the manuscript
and stable evidence/pass2-resolution.md; it must also be checked by a reader.

Environment: Python 3.14 was used for the project; scripts use only Python's
standard library. See requirements.txt. Manuscript build: a TeX Live installation
providing latexmk, pdfLaTeX, BibTeX, amsmath, amsthm, geometry, booktabs,
lmodern and hyperref. From manuscript/, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

The included rational result files are the accepted calculation outputs.
Float display fields and timings may differ between machines; exact interval
sign checks must pass. Raw primary papers and private workflow/job logs are
excluded from the submission file list. Obtain cited papers through their DOI
or arXiv records rather than redistributing the local literature cache.
