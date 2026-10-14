# Reproducing the subdivided two-star gap

This package reproduces the exact algebra supporting the manuscript's restricted full-gap result: integer k>=100, real theta in [1/2,2], eta=theta/k, s=sqrt(1-eta). The Hamiltonian uses negative unnormalized unit-edge projectors, identity spectators and J=1. H has full-spectrum multiplicities. No all-graph/all-s or bounded-degree thermodynamic conclusion is asserted.

The required scientific library is SymPy1.14.0. No network, primary-PDF cache, research transcript or operational file is read by the portable certificate. In the writer environment the existing research Python at python3 was used; an equivalent Python environment with the supplied requirements is sufficient. TeX compilation requires installed pdflatex, bibtex, pdfinfo and pdftotext; rendering additionally uses pdftoppm. No package installation is part of these commands.

From the project root, with Python pointing to that environment:

```sh
python3 reproducibility/endpoint_certificate.py --output build/replay/certificate.json
python3 reproducibility/make_endpoint_table.py --input build/replay/certificate.json --output build/replay/anchors.tex
python3 reproducibility/replay_endpoint.py
python3 reproducibility/build_endpoint_manuscript.py
```

The first command regenerates the matrices, characteristic polynomials, exact rational derivative/residual norms, complete anchor-root intervals, full low-sector margins and source-convention controls. The second rounds the gap-ratio intervals outward using integer arithmetic. The third copies only the two portable programs into an initially empty project-local directory, reruns them, and requires byte equality with the reference certificate and manuscript table. This is a portability test using the same implementation and CAS; it is not an independent referee or an independent software-stack check. The final command compiles from only the five listed TeX/Bib inputs in a fresh directory and retains compiler, BibTeX, dependency and extraction logs.

Reference data: reproducibility/endpoint-certificate.json. Its records contain the 7x7 and 11x11 reflection-even quotients, all orbit states, monic characteristic polynomials and normalized polynomials. The latter use e=1/k and lambda=2/e+4+e(h-N theta), with lowest Laurent exponents -5 and -8. Coefficient norms apply to the entire box e in [0,1/100], theta in [1/2,2], |h|<=1; exact errors in lambda are bounded by81/k^4 and101/k^4. The complete root-isolation anchors are k=100, theta=1/2 and2, with rational interval widths at most10^-24.

The tiny physical controls retain complete number spaces at k=3, s=3/5, dimensions36 and84, and check exact matrix intertwiners. Site bits in the direct physical matrices are indexed least-significant first: hubs0/1, middle2, then the two private groups. The diagonal amplitude similarity is s^(hub occupation sum); it changes coordinates only. A separate direct full four-qubit star and local Pauli comparison reproduce the known s=1/2 baseline. Corrected auxiliary C characteristic polynomials reproduce the N1/N2 spectra in the paper.

The full-Hilbert-space universal result additionally requires the analytic star-spin envelope, the overlapping-star tail inequality and the full internal N2 Weyl bound. They are proved in the manuscript and are not replaced by the finite control cases. The program does not enumerate the 2^(2k+3) physical states for large k or treat a sector Ritz difference as the physical gap.

All public supplement inputs are authored manuscript/code/data. Third-party full papers, web responses, private and operational logs are excluded. Bibliographic links identify the primary sources. The local draft requires human scientific review and a fresh release review; running these commands does not constitute journal acceptance or authorize submission.
