# phys-smallmac00001-p06

**A missing spectral arc at finite cycle affinity in four-state Markov generators**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `14`
- Original internal ID: `phys-smallmac00001-p06`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

有限热力学力下 Markov 谱集合是否等于 Karpelevich 区域的纵向缩放

## Frozen scientific claim

At B*=log(3)/2 there exists eta>0 such that every four-state generator with escape rates <=1 and both oriented cycle-product bounds product_forward<=3^n_c product_reverse obeys |Im(lambda)|<=1/2-delta/2+delta^2/4 whenever delta=-1-Re(lambda) is in (0,eta). The exact-alpha unrestricted companion supplies compressed points Lambda(delta)=-1-delta+(i/2)sqrt(1-2delta+3delta^2), all strictly above that bound for 0<delta<min(eta,1/2). Thus the affine-image equality H_eq fails by nonattainment, including the closure of the larger bounded-affinity class.

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

- [manuscript/README.md](manuscript/README.md)
- [manuscript/repro/README.md](manuscript/repro/README.md)

The package includes 3 source-code file(s). Dependency declaration(s):

- `manuscript/repro/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
