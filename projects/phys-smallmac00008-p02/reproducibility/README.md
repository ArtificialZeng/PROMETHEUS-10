# Reproducibility guide

The central statement is exact; numerical tests are checks, not its proof.
Run commands from the project root. The authoritative environment used here
resolved `python3` to
`python3` and reported Python
3.12.14, NumPy 2.3.5, SciPy 1.18.1 and SymPy 1.14.0. A new user should record
their own environment and should not interpret altered floating-point output as
altering the exact theorem.

## Exact structural replay

```sh
python3 evidence/o4_rank_one_lemma_replay.py
```

This independently checks, with symbolic arithmetic, the quaternionic
`Sym_0(R^4)` basis, involution and trace-pairing identities used in the proof.
The frozen reference output is `evidence/o4-rank-one-replay.log`.

## Published rank-three control

```sh
python3 evidence/reproduce-a.py
python3 evidence/reproduce-b.py
python3 evidence/compare_inputs.py
```

The first implementation builds corrected Kraus channels and evaluates the
normalized Choi--Bell fidelity. The second uses independent exact
trace--determinant arithmetic. The comparison script applies the explicit
row/column convention map only after the two inputs were prepared. Expected
values at `lambda=3/4` are `F1=3/4` and `F2_M=F2_B=5/8` in the original
three-dimensional environment domain.

## Corroborating full-rank scans

```sh
python3 evidence/takagi_o4_scan.py
python3 evidence/o4_frame_lemma_scan.py
```

These fixed-seed finite-precision programs test the Takagi convention,
determinant maximum, commutator gap and orthogonal-frame construction on
generic inputs. Their output is not an enclosure or a proof of universal
quantifiers.

## Clean manuscript build

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=build manuscript/main.tex
```

The handoff bundle intentionally excludes downloaded third-party papers and
private/audit/job logs. It contains authored TeX/Bib sources, this guide, and
the scripts/data needed to inspect the central identities and published
control.
