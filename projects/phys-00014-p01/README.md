# phys-00014-p01

**Exact single-use Bayesian Nagaoka–Hayashi attainment for noisy qubit rotations**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

A fixed single-qubit pre-rotation followed by a Bell measurement achieves the ultimate three-axis Bayesian mean-square precision for one noisy channel use. Only the posterior estimator shrinks with known noise, so the measurement needs no noise-dependent redesign. The finite Bayesian incompatibility penalty relative to the reproduced SLD value is 8B Q^2/(A+B) for lambda<1.

## Original question

带退极化噪声的三参数旋转估计，Bayesian Nagaoka–Hayashi 下界能否精确实现？

## Frozen scientific scope

For k=1 in the frozen fixed-Bell-probe model U_theta=exp(-i theta dot sigma) followed by known depolarization 0<=lambda<=1, with uniform Cartesian-volume prior on ||theta||<=pi/4 and R=E[||hat theta-theta||^2]/3, the optimum over all system-ancilla physical POVMs and finite-second-moment estimators equals the source Bayesian Nagaoka-Hayashi SDP: R_1(lambda)=C_NH(1,lambda)=pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2. It is attained by four orthonormal vectors (|0>-i sum_i s_ji|i>)/2 in the source spin basis, for tetrahedral signs s=(+++),(+--),(-+-),(--+), with posterior estimates 2(1-lambda)(3/(2pi)-12/pi^3)s. Equivalently, one fixed local pre-rotation followed by a Bell measurement implements this PVM. A normalized covariant sphere measurement also attains it. Exact continuum physical-risk and NH PSD dual certificates establish the all-noise equality, including endpoints. No claim for k=2,3,4 or optimized/adaptive probes; the frozen original remains unresolved.

## Proposed contribution and limitations

Exact k=1 fixed-Bell attainment for the full continuum 0<=lambda<=1 under the specified pi/4 volume prior: closed optimal risk pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2; four-outcome noise-independent rotated-Bell projective measurement; exact posterior estimates; distinct all-estimate physical-risk and NH SDP dual certificates. The original k=1,2,3,4 question remains unresolved.

2026-10-12 21:10-21:19 UTC: current 2607.15398 v1 and 2511.16645 v4 metadata/bodies; selected current author fulltext 2008.02612v2 and previous exact-scope Suzuki/Zhao/Andre source records. Exact identifier/title, Bayesian NH exact/proof/attainment, depolarization/SU(2), tetrahedral/simplex, Hadamard/projective, phase-imaging/N00N queries. No verified later exact resolution found. Bounded coverage is not a proof of priority; Nature publisher redirect failure and incomplete old-method appendices are disclosed. Fresh referee must assess novelty/significance. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](manuscript/REPRODUCE.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
