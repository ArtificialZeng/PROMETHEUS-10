# Exact replay and manuscript build

The article gives the full fixed-label six-qubit counterexample and its analytic proof.
The supplementary code cross-checks this finite certificate; it is not needed to assume
an unproved numerical rule. No experimental inputs, network access, random seed, or
third-party article files are required to run it. No software is installed by the scripts.

From the package root, using an existing Python 3.9+ environment with SymPy 1.14.0:

```sh
python3 supplement/reproduce.py
```

Outputs are written under the new directory `build/reproduction`. To repeat a run without
changing existing outputs, supply a fresh project-relative path:

```sh
python3 supplement/reproduce.py --output build/reproduction-second
```

The wrapper copies each checker and its explicit inputs, then runs three foreground
checks in sequence. It never executes a frozen evidence program in place and refuses
to reuse an output directory. An exit status of zero means that all assertions passed.

The implementations are:

1. `supplement/referee_replay.py`: the unchanged implementation from the currently
   accepted independent scientific check. It needs only the Python standard library.
   It independently encodes the complete edge sets and computes Clifford rotations
   using Gaussian integers with an explicit power-of-sqrt(2) denominator; direct
   partial traces use Fraction. It does not import discovery code or cached answers.
   It prints a JSON report to stdout; the wrapper saves it as `referee_replay.py.log`.
2. `evidence/research-pass1/check_witness.py`: edge-set operations, binary row spans,
   endpoint conditions, and the complete four-vertex LC orbit. Its explicit input
   files are `witness-input.json` and `old-figure-input.json`.
3. `evidence/research-pass1/replay_quantum.py`: an independent input transcription
   within the discovery phase, using explicit SymPy CZ-state amplitudes and local
   Clifford matrices, with `independent-circuit-input.json` as input.

The last two programs originated in one discovery context. The first was generated
in a different context from the same witness and primary conventions. This limited
independence does not imply external peer review; rerunning any program is a code
replay, not another scientific review. The original identifier in the unchanged first
program records its provenance, not the identity of a later run.

Expected exact certificate: chronological LC word (3,1,5), final global phase -1,
endpoint external-degree vectors (1,1,1), input cut ranks 3, output cut ranks 2 and 1,
and reduced spectra (1/4,1/4,1/4,1/4) and (1/2,1/2,0,0). Label `7` in the independent
checker denotes `c` only for the witness quotient; its ordered vertices are (4,5,6,7).
The same bipartition is compared in both outputs. Their fixed-label LC orbit check
has 11 members and exhausts the queue. Swapping external labels 5 and 6 restores LC
equivalence, so this is not an unlabeled counterexample. The condensed set is disconnected.

The first program also cross-checks every nonempty proper-subset marginal of the
six-qubit input pair and four-qubit output pair: 2(2^6-2)+2(2^4-2)=152 exact tests.
It verifies n=4 and n=7 star-to-complete controls, the rank-one condensation control,
the old Fig.15 endpoint-degree failures, and a deliberately wrong rotation-sign control.
The n=7 example is Fig.3 of Vandré et al.; n=4 is a special case of its general formula.
The Fig.15 graph inputs are attributed to that paper; its primary image is needed to
audit the transcription but is intentionally not bundled. See `manuscript-source-map.md`.

There are no tolerances, fits, perturbative terms, truncation tails, or numerical error
bars. The witness has 64 amplitudes; the seven-qubit control has 128. The all-marginal
checks reach 32 by 32 matrices. Actual software versions and observed core replay time
are in `supplement/environment.json`; peak memory of the independent replay was not
measured. No minimality, computational speedup, or exhaustive input-graph search is claimed.

To build the article with already installed TeX tools:

```sh
python3 manuscript/build.py
```

This creates `build/manuscript` and runs pdflatex, BibTeX, and two final LaTeX passes,
with shell escape disabled. It also runs pdftotext and pdfinfo, retaining the logs,
recorder file, PDF, and text. Required system components are pdflatex, bibtex, pdftotext,
pdfinfo, REVTeX 4.2, amsmath/amssymb, fontenc, and hyperref. No local custom style or
external figure is used. Existing directories are preserved; `--output build/rebuilt`
selects another clean location. In the local dossier, `publication.json` records the writing phase's current PDF;
that workflow manifest is not part of the public source bundle. The default command
is deliberately independent of the writing run's directory name.

The public handoff whitelist contains the article sources, these code/input files,
reproduction instructions, and author handoff. It excludes third-party full papers,
browser records, scientific-audit reports, and private execution logs. See the handoff
for the pending author review, AI disclosure details, and final license decisions.
