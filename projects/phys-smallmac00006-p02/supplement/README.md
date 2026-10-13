# Exact reproduction

The manuscript proves that subsystem size does not order coherent information in the specified uniformly phase-noisy graph-state model. `replay.py` checks the explicit nine-qubit witness using only the Python standard library. Run from the bundle root, on a Unix-like system with Python 3.9 or later:

```sh
python3 supplement/replay.py > replay-result.json
```

The program writes JSON to standard output and does not modify other files. Do not use `python -O`, which would disable the exact assertions. No network access, installation, random seed, external solver or parallel process is needed. `resource` is a Unix standard-library module; the recorded environment is macOS. `environment.json` records the actual tested Python, precision, time and memory use.

The program encodes the graph as ten explicit edges on qubits numbered 0 through 8, forms all phase-error weights, applies the graph-state computational-basis signs and takes exact partial traces. It then checks every Walsh-character eigenvector equation. All comparisons use integers or `Fraction`; logarithms are bounded by a 96-term positive Mercator series with a rigorous rational tail. Decimal endpoints are rounded outward. No cached spectrum is read.

`expected.json` contains the scientific outputs of the accepted independent calculation: two source benchmarks, the nine-qubit graph at five probabilities, and seven finite-rank consistency checks. A replay can be compared without the machine-dependent timing and metadata fields:

```sh
python3 - <<'PY'
import json
from pathlib import Path
actual = json.loads(Path('replay-result.json').read_text())
expected = json.loads(Path('supplement/expected.json').read_text())
assert {key: actual[key] for key in expected} == expected
print('Exact spectra and outward entropy bounds match.')
PY
```

The finite-rank checks do not prove an infinite quantifier. The manuscript's proposition proves every finite integer rank at the common noise parameter by explicit kernels, binary-entropy monotonicity and a positive coherent-information slope. No exhaustive search, minimality or threshold uniqueness is claimed.

The numerical routines are the implementation produced during the independent scientific calculation, repackaged without its internal identifiers or output-file writes. The packaging replay is not an additional independent review. Source benchmarks are the rank-one formula in Eqs. (25)–(27) and the graph in Eq. (28) of Sajjad et al., *Quantum* **10**, 2111 (2026), [DOI](https://doi.org/10.22331/q-2026-05-21-2111). The exact script retains separately transcribed edge inputs.

To rebuild the manuscript with an existing TeX installation and Poppler:

```sh
python3 manuscript/build.py
```

This clears only its named generated outputs in `build/`, runs pdfLaTeX, BibTeX and two further pdfLaTeX passes serially, then saves the PDF, compiler transcript and text extraction. The authored TeX, bibliography and diagram stay unchanged. Rebuilding changes output hashes and requires a new manuscript freeze and final audit in the local workflow; do not overwrite an active audited build merely to test a download.

The bundle contains authored text, diagram code and exact calculations. It does not contain third-party papers, browser captures, account material or internal job logs. No open-source license or external repository is asserted; license choice and public distribution remain for the named author's approval.
