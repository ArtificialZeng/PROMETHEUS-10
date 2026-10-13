# Reproducing the exact checks

The manuscript's universal claim is proved analytically. The supplied programs are
deterministic exact-arithmetic consistency checks and do not replace that proof.

Use Python 3.12.14 and install the pinned packages in `requirements.txt`. From the
project root run:

```sh
python3 code/test_support_congruence.py
python3 code/reproduce_input_a.py
python3 code/reproduce_input_b.py
python3 code/compare_reconstructions.py
```

The first command checks the support-congruence identity, exact parameter endpoints,
phase covariance, trace preservation, qutrit Choi ranks 2--8, and all six ordered
energy-level pairs. The other three reconstruct the published Example 3 baseline
through independent Choi and superoperator encodings and compare them only in the
third program. No random seed, floating-point tolerance, parameter grid, or external
dataset is used.

Build the manuscript from `manuscript/` with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

The local source package includes no downloaded third-party article or private runtime
log. Citation metadata and scientific claims require final author review before use.
