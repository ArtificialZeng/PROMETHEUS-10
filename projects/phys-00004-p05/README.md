# phys-00004-p05

**Diagonal quantum discord under unital qubit noise: a relative-entropy proof for two-qubit states**

Result class: `proofs`; original question: `proved`; release: `draft_ready_author_review_required`.

## Background

Within the stated finite-dimensional single-use noise model, local unital noise cannot increase diagonal discord despite a moving marginal eigenbasis. This supplies the resource monotonicity left numerically supported in S1 for the frozen two-qubit domain.

## Original question

单比特unital噪声，能否增加二比特态的对角量子失谐？

## Frozen scientific scope

For every two-qubit density operator rho_AB and every unital CPTP channel E_A, provided both rho_A and E_A(rho_A) are nondegenerate, the entropy-based diagonal discord S(pi_A rho_AB)-S(rho_AB), using each state's own marginal spectral projections, is nonincreasing under E_A tensor id_B. This settles precisely the frozen source.md/problem.md domain, including rank-deficient global states and arbitrarily small positive marginal gaps.

## Proposed contribution and limitations

Exact proof of the entire frozen nondegenerate two-qubit/unital-CPTP inequality via channel-image compatibility with output marginal pinching and the quantum relative-entropy Pythagorean identity. Channel/dephasing commutation is unnecessary for this entropy-based claim.

2026-10-12 exact-title and diagonal-discord/unital/monotonicity/counterexample/conjecture/proof/relative-entropy/pinching/noncommuting/Pythagorean searches; latest S1 version record and relevant full primary passages checked; S2 actual v4 primary PDF/text rechecked. No later exact resolution identified, but no exhaustive citation graph or priority guarantee. Primary and raw query evidence preserved. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
