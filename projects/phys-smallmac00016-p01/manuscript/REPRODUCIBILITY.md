# Reproducing the calculations and manuscript

Run all commands from the extracted project root. The accepted calculations were run
with Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5, and SciPy 1.18.1. Install the Python
packages from `manuscript/requirements.txt` in an isolated environment.

## Scientific checks

1. Reconstruct the ordered GAD instrument and the 16 hidden history paths directly:

   `python3 scripts/reconstruct_a_exact.py`

2. Reconstruct the same channel independently with Liouville matrices and general
   clock-dependent recovery maps:

   `python3 scripts/reconstruct_b_liouville.py`

3. Compare the two representations:

   `python3 scripts/compare_reconstructions.py`

4. Check the exact constants in the sharp centre certificate:

   `python3 scripts/verify_global_bound_constants.py`

   The output must include `exact_F2M=289/400`,
   `history_witness_advantage=99/10000`, and `exact_constant_checks=PASS`.

5. Reconstruct and check the full rational robustness rectangle:

   `python3 merged/phys-00016-p02/scripts/verify_robust_rectangle.py`

   The output must include `gap_min_upper_corner=2013407/2000000000`,
   `epsilon_residual=13407/2000000000`, and `certificate_status=pass`.

The two theorem proofs are analytic. Floating-point residuals in the independent
Liouville reconstruction check conventions and implementations; they are not the
logical certificate.

## Manuscript build

With a TeX Live installation providing `latexmk`, run:

`cd manuscript`

`latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build/final main.tex`

The verified clean local build used pdfTeX 1.40.29 and produced an eight-page PDF. The
submission source consists only of the authored LaTeX and BibTeX files; standard TeX
packages are external dependencies.
