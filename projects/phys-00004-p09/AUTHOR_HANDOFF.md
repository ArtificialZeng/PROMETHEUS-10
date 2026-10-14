# Author handoff

Status: local draft ready for fresh release review; human scientific review and authorship approval are required. No external submission is authorized.

## Core accepted result

For every strictly positive normalized binary probability table with `det(sqrt(P)) != 0`, consider the canonical two-copy purification with the fixed split `R=S=C^4` and an auxiliary path `U(t)=exp(i t H)`. Generic nongauge generators open new Schmidt weights and have a positive `t^2 log(1/t^2)` entropy term. On the 112-real-dimensional exceptional space where that first null-to-null block vanishes, the exact `t^2` form is nonnegative; its kernel is precisely the 31-dimensional local auxiliary-unitary gauge, so the 81-dimensional quotient is positive definite. Hence every fixed nongauge exponential path initially increases entropy.

The original all-auxiliary, global two-copy additivity question remains unresolved. The draft makes no common-neighborhood, finite-distance, boundary/product-table, larger-split, global lower-bound, preparation-rate, or experimental claim.

## Hardest checks and source map

- Accepted statement and scope: `claim.json`; independent AI referee report: `audit/science.md`.
- Stable analytic derivation: `evidence/research/pass2-8ac137aacbe0/quadratic-form.md`; generic singular-spectrum obstruction: `evidence/research/pass1-ed42e17e0d25/tangent-obstruction.md`.
- Exact phase identity: `check_phase_identity.py`, `symbolic-phase-identity.json`, and its log in the pass-2 evidence directory. All 45 polynomial coefficients vanish exactly after reversible denominator clearing.
- Independent referee replay and limitations: `audit/referee-6429b9ba42dc/independent-derivation.md` and `audit/referee-6429b9ba42dc/replay.log`.
- Current literature boundary: `evidence/write/2dc1f140ec42/literature-recheck.md`. The 2026 Werner-state paper resolves general von Neumann nonadditivity in a different state family but explicitly leaves the locally classical question open.
- Reproduction commands and exact package versions: `reproducibility/README.md` and `reproducibility/requirements.txt`.

## Manuscript and build

Primary sources are `manuscript/main.tex` and `manuscript/references.bib`; the clean local output is `build-clean/main.pdf`. The manuscript is self-contained, labels the fixed split and pathwise nature in the theorem, discloses AI involvement, and distinguishes exact proof from floating diagnostics. The build has resolved references and citations and no logged LaTeX warnings. A fresh release worker must still audit every citation, the build log, journal policy, dependency list, and every rendered page.

## Decisions required from Xiaojian Zeng

1. Independently verify the theorem, proof, code, literature comparison, and interpretation; obtain expert review where appropriate.
2. Confirm the displayed name, email, and PBC School of Finance, Tsinghua University affiliation and postal code; their presence in the draft is not institutional endorsement.
3. Supply or confirm funding, competing-interests, data/code, and author-contribution declarations.
4. Decide whether the scientific contribution and article type are suitable for Quantum Information Processing or another venue.
5. Review the current Springer Nature AI policy. Because AI contributed to claims, derivations, checks, and drafting before human oversight, `venue.json` records `needs_author_judgment`; disclosure alone is not a compliance determination.
6. Approve, substantially revise, or withhold the manuscript. Do not submit the present local draft merely because automated and AI-referee gates passed.

## Rights and redistribution

The proposed handoff bundle contains authored TeX/Bib, this handoff, venue/reproducibility notes, and project-generated scripts and outputs. It excludes downloaded third-party PDFs/full texts, credentials, job logs, audit runtime trees, and mutable handoff state. Citation URLs do not redistribute the cited works. Rights and licensing remain for the human author to confirm before public distribution.
