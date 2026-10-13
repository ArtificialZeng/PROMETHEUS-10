# Author handoff: exact coarse-GAD current-bit optimum

## Core result in the draft

For the fixed ordered full-Choi-rank GAD instrument with the incoherent `03|12`
readout, two fresh uses, and four arbitrary clock-dependent qubit CPTP recoveries that
see only the current bit, the draft proves

`F_2^M = 289/400`

at `p=18/25`, `gamma=3/10`. Identity recovery attains the value. The fixed feasible
retained-first-bit policy reaches `1831/2500`, so its exact advantage over the optimal
current-bit policy is `99/10000`. The draft also proves a uniform full-history gap of
at least `1/1000` on

`[71/100,723/1000] x [29/100,303/1000]`.

This manuscript is the coherent successor to the Batch-15 parent draft. It replaces
the old nonsharp `456/625` centre bound and adds the robustness theorem; it is not a
second paper about the same model.

## Hardest checks already performed

- The accepted science audit independently reconstructed the Kraus ordering, the
  incoherent bins, full rank, all 16 hidden paths, and genuinely time-dependent
  current-bit factorization.
- The centre proof controls nonunital recovery translations through Hermitian
  trace-norm contraction, then uses axial Gram averaging, concavity of `Tr sqrt`,
  nuclear-norm duality, and a sharp Frobenius bound.
- Independent exact arithmetic reproduces the crossing `49/54`, endpoint derivative
  `2991/1274`, one-clock cap `189/100`, and optimum `289/400`.
- The rectangle proof uses an all-CPTP column bound and exact derivative margins; its
  minimum is the upper-right rational corner, not a grid sample.
- The current write-role replay used Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5, and
  SciPy 1.18.1. Both decisive exact checkers passed.

## Scope and caveats to preserve

- `99/10000` is the exact advantage of the displayed history witness over `F_2^M`.
  It is not the exact optimum gap `F_2^B-F_2^M`, because `F_2^B` is not determined.
- The rectangle is sufficient and nonmaximal; no exact off-centre current-bit optimum
  is claimed.
- The result is tied to the displayed ordered Kraus realization and `03|12` readout.
  Other pairings, Kraus-gauge changes, correlated baths, more uses, and persistent
  quantum memory are outside scope.
- The literature search and venue assessment are bounded. Priority, broader control
  literature, and journal fit require human review.

## Source and reproducibility map

- Manuscript: `manuscript/main.tex`; bibliography: `manuscript/references.bib`.
- Centre proof: `evidence/exact-global-certificate.md` and
  `scripts/verify_global_bound_constants.py`.
- Robustness proof: `merged/phys-00016-p02/evidence/robust-rectangle-certificate.md`
  and `merged/phys-00016-p02/scripts/verify_robust_rectangle.py`.
- Independent model reconstructions: `scripts/reconstruct_a_exact.py`,
  `scripts/reconstruct_b_liouville.py`, and `scripts/compare_reconstructions.py`.
- Commands and versions: `manuscript/REPRODUCIBILITY.md` and
  `evidence/write-runtime-versions.txt`.

## Venue and pending author decisions

The provisional target is *Quantum Information Processing*, Regular Article. Its
official scope includes quantum error correction and it published the closest 2024
feedback paper. Current Springer Nature policy requires substantive AI use to be
declared and the scholarly argument to remain author-led and human-verified. Because
AI assisted with derivation, code, checks, and drafting, the author must independently
check the proof, references, code, interpretation, and AI declaration before deciding
whether the journal's policy is satisfied.

Before any submission, the author must also confirm the name, affiliation, postal
address, email, funding statement, competing-interest statement, target journal,
bibliography coverage, and whether the source bundle may be redistributed. No external
submission or human approval has been recorded.

