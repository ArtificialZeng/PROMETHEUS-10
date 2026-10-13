# phys-smallmac00005-p02

**A computer-assisted three-state counterexample to a nonlinear phase-lag bound**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `21`
- Original internal ID: `phys-smallmac00005-p02`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

三态非线性周期响应的相位滞后，是否受最慢跃迁前因子约束？

## Frozen scientific claim

The frozen universal complete-three-state positive-branch phase bound is false. For the exact terminating-decimal M=2 parameters in evidence/counterexample-parameters.json, the unique strictly positive periodic state satisfies A>0 and B>0, while A-k0,min B<0; specifically the primary outward-rounded certificate gives A in \[0.1913253462459419,0.8081296470533585\], B in \[6.1034541204110998,6.1582195856729802\], and A-k0,min B in \[-5.966894239630766,-5.295324473154014\].

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

- [reproducibility/README.md](reproducibility/README.md)

The package includes 1 source-code file(s). Dependency declaration(s):

- `reproducibility/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
