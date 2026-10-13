# Reproduce the spin-1 projection calculation

The article is an exact finite-dimensional result. The universal argument is in
manuscript/main.tex, Sections III--V. The scripts check its algebra and explicit
examples; finitely many checks do not prove the universal inequality.

Run from the directory containing manuscript/ and reproducibility/:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 reproducibility/verify_exact.py --output-dir replay-output
    python3 reproducibility/verify_scope.py --output-dir replay-output
    python3 reproducibility/build.py

verify_exact.py reconstructs spin moments through two-qubit Pauli compression,
checks the generic complex traceless Hermitian inverse and metric factor, verifies
the normal-cone identities, and checks the published pure-state baseline and the
two mixed states in the article. It also checks a complex SU(2) rotation.
There are 46 checks, including six explicitly nonphysical diagnostic checks.
The nonphysical target is a control for the logical role of target positivity;
it is not a physical counterexample or a new state.

verify_scope.py has 13 exact diagnostics for the affine kernel restriction and
the difference between general separability and full symmetric support. It
includes another explicitly nonphysical Hermitian control. The two programs are
portable adaptations of the symbolic code used in the separate scientific check.
The mathematical check bodies were retained; only documentation, provenance
metadata, and output handling were adapted. Running these copies is not a new
independent scientific audit.

The outputs are replay-output/exact-results.json and
replay-output/scope-results.json. Reference outputs accompany this directory.
The eigenvalue sorting in the exact program uses floating evaluation only for
display. The eigenvalues themselves, all norm identities, and all checks use
exact SymPy rational or algebraic expressions. The article establishes the
minimum eigenvalue of its nonzero-dipole example analytically from its 2x2 block.
No sampled coherent-state dictionary, numerical SDP tolerance, perturbation
series, or infinite-dimensional truncation enters the proof.

The tested environment is recorded in environment.json. Only SymPy is required
for the scientific replay; no dependency is bundled or installed by these files.
The largest matrices are 4x4. Peak memory was not measured. No performance or
speedup claim is made.

build.py requires Python 3, pdfLaTeX, BibTeX, REVTeX 4.2, and the ordinary TeX
packages used in the article. It copies the TeX and Bib into a fresh directory
under build/, runs pdfLaTeX, BibTeX, and two further pdfLaTeX passes without
shell escape, and retains every command log. The resulting PDF is
build/main.pdf; the final compiler and bibliography logs are build/main.log
and build/main.blg. Each invocation uses a new clean directory. System TeX
packages are not included in the source bundle.

The three bibliography entries point to public primary records. The corrected
2016 paper is reproduced in Appendix A.1 of the cited 2017 university
dissertation. Downloaded third-party PDFs, browser captures, private execution
records, and independent-review reports are outside the handoff file list.
See SOURCE_MAP.md for formula locations. No external data or public
repository deposit is claimed.
