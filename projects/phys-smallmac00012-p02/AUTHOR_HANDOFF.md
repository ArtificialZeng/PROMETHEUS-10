# Author handoff

This is a local **result-note draft** for author review. It has not been
submitted, peer reviewed externally, or approved by the named author.

## Core accepted claim

For every dimension `d`, if a circulant bistochastic matrix
`B[i,j]=b[i-j]` is realized as `|U[i,j]|^2` by any same-dimensional unitary,
then each Fourier eigenvalue equals
`tr(D_k U D_k^dagger U^dagger)/d` and lies in the closed unit
`d`-hypocycloid. At `d=5`, the exact rational vector
`(209/500,3/40,7/500,3/40,209/500)` passes all bracelet inequalities but is not
unistochastic because its first Fourier mode lies strictly outside that
hypocycloid.

The original proposition `C_5 intersect U_5 = C_5^2` remains unresolved. The
rational witness is not a counterexample to it because the witness is not
unistochastic.

## Hardest checks and limitations

- The displacement sign and factor of `d` in the commutator-trace identity were
  derived explicitly and replayed on a distinct exact noncommuting unitary.
- All row and column bracelet cases reduce to two cyclic separation multisets;
  the only nearly saturated inequality has a certified positive lower margin
  of `1/1250`.
- The first Fourier eigenvalue is exactly
  `((465+343*sqrt(5))/2000) exp(i*pi/5)`, strictly beyond the radial boundary
  `3/5`.
- The result constrains individual Fourier modes only. It does not characterize
  their joint phase image, prove sufficiency of hypocycloid membership, or
  settle the five-site phase-recovery conjecture.
- The primary-source search was bounded. The referee found no exact prior
  statement in the checked sources, but exhaustive priority is not claimed.

## Source map

| Draft material | Frozen or publication source |
| --- | --- |
| Original five-site question and physical domain | `source.md`, `problem.md`, `physics.json` |
| Published `d<=4` baseline and convention map | `reproduction.json`, `evidence/primary-source-excerpt.md` |
| All-`d` proposition and rational witness | `evidence/hypocycloid-gate-no-go.md` |
| Deterministic exact check | `code/hypocycloid_gate_no_go.py`, `evidence/hypocycloid-gate-no-go.log` |
| Independent scientific replay and accepted scope | `audit/science.md`, `audit/referee_replay.py`, `audit/referee_replay.log` |
| Bounded literature comparison | `evidence/research-literature-check.md` |
| Journal scope and policy | `venue/aims-and-policy.md`, `venue.json` |

## AI involvement

OpenAI Codex assisted with research ideas, derivation, symbolic-checking code,
bounded literature screening, independent AI review, and manuscript drafting.
The draft discloses this in its Methods section because the current AIP policy
requires disclosure when AI may affect findings or conclusions. The local AI
referee is not external peer review. The human author must independently assess
the science, references, novelty language, and disclosure before any use of the
draft.

## Target fit

The provisional target is the *Journal of Mathematical Physics*, Research
Article. Its current scope explicitly includes mathematics applied to physics
and mathematical methods for physical theories, and the closest source paper
appeared in the same journal. No ranking or acceptance claim has been made.
Target and article type still require author approval.

## Decisions required before submission

1. Confirm the author name, PBC School of Finance affiliation, postal code, and
   email exactly as they should appear; inclusion here is not institutional
   endorsement.
2. Perform a full human scientific review, including the sign convention,
   bracelet reduction, radial-boundary argument, and strict inequalities.
3. Perform a broader human literature and priority search and revise novelty
   wording if an equivalent result is found.
4. Confirm the target journal and article type, and recheck its live policies at
   the time of submission.
5. Replace the pending conflict-of-interest and CRediT text with accurate,
   author-approved declarations; add funding and acknowledgments if applicable.
6. Confirm that the AI disclosure names the exact tool/model information
   available to the author and fully describes all relevant uses.
7. Choose a public repository or journal supplementary-material route for the
   exact checker and reference output, then update the data-availability text.
8. Review the final compiled PDF and approve any external submission. No
   external submission is authorized by this handoff.

## Redistribution scope

The proposed bundle contains only newly authored TeX/Bib/handoff/instruction
files plus the project-authored exact checker and its output. It excludes the
downloaded literature cache, third-party full texts, audit/job logs, browser
records, credentials, and release internals.
