# Author handoff: elementary right divisibility of quantum channels

## Core claim

For every finite-dimensional CPTP map and every orthogonal ordered pair of unit
vectors, the published Kraus-subspace condition (N) is necessary and sufficient for
the existence of a positive-strength elementary amplitude-damping right factor. If
`V` is a full-column-rank minimal Kraus synthesis and `ZV=VA`, then the quotient is CP
exactly when `0 <= lambda < 1` and `lambda ||A||_op^2 <= 1`. This proves the complete
frozen phase-covariant qutrit claim for Choi ranks 2--8 and all six ordered pairs.

## Hardest checks already performed

- The exact Choi congruence and the transpose-sensitive vectorization identity were
  independently rederived by the referee.
- The converse was attacked through a Choi-kernel compression and found complete.
- Exact symbolic tests compare a direct superoperator quotient, the published Choi
  formula, and the congruence; they cover all target ranks and ordered pairs.
- The published Example 3 interval `[0, 1/6]` was independently reconstructed.
- The accepted science snapshot passes the structural science gate unchanged.

## Scientific caveats

- The general theorem assumes that the two defining states are orthogonal.
- `lambda=1` is outside the inverse domain; when the spectral threshold is at least
  one, the physical interval has supremum one but no endpoint at one.
- The result is a static channel factorization, not a time-family CP-divisibility,
  Markovianity, or experimental-decay claim.
- Priority is supported only relative to the checked primary source and bounded search.
  A human specialist should repeat the current search and consider contacting the source
  author before submission.

## AI use and policy

OpenAI Codex (`gpt-5.6-sol`) contributed to the idea, derivation, exact-code
preparation, verification support, literature synthesis, and drafting. The target
journal's current policy requires detailed Methods disclosure for this level of use;
the draft includes it. The named author must critically review every scientific claim,
citation, code path, figure, and disclosure before submission.

## Source map

- Accepted statement and scope: `claim.json`, `verification.json`, `physics.json`.
- Exact proof: `research/support-congruence-proof.md`.
- Independent audit: `audit/science.md`, `audit/replay.log`.
- Primary comparison: `literature/vom-ende-2407.17103v3-primary-excerpt.md`,
  `evidence/prior-comparison.md`, `evidence/literature-search.md`.
- Reproducible tests: `code/test_support_congruence.py` and the three baseline scripts.
- Manuscript: `manuscript/main.tex`, `manuscript/references.bib`, and the imported
  figure source under `manuscript/figures/`.

## Venue fit and pending author decisions

The provisional target is the *Journal of Mathematical Physics*, as an original
research article. Official scope and AI-policy sources are recorded in
`venue/aims-and-policy.md`; no ranking or acceptance claim is made. Before submission,
the author must confirm the byline and affiliation, CRediT roles, conflict-of-interest
statement, title and venue, priority language, code-sharing destination, AI disclosure,
and the final manuscript text. External submission is not authorized.
