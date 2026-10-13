# Author handoff: symmetric three-state weak-driving phase bound

This is a local draft for author review. It has not been submitted, peer reviewed, or
approved by the named author.

## Core accepted claim

For the complete three-state Markov graph with common `k0`, symmetric splitting,
finite static offsets, and any non-gauge finite real Fourier perturbation, the unique
periodic state has

`A = epsilon^2 A2 + O(epsilon^3)` and
`B = epsilon^2 B2 + O(epsilon^3)`, with `B2 > 0` and `A2 > 2 k0 B2`.

The remainder is for each fixed finite input. The constant 2 is a strict finite-offset
bound and a sharp infimum approached only in an effective-two-state infinite-offset
limit. The original all-amplitude three-state inequality remains unresolved.

## Hardest checks completed in the research dossier

- Two independent source representations reproduce the published two-state weak-drive
  phase `atan[Omega/(2 k0)]` and agree on the departure-rate convention.
- A fresh, separately initialized scientific audit reconstructed the generator and
  derived the strict spectral bound with a Dirichlet-form argument different from the
  discovery proof.
- The accepted modal formula covers both tangent relaxation modes and every harmonic of
  an arbitrary finite Fourier drive; a non-gauge drive gives `B2 > 0`.
- The exact identity `Z-2 r_i r_j=(r_i-r_j)^2+r_k^2` makes the relaxation bound strict
  for every finite offset. The family with offsets `(0,0,H)` excites a rate
  `k0(2+exp(-H/2))`, proving sharpness without inserting an infinite energy into the
  theorem.
- Independent full-propagator and Fourier-collocation calculations reproduce the two
  numerical rows in the paper. They check conventions and convergence only; the proof
  is analytic.

## Source map

- Immutable prompt/source: `source.md` (SHA-256
  `1ca279aa88b4e2512bbbabaea7a64190a671eb1d4514f75d08ab251a2c2cbcb5`).
- Exact interpreted model and unresolved original target: `problem.md`, `physics.json`.
- Primary-source ledger and baseline: `source-ledger.json`, `reproduction.json`,
  `literature/deguenther-jstat-2022-vor.pdf`.
- Accepted scoped claim and verification: `claim.json`, `verification.json`,
  `evidence/k3-linear-response-proof.md`.
- Independent audit: `audit/science.md`, `audit/replay.log`.
- Manuscript and bibliography: `manuscript/main.tex`, `manuscript/references.bib`,
  `manuscript/main.bbl`.
- Exact figure and data: `manuscript/figure_sharpness.py`,
  `manuscript/sharpness-data.csv`, `manuscript/sharpness.pdf`.
- Reproduction instructions and captured public-facing values:
  `reproducibility/README.md`, `reproducibility/check-results.txt`.
- Clean draft PDF and compiler log: `build/clean/main.pdf`, `build/clean/main.log`.
- Venue and policy evidence: `venue.json`, `venue/aims-and-policy.md`.

## Target fit and policy status

The provisional target is *Journal of Statistical Mechanics: Theory and Experiment*,
standard research paper, area "Classical statistical mechanics, equilibrium and
non-equilibrium". The closest source article appeared there, and the journal's current
scope covers this work. No ranking, quartile, acceptance, or indexing claim has been
verified.

IOP/JSTAT permits disclosed AI assistance for several research and drafting tasks, but
requires critical human revision and detailed model/use disclosure. The current IOP
policy also says that authors may not use AI to generate reference lists. The three-entry
BibTeX draft was transcribed from primary full text and official/repository metadata, but
the author must manually verify and, if necessary, recreate every entry before submission.
For that reason `venue.json` records `needs_author_judgment`, not completed compliance.

## AI-use disclosure

OpenAI Codex with model `gpt-5.6-sol` assisted with problem scoping, analytic derivation,
code generation/execution, numerical verification, literature discovery, and manuscript
drafting. A separately initialized session of the same model replayed and stress-tested
the science. The draft states this explicitly and does not name AI as an author or claim
completed human verification.

## Pending author decisions and checks

1. Confirm the draft author details: Xiaojian Zeng; PBC School of Finance, Tsinghua
   University, Beijing 100190, China; `xiaojianzeng@foxmail.com`.
2. Re-derive the key modal and Dirichlet identities, inspect the rate direction and phase
   convention against the version of record, and decide whether to endorse the result.
3. Manually verify every citation and bibliography field; broaden the literature search
   before making any novelty or priority statement.
4. Confirm JSTAT as the target, the standard-research-paper type, the journal template,
   code/data packaging, and the exact AI disclosure current at submission time.
5. Review the numerical scripts, table inputs, figure, and all six PDF pages. Decide
   whether the numerical table is useful enough to retain in a short analytic paper.
6. Confirm that no third-party full text is included in any submission archive. The
   proposed handoff list deliberately excludes the local literature cache and internal
   job/audit trees.

External submission is not authorized by this handoff.

