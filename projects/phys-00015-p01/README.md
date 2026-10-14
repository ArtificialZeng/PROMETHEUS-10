# phys-00015-p01

**Local dissipation optimality at the spectral coherence threshold of unicyclic clocks**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Small kinetic heterogeneity cannot reduce the homogeneous dissipation cost once the leading spectral coherence is restored to the source's eligibility threshold. Any improvement or counterexample must leave the n-dependent local neighborhood. This is a finite-model response result, not an experimental entropy estimate or a global bound.

## Original question

异质单环随机时钟的谱熵产生界，是否仍有普适系数一？

## Frozen scientific scope

For each integer n>=5 put t=tan(pi/n). The homogeneous strictly positive single-cycle rates u=c(1+t), d=c(1-t), c>0, have a simple globally leading conjugate pair with b/a=1. In a sufficiently small n-dependent neighborhood modulo common time scaling, every legal rate tuple with b/a>=1 satisfies Y=sigma*a/b^2 >= (1+t^2)*atanh(t)/t>1, with equality only at that homogeneous threshold ring up to scale. The full fixed-b/a=1 heterogeneous tangent Hessian is positive definite, including even-n Nyquist modes. No explicit or uniform-in-n radius, arbitrary-coherence optimality or global heterogeneous inequality is claimed.

## Proposed contribution and limitations

Exact positive full heterogeneous tangent Hessian at b/a=1 for every n>=5, and resulting strict local minimum of Y=sigma*a/b^2 among nearby positive-rate single cycles on b/a>=1, modulo time scale. Stationary probabilities and edge flows both vary freely. Nyquist modes and the local spectral ordering are included.

Bounded primary checks on 2026-10-12: OBS 2112.01607v2, Gu 2606.05498v1, Shiraishi 2609.34352v1, Kolchinsky 2510.14101v3, winding paper 2605.15884v3, current Jason author TeX scope and Uhl--Seifert 1907.04260v1 Section 4. Searches included entropy/coherence, unicyclic/heterogeneous, uniform rates, perturbation, second order and local minimum. No exact predecessor for this restricted entropy-cost statement was identified. Priority and significance remain candidate assessments; publisher-final-body comparison and a complete forward-citation census are not completed. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
