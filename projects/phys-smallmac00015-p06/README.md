# phys-smallmac00015-p06

**A two-use history advantage under one-bit coarse-grained environment feedback**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `42`
- Original internal ID: `phys-00015-p06`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

把四个环境结果粗粒化成两个时，qubit 历史反馈首次何时有增益？

## Frozen scientific claim

In the model and policy classes fixed by problem.md, the earliest use count at which retained coarse environment-bit history can outperform every current-bit-only qubit controller is n_*=2. Specifically, for the full-Choi-rank generalized-amplitude-damping channel with p=18/25, gamma=3/10, the displayed ordered minimal Kraus representation, and balanced readout 03|12, every arbitrary-CPTP n=2 Markov policy satisfies F_2^M<=456/625, while an explicit full-history policy attains 1831/2500. Therefore Delta_2>=7/2500>0; at n=1 the two policy classes coincide.

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

- [REPRODUCIBILITY.md](REPRODUCIBILITY.md)

The package includes 1 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
