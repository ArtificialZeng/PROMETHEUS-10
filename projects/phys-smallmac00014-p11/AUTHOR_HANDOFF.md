# Author handoff

## Status and core claim

This is a local `resolution-paper` draft with status
`draft_ready_author_review_required`. It has not been submitted, peer reviewed,
or approved by the listed author.

The accepted claim is: for every qubit CPTP channel with positive-definite
Choi matrix, when one four-outcome orthogonal projective measurement is reused
on each fresh minimal environment, the separately optimized current-outcome
polar and full-history/final-only entanglement fidelities are equal for every
positive integer `n` and have value

`(1 + ||Q||_*^n)/2`,

where `Q` is the complex symmetric determinant-polarization matrix of a
minimal Kraus frame. The requested full-rank three-use equality is the `n=3`
case.

## Hardest checks for the author

1. Reconstruct the quaternion identities in the basis `(1,i,j,k)`, including
   symmetry, tracelessness, and rank two of
   `P=(I+L_u R_v)/2`, and verify the factor in
   `tr(PH)=u^T C(H)v/2`.
2. Audit every degeneracy in the collinear-diagonal lemma: an ellipse map of
   rank at most one must admit a zero, while two rank-two image planes in
   `R^3` must intersect in a line.
3. Check the Kraus-index convention through the Takagi change of frame:
   `Q=V Sigma V^T`, `U=O V^dagger`, and
   `det K(r)=r^T Sigma r`. Confirm that the constructed real-orthogonal family
   attains the global diagonal trace-norm bound.
4. Re-derive the traceless Bloch forms from trace preservation and confirm
   that collinear effect Bloch vectors imply pairwise commuting effects.
5. Re-derive both fixed-measurement scores, retaining the complex modulus in
   the Markovian branch trace at three uses. Confirm that pointwise equality is
   not confused with equality of separately optimized values.
6. Run both programs in `reproducibility/README.md` and compare with the bound
   logs. The floating-point checks support implementation fidelity only; they
   do not replace the exact proof.

## Source map

| Manuscript content | Bound source/evidence |
| --- | --- |
| Physical model, history order, fidelity normalization | `problem.md`, `physics.json` |
| Fixed-decomposition polar and final-only recovery | `literature/gregoratti-quant-ph-0403092v1.pdf`, `evidence/source-reconstruction.md` |
| Closest Bayesian/Markovian comparison and Conjecture 9 | `literature/rexiti-2402.18941v1.pdf`, `evidence/source-reconstruction.md` |
| Determinant reduction and three-use deficit | `evidence/three-use-reduction.md` |
| Quaternionic lemma and optimal commuting frame | `evidence/takagi-commuting-frame-proof.md` |
| Diagnostic implementation and values in Table 1 | `code/takagi_commuting_frame.py`, `code/search_three_use.py`, `evidence/takagi-commuting-frame.log` |
| Published-baseline reconstruction | `code/reproduce.py`, `evidence/baseline.log`, `reproduction.json` |
| Bounded novelty comparison | `value.json`, `evidence/prior-comparison.md`, `audit/science.md` |
| Venue scope, article type, and AI policy | `venue.json`, `venue/aims-and-policy.md` |

## Scope and caveats

The proof does not cover adaptive environment bases, extra-outcome POVMs,
correlated uses or environments, imperfect classical records, nonunitary
recovery models, higher system dimension, or implementation cost. No
experimental claim is made. Full Choi rank is used to bind the model to a
minimal four-dimensional environment and a `U(4)` projective measurement.
The literature search was bounded; priority and related-work coverage remain
for human review.

## Venue fit and policy

`Quantum Information Processing`, Regular Article, is the provisional target.
Its current scope includes theoretical quantum error correction, and it
published the closest prior article. The publisher page currently lists SCIE;
no quartile or acceptance claim is made.

Springer Nature's current AI policy requires transparent disclosure and human
accountability, and does not permit AI to replace scholarly judgment. This project used
AI for proof discovery, calculations, code, literature comparison, audit, and
writing. `venue.json` therefore records `needs_author_judgment`. The current
manuscript disclosure accurately says that author verification is pending;
submission must wait until the author independently reviews the work, decides
whether the use is policy-compatible, and assumes responsibility. If that
happens, the disclosure must be updated to state the human oversight actually
performed.

## Decisions pending from Xiaojian Zeng

- Confirm name, affiliation, postal code, and email on the title page.
- Independently verify the full proof, physical conventions, code, sources,
  novelty framing, and all numerical values.
- Confirm or replace the funding and competing-interest statements.
- Confirm the journal and article type; resolve the journal page's inconsistent
  abstract-length instructions and migrate to the current Springer template if
  required.
- Decide on a license for any public code/data package and approve the exact
  redistribution set.
- Revise and approve the generative-AI disclosure in light of the review
  actually performed and the policy in force on the submission date.

## Local artifacts

- Manuscript source: `manuscript/main.tex`
- Bibliography: `manuscript/references.bib`
- Built PDF: `build/main.pdf`
- Build transcript: `build/main.log`
- Reproduction instructions: `reproducibility/README.md`
