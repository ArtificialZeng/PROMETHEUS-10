# Reproduce the three-copy qubit certificate

This package contains exact generated mathematical data and code for the accompanying manuscript. It contains no experimental measurements or downloaded third-party papers. Execute it in a local copy, with Python, SymPy and NumPy already available; no script installs software or accesses the network.

From the package root:

```sh
python3 supplement/run.py --output replay-output
```

The chosen output directory must not exist. The runner copies the seven calculation scripts into that new directory and runs one foreground process at a time, with BLAS/OpenMP thread counts set to one. It never reruns a generator in the frozen evidence directory. Results and actual command logs appear below `replay-output/`. To retain a previous run, choose another output name.

The reproduced sequence is:

1. `reproduction/input_a.py`: reconstruct the n=2,3 Haar operators from permutation projectors and independent local noise, using delta and input-first ordering.
2. `reproduction/input_b.py`: reconstruct them from Bloch moments, using t=1-delta and output-first ordering.
3. `reproduction/check_physics_inputs.py`: check the channel and admissible input identities.
4. `research/exhaustive_certificate.py`: construct all isotropic Pauli spaces and signed eigenstates; verify every ray polynomial and the operator interpolation.
5. `research/independent_replay.py`: independently generate the Clifford orbit, compare exact signed supports and polynomial coefficients, and check the rank-five projector and arbitrary-s attainer.
6. `supplement/phase_replay.py`: reconstruct the Haar operators from amplitude/phase integration and separately from local-noise permutation projectors; check the operator identity, success normalization, and the published two-copy F=3/4 baseline.
7. `supplement/affine_replay.py`: generate all stabilizer vectors from affine supports and quadratic phases, then compare their projectors and polynomials with the preceding corpus.

The last two scripts export the separate scientific review implementations. Only their output paths and descriptive metadata were changed for portability. Mathematical code was preserved. Their transformation record is `supplement/code-provenance.json` in the local dossier; a replay does not itself constitute new independent review.

Expected exact invariants: isotropic-space counts `[1,255,5355,11475,2295]`; 36720 distinct four-qubit rays; 36 coefficient pairs; 180 identically zero polynomials; all alpha <= 0 and alpha+beta <= 0; maximum commuting star subset 3; rank(P)=5; all 256 witness entries have zero residual; arbitrary-s success s and numerator s(1+t)/2. The separate source reconstruction compares 2560 entries across the two conventions. The affine replay checks all 587520 signed Pauli eigenvector relations. Run-specific timings and log hashes are expected to vary.

The data supplied at `evidence/input-a.json`, `evidence/input-b.json`, `evidence/stabilizer4-rays.jsonl`, `evidence/stabilizer4-certificate.json`, and `evidence/analytic-operator-certificate.json` are the accepted reference outputs. Regeneration creates separate copies of these outputs. The JSONL corpus lists complete signed Pauli supports and the exact coefficient pair for each ray. The first input uses delta; the second uses t. Matrix entries are lists of rational polynomial coefficients in ascending powers. Consult the field names and script definitions before changing basis or variable.

The working environment was Python 3.9.6, SymPy 1.14.0, NumPy 2.0.2; `requirements.txt` records package versions, not a guarantee about untested versions. Arithmetic is exact rational/Gaussian integer. The largest dense matrix is 16 by 16; fixed-width integer intermediates have the documented bound 8192. There are no stochastic samples, convergence tolerances, numerical optimizers, or continuum extrapolations. Peak process memory was not measured.

The mathematical scope is exactly three independent locally depolarized inputs of the same Haar pure qubit, a completely stabilizer-cone-preserving CP/TNI successful branch, and the success-weighted conditional objective. No more-copy, arbitrary-circuit, or general free-instrument-completion result is supplied.

To build the paper in a new local directory using installed TeX Live tools:

```sh
python3 manuscript/build.py --output build/rebuilt
```

The runner preserves the full compiler transcript, final TeX/BibTeX logs, and PDF. It uses the system REVTeX class and APS bibliography style, which are not redistributed. This is a local author-review package; no submission or publication is performed.
