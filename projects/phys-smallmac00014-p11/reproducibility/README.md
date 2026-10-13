# Reproducing the checks and manuscript

The theorem in the manuscript is exact. The Python programs below are
diagnostic implementations and baseline reconstructions; finite-precision
output is not used as a proof.

## Scientific runtime

The checked environment was:

- Python 3.12.14
- NumPy 2.3.5
- SciPy 1.18.1

The authoritative interpreter for this project is:

`python3`

Before running a scientific check, verify that both `command -v python3` and
`python3 -c 'import sys; print(sys.executable)'` resolve to that path. Version
and binding evidence is retained in `evidence/write-runtime-probe.txt`.

## Commands

Run from the project root:

```sh
python3 code/reproduce.py
python3 code/takagi_commuting_frame.py
```

`code/reproduce.py` reconstructs the published special rank-three baseline,
the one-step polar-recovery baseline, full-rank controls, explicit Kraus
histories, and normalized Choi--Bell contractions. Its accepted reference
output is `evidence/baseline.log`.

`code/takagi_commuting_frame.py` implements the quaternionic neutral-plane
construction, the collinear-basis step, Takagi-optimal Kraus mixing, commuting
effect checks, transfer-power scores for `n=1,...,7`, and an explicit 64-history
check at `n=3`. It imports shared channel and score routines from
`code/search_three_use.py`. Its accepted reference output is
`evidence/takagi-commuting-frame.log`.

Successful runs end respectively with `STATUS PASS` and
`STATUS=PASS_FLOATING_POINT_REPLAY_EXACT_PROOF_IS_SEPARATE`. Small changes at
the last displayed digits can occur on another BLAS/LAPACK implementation;
the exact proof does not depend on any tolerance.

## Manuscript build

The local PDF was built with TeX Live 2026 and `latexmk` 4.88:

```sh
cd manuscript
latexmk -C -outdir=../build main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=../build main.tex
```

The output is `build/main.pdf`, and the compiler transcript is
`build/main.log`. The LaTeX source uses only standard TeX Live packages and
BibTeX.

