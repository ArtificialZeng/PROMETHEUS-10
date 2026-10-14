# Author handoff

## Core claim

The draft proves both orientations of Schouten--de Leeuw Conjecture 2.7 for every
finite-dimensional local complex space, every source-regular braiding-normalized
Yang--Baxter `R(u,v)` (including non-difference form), every `k>=2`, and every homogeneous
untwisted periodic length `L>=k`. Each endpoint density has cyclic sum equal to the raw
logarithmic-transfer charge, and the two densities differ by exactly
`I tensor m - m tensor I`. The result is undeformed (`lambda^0`) and does not cover open,
twisted, inhomogeneous or positive-order long-range systems.

## Hardest checks

- Regular-factor unfolding and partial-trace cyclicity in manuscript Lemma 4.1.
- Inclusion of the differentiated root even when its remaining monomial exponent is
  zero, and the strict `k-1<L` support bound at the minimal size `L=k`.
- Exact left/right sign and product order, especially braiding normalization in equation
  (19).
- The tensor-word proof that the entire cyclic kernel, including scalar words and
  arbitrary local dimension, is a local gradient.
- The separate use of Yang--Baxter commutativity to identify the two Maurer--Cartan
  forms; generic non-YB controls are not physical counterexamples.

## Evidence map

- Primary target and conventions: `literature/2604.27189v2.pdf`, `problem.md`,
  `source-ledger.json`.
- Stable all-order derivation: `evidence/research-ordered-product-proof.md`.
- Exact convention/control tests: `evidence/reproduce-comparison.json`,
  `evidence/research-reparam-comparison.json`,
  `evidence/research-structural-comparison.json`.
- Fresh accepted AI scientific review: `audit/science.md` and `audit/replay.log`.
- Current bounded literature checks: `audit/current-literature-check.md` and
  `evidence/write-current-literature-check.md`.
- Draft and bibliography: `manuscript/main.tex`, `manuscript/references.bib`.

## Venue fit

The proposed target is Journal of Physics A: Mathematical and Theoretical, article type
“Paper”. Its official scope expressly covers quantum spin chains, quantum groups,
exactly solvable models and integrable systems. Ranking/indexing was not verified and no
acceptance prediction is made. See `venue.json` and `venue/aims-and-policy.md`.

## Caveats and pending author decisions

1. Independently read the proof line by line and confirm the theorem, title and novelty
   wording; an accepted AI referee is not human peer review.
2. Confirm the author name, affiliation, postal code and email before any dissemination.
3. Recheck the literature immediately before submission; current searches are bounded
   and do not prove priority.
4. Decide whether Journal of Physics A is the desired target and whether the standard
   article source should be converted to the current journal template.
5. Review and approve the AI disclosure. IOP's current policy permits disclosed use but
   requires author validation and responsibility; `ai_policy_status` remains
   `needs_author_judgment` until then.
6. Decide whether the exact scripts/data should be deposited in a public repository and
   assign a durable identifier. No external upload, submission or communication has
   been performed or authorized.

## AI-use statement

Codex assisted with literature retrieval, mathematical development, exact-arithmetic
code, independent AI audit and drafting. The manuscript accurately says that the named
author has not yet completed the required critical review. This wording must be updated
only after that review actually occurs.
