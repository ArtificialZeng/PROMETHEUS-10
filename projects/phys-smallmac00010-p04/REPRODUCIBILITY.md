# Reproducing the seven-T rank-220 result

This packet concerns one ideal four-data-qubit, seven-|0>-ancilla, seven-T fixed circuit. It does not resolve the universal seven-T informational-completeness question. Run the commands below from the project root in a **copy** of the packet so the accepted frozen evidence files in this local research project are not overwritten.

The core inputs are `evidence/seven-t-witness.json` (seven Pauli rotations, eleven readout generators, and the Clifford readout sequence), `evidence/certify_220_exact.py` (standard-library exact binary-symplectic enumeration), and `evidence/replay_explicit_seven_t.py` (independent matrix representation over a finite field). Their reference outputs are `evidence/seven-t-rank-220-exact.json` and `evidence/seven-t-replay-best.json`.

Reference environment: Python 3.12.14, NumPy 2.3.5 on macOS. The branch certificate uses only Python's standard library. The explicit-state replay uses NumPy. No external service, Monte Carlo sample, or floating-point threshold is involved in the rank proof.

From the root of a scratch copy:

```sh
python3 evidence/certify_220_exact.py
python3 evidence/replay_explicit_seven_t.py --input evidence/seven-t-witness.json --output replay-check.json
```

The first command must report ancillary-X rank 7, 2048 group rows, 1788 zero rows, 260 nonzero rows, and 220 distinct four-qubit Pauli labels; the output file records all 36 absent labels. The second must report 333 total gates, exactly seven T/T-dagger gates, 2048 outcomes, isometry and POVM-sum identities, and rank 220 over \(\mathbb F_{1009}\). Its output also contains a nonzero 220-by-220 minor. The exact branch argument in the paper supplies the characteristic-zero upper bound; the modular minor alone supplies only the lower bound.

The local independent scientific audit additionally contains `audit/referee_replay.py`, `audit/referee_state.py`, and `audit/replay.log`, written separately from the discovery programs. Those audit records are not part of the proposed external source supplement, but remain available to the author for review. All cited third-party papers remain in the local literature cache and are excluded from this handoff package.
