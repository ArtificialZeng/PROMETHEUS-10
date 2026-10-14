# phys-00002-p13

**Sharp first-passage skewness and excess-kurtosis bounds for three-state cycles at large affinity**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Replaces rate-space numerical maximization by algebraic sharp limits on entropy-threshold timing asymmetry and excess tails in three-step dissipative cycles. Identifies an attaining half-affinity tilted-spectrum degeneracy and allows direct envelope evaluation at fixed dissipation.

## Original question

单环熵产生首达时间的最优上界：大亲和力分支能否解析求出？

## Frozen scientific scope

For the strictly positive finite-rate time-homogeneous N=3 periodic Markov ring and the large-threshold entropy-current FPT conventions of problem.md, at every finite A>=log(64), the separate sharp envelopes are U_S=sqrt(A) N(p_S)/V(p_S)^(3/2) and U_K=A Q(p_K)/V(p_K)^2. Here d=coth(A/4), H=(d^2+1)/(2d), t(p)=d p(2+p)/(1+2p)^2, zeta(p)=d^2 p^2/(1+2p)^3, V=H-2t, N=3H^2-1-6Ht+6zeta, and Q=3H(5H^2-3)-12(3H^2-1)t+12Ht^2+24Hzeta. p_S is the unique positive root of 4(d^2-1)p^2+(12d^2-4)p-(d^2-1)^2=0; p_K is the unique positive root of 8(d^2-1)p^3+(-4d^4+24d^2-12)p^2+(2d^4+12d^2-6)p-(d^2-1)^2(d^2+1)=0. Both bounds are attained by strictly positive finite rate vectors constructed in spectral-envelope-proof.md Section 5. This does not settle the original all-N/all-affinity problem or the kink locations.

## Proposed contribution and limitations

Exact sharp upper envelopes for both large-threshold scaled FPT skewness and scaled excess kurtosis for every strictly positive three-state ring at every finite A>=log(64). They are specified by unique positive quadratic/cubic roots in d=coth(A/4), and explicit strictly positive rate vectors attain each bound.

Current primary arXiv history/HTML 2110.14540 and exact-claim/later-resolution searches rechecked 2026-10-12 before extension. Compared retained 1510.03279v1, full 2204.08421v4 definitions/Section III E/Appendix A, and 2025 JSP 192,126 publisher fulltext definitions. No equivalent envelope found in this bounded screen. Publisher version of the 2021 source and exhaustive citation tracking remain incomplete; priority is proposed, not certified. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
