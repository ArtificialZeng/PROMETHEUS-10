# Reproduce the exact four-spin result

Reference environment: Python 3.12.14 and SymPy 1.14.0. The exact checks need only SymPy; NumPy is needed only for the separate discovery scan, which is excluded here. Use a Python environment already providing SymPy, or arrange dependencies separately. No installation is performed by this package.

From the package root:

    python supplement/pauli_check.py

This portable derivative of the separately written referee Pauli construction imports no proposer code or saved matrices. It prints the exact complex local identity, complete parity polynomials, rational root counts, LDL pivots, star checks and neighborhood arithmetic. Its execution is a reproducibility check, not another independent scientific review. The analytic operator-norm proof is in the manuscript and counterexample-proof.md.

For the two original representations, stage a separate scratch tree to keep the retained witness files unchanged:

    mkdir -p scratch/code scratch/evidence/research
    cp code/input_a.py code/input_b.py code/certify_k4.py scratch/code/
    cd scratch
    python code/certify_k4.py

This creates regenerated rational matrices and exact-certificate.json in scratch/evidence/research. Compare them with the supplied witness-matrix-a.json, witness-matrix-b.json and exact-certificate.json. No downloaded full papers, private job logs, acceptance records, mutable handoffs or credentials are required by these portable scientific computations.

Build the article from manuscript/ with a TeX distribution providing the standard packages listed in main.tex:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

The bibliography's source versions and DOI identify public primary papers. Full source papers are excluded from the submission bundle. No figures or numerical interpolation are needed for this exact result.
