# phys-00003-p10

**Weak periodic phase shaping lowers the worst-case sensitivity of coherent-state qubit readout**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Rules out all fixed weak periodic same-axis phase shaping, including multiharmonic and discontinuous profiles, as an infinitesimal route to improving the established uniform single-mode qubit readout. Any improvement must evade this restricted perturbative conclusion. No improved interaction, hardware benefit or unrestricted optimum is asserted.

## Original question

单比特读取相干光场，能否严格超过 \(4/e\) 的最坏幅度灵敏度？

## Frozen scientific scope

In the one-real-coherent-mode, fixed-ground-state-qubit, alpha-independent-unitary, qubit-only SLD-QFI model of source.md/problem.md, for every fixed L>0 and fixed real bounded Borel L-periodic function g nonconstant almost everywhere, set V_epsilon=exp[-i sigma_y(Q/sqrt(2)+epsilon g(Q))]. There exists epsilon0(g,L)>0 such that for every real epsilon with 0<abs(epsilon)<epsilon0, of either sign, the outputs are uniformly full rank and inf_{alpha in R} F_Q[rho_epsilon(alpha)]<4/e. Explicitly epsilon0=min(h/M,gamma/(2KM^2)), where M bounds abs(g), G is the exact first-variation response, gamma=min(-min G,max G)>0, and h,K are the uniform-rank/remainder constants in evidence/research/periodic-variation-proof.md. Constant g preserves 4/e. The profile and period are fixed before taking epsilon small; no common radius, norm-neighborhood maximum, finite-strength no-go or unrestricted optimum is asserted.

## Proposed contribution and limitations

A restricted exact directionwise obstruction: for every one fixed real bounded Borel periodic phase profile g, nonconstant almost everywhere, f_epsilon(x)=x/sqrt(2)+epsilon g(x) has inf over every real alpha of qubit QFI strictly below 4/e for both sufficiently small signs of epsilon. The radius depends on the profile and period. Explicit first-variation Fourier multipliers have no nonzero-frequency nulls; uniform full rank and a quadratic remainder establish the continuum conclusion.

Checked current official arXiv:2509.22361 history and full v2 primary Sections III.1 and III.6 on 2026-10-12; no later version listed. Existing full publisher and preprint sources and preprocessing/compression/repeated-query neighbors were read at their decisive premises. Current exact-title/identifier/author, coherent/qubit/worst-case/Fisher, 4/e/nonlinear and Gaussian/minimax/qubit/encoding searches identified no checked primary reporting this obstruction. Absence of hits is not priority proof. The source's in-preparation reference remains inaccessible and could affect novelty; fresh independent significance/novelty review remains required. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
