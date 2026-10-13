# phys-smallmac00016-p01

**Exact current-bit optimum and a robust history advantage for coarse-grained generalized-amplitude-damping feedback**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `43`
- Original internal ID: `phys-00016-p01`
- Claim class: **Proof**
- Original problem status: **proved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

粗粒化 GAD 反例中两步 current-bit 恢复的精确最优值是多少？

## Frozen scientific claim

For the ordered full-Choi-rank generalized-amplitude-damping qubit instrument, the incoherent 03|12 one-bit readout, two independent uses, and arbitrary clock-dependent qubit CPTP recoveries conditioned only on the current bit: (i) at p=18/25 and gamma=3/10 the exact optimum is F_2^M=289/400, attained by identity recovery, while the fixed feasible history policy attains 1831/2500 and therefore has exact advantage 99/10000; and (ii) on the closed rectangle R=\[71/100,723/1000\] x \[29/100,303/1000\], the same history policy attains H=1-gamma+p gamma^2/2 and every admissible current-bit policy obeys F_2^M<=H-1/1000, hence F_2^B-F_2^M>=1/1000 throughout R. The rectangle is a sufficient certified region, not a maximality claim, and no off-center exact optimum or exact Bayesian optimum is asserted.

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

The package includes 5 source-code file(s). Dependency declaration(s):

- `manuscript/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
