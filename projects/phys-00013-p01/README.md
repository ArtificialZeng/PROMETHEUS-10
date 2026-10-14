# phys-00013-p01

**Exact pure-state contraction spectrum of a three-qubit Haar circuit**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Identifies centered single-qubit purity as the slowest state-observable mode at every symmetric moment order, excludes higher symmetric moments as slower counterexamples, and gives exact stationary L2 contraction for random pure-state preparation. The pure-state quotient is faster than the known group-level fourth-moment cosine1/2. It does not settle the original unitary-group mixing constant or imply a total-variation mixing time from a delta initial law.

## Original question

三量子比特 Haar 随机电路，所有表示的最慢模是否已在第四阶出现？

## Frozen scientific scope

For the specified three-qubit adjacent normalized Haar-SU4 circuit, the complete nonzero principal cosines on L2(CP7, normalized Haar) are c_r=6/((r+2)(2r+3)), r>=0. In conjugation on End(Sym^k C8), k>=0 integer, the cosines truncate to0<=r<=floor(k/2). Removing the whole global invariant gives norm0 for k<=1 and2/5 for every k>=2, and pure-state ordered m-step norm(2/5)^(2m-1), m>=1. This is a natural state quotient/symmetric-moment result; the original all-PU8 equality c_*=1/2 remains unresolved.

## Proposed contribution and limitations

For the same adjacent Haar-SU4 three-qubit circuit, derive the complete principal-cosine sequence c_r=6/((r+2)(2r+3)) on L2(CP7), r>=0, and its exact truncation to every End(Sym^k C8), r<=floor(k/2). The stationary pure-state nonfixed norm is2/5, and the ordered m-step norm is(2/5)^(2m-1). This is an all-degree quotient result; the number2/5 at degree2 and the finite k7/k8 tables are not the novelty claim.

Current official metadata and decisive primary full-text passages checked2026-10-12:2609.40164v2,2012.05259v1,2411.13739v2,2408.11201v2,1809.00642v1,math-ph/0610045v2,quant-ph/0012101v3,2606.11438v1. Searches covered exact original constant, later resolutions, pure-state/all-symmetric-moment spectra, joint purity correlations and Jacobi/projective-space equivalents. No examined primary source gives this exact local-circuit all-degree sequence. This is bounded proposer novelty analysis, not exhaustive priority proof; the older Haferkamp-Hunter-Jones publisher body remains unexamined. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
