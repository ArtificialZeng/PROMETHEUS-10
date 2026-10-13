# Reproducing the exact rank-gap certificate

The central computation is exact and uses Python 3.12.14 with SymPy 1.14.0.
NumPy and SciPy are not used by the certificate scripts, but the controlled
project environment records NumPy 2.3.5 and SciPy 1.18.1.

From the project root, with the dependencies in `manuscript/requirements.txt`,
regenerate the certificate into a new path (do not overwrite the frozen evidence):

```sh
python3 scripts/certify_clifford_rank_gap.py --output /tmp/clifford-rank-gap-certificate.json
python3 scripts/replay_clifford_rank_gap.py /tmp/clifford-rank-gap-certificate.json
```

For byte-for-byte comparison with the manuscript's evidence, replay the retained
certificate directly:

```sh
python3 scripts/replay_clifford_rank_gap.py evidence/clifford-rank-gap-certificate.json
```

Expected scientific output is target rank 78, low-stratum upper bounds
`57,57,74,57,74,74,74,74,57,57,57`, high-stratum lower bounds
`84,83,83,84`, coverage of all 15 strata, and `independent_replay PASS`.
All determinant and nullspace checks use exact SymPy arithmetic.

The source-order convention is documented in the manuscript and `problem.md`.
The scripts order the 120 Clifford rows lexicographically by Majorana pairs and
the 128 columns by ascending even occupation mask.
