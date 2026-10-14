# phys-00005-p06

**An eighth-order inverse-response filter in a ten-site quantum walk**

Result class: `proofs`; original question: `proved`; release: `draft_ready_author_review_required`.

## Background

The same autonomous ten-site model and tau=2pi achieve one higher absolute response order, hence seventh rather than sixth conditional inverse-state power in gamma under the stated spectral and normalization factors. Couplings remain of order one, with a larger leading scalar success coefficient. Matched full-propagation samples show much smaller error at similar norm(H)*t; no complete algorithmic or hardware speedup is asserted.

## Original question

单次量子行走求逆，十站点链能否实现有统一余项的八阶滤波？

## Frozen scientific scope

For the exact R=4 ten-site zero-diagonal open Hermitian Jacobi chain of source.md/problem.md, there exist fixed positive couplings specified by the unique cancellation root in evidence/research-root-certificate.json, tau=2pi, a nonzero real linear coefficient ell in (-1.078612,-1.078611), x0=1/16 and C=131072002 such that |<10|exp(-i tau T4(x;J))|1>-i ell x|<=C*x^8 for every 0<x<=x0. This is the precise R=4 existence resolution, including the high-energy branch; it does not settle the original author all-R conjecture.

## Proposed contribution and limitations

An explicit exact-root specification of positive fixed R=4 couplings cancels cubic, quintic and septic low-energy coefficients simultaneously, retains a nonzero linear response, and gives the full-amplitude bound |a4-i ell x|<=131072002*x^8 for every 0<x<=1/16. Root existence is certified by interval contraction; the oscillatory high branch is bounded separately.

Primary version pages were reopened on 2026-10-12 around 17:32-17:34 UTC: 2508.06611v1, 2512.08141v1 and 2510.06316v3. Reread the original Conjecture 1/Table I/Appendix A, successor Theorem 4.1/Sections 4.2 and 6, and competitor v3 Section 4.4/Proposition 19/Corollary 20. Targeted exact-title/identifier/author searches identified no direct later resolution in this limited screen. The competitor uses repeated Hamiltonian-QSVT queries. Coverage is not exhaustive, absence of a hit does not prove priority, and candidate_novel requests independent novelty/significance review. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
