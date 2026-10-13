# Reproducing the exact algebra

The paper's model and all matrix conventions are defined in main.tex. The supplied code/check_full_kernel_structure.py starts from evidence/input-a.json, an exact rational Pauli-string reconstruction of the 37 measured operators and their 26-dimensional Hermitian null space. It checks the full-kernel block identities, constructs the endpoint and four remaining charts, verifies their maximal minors and all 188 cubic coefficients, and writes the certificate evidence/check-full-kernel-structure-v1.json. The companion code/check_antipodal_rotation.py checks one complex common-rotation convention against independently built Pauli sums. That example is a regression test; the general antipodal argument is analytic in the paper.

From a **separate extracted copy** of the handoff bundle, with Python 3 and SymPy 1.14 or later already installed:

    python3 code/check_full_kernel_structure.py
    python3 code/check_antipodal_rotation.py

The scripts write in the copy's evidence/ directory and may replace the supplied certificate with a freshly timestamped one. Do not run them in the frozen research directory. Expected exact checks: measured-space dimension 38, kernel dimension 26, endpoint intersection dimension 14, chart dimensions 6/6/6/4, nonzero real-domain minor r^4(r^2+1)^2 for r nonzero, and 188 identically zero polarized cubic coefficients. There is no numerical precision or stochastic seed. The actual prior runs and an independently implemented Born-effect replay are retained in the private scientific dossier; the latter is not part of this redistribution bundle because it writes into audit records.

To build the article, use an existing TeX Live installation with REVTeX 4.2 and BibTeX:

    cd manuscript
    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build main.tex

The result is build/main.pdf. No external data or downloaded article is needed to build or replay the algebra. The cited articles are identified by DOI/arXiv in references.bib and are deliberately not copied into this bundle.
