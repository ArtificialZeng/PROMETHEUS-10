# Reproduce the third-block candidate

Use the already installed research Python from the project root. No installation, inference process, external account, or background worker is needed. The new enclosure kernel needs mpmath; the retained parent source reconstruction uses NumPy, SciPy, SymPy, and mpmath. Actual environment versions are in `evidence/research/r3-environment.json`.

Preserve the current completed evidence. The following commands identify the actual performed calculations; running them again regenerates their output files, so use an isolated copy for referee replay after freezing.

    python3 -B -u evidence/research/r3-interval-enclosure.py --seconds 1000 --target-width 0.012 --output evidence/research/r3-interval-enclosure.json
    python3 -B -u evidence/research/r3-independent-check.py
    python3 -B -u evidence/research/r3-independent-check.py --certificate evidence/research/r3-interval-enclosure.json --partition-only --output evidence/research/r3-partition-check.json
    python3 -B -u evidence/research/r3-interval-refine.py --seconds 300 --target-width 0.0048
    python3 -B -u evidence/research/r3-independent-check.py --certificate evidence/research/r3-interval-refine.json --partition-only --output evidence/research/r3-refined-partition-check.json

Each executed command's stdout/stderr is retained in its corresponding `evidence/research/r3-*.log`. Both enclosure runs actually completed normally, before their computation ceilings. The first uses no old quadrature/scattering outputs. The second legitimately refines the first completed exported range certificate as an explicit stable input. The independent point reconstruction reads no cached scattering results or interval polynomial coefficients. The exact-fraction partition checker consumes only the declared completed certificate and checks all panels and exported sums.

Proof and scope: `evidence/research/r3-counterexample.md`. Exact model: `evidence/research/r1-tightbinding-model.md` and `evidence/research/r1-proposed-witness.json`. Finite determinant/range derivation: `evidence/research/r2-enclosure-derivation.md`; arithmetic audit: `evidence/research/r3-arithmetic-audit.md`; physical inputs: `evidence/research/r3-physical-admissibility.md`. The old r1/r2 incomplete calculations and failed checks remain historical evidence, not certified starting integrals. The first new independent precision failure is retained and diagnosed in `evidence/research/r3-independent-precision-diagnostic.json`.

The candidate is proposer verification only. Fresh referee reconstruction of primary data, exact physical identities, range arithmetic, full energy coverage, and novelty is the next step. No scientific acceptance or local publication exists. Mutable checkpoint/state and workflow trees are excluded from scientific snapshot inputs and from the mathematical derivation.
