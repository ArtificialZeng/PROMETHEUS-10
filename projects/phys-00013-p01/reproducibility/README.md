# Reproducing the three-qubit pure-state spectrum

The analytic proof is self-contained in manuscript/main.tex. The central all-degree result is exact; finite checks do not establish its infinite quantifiers. This package uses no experimental dataset, floating-point eigensolver or downloaded third-party paper. All quantities are dimensionless. Exactly three complex qubits and independent adjacent normalized Haar-SU4 gates are assumed.

Tested environment: Python 3.12.14, SymPy 1.14.0, Matplotlib 3.11.2 on macOS arm64. The research interpreter in the present installation is `python3`. On another computer, use an existing Python with the packages listed in requirements.txt. No package installation was performed for this draft. The finite kernels use Python integers/Fractions and SymPy exact rationals; Matplotlib converts rationals to floats for visual display only.

From the root of an extracted source package, the read-only table/algebra check is:

```sh
python reproducibility/check_support.py
```

This reads saved independent-construction A/B inputs for k=7 and k=8, verifies ranks and cross Gram equality, diagonalizes the small rational overlap matrices, removes the whole identity direction, checks the two displayed conditional expectations, and verifies the general radial integral. It is an algebra check using stored data, not a source reconstruction or a new referee. It does not overwrite those input files.

The figure is rendered from exact Fractions and the accepted degree-eight output:

```sh
python manuscript/make_figure.py
```

It writes manuscript/figures/spectrum.pdf and spectrum.csv. Run in an extracted or scratch package if the original manuscript snapshot must remain fixed. The plotted r=1..12 values come from the proved formula; the degree-eight comparison uses stored exact calculations. The dashed 1/2 line is a known group-level witness, not an all-representation upper bound. The figure is AI-assisted code rendering of exact mathematical data.

For full regeneration of the two different finite constructions, create a fresh scratch directory with `evidence/research/`, and copy these programs into that subdirectory: symmetric_a.py, symmetric_b.py, compare_sym7.py, compare_holdout.py, check_analytic.py and probability_check.py. Then run the following from the scratch directory:

```sh
python evidence/research/symmetric_a.py --degree 7
python evidence/research/symmetric_b.py --degree 7
python evidence/research/compare_sym7.py
python evidence/research/symmetric_a.py --degree 8
python evidence/research/symmetric_b.py --degree 8
python evidence/research/compare_holdout.py
python evidence/research/check_analytic.py
python evidence/research/probability_check.py
```

These original programs write generated scientific records under their current working directory's evidence/research. **Never run them against the frozen live evidence directory.** Timestamps will differ; compare the defining inputs, ranks, exact Casimir entries, trace moments, cross Gram matrices and rational spectra. A uses differential bosonic generators in mode order 4a+2b+c. B uses symmetric tensor-slot swaps in mode order 4c+2b+a. The comparison explicitly reverses the endpoint bits. Both keep the factorial physical monomial metric and complete global-identity subtraction. The original finite calculations measured less than 131 MB RSS; this is a historical measurement, not a universal runtime guarantee.

Rebuild the manuscript from its directory using existing TeX tools:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build/rebuilt main.tex
```

REVTeX 4.2 and its APS bibliography style are standard system dependencies. The full TeX, bibliography, generated bibliography and figure are supplied. The bibliography uses primary-source metadata and cites established probability laws, joint marginal results and the known low-moment numbers. Original all-PU8 mixing, other gate ensembles, other site/local dimensions, and deterministic-initial-state total-variation bounds are outside the result.
