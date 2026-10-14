# Author handoff for the local result note

This is a local draft prepared for human scientific review, not an externally submitted or journal-accepted manuscript. Its scientific scope has a separate AI referee acceptance in the current dossier; final release review is bound in separate citation, build and visual audit records; human authorship approval remains pending.

## Core claim and its scope

For the published two-parameter noisy Werner--Holevo channel in the immutable original domain x>0,y>0,x+y<=1 and d>=3, positive sector eigenvalues s,a admit an arbitrary finite time-independent GKLS embedding on the same system exactly when s^((d+2)/d)<=a<=s^((d-2)/d). This allows arbitrary Hamiltonians, jumps and logarithm branches. For d=3, odd sector multiplicities and singularity exclusions make the criterion complete: s=1-3x/2-3y/4>0, a=1-x/2-5y/4>0 and s^5<=a^3<=s.

The original signed all-d classification remains unresolved. Negative even-multiplicity sectors for d>=4 are not covered. The draft makes no experimental, enlarged-system, time-dependent, perturbative or particle-discovery claim.

## Actual contribution and closest prior

Bhat--Chakraborty--Franz, arXiv:2301.10679v4, already provide the covariant generator, exponential and rate cone. The map alpha=-log(s), eta=(log(s)-log(a))/2 makes their cone alpha>=d|eta| exactly the displayed power inequalities. Hashagen et al. already provide the orthogonal sectors; Wolf et al. provide the general conditional-CP logarithm test. These ingredients are credited as prior work.

The surviving contribution is necessity without choosing a covariant generator or a principal logarithm. Real branch-independent sector traces survive full-O(d) averaging, and the orthogonal commutant makes the average the principal covariant logarithm. The qutrit parity argument then closes the entire physical triangle. Priority is supported only by the bounded current-primary-source search and must still be assessed by the author.

## Hardest checks for the author

1. Confirm that an arbitrary Hermiticity-preserving logarithm commutes with the endpoint and preserves its distinct real Hermitian sectors. Recheck the determinant identities fixing real restricted traces, including nonnormal/nonprincipal logarithms.
2. Confirm averaging inside the closed convex GKLS cone and the elementary full-O(d) scalar-intertwiner argument. The d=4 reflection step is material; SO(4) alone would retain separate Hodge sectors. Averaging is not assumed to commute with exponentiation.
3. Recheck Choi order, unnormalized Omega, and the two projected-Choi coefficients; distinguish Choi projectors from operator-space projectors. Verify the normalized symmetric/imaginary-antisymmetric jump sums.
4. Check the depolarizing coincident-eigenvalue case separately and the singular/negative odd-dimensional qutrit complement. Do not extend the proof to even negative sectors.
5. Inspect the exact 2023 parameter map and the 2026 Pauli semantic neighbor. Repeat priority searches before submission.

Stable arguments are evidence/research/sector-trace-reduction.md, evidence/research/pass3/proof-audit.md and evidence/research/pass4/prior-comparison.md. The accepted current report is audit/science.md; independent exact replay is audit/replay-a7261c1a2cbb.py and .log. Those audit records attest a bounded AI review, not human peer review. Neither checkpoint.md nor state.json supplies a derivation or publication input.

## Manuscript, reproduction and source map

The manuscript is manuscript/main.tex; bibliography is manuscript/references.bib; the draft PDF is build/release-final-1c77995c289b/main.pdf. The chart and exact rational coordinates are in manuscript/figures/. Every numeric example is an accepted exact benchmark or rational cone check. Rendering samples are not a numerical proof.

reproducibility/README.md gives portable regeneration instructions and the primary-source locators. publication.json enumerates the complete source snapshot and explicit proposed submission files. The proposed submission package excludes downloaded full third-party papers, raw literature responses, mutable handoffs, job metadata and private audit logs.

## Target and policy

The current source-backed target is Quantum Information Processing, Regular Article. Its official scope includes theoretical quantum information and the journal published the exact model paper in 2025. venue.json and venue/aims-and-policy.md record the current policy. No indexing or quartile is asserted, and no editorial acceptance is predicted.

The policy requires substantive generative-AI use to be documented and human accountability for the final work. The manuscript disclosure covers literature comparison, ideas, derivations, symbolic/numerical code, verification and drafting. It also states that human scientific review and accountability are still pending. The current policy flag is needs_author_judgment, not completed approval.

## Pending human decisions

- Confirm the draft author: Xiaojian Zeng; PBC School of Finance, Tsinghua University, Beijing 100190, China; xiaojianzeng@foxmail.com. The supplied affiliation and contact do not establish institutional endorsement.
- Review and take responsibility for all mathematics, physics, source attribution and novelty. Decide whether the extensive disclosed AI involvement is acceptable to the author and target journal.
- Supply accurate funding, competing-interest and author-contribution declarations. None has been invented.
- Choose the final target/article type and any publisher template changes; confirm redistribution of authored code and figures.
- Resolve the current QIP guidelines' conflicting abstract lengths (80-100 words in its single-blind subsection, 150-250 in its title-page subsection). This local draft uses the latter; no submission-format approval is implied. The unpublished 2026 Pauli comparison is identified in the text, while the five bibliography entries are published articles.
- Authorize any future submission separately. No external submission, communication or publication occurred in this job.

One next test: the named author should independently rederive the branch-invariant real-sector traces and full-O(d) averaging step, then confirm attribution and venue-policy decisions before any external action.
