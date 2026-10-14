# phys-00004-p08

**Arbitrarily clustered hot spots on bridgeless quantum graphs**

Result class: `proofs`; original question: `proved`; release: `draft_ready_author_review_required`.

## Background

For homogeneous standard-Kirchhoff network diffusion, the hottest/coldest set of the unique slowest nonconstant mode does not impose any positive universal lower bound relative to network metric diameter, even when every edge lies on a cycle. This is a model prediction with constant diffusivity, without a fixed-volume or bounded-degree constraint.

## Original question

没有桥的输运网络，能否让最慢热模态的全部冷热极值任意靠近？

## Frozen scientific scope

For every real epsilon>0 there is a finite connected compact positive-length standard-Kirchhoff metric multigraph Gamma with every edge on a cycle, diameter 1, simple first positive eigenvalue mu2, and complete global maximum/minimum union M satisfying diam(M)<epsilon. Explicit witness: for m=max(4,ceil(36/(pi^2*epsilon^2))), h=atan(1/sqrt(m))/pi, take a central tree with two long arms 1/2, two stems h to fan hubs, and m leaves of length 2h per hub; replace every edge by two equal parallel copies. Its simple mu2=[atan(1/sqrt(2m+1))/h]^2, its full metric diameter is 1, and its complete extrema union is exactly the 2m fan leaf vertices of diameter 6h<epsilon. This is the original Conjecture 8.9 no-bridge scope, allowing articulation vertices and no fixed volume/degree restriction.

## Proposed contribution and limitations

An explicit one-integer uniformly doubled lengthened split-tree family proves the full printed existence statement: for m>=4, h=atan(1/sqrt(m))/pi, mu2=[atan(1/sqrt(2m+1))/h]^2 is simple, the exact complete extrema union has diameter 6h, and the actual doubled metric diameter is 1. m=max(4,ceil(36/(pi^2*epsilon^2))) makes 6h<epsilon for every epsilon>0.

Fresh bounded primary-source searches and exact-transfer comparison on 2026-10-12, recorded in evidence/research-pass1-literature.md and raw web-01 through -08. Current official original v4, survey v3, and same-authors higher-dimensional v2 were checked. No direct later resolution was identified; incomplete indexing and other terminology limit any priority claim. candidate_novel is provisional and requires a fresh referee novelty/significance check. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](REPRODUCIBILITY.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
