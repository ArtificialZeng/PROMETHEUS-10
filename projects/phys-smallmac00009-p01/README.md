# phys-smallmac00009-p01

**Unique spanning-tree families bound the static response of every complete four-state Markov network**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `30`
- Original internal ID: `phys-smallmac00009-p01`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

四态反应网络的稳态灵敏度，是否落在唯一生成树家族的凸包内？

## Frozen scientific claim

For every strictly positive finite set of twelve directed rates k on K4 with sum k=1 and every d in \[-1,1\]^12 in the original column-generator model, r_j=partial_lambda log pi_j|0 lies in the convex hull of v^alpha_j=G^alpha_j-sum_l pi_l G^alpha_l over exactly the families unique under the full directed-edge multiplicity vector. More strongly, the 4x12 rooted-tree edge-marginal matrix H(k) is a convex combination of the unique-family incidence matrices with nonnegative normalized weights depending on k only. Proof: research/proof.md and the complete 93-coefficient exact certificate. This resolves only the full K4 source claim, not the general-graph conjecture, full-hull attainability or full-tree coupling.

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

The package includes 4 source-code file(s). Dependency declaration(s):

- See the linked replay guide for standard-library or system-tool requirements.

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
