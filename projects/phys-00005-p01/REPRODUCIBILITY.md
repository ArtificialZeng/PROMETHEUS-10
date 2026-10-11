# Reproducibility instructions

The decisive result uses exact rational arithmetic; floating-point output is
an independent cross-check, not the sign certificate. Commands below are run
from the project root with the supplied Python environment. No network access
or external data are required.

Tested environment: Python 3.12.14, SymPy 1.14.0, NumPy 2.5.3 and Matplotlib
3.11.2 on macOS. Package versions are recorded in `requirements.txt`.

## Recompute the two witness representations

Create a new empty directory such as `build/replay` and run:

```sh
python code/counterexample_spectral_a.py \
  --output build/replay/method-a.json \
  --log build/replay/method-a.log

python code/counterexample_commutant_b.py \
  --output build/replay/method-b.json \
  --log build/replay/method-b.log

python code/compare_counterexample.py \
  --method-a build/replay/method-a.json \
  --method-b build/replay/method-b.json \
  --output build/replay/comparison.json \
  --log build/replay/comparison.log
```

The exact run must report 62 edges,
`tau=1673/1192`, `path_tau=23/16` and `delta=-81/2384`. The comparison must
report `exact_counterexample_verified` and numerical/exact agreement within
`1e-12`.

## Regenerate the figure

```sh
MPLCONFIGDIR=build/mplconfig \
python figures/generate_witness_figure.py \
  --input evidence/counterexample-method-b.json \
  --output figures/witness_graph.pdf
```

## Rebuild the manuscript

Use a new empty output directory and run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=build/clean manuscript/main.tex
```

The generated article is `build/clean/main.pdf`; the complete TeX build log
is `build/clean/main.log`. Third-party literature PDFs are evidence inputs
only and are deliberately excluded from the handoff/submission file list.
