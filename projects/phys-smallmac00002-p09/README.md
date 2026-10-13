# phys-smallmac00002-p09

**A counterexample to the forward waiting-time entropy bound in periodically driven Markov networks**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `16`
- Original internal ID: `phys-smallmac00002-p09`
- Claim class: **Disproof**
- Original problem status: **disproved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

周期驱动中，正向相位平均等待时间是否仍给熵产生下界？

## Frozen scientific claim

Counterexample to the universal upper bound hat_sigma_Psi<=bar_sigma exactly as quantified in immutable source.md and problem.md. On the complete three-state graph, observe only 1->2 and 2->1; take symmetric edge triples (k12,k23,k31)=(r,1,1),(1,r,1),(1,1,r)/t_star in consecutive segments of length t_star, with r>0,r!=1. The unique periodic distribution is uniform and bar_sigma=0, whereas the finite same-forward-protocol waiting estimator is strictly positive. The same-direction waiting-density difference has dimensionless x^3 coefficient -(r-1)^2/\[6(r+2)\]. For r=10, t_star*hat_sigma_Psi>=27/5734400000000000000000000000000000>0, with normalized joint waiting laws and controlled infinite logarithmic tail. This resolves the original conjunction by violating its upper half; no separate universal lower-bound theorem, smooth/fixed-prefactor claim, controller-cost claim, or independent acceptance is included.

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

The package includes 8 source-code file(s). Dependency declaration(s):

- `reproducibility/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
