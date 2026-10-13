# phys-smallmac00010-p02

**Weak regulation increases stationary abundance noise in a three-species stochastic feedback ring**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `34`
- Original internal ID: `phys-00010-p02`
- Claim class: **Partial result**
- Original problem status: **unresolved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

三组分随机生化反馈环，是否至多一个组分能低于Poisson噪声？

## Frozen scientific claim

For the exact infinite-state three-species unit-birth feedback ring with fixed a_i,tau_i>0 and bounded nonconstant h_i:N_0->R, put f_i(n)=a_i+epsilon h_i(n). For |epsilon| H_k<=a_k/2, each stationary Fano factor obeys F_i(epsilon)-1=epsilon^2 S_i/a_i+R_i(epsilon), where S_i=integral_0^infty exp(-t/tau_i) Cov_0(h_i(Y_{i-1}(0)),h_i(Y_{i-1}(t)))dt>0, Y_{i-1} is a stationary baseline immigration-death chain, and |R_i(epsilon)|<=K_i|epsilon|^3 for the explicit finite K_i in evidence/research-pass3.md. Consequently all three F_i>1 for each fixed triple at sufficiently small nonzero epsilon. No claim is made for arbitrary coupling strength; the original conjecture remains unresolved.

## Result classification

This release is classified as `result-note`; the original problem status is `unresolved`. The paper and author handoff state the scoped contribution, assumptions, physical use and remaining limitations.

## Files

- [Frozen release PDF](paper.pdf)
- [Manuscript source](manuscript/main.tex)
- [Author handoff](AUTHOR_HANDOFF.md)
- [Release status and verification boundary](RELEASE-STATUS.md)
- `SOURCE-BUNDLE-CONTENTS.json` records the frozen release-selected inputs before portability substitutions.
- `PACKAGE-PROVENANCE.json` binds this public ID to the original internal project and release bundle.
- `ARTIFACTS.sha256` verifies every packaged artifact in this directory.

## Reproduction

Release-selected replay guide(s):

- [REPRODUCE.md](REPRODUCE.md)

The package includes 2 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
