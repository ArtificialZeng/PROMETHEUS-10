# Online Resource 1: exact symbolic reproduction

Article: An exact anti-degradability threshold for the three-level bosonic
loss–dephasing channel. Proposed journal: Quantum Information Processing.
Draft author: Xiaojian Zeng, PBC School of Finance, Tsinghua University, 100190;
xiaojianzeng@foxmail.com. Author details and submission decisions require confirmation.

The accepted scientific claim is the exact threshold at Gaussian phase variance
ln 2 for arbitrary inputs in the invariant first-three-Fock-state restriction.
The analytic proof is in the manuscript. These checks validate its symbolic
transcription and rational sign calculations. No numerical SDP optimizer is
needed, and no positive-capacity conclusion is drawn above the threshold.

## Environment and complete reproduction

Recorded versions: Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5, SciPy 1.18.1.
Only Python and SymPy are needed by the included decisive scripts. The exact
dependency is recorded in requirements.txt; NumPy and SciPy were used in the
earlier optional numerical discovery, which is not required here.

In the original project the required interpreter is
python3. Check command -v python3
against PHYSICS_PYTHON before running. A portable copy can use another existing
Python environment with the stated SymPy version; no installation is performed
by the reproduction script.

Run from the package's parent directory:

```sh
python3 supplementary/reproduce.py --output build/reproduction-run
```

The output directory must not already exist. The command copies the supplied
scripts and exact reference data into that new directory, runs every check
sequentially in the same interpreter, and saves environment.json, replay.log,
generated evidence and comparison.json there. It never overwrites the supplied
reference data. Successful comparison includes exact reconstruction of both
input forms, the qubit baseline, support reduction, root and sign certificates,
endpoint marginal/dual identities and the nine loss-composition units.

Script order and roles:

1. input_a_number_states.py: direct source number-state reconstruction.
2. input_b_kraus.py: independently expressed pure-loss and Gaussian Gram Kraus input.
3. compare_inputs.py: all Choi entries, normalization, basis map and legal limits.
4. qubit_baseline.py: published two-level Choi and threshold 2/3.
5. reduce_extension.py: full population support and antisymmetric marginal transfer.
6. exact_certificate.py: exact Sturm root counts and outward rational sign bounds.
7. endpoint_symbolic_replay.py: direct 27-dimensional endpoint and dual identities.
8. composition_check.py: exact post-loss rule and Kraus completeness.

The endpoint replay leaves the displayed radical residual formal; the separate
root/sign certificate and the manuscript's branch argument establish its zero.
The full-space lift and all-parameter coverage are analytic Schur-complement
and completely positive pullback arguments, not finite numerical sampling.

The supplied research scripts are preserved byte for byte. Historical comments
about a referee being pending refer to their original creation; they do not
assert the status of the present draft. The implementations share SymPy, and
their exact checks do not replace the author's scientific review.

## Rebuild the manuscript

With an existing TeX installation containing the standard packages used in main.tex:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error -outdir=../build/portable manuscript/main.tex
```

This resolves references.bib relative to manuscript/ and generates the complete
PDF and logs in build/portable/. No external source download is required.
Third-party full-text sources are cited and linked in the manuscript and local
source map; they are excluded from the public supplement.
