# phys-smallmac00007-p01

**Common output bias matters in randomness certification from quantum speed limits**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `26`
- Original internal ID: `phys-smallmac00007-p01`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

量子速度极限的随机性认证：固定相关差，输出共同偏置是否真的无关？

## Frozen scientific claim

In the exact average branch-speed-budget relaxation defined in source.md and problem.md, take e=1/2, C_off=(sin(3/5),-sin(2/5)), and d=(sin(3/5)+sin(2/5))/2. Both C_off and (d,-d) lie in Q_(1/2). The submitted computer-assisted proof gives H*(C_off,1/2)>0.7758 bits and H*((d,-d),1/2)<0.7653 bits, so their difference exceeds 0.0105 bits. This counterexample disproves the original universal common-bias equality. It does not refute the proven midpoint lower-bound lemma or assert an optimal physical attack under a true total-state-variance constraint.

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

- [supplement/README.md](supplement/README.md)

The package includes 5 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
