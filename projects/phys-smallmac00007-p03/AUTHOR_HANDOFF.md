# Author handoff: split-core threshold random walks

## Core claim

For every positive integer `s,q,t`, the two threshold codes
`01 0^t 1^s 0^q 1` and `0 1^s 0^t 1 0^q 1` have Kemeny's constant strictly
below the larger of the two legal pineapple values with parameters `s+1` and
`s+t+1`. This is an exact partial result; the original all-threshold-graph
conjecture remains unresolved.

## Hardest checks already performed

- Exact block summation of the source formula produces four rational gaps.
- Positive-coefficient identities cover every positive `s,q,t`, including the
  low/high-pineapple branch switch.
- A separate exact checker tested 3,600 parameter triples and ten literal full
  graphs. A fresh referee independently rebuilt a six-block quotient derivation
  and accepted only this restricted result-note scope.
- The simpler edge-filling surgery is genuinely nonmonotone: the draft retains
  exact examples in both directions and one equality case.

## Caveats requiring author attention

- The result does not cover other six-run placements, multiple interior zero runs,
  a global equality classification, or the full conjecture.
- The proof is computer-assisted exact algebra. The author should personally review
  the source formula, the normalization of all four gap numerators, the positive
  identities, and the independent replay before taking responsibility.
- Novelty language is deliberately bounded. The 2025 version-of-record paper was
  not available for equation-by-equation comparison, and no exhaustive worldwide
  priority claim is made.
- Author name, affiliation and email in the draft were user supplied and require
  confirmation: Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190;
  xiaojianzeng@foxmail.com.

## AI involvement

OpenAI Codex assisted with problem development, symbolic-code construction, exact
calculations, evidence organization, computational checking, literature organization
and manuscript drafting. The draft does not claim that the named author has reviewed
or approved those outputs. The included declaration must be reconciled with the
author's actual review and the current journal policy before submission.

## Source map and target fit

- Model, general code formula and pineapple conjecture/formula: Breen et al.,
  arXiv:2310.08552v1, Theorem 3.8, Conjecture 3.13 and Lemma 3.14.
- Exact new derivation: `evidence/surgery-family-proof.md`,
  `evidence/surgery-symbolic.json`, `code/derive_surgery_exact.py`.
- Independent checks: `code/check_surgery_exact.py`,
  `evidence/surgery-exact-check.json`, and the frozen referee dossier under `audit/`.
- Venue rationale and current policy: `venue/aims-and-policy.md`. Linear Algebra and
  its Applications is a plausible research-article target because it published the
  closest paper and explicitly covers combinatorial matrix theory. Fit and acceptance
  are not guaranteed.

No external submission has been made or authorized.
