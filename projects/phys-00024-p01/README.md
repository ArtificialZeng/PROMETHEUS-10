# phys-00024-p01

**Local stability of a sharp q-deformed commutator response for conditional quantum operations**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

The already reconstructed conditional-Kraus ordered-amplitude response has a locally stable sharp upper envelope: general operator errors normal to the saturation family, including spectator-level coupling, reduce the optimized response quadratically. A violating tuple cannot approach this orbit at fixed n,q. No explicit neighborhood radius or new relaxation-rate prediction is claimed.

## Original question

非正规量子跃迁的顺序响应，q 变形对易子的锐界是否对所有维数成立？

## Frozen scientific scope

For each finite n>=3 and each real q not equal to -1 or 1, set R=sqrt(2(1+q^2)), c=(1+q+R)/2, u=sqrt(c-1), b=sign(1+q)sqrt(c-q), A_q=diag(u,-b,0,...,0). For g_q(A)=lambda_max(H_q(A))/||A||_F^2, where vec(B)^dagger H_q(A) vec(B)=Re Tr((BA-AB)^dagger(BA-qAB)), there exists an n,q-dependent neighborhood of A_q in M_n(C) on which g_q is real analytic with a Morse-Bott local maximum c. Its local maximum set is the smooth 4n-2 real-dimensional manifold of unitarily embedded two-plane matrices C satisfying det C+[ub/(u-b)^2](tr C)^2=0 near diag(u,-b). The complete negative normal Hessian spectrum at A_q is -2, -4c(c-q)/[(2c-q)R], -4c(c-1)/[(2c-1)R], -2c/R, with multiplicities 2,2(n-2),2(n-2),2(n-2)^2. For mu the smallest magnitude and Lambda the largest, a smaller tubular neighborhood satisfies (mu/8)dist_F(A,M_q)^2 <= c-g_q(A) <= Lambda dist_F(A,M_q)^2, hence the corresponding local sharp f-bound holds for every complex B. No explicit radius, global bound, or uniform n/q limit is claimed. Auxiliary q=1/2 n=2 nonzero equality matrices are exactly det A+(3/2)(3+sqrt(10))(tr A)^2=0.

## Proposed contribution and limitations

For every finite n>=3 and real q except -1,1, prove a full-dimensional local sharp bound near the embedded witness, classify its smooth equality manifold of dimension 4n-2, and derive the complete negative normal Hessian spectrum with multiplicities. Auxiliary q=1/2 equality determinant and curvature explain the previous flat directions.

Primary-source and exact-claim rechecks on 2026-10-13: arXiv:2208.10005v1, current publisher abstract, arXiv:2608.03897v1 q-commutator norms, arXiv:2409.00436v1 averaged relaxation resolution, exact identifier/title/formula/author and equality/stability/Morse searches. No primary statement of this local all-q f-response spectrum was found; this bounded screen is not priority certification. Fresh novelty and significance review remain required. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
