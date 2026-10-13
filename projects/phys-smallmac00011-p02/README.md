# phys-smallmac00011-p02

**Directional stability of the reverse-depolarizing entanglement-assistance benchmark for qubit entanglement-breaking channels**

- Series: `small_mac`
- Display number in PROMETHEUS-10: `35`
- Original internal ID: `phys-00011-p02`
- Claim class: **Partial result**
- Original problem status: **unresolved**
- Release status: `draft_ready_author_review_required`

## Original topic (Chinese source text)

完全破坏纠缠的 qubit 信道，预共享纠缠的容量增益是否仍不超过已知反向去极化基准？

## Frozen scientific claim

Let D be the reverse-depolarizing qubit channel D_(4/3), and let Psi be any fixed qubit entanglement-breaking channel. For Phi_e=(1-e)D+e Psi as e decreases to zero through positive values, put c=<Omega|J_Psi/2|Omega>. If c>0, then K_* chi(Phi_e)-C_E(Phi_e)=c e log2(1/e)+O_Psi(e). If c=0, Psi has Bloch action r -> -Q r with Q positive semidefinite and trace one, and the gap is \[K_*/2\](lambda_max(Q)-1/3)e+O_Psi(e^2). The gap is strictly positive for all sufficiently small e>0 whenever Psi differs from D; if Psi=D, equality holds identically. All capacities are fully optimized and C=chi for these EB maps.

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

- [manuscript/reproducibility/README.md](manuscript/reproducibility/README.md)

The package includes 1 source-code file(s). Dependency declaration(s):

- `manuscript/reproducibility/requirements.txt`

No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.

This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.
