# Reproducing the algebraic checks

The manuscript's proof is self-contained. The companion script
'scripts/resonance_classification.py' checks the factor identities with
SymPy and performs high-precision illustrative back-substitution with
mpmath. It does not replace the analytic monotonicity proof.

Tested environment:

- Python 3.12.14
- SymPy 1.14.0
- mpmath 1.3.0
- NumPy 2.3.5
- SciPy 1.18.1

From the project root, run:

    python3 scripts/resonance_classification.py

The expected final line is:

    EXACT_TWO_SHEET_IDENTITIES_AND_BACKSUBSTITUTION_PASS

The captured reference output is
'evidence/resonance-classification.log'. On the research machine,
'python3' was resolved before computation to the interpreter recorded in
'evidence/research-pass2-python-environment.txt'. A different platform may
use any compatible Python environment containing the versions above.

To build the article, run:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build manuscript/main.tex

The bibliography file is 'manuscript/references.bib'.
