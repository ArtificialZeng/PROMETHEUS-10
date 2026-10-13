# phys-smallmac00009-p02

**Pure-state uniqueness under common-axis measurements of three qubits excludes mixed-state impostors**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `31`
- Original internal ID: `phys-smallmac00009-p02`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

三qubit均匀旋转测量：纯态唯一性是否足以排除所有混态仿冒？

## Frozen scientific claim

For every complex unit vector psi in C^8, under the complete labeled three-qubit common-axis effects E_b(n)=tensor_j(I+b_j n.sigma)/2 for all unit n and all b, uniqueness of P=|psi><psi| among pure states implies uniqueness among all complex density matrices. More strongly, every nontrivial density-matrix competitor rho with the same data has K=rho-P of rank two with eigenvalues +/-s, and P,rho share its two-dimensional range; Q=P-2Tr(PK)K/Tr(K^2) is a distinct pure competitor. This is an exact three-qubit identifiability theorem, not an all-N or finite-error certification claim. A complete proposed computer-assisted proof is submitted for fresh review.

## Result classification

This release is classified as `resolution-paper`; the original problem status is `proved`. The paper and author handoff state the scoped contribution, assumptions, physical use and remaining limitations.

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

- [manuscript/REPRODUCE.md](manuscript/REPRODUCE.md)

The package includes 2 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
