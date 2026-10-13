# phys-smallmac00008-p01

**Comment on “Distinguishing graph states by the properties of their marginals”**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `28`
- Original internal ID: `phys-smallmac00008-p01`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

图态凝聚：内部顶点各接至多一个外部顶点，是否足以保留局部Clifford等价？

## Frozen scientific claim

原始固定标签双端外度≤1的Boolean OR凝聚保持LC等价的全称命题为假。完整证书：V={1,…,6}，C={1,2,3}，E(G)={13,16,24,35,46}，E(G′)={13,15,24,36,46,56}；G′=τ5τ1τ3G，两端连通且C外度均(1,1,1)、r_C=3。凝聚后B={4,5}对{6,c}的切割矩阵分别\[\[1,1\],\[0,1\]\]与\[\[1,1\],\[1,1\]\]，GF(2)秩2与1，边缘谱(1/4×4)与(1/2×2,0×2)，因此不LU等价，特别不LC等价。此反例允许C不连通；不主张无标签版本、C连通修正版或最小性。

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

- `supplement/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
