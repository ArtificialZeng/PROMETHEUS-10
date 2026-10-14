# phys-00034-p01

**Replica twist entropy fails strong monotonicity under fermionic Gaussian measurements**

Result class: `disproofs`; original question: `disproved`; release: `draft_ready_author_review_required`.

## Background

Replica twist entropy cannot be used as a strong monotone to upper-bound average pure-state Gaussian resource-conversion yield. Its source diagnostic and dynamical properties are unaffected. This gives an exact operational limitation for the actual high-order two-copy observable, including fermion-parity and graded-copy constraints.

## Original question

双副本扭转熵能否作为纯态费米资源的强单调量？

## Frozen scientific scope

In the fixed-parity finite-mode graded-CAR model of problem.md, replica twist entropy at alpha=pi/4 is not a strong pure-state Gaussian monotone. The normalized even-parity N=34 state sqrt(3)/2 |00>|0000>^tensor8 + 1/2 |11>[(|0000>+|1111>)/sqrt(2)]^tensor8 followed by occupation measurement of its first mode, retaining both outcomes with probabilities 3/4 and 1/4, has exact average increase log(25836385/25165824)>0. More generally the explicit N=4m+2 flagged family has the exact all-angle formula in evidence/flagged-twist-proof.md and, at every fixed 0<alpha<pi/2 and 0<q<1, violates strong monotonicity for sufficiently large finite m with unbounded average increase as m grows.

## Proposed contribution and limitations

An exact fixed-parity fermionic family N=4m+2 has F=p^2+q^2 f(alpha)^m+2pq K_m(alpha), with explicit f and K. At alpha=pi/4, m=8,q=1/4 gives a finite N=34 two-outcome violation Delta=log(25836385/25165824)>0. For every fixed interior angle, parent P remains bounded but average measured-branch P grows linearly with m.

Current primary version records and targeted defining/proof sections rechecked 2026-10-14, including the newly identified current bridge-degree v2 and stabilizer counterexample v2/v3. Existing covariance and convolution comparisons retained. Bounded search cannot certify priority; candidate_novel is a proposer hypothesis for fresh review, not acceptance. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
