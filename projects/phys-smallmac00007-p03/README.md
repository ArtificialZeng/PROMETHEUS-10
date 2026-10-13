# phys-smallmac00007-p03

**A two-pineapple envelope for split-core threshold random walks**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `27`
- Original internal ID: `phys-smallmac00007-p03`
- Claim class: **Partial result**
- Original problem status: **unresolved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

阈值输运网络中，单核心菠萝结构是否已经最慢？

## Frozen scientific claim

For every positive integer s,q,t, put n=s+t+q+3. In the frozen non-lazy threshold-graph random-walk model, each construction code 01 0^t 1^s 0^q 1 and 0 1^s 0^t 1 0^q 1 has Kemeny's constant strictly less than max{F_n(s+1),F_n(s+t+1)}, and hence strictly less than or equal to the global pineapple bound B_n. The original conjecture for all legal threshold codes remains unresolved.

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

- [manuscript/REPRODUCIBILITY.md](manuscript/REPRODUCIBILITY.md)

The package includes 2 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
