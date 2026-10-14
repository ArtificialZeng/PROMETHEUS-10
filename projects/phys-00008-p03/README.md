# phys-00008-p03

**Exact local spectrum and a residual-rate obstruction for quantum Latin-square normalization**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

For this measurement-array generator, excellent individual Gram conditioning does not guarantee a strict uniform one-cycle residual reduction. The family gap collapses quadratically near a classical endpoint. This identifies a geometric obstruction to a conditioning-only progress guarantee; no nonlinear iteration budget or probability law is claimed.

## Original question

量子Latin方阵的交替归一化，是否对几乎所有初值达到任意精度？

## Frozen scientific scope

For the explicit n=4 Q(theta) block-rotation quantum Latin square in evidence/research/local-spectrum-proof.md, the real derivative of one source row-then-column normalization cycle restricted to the 64-dimensional column-unitary tangent space has spectrum 0 (16), 1 (32), (1+cos(theta))/2 (8), (1-cos(theta))/2 (8), with degeneracies combined for all real theta. For every q in (0,1), delta in (0,1), eta>0, some theta in (0,pi/2) and legal column-unitary x with 0<||x-Q(theta)||_F<eta satisfy e(F(x))>q e(x)>0 while all eight inverted Gram spectra lie in [1-delta,1+delta]. This is a local one-cycle rate obstruction only and leaves the original almost-sure arbitrary-precision question unresolved.

## Proposed contribution and limitations

Exact complete spectrum 0^16, 1^32, ((1+cos(theta))/2)^8, ((1-cos(theta))/2)^8 of the n=4 family derivative restricted to the column-unitary tangent space, including classical endpoint degeneracies. Prove legal arbitrarily close curves with source-residual ratio tending to the slow eigenvalue and all inverted Grams arbitrarily close to I, excluding a uniform one-cycle q<1.

2026-10-12 primary version/conjecture, original Sections 3-4, 2016 Sections 5-6, 2017 strictly positive-block theorem domain, 2023 Problem 3.13, current author bibliography and limited 2026 v3 successor screen; Lewis-Malick Lemma 2.1/equation (11)/Theorem 4.3 and Musto-Vicary Definition 1/Example 2. Exact-title, alternating-projection, linear-convergence, principal-angle and quantum Sinkhorn rate searches. No matching explicit family spectrum identified in bounded checked sources; equivalent older results and priority remain a fresh-review question. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](manuscript/REPRODUCIBILITY.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
