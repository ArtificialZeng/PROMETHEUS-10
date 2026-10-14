# Reproducing the local unicyclic-clock result

This package supports the manuscript's exact local result for each fixed n>=5 at q=b/a=1. It supplies no proof or disproof of the arbitrary-heterogeneity cycle inequality. The main argument is self-contained in manuscript/main.tex. The saved defining proof is evidence/research-local-proof.md.

Use Python 3.12 with the versions in requirements.txt. The recorded environment was Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0 and mpmath 1.3.0. TeX compilation additionally needs REVTeX 4.2, AMS math, microtype, hyperref, BibTeX and latexmk. No installation is performed by the scripts.

From the unpacked project root, select a new output directory:

```sh
python3 reproducibility/run_checks.py --suite all --output replay-local
```

The command copies only the selected calculation scripts into that directory before running them, records input hashes, actual commands, software versions, return codes and logs, and writes generated evidence there. It refuses an existing output directory. Do not run the original fixed-output scripts directly in an accepted evidence tree: their historical output paths overwrite their own results.

The suites can also be run separately with --suite baseline, --suite algebra, or --suite independent and a different new output directory for each. Exact symbolic reductions take longer than direct numerical checks. They evaluate rational identities with the logarithm retained as a formal real symbol; the all-n transcendental signs are proved by the explicit integral inequality in the manuscript, not by numerical sampling.

- baseline reconstructs n=7,u=8,d=1 using an integer/rational forward generator and a separate cycle-tree/Fourier construction, then compares the full spectrum, entropy conventions and OBS Eqs. (8)-(10).
- algebra derives the generic constrained blocks from exponential flow/probability coordinates, checks the displayed sign factorizations, and independently differentiates the full n=6 generator over an exact algebraic field, including phase-coupled and Nyquist directions.
- independent derives the generic and Nyquist blocks from linear stationary coordinates without reading the proposer matrices or eigenvalues, and separately checks the full direct generator response at n=5,6,7,8,11,12 and a nonlinear fixed-coherence mixed-mode path. Only the exported result-file locations differ from the independently audited implementations; calculations are preserved.

The exact outputs included in the handoff are evidence/research-symbolic-curvature.json, evidence/research-curvature-sign-identities.json and evidence/research-exact-local-replay.json. Input/baseline outputs are evidence/input-a.json, evidence/input-b.json, evidence/input-comparison.json and evidence/baseline.log. Metadata timestamps can change during replay; compare defining mathematics and residuals rather than timestamped byte hashes. Historical workflow identifiers in calculation records do not confer acceptance on a rerun.

The scripts' finite spectral and finite-difference checks are float64 diagnostics, not interval certificates. Their role is to catch implementation and convention errors. No random scan, optimizer, or negative search is needed to regenerate the paper's proof, and no such scan is bundled as a proof premise.

For the PDF, start from manuscript and run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build-replay main.tex
```

Use a new build-replay directory. The complete authored PDF dependencies are main.tex and references.bib; REVTeX's generated mainNotes.bib and main.bbl are compiler products. No downloaded paper or external figure is imported. The local dossier retains primary papers for private checking; the proposed submission bundle contains citations, original text, original code and original outputs, not third-party full texts or internal review/job logs.
