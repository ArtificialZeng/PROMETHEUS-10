# phys-00007-p05

**Exact conditional min-entropy of two-qubit unitary channels with white noise**

Result class: `proofs`; original question: `proved`; release: `draft_ready_author_review_required`.

## Background

The conditioning-channel TP restriction has zero cost for this single-use family; its conditional channel min-entropy is computed exactly from the pure-unitary Choi Schmidt spectrum rather than by a constrained SDP. Units are bits and the resource interpretation uses trivial output Hamiltonians.

## Original question

任意双qubit酉门叠加白噪声，其条件信道min-entropy能否直接由Choi态求得？

## Frozen scientific scope

For every U in U(4) and real p in [0,1], let Omega=(1-p)|u><u|+p I16/16 be the normalized Choi state in the grouped X=RA A,Y=RB B order, rho_U=Tr_X |u><u| and L=Tr sqrt(rho_U). For the exact SDPs in problem.md, including Tr_B Q=(Tr Q)I_RB/2 in t, s(Omega)=t(Omega)=(1-p)L^2+p/4. A common optimizer is Q=(1-p)L sqrt(rho_U)+(p/16)I4. Hence S_infty[A|B]_N=H_min(X|Y)_Omega-1 for every frozen noisy two-qubit gate, including degeneracies, deficient Schmidt rank and p endpoints. This is a proposer proof awaiting fresh referee review.

## Proposed contribution and limitations

Settle the frozen all-U(4), all-p in [0,1] noisy identity and supply explicit common optimum (1-p)(Tr sqrt(rho_U))^2+p/4 with a common TP-feasible optimizer and matching state-dual witness.

2026-10-12: current official arXiv pages/fulltext confirm v2 for both decisive preprints; decisive local source sections re-read; exact identifier/title, author/noisy, white-noise, depolarized-pure, pseudopure and Schmidt/min-entropy queries. No later primary resolution verified; bounded searches do not establish global priority; independent referee comparison remains required. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](REPRODUCIBILITY.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
