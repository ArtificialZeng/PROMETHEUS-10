# Environment and dependencies

The scientific programs require Python 3.9 or newer and only its standard library:
fractions, decimal, integer arithmetic, math, pathlib, json, importlib and ordinary
file handling. The scratch runner additionally uses argparse, contextlib, runpy,
platform, shutil and sys. No NumPy, SciPy, symbolic-algebra package, external
data service or installed optional solver is used by the certificates.

The exact tested Python version and operating-system description are preserved
in reproducibility/environment.json. The scratch runner records a fresh environment
with each execution; its actual local results and comparison are in
build/write-bb985-replay/. Floating-point elapsed times
are diagnostic only; all central certificate quantities use exact rational,
integer interval or directed Decimal arithmetic.

The manuscript uses the article class and ordinary TeX-distribution packages
geometry, fontenc, lmodern, amsmath, amssymb, booktabs and hyperref, plus the
standard unsrt BibTeX style. There are no custom styles, imported TeX fragments,
figures or generated scientific plots. pdflatex and bibtex build the paper;
pdfinfo, pdftotext and pdftoppm inspect its output. The build's exact tool versions
and commands are recorded in build/write-bb985-final/build.log; the complete
intermediate-pass transcript is retained as transcript.log in the same directory.
