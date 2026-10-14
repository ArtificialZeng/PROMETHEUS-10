# Reproducing the two exact results and the local draft

The manuscript proves the exact n=4 tangent spectrum and local one-cycle residual obstruction. The original almost-sure convergence question remains unresolved. No ensemble statistics or finite-tail numerical claims enter this article.

Python 3.12 was used with SymPy 1.14.0, NumPy 2.5.3 and Matplotlib 3.11.2. `requirements.txt` records observed versions; no installation was performed for this draft. Standard TeX Live, pdfLaTeX, BibTeX and Poppler supply the build and rendering tools. The exact result needs only SymPy for its optional symbolic replay. The analytical proof does not depend on Python or a numerical eigenvalue calculation.

Run the following commands from the package/project root with a Python interpreter containing those libraries:

```sh
python manuscript/reproduce_exact.py --output build/my-exact-replay
python manuscript/plot_spectrum.py
python manuscript/build.py --output build/my-clean-build
pdftotext build/my-clean-build/main.pdf build/my-clean-build/main.txt
pdftoppm -r 110 -png build/my-clean-build/main.pdf build/my-clean-build/page
```

Each replay or build output directory must be new. The exact replay wrapper loads `evidence/research/exact_family.py` and redirects its output to the isolated directory. Do not run that frozen generator directly in its evidence directory: its main function writes outputs there. Running the wrapper preserves the original scientific data. Its reuse of the original generator is a reproducibility replay, not independent referee verification.

The exact generator constructs all 24 real skew and 40 imaginary symmetric column-tangent coordinates from the displayed Q(theta). It applies the derivative formula to the rows and columns, identifies every connected block, and factors characteristic polynomials over Q(t). A successful result reports `exact_difference: "0"`, real block sizes `[2,8,8,2,2,2]`, and imaginary blocks consisting of sixteen scalar blocks, four 2x2 blocks and two 8x8 blocks. Block order may differ; the multiset and product are decisive. The output `exact-family-spectrum.json` supplies every generator label, block entry and characteristic polynomial. The rational parameter misses theta=pi modulo 2pi; the manuscript's direct cos/sin argument covers that endpoint and all degeneracies.

`evidence/research/local-spectrum-proof.md` is the stable underlying derivation. `evidence/research/exact-family-spectrum.json` and `exact-family.log` preserve the original exact run. The local source map gives precise primary-source versions and scope. The two propositions are exact finite-dimensional identities and local analytic existence statements; sampled figure curves are binary64 display data with no certification role.

The plot script writes `manuscript/spectrum-data.json` and `manuscript/figures/spectrum.pdf`. This figure is a deterministic analytical plot, with no synthesized imagery or eigenvalue fitting. Regenerating a figure or changing source text changes publication bytes and requires a fresh manuscript freeze and affected release checks. It does not replace scientific review.

The clean build executes pdfLaTeX, BibTeX and two further pdfLaTeX passes in the foreground. It records real stdout, compiler logs, command status, recorder inputs and input/output hashes in the fresh build directory. It does not write science audits, invent final release acceptance, or publish a deliverable.

Only the explicit submission-file list is suitable for handoff. Full third-party papers, source-retrieval captures, job logs and internal audits are excluded from that list. Human scientific review, author details, declarations, venue choice and any future submission remain pending.
