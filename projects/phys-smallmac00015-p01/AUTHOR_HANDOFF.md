# Author handoff: sharp weak-driving phase bound

## Core result

At the accepted scope—complete `K_N`, `N>=3`, common `k0`, symmetric rate splitting,
finite offsets, normalized periodic steady state, finite real Fourier drives, and the
coefficients through `O(epsilon^2)`—the draft proves `A2 >= 2 k0 B2`. Every
response-active finite-offset drive is strict; equality is exactly the zero-response
class. The two-heavy family gives `A2/B2 = k0[2+(N-2)delta]`, so 2 is the unattained
sharp infimum.

## Hardest checks already completed

- Fresh referee reconstruction confirmed the departure-rate convention, similarity
  transform, modal response weights, and the symmetric two-state baseline.
- The accepted proof handles `q_max<1/2`, `q_max=1/2`, and `q_max>1/2`; the last branch
  uses the monotone secular equation and strict superadditivity of `t/(1-2t)`.
- Exact-rational and symbolic checks attack the branch boundary, secular sign,
  superadditivity identity, and sharp-family eigenpair. They corroborate rather than
  replace the proof.

## Scope and caveats

- Do not extend the conclusion to finite amplitudes, unequal edge prefactors,
  asymmetric splitting, missing links, transients, or singular offsets.
- The literature search supports cautious candidate novelty only. Classical matrix or
  Markov-chain literature under different notation was not exhaustively excluded.
  Avoid “first proof” or exhaustive-priority wording unless a fresh citation audit
  justifies it.
- This project is the canonical all-`N` successor. If the neighboring `N=3` draft is
  retained, it should be treated as a superseded local archive only after this project
  passes release; do not submit both as competing papers.
- The shorter alternative proof mentioned in `MERGE_PLAN.md` was not in the accepted
  scientific snapshot and is deliberately absent from this manuscript.

## AI use and venue

The target considered is JSTAT, standard research Paper. The subject scope is verified,
but ranking is unverified and journal acceptance is not implied. IOP/JSTAT require
detailed AI disclosure. OpenAI Codex using model `gpt-5.6-sol` assisted with ideation, derivations, code, verification,
literature discovery, and drafting; the current policy record conservatively marks this
as requiring author judgment and possibly editorial confirmation.

The manuscript contains an accurate draft-stage disclosure and does not claim that a
human has already verified everything. Before submission, the named author must review
the complete science, citations, code, disclosure wording, conflict statement, and data
availability statement.

## Source map

- Model and closest prior physical result: `literature/deguenther-jstat-2022-vor.pdf`,
  Eqs. (1)–(4), (31)–(36), and Appendix B.
- Accepted response derivation: `evidence/source-reconstruction.md` and
  `reproduction.json`.
- Accepted exact proof: `evidence/spectral-gap-proof.md` and `verification.json`.
- Independent audit: `audit/science.md` and `audit/replay.log`.
- Bounded novelty comparison: `evidence/prior-comparison.md`.
- Venue and AI policy: `venue/aims-and-policy.md` and `venue.json`.
- Reproduction instructions: `reproducibility/README.md`.

## Pending author decisions

1. Confirm the name, affiliation, postal code, and email shown in the draft.
2. Approve or revise the title, venue, article type, AI disclosure, and conflict statement.
3. Perform independent scientific and citation review; broaden the literature search if
   making any priority claim.
4. Choose a public repository and persistent identifier for the code availability
   statement.
5. Decide whether to contact JSTAT about the disclosed AI research use.
6. Do not submit externally until the fresh citation/build/visual release audit passes.
