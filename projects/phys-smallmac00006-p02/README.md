# phys-smallmac00006-p02

**Coherent information in uniformly noisy graph states is not ordered by subsystem size**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `24`
- Original internal ID: `phys-smallmac00006-p02`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

均匀噪声图态中，节点较多的一侧是否总有较高的相干信息？

## Frozen scientific claim

For the exact independent uniform phase-noise graph-state model of source.md/problem.md, the connected 5x4 biadjacency matrix with rows (1001),(1001),(1001),(0101),(0011) at P=199/200 has GF(2) rank3, no zero rows/columns, n_A=5>4=n_B>=3, and -0.0043<S_A-S_B<-0.0042 bits, with I_A>2.7 and I_B>2.7 bits. This is a strict counterexample to the frozen universal node-count ordering. More generally, for every integer r>=3, Gamma_r has rows v1,v1,v1,v2,...,vr, vi=ei+e_(r+1) in F2^(r+1); it is connected of size(r+2)x(r+1), rankr, and at the same P has Delta_r<=Delta_3<-0.0042 and I_B(r)>I_A(r)>2.7. These are coherent-information lower bounds, not equalities for optimal distillable entanglement.

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

The package includes 2 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
