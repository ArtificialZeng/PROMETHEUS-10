# Reproducing the replica-twist measurement result

The article proves an exact finite-mode result. Symbolic and numeric checks
are supplementary; floating point never establishes the strict inequality.
Use a Python environment with the versions in requirements.txt. Python 3.12.14
was used locally. The code is provided as text and requires no downloaded
third-party paper or private input. No installation is performed by these
commands.

From the top level of the handoff bundle:

    python reproducibility/run_checks.py
    python reproducibility/make_figure.py
    python reproducibility/build_manuscript.py --output-dir build/clean-new

The first command copies the two accepted evidence programs into a new
directory under build/replays, then performs complete exact local
Hermitian-Majorana string sums, a separate occupied-minor calculation, and
the full graded two-register replay. Original frozen programs and their
results are never overwritten. The exact checker gives
F_parent=77509155/134217728 and exp(Delta)=25836385/25165824.
The independent minor checker retains the accepted determinant algorithms
and assertions; only internal snapshot inspection was removed and output
paths changed for portability. This replay is not a fresh referee audit.

The second command regenerates the analytic plot and its 96 CSV rows.
Only the plotted logarithms use double precision. The midpoint parent
values and 34-mode certificate are cross-checked using Fraction arithmetic.
It writes the PDF/PNG/data/environment in manuscript/figures and places
Matplotlib's cache inside build. Regenerating a publication source after
freezing requires a new manuscript freeze and affected release reviews.

The third command needs an existing TeX installation with REVTeX 4.2,
latexmk, pdfLaTeX and BibTeX. It rejects a nonempty output directory so the
build is clean. It uses the canonical manuscript sources and writes
compiler-console.log, main.log, main.bbl, main.fls and main.pdf in the
selected directory. Use a new directory name for a further clean build.

The model is finite-dimensional, fixed-parity and uses cross-copy graded
CAR, the alpha/2 Majorana exponent, natural logarithms and pure recorded
outputs. Both measurement outcomes are included. The 34-mode witness is
not claimed minimal, and the growing-mode formula is not an
infinite-system or perturbative approximation.

Only authored TeX/Bib/figure/data/instructions and reproduction code are
selected for submission handoff. Primary third-party PDFs/text, browser
captures, internal job records, caches and audit logs stay local. There is
no automatic installation, external submission or author approval here.
