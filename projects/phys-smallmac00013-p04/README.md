# phys-smallmac00013-p04

**An exact criterion for removing an elementary amplitude-damping factor from a quantum channel**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `46`
- Original internal ID: `phys-00013-p04`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

相位协变 qutrit 的 elementary 右除必要条件是否充分

## Frozen scientific claim

For every phase-covariant CPTP map Phi:M3->M3 with H=diag(0,1,2), Choi rank 2 through 8, and every ordered pair of distinct energy levels (a,b), condition (N) implies the existence of lambda in (0,1) and a CPTP Theta such that Phi=Theta composed with Psi_{lambda,a->b}. In fact, for any finite-dimensional CPTP Phi and orthogonal x,y, (N) is necessary and sufficient for such an elementary right quotient; if ZV=VA for a linearly independent minimal Kraus synthesis V, the quotient is CP exactly when 0<=lambda<1 and lambda<=||A||_2^{-2}.

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

- [manuscript/README.md](manuscript/README.md)

The package includes 4 source-code file(s). Dependency declaration(s):

- `manuscript/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
