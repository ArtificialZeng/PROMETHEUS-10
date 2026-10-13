# phys-smallmac00018-p01

**Exact indirect-gap boundary in a flux-one-third Harper–Hofstadter model with a period-three mass**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `44`
- Original internal ID: `phys-00018-p01`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

磁通 1/3 Harper–Hofstadter 三带模型的间接绝缘隙边界

## Frozen scientific claim

For the frozen Hamiltonian in problem.md, G1(r,m)=G2(r,m)=G(r,m). Let rc=sqrt((69-11sqrt(33))/8). For 1/2<=r<=rc, G is positive for every m except m=+/-sqrt(3)r, where G=0. For rc<r<=2 there are unique 0<m_-(r)<sqrt(3)r<m_+(r), given by the two physical branches X in (Xc,1) and X in (3/4,Xc) of equations (1)-(2) in evidence/global-boundary-certification.md with Xc=(7+sqrt(33))/16, such that G<0 exactly when m_-(r)<|m|<m_+(r), G=0 at |m|=m_-(r),m_+(r), and G>0 otherwise. Hence the relative insulating boundary consists exactly of the two direct segments m=+/-sqrt(3)r for 1/2<=r<=rc joined at their cusps to four mass-reflected indirect branches for rc<=r<=2. The extremizers are exactly those parametrized in Section 4 of that evidence file and their spectral/mass reflections; no other momentum or exceptional Laurent-factor sector occurs. The isolated-band Chern tuple is (+1,-2,+1) for |m|<sqrt(3)r and (0,0,0) for |m|>sqrt(3)r, with the nonzero tuple negated under flux/orientation reversal.

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

- [manuscript/REPRODUCIBILITY.md](manuscript/REPRODUCIBILITY.md)

The package includes 6 source-code file(s). Dependency declaration(s):

- `manuscript/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
