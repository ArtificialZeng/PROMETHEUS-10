# Reproducing the finite-RNA local tradeoff

This is a restricted computer-assisted result for parent tuples
(c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1). It does not solve the
arbitrary-network question. Paths are relative to the source package root.
No command writes into the supplied scientific input files.

## Exact supplied-certificate replay

Use Python 3.11 or later:

    python3 reproducibility/replay.py

The wrapper copies the 13 required supplied files into a fresh directory
inside build/, runs the standard-library exact checker there, records
actual output and compares input hashes before and after. It replays both
128-dimensional blocks and all n32/n48 Riesz residuals, tails and rational
square-root bounds. The n32 bounds fail the selected 4/5 target; n48 passes.
Stored-certificate replay does not independently establish the analytic
premises or provide a fresh scientific referee.

## Optional full reconstruction

In an environment already containing the versions in requirements.txt:

    python3 reproducibility/regenerate.py

This generates new parent probability/Palm intervals, n64 resolvent Gram
enclosures and integer congruences, then n32/n48 Riesz approximants and exact
replays. It can take substantially longer than supplied-data replay.
Floating proposals may differ across platforms; exact inequalities, rather
than identical floating vectors or hashes, determine success. The wrapper
calls only necessary parent generation, bypassing historical n16 branches.
All generated outputs go to a fresh directory under build/.

The full reconstruction wrapper was not executed in the write role.
Its underlying generators and exact data were used in the accepted
scientific packet. The writer actually replayed the supplied certificates
in an isolated local tree; the local dossier retains the real log.

## Table and PDF

    python3 reproducibility/make_table.py
    python3 reproducibility/build_draft.py --outdir build/author-clean

The table rounds exact rational upper bounds upward to 12 decimal places.
The PDF command requires existing pdflatex and BibTeX, uses an empty local
directory and records actual commands, main.log and main.fls. Standard TeX
packages are system dependencies; no custom style or image asset is needed.

## Scientific input map

The manuscript defines the positive stationary cluster PGF, exact marginal
recurrence, extra-RNA response measures and mixed factorial-moment recurrence.
The n64 matrices, entry errors and congruence witnesses, and n48 residual
records are retained under evidence/research-pass3 and research-pass4.
They are author calculation outputs. The caps 48/128 construct resolvent
witnesses with enclosed infinite-state errors; they do not define a
finite-box stationary law. The whole-space W4 bound controls all omitted
response directions. The cubic remainder is an analytic estimate, not a fit.

Downloaded papers, retrieval caches, execution transcripts, mutable handoffs
and credentials are excluded from the submission source selection.
Primary identifiers are in references.bib; the local citation map locates
the preserved sources. Analytic premises, physical assumptions, novelty
and human author responsibility remain necessary beyond arithmetic replay.
