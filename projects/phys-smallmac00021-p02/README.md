# phys-smallmac00021-p02

**A unique cubic-coupling cancellation locus for collinear constant-vorticity capillary–gravity triads**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `53`
- Original internal ID: `phys-00021-p02`
- Claim class: **Partial result**
- Original problem status: **unresolved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

常涡度共振三波的涡度公式与耦合零点符号审计

## Frozen scientific claim

In the reproduced Ivanov-Martin arXiv:1911.05213v1 co-propagating cubic model, for every g>0, sigma>0 and distinct k1,k2>0 with k3=k1+k2, the unrestricted real dispersion-plus-resonance system has exactly the two common-sign frequency solutions in Eq. (3) of evidence/resonance-classification.md, related by (omega_j,gamma)->(-omega_j,-gamma). With q_j=k_j(g+sigma*k_j^2), ell=q3-q1-q2, N=ell^2-4q1q2 and D=2ell\[q3^2-(q1-q2)^2\], the selected positive-frequency sheet has the unique physical vorticity gamma=-N/sqrt(D); the companion root belongs to the genuine all-negative-frequency sheet, not an algebraic artifact. On either sheet C=\[16q1q2(q3-q1)(q3-q2)-ell^4\]/D. For every positive pair (k1,k2), exactly one positive r=g/sigma makes C=0, namely the unique positive root of Eq. (9) in the proof; at that zero gamma<0 on the positive-frequency sheet and gamma>0 on its sign-reversed companion.

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

- [reproducibility/README.md](reproducibility/README.md)

The package includes 1 source-code file(s). Dependency declaration(s):

- `reproducibility/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
