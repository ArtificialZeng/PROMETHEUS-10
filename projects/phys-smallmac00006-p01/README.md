# phys-smallmac00006-p01

**Activity above one half in finite Glauber annealing**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `23`
- Original internal ID: `phys-smallmac00006-p01`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

单调降温的Glauber退火，每步跳跃概率是否始终不超过 \(1/2\)？

## Frozen scientific claim

For the layered graph A(3),B(4),C(4), complete A-B edges, a B-C matching and C clique, with E/epsilon=(0x3,1x4,64x4), q=(10001/10000,33/32,64), beta epsilon=log q, K=2 and exact Gibbs initial state, A1>63/125 and (A0+A1)/2>251/500. For all independent perturbations |delta(E_i/epsilon)|<=1/1000 with the same temperatures and a redefined Gibbs initial state, A1>1003737/2000000 and the mean>8014821/16000000, both >1/2. This admissible finite example disproves the original all-regular-graph single-step activity bound in source.md/problem.md. It also violates its two-step averaged counterpart. Both are research claims submitted for fresh review, not an accepted scientific audit.

## Result classification

This release is classified as `resolution-paper`; the original problem status is `disproved`. The paper and author handoff state the scoped contribution, assumptions, physical use and remaining limitations.

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

- [reproducibility/README.md](reproducibility/README.md)

The package includes 11 source-code file(s). Dependency declaration(s):

- `reproducibility/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
