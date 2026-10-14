# phys-00009-p01

**Exact two-particle relaxation crossover for the symmetric inclusion process on hypercubes**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Determines when a pair-separation relaxation mode is strictly slower than every one-particle mode, at finite diffusivity. Provides a dimension-dependent crossover boundary and its scaling. Published monotonicity then excludes one-particle reduction of the full conservative SIP below the threshold, while its all-k gap above the threshold remains undetermined.

## Original question

吸引粒子与热传导模型的最慢弛豫，是否永远只需两粒子信息？

## Frozen scientific scope

For the conservative SIP with exactly two particles on the D-dimensional Boolean hypercube Q_D, every finite integer D>=1, homogeneous site weight a>0 and common edge conductance c>0, lambda_2=c*min(2a,rho_D(a)), where rho_D(a) is the smallest positive eigenvalue of the D+1-state birth-death negative generator with downward rates 2*d*a+2*1_{d=1} and upward rates 2*(D-d)*a. The one-particle gap is 2*c*a. With a_D=(D-1)*2^{-(D-1)}*integral_0^1(1+u^2)^{D-1}du-1, lambda_2<lambda_1 iff 0<a<a_D for D>=4; for D<=3 lambda_2=lambda_1 for all a>0. The threshold satisfies a_4=1/35, a_(D+1)=(D^2*a_D+1)/((D-1)*(2D+1)) for D>=2, and D^2*a_D tends to 1. No k>=3 identity is claimed.

## Proposed contribution and limitations

Exact full two-particle gap reduction for every homogeneous hypercube Q_D and every finite positive a to a D+1-state distance chain, including rigorous bounds on omitted sectors. An exact finite-a crossover formula, a_4=1/35, an all-D recurrence and D^2*a_D->1 are obtained.

Primary current versions, relevant journal sections, the 2024 institutional published PDF and bounded hypercube/Hamming/1-over-35 searches checked on 2026-10-12, before and during research. The inspected texts and searches did not yield this formula. No exhaustive global priority claim; novelty and significance require a fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
