# Reproduce the common-bias counterexample

From the root of the accompanying source package, run:

```sh
python3 supplement/reproduce.py --output replay-output
```

This sequential command uses only the Python standard library. It recomputes
65,536 continuous cells using 128-bit fixed-point outward intervals and 32,769
nodes using 48-digit directed Decimal arithmetic. It checks the global affine
witness, its continuum coverage, all scalar bounds, and the strict positivity
conditions for the algebraically defined center ensemble. Do not use `python -O`.
No optimization, search, network access, precomputed node table, or third-party
numerical library is used by these two checkers. The shipped `certificate.json`
is read only to compare outputs after the full computations; it is not a source
of function values or a substitute for recomputation. New outputs are written
under `replay-output/`, preserving the shipped reference data.

The exact scientific statement, endpoint arguments, interval coverage, and
elementary-function remainder bounds are in the manuscript. Passing program
assertions alone does not replace reviewing those arguments. The decimal
implementation relies on correctly rounded Decimal logarithms, while the
integer implementation uses explicit rational logarithm series. Both assume
correct Python integer arithmetic. No formal proof-assistant verification is
claimed. The checkers are different implementations of the same fixed witness;
their agreement does not constitute external peer review.

The tested environment is Python 3.9.6, Decimal 1.70, and libmpdec 2.5.0 on macOS.
There are no mandatory pip requirements. Memory usage was not instrumented.
The algorithms run on one CPU process, with linear work in the mesh size;
the integer checker uses constant auxiliary storage. Execution times in
`replay-output/results.json` are measurements on the machine that runs it,
not portable performance guarantees.

The optional figure uses NumPy 2.0.2 and Matplotlib 3.9.4 in the checked
environment:

```sh
python3 supplement/plot_gap.py --output replay-output/bias-gap.pdf
```

The plotted geometry uses ordinary floating point solely for visualization.
Its two entropy marks use the verified bounds from `certificate.json`, and
are not plotted estimates of optimized entropy. The supplied PDF is sufficient
to compile the article without installing these plotting dependencies.

To build the manuscript using an existing TeX installation:

```sh
python3 manuscript/build.py --output build/local
```

The builder stages the complete TeX, bibliography, and figure in a new empty
directory. It runs pdfLaTeX, BibTeX, then pdfLaTeX twice, with shell escape
disabled, and retains each tool transcript. Use a new output directory for
every clean build. Required TeX packages are REVTeX 4.2, AMS math packages,
graphicx, booktabs, xcolor, hyperref, and the standard T1 fonts. No custom
style file is needed. The local build has not been submitted to any journal.

The files are newly authored manuscript and reproducibility material, with
substantive AI assistance disclosed in the manuscript. They contain no full
third-party article, browser capture, private research conversation, or account
information. Publication, licensing, author identity and affiliation, and
human scientific approval remain the author's decisions.
