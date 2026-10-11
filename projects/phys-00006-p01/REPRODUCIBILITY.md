# Reproducibility instructions

Run all commands from the project root.  The manuscript build used Python
3.12.14, SymPy 1.14.0, Matplotlib 3.11.2, pdfTeX 1.40.29 (TeX Live 2026), and
Latexmk 4.88.  The existing project virtual environment is shown below; an
independent environment may instead install the two pinned packages in
`requirements.txt`.

## Exact scientific checks

```sh
python code/certify_alpha_plus.py
python code/certify_counterexample.py
python code/verify_counterexample_independent.py
```

Every decisive quantity is evaluated as an exact rational number or quadratic
radical.  The displayed decimal margin is diagnostic only.  The two
counterexample checkers do not import one another; the second begins from the
explicit rational states and the independently reconstructed block action.

## Figure and data table

Use a writable Matplotlib cache directory and regenerate both the vector PDF,
the preview PNG, and the CSV table:

```sh
MPLCONFIGDIR=/private/tmp/phys-00006-mpl \
XDG_CACHE_HOME=/private/tmp/phys-00006-cache \
  python code/make_witness_figure.py
```

Expected outputs are `figures/witness_comparison.pdf`,
`figures/witness_comparison.png`, and `figures/witness_values.csv`.

## Clean manuscript build

```sh
latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error \
  -outdir=build/write-clean manuscript/main.tex
```

The manuscript PDF is `build/write-clean/main.pdf`; the corresponding TeX log
is `build/write-clean/main.log`.  No downloaded literature PDF is required for
the build or included in the declared submission files.
