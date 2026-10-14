# Reproducing the restricted result and manuscript

Run all commands from the package/project root. Python 3.12.14 was used for
the scientific computations; package versions are in `requirements.txt`.
The code uses NumPy, SciPy and SymPy for the supporting checks, and
Matplotlib for the figure. The recorded versions were already installed;
no software was installed for this manuscript job.

The analytical result is self-contained in `manuscript/main.tex` and
`evidence/research/periodic-variation-proof.md`. It concerns each fixed
bounded periodic profile and finite period, at a profile-dependent small
strength. The original arbitrary-unitary optimization remains unresolved.

The saved 170-case numerical data are
`evidence/research/general-variation-check.json`. The numerical generator is
`general_variation_check.py`, with `sinusoidal.py` supplying the independently
derived Fourier multiplier. The data include a sine, a mixed profile,
square wave, high harmonic and constant control. The tested parameters and
Gaussian-domain splitting are specified explicitly in the code. These are
ordinary floating-point consistency checks with analytical Gaussian tails,
not outward-rounded error enclosures. The proof of the continuum statement
does not use numerical minima.

To replay without changing the original frozen outputs, use a new empty
directory under `build/`:

```sh
python3 reproducibility/run_consistency_checks.py --output build/replay-example
```

Use a Python interpreter with the recorded scientific packages. In the
research workspace, the existing interpreter is
`python3`. The wrapper copies the two
unchanged scripts into the chosen destination, verifies their source
hashes, and retains the actual data and log there. It is a replay of the
submitted implementation, not an independent referee check.

The figure is generated only from the saved accepted data. Its generator
checks the input hash and preserves all source files:

```sh
python3 reproducibility/make_figure.py
```

It writes `manuscript/figures/sensitivity-ripple.pdf`, a preview under
`build/`, and `evidence/write/figure-provenance.json`. Its polylines join
the 17 sampled phases and do not certify an unsampled minimum.

A clean manuscript build requires an installed TeX distribution with
REVTeX 4.2 and the standard AMS, graphics and hyperref packages, plus
BibTeX and Poppler's `pdfinfo`/`pdftotext`:

```sh
python3 reproducibility/build_manuscript.py --build-dir build/clean-example
```

The destination must be empty. The script runs pdfLaTeX, BibTeX and two
further pdfLaTeX passes; records all command outputs and final compiler
log; and extracts PDF metadata and text. TeX's auxiliary files and generated
`.bbl` are build outputs from the bound TeX/Bib sources and system style,
not additional authored inputs. Inspect the final compiler log rather
than treating unresolved citations on the initial bootstrap pass as final.

For human or external checking, independently reconstruct the Gaussian
score, verify the nonzero-frequency multiplier sign, and check every term
of the rank/remainder estimate. Code agreement alone cannot replace these
checks. A local AI referee performed such a reconstruction in the research
dossier; it is not external peer review or completed human validation.

Only the explicitly enumerated authored manuscript/reproduction files are
selected for handoff. Third-party full papers, private logs and the
literature cache are excluded. The source references remain accessible by
their DOI/arXiv links in the manuscript and source map. The author must
confirm authorship, any license for the authored code/data, AI disclosure,
and scientific responsibility before any external use.
