# phys-smallmac00005-p01

**Three-copy universal qubit purification under complete stabilizer preservation**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `20`
- Original internal ID: `phys-smallmac00005-p01`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

三份未知噪声qubit：完全稳定子保持操作能否提高普适提纯保真度？

## Frozen scientific claim

For a normalized-Haar pure qubit psi and three copies independently subjected to D_delta(X)=(1-delta)X+(delta/2)Tr(X)I, every completely positive trace-nonincreasing map E:M8->M2 that, tensored with any finite qubit identity, preserves the stabilizer positive cone has success-weighted conditional Haar fidelity F_delta(E)<=1-delta/2 whenever its average success is s>0. For every 0<delta<1 and every 0<s<=1, E_s=s Tr_(two inputs) is admissible and attains equality. Therefore the maximum in the unchanged source.md is exactly 1-delta/2 throughout its full stated domain. This three-input proof candidate does not assert the source paper's broader arbitrary-copy conjecture.

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

- [supplement/README.md](supplement/README.md)

The package includes 9 source-code file(s). Dependency declaration(s):

- `supplement/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
