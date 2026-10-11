# Exact reproducibility

The scientific claim in `main.tex` is an exact finite-dimensional identity.
No parameter grid, floating-point eigenvalue, optimizer tolerance, or
perturbative truncation is used in its proof.

Tested environment:

- Python 3.12.14
- SymPy 1.14.0
- pdfTeX 1.40.29 (TeX Live 2026)
- latexmk 4.88

From this directory, regenerate the exact machine-readable record with:

```sh
python3 reproduce.py --output reproduction-output.json
```

The script reconstructs the normalized Choi families in `(B,A)` order,
checks exact trace preservation and output marginals, derives the local
magic-basis radii, certifies strict interval signs with exact Sturm root
counts, derives all six local `LDL^T` pivots, verifies the
`B1,A1,B2,A2 -> B1,B2,A1,A2` permutation and tensor-remainder identity, and
checks the exact rank-15 specialization at `s=1/10,t=1/8`.

Build the article in a clean directory containing `main.tex` and
`references.bib` with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected SHA-256 values are recorded in `publication.json` after the clean
write-stage build. The named human author must still inspect the mathematics,
citations, code, declarations, and every rendered page before submission.
