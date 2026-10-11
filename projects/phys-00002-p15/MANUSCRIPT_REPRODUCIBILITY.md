# Manuscript reproducibility

This package supports the exact finite-dimensional, discrete-time result in
`manuscript/main.tex`. It does not extend the claim to a closing spectral gap,
other hazard exponents, infinite dimension, altered reset rules, dissipation,
or experiment. Floating calculations are diagnostics; the convergence proof
is analytic.

## Environment used

- macOS arm64; Python 3.12.14
- NumPy 2.5.3, SciPy 1.18.1, Matplotlib 3.11.2
- TeX Live 2026, pdfTeX 1.40.29, REVTeX 4.2f, latexmk 4.88
- Poppler `pdfinfo`, `pdftotext`, and `pdftoppm`

The validated task-local interpreter is
`python`. No random samples are used.
No system software or package installation is required.

## Regenerate the authored figure and data

From the project root, using project-local caches:

```sh
mkdir -p build/cache build/mpl-cache
XDG_CACHE_HOME="$PWD/build/cache" MPLCONFIGDIR="$PWD/build/mpl-cache" \
  python -B manuscript/make_figure.py
```

The script rewrites only `manuscript/figure_data.csv` and
`manuscript/figures/coherence-decay.pdf`. It evaluates the exact coefficient
recurrence printed in the paper, checks every plotted fixed-phase coefficient
against the proved endpoint-mass bound, and constructs the parity panel from
the exact central-binomial formula. The write-side run recorded 1569 rows,
maximum `abs(F)/bound = 0.658052741078`, and exact zero for every displayed odd
parity coefficient. The recurrence agreed with an independent 80-digit direct
age-law convolution within `7.75e-15`; see
`write-evidence/figure-generation.log` in the local
dossier (the dossier log is not a submission file).

## Replay central diagnostics

Run the following in a scratch copy if the accepted evidence snapshot must
remain hash-stable, because the programs write their named JSON/log outputs:

```sh
python -B code/check_fixed_gap.py --output fixed-gap-replay.json
python -B code/check_trace_bound.py --output trace-bound-replay.json
```

The first program compares the closed critical age law with forward recursion,
checks summation by parts and the fixed-gap bound, tests exact phase-pi parity,
and probes the fixed-gap asymptotic. The second constructs complete finite-age
density matrices for source, degenerate, small-fixed-gap, and trivial finite
registers and compares them with the spectral formula and trace bound. Every
age from zero through the requested time is retained; neither test proves the
infinite-time theorem numerically.

## Clean manuscript build

Copy the contents of `manuscript/` to a new empty directory and run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The bounded write job built from a newly created directory under
`/private/tmp` and copied the resulting PDF to `build/main.pdf`. Its actual
compiler transcript is `build/latexmk.log`. A future source change requires a
new clean build and fresh manuscript/release review.

## Redistribution scope

The explicit submission list contains authored TeX, BibTeX, figure, figure
data/code, this README, and selected authored diagnostic code/results. It does
not contain downloaded third-party PDFs, extracted source text, browser or job
logs, private review material, credentials, or external data. Bibliographic
records cite third-party works by DOI/arXiv identifier rather than
redistributing their content.
