# Manuscript source and evidence map

The paper writes the unchanged claim accepted by the actual fresh referee
`phys-smallmac00001-p06-referee-874040fd36a6`. The accepted research snapshot is
`f63005999e452a2e783bd6c841ce25b32be7a51feaaee2cf1104376fce5a89bc`.
The current `audit/science.json` and `audit/science.md` are the operative
acceptance, rather than stale status strings in immutable research records.
The writing job did not amend that acceptance or re-freeze scientific inputs.

## Accepted contribution and mathematical locations

| Manuscript location / TeX label | Accepted evidence | Meaning and limits |
| --- | --- | --- |
| Section 1.1; `eq:affinity`, `eq:question` | `source.md`, `problem.md`, `physics.json` | Exact four-state, exact-rate, exact-B question; row/column transpose and units are explicit. |
| Section 2; `eq:cycleproducts`, Theorem 1 | `claim.json`; `evidence/research/curvature-proof.md`, statement; `audit/science.md`, Sections 2 and 5 | Exclusion in the larger compact all-cycle polynomial class. The closure need only be contained in this class. |
| Section 3; `eq:sourcebound`, Lemma 1 | `curvature-proof.md`, Section 1; `audit/science.md`, Sections 1–2; primary S2 below | Source localization and its finite-affinity equality chain force a labelled biased square. |
| Section 4; `eq:logistic`–`eq:hexp` | `curvature-proof.md`, Section 2; `audit/science.md`, Sections 3–4 | Exact coordinates; all four escape deficits and unused affinity retained; uniform Taylor remainder. |
| Section 4.1; `eq:quadratic`–`eq:Kmax` | `curvature-proof.md`, Sections 2–3; `evidence/research/local-curvature-symbolic.json`; `audit/referee-replay.json` | Homogeneous quadratic identity and negative-definite Hessian. The unconstrained maximizer is not an assertion of exact feasible attainability. |
| Section 4.2; `eq:bootstrapineq`, `eq:bootstrap` | `curvature-proof.md`, Section 3; `audit/science.md`, Section 4 | Coercivity controls arbitrary, including nonsmooth, approaches. This is the uniform scale argument, not a numerical fit. |
| Section 5.1; `eq:triangle`–`eq:localfinal` | `curvature-proof.md`, Section 4; `audit/science.md`, Section 5 | Triangle inequalities remain valid on zero-chord faces; upper coefficient 1/5 and uniform cubic remainder. |
| Sections 5.2–5.3; `eq:companion`–`eq:separation` | `curvature-proof.md`, statement and Section 5; `audit/science.md`, Sections 1 and 5; `audit/referee-replay.json` | Global compactness, exact-alpha comparator, explicit arc and positive separation polynomial. No numerical eta or fixed midpoint conclusion. |
| Appendix A; `eq:detJ` | S2 SM5; `audit/referee-replay.json`, strict Jensen determinant check | Strict positive Hessian determinant at the endpoint source parameters, used only for the accepted rigidity argument. |
| Appendix B; `eq:invariantcubic`–`eq:implicit` | `audit/referee_replay.py`, `audit/referee_fraction_check.py`; both exact result JSON files | Accepted referee's independent representations, exposed as reproducible algebra. They supplement the analytic proof and do not constitute a new central result. |

In this table, abbreviated `curvature-proof.md` means
`evidence/research/curvature-proof.md`. All project paths are local dossier
references; the original primary papers and private workflow records are not
included in the source handoff.

## Primary citations

The four entries in references.bib were transcribed from actual official
metadata and the frozen full texts, rather than inferred from titles. Current
official metadata checks are saved in `evidence/write/primary-web.json`.
The fresh release checks are recorded in `evidence/release/primary-metadata-and-policy-web.json`
and `evidence/release/primary-fulltext-and-policy-web.json`; the current citation audit
is in `audit/citations.md` in the local dossier.

| Key / source | Exact primary location used | Local frozen copy | Role |
| --- | --- | --- | --- |
| `UhlSeifert2019` / S3 | Section 4.1 condition (i); Section 4.2 | `literature/supervisor-supplement/uhl-seifert-1907.04260v1.pdf` and `.txt` | Closest existing-edge perturbation comparison; JPhysA 52, 405002 (2019), DOI 10.1088/1751-8121/ab3a7a. |
| `Xu2025` / S1 | End Matter p. 5; combined PDF p. 10, Supplementary Eqs. (S2)–(S3) | `literature/xu-et-al-v2.pdf` and `.txt` | Actual set-equality question and four-state Karpelevich polynomial; PRL 135, 257102 (2025), DOI 10.1103/z4t2-18cx. |
| `Kolchinsky2026` / S2 | Theorem 3 / Table I; SM3 Eq. (S55); SM5 Hessian; SM6 Eq. (S66) | `literature/kolchinsky-ohga-ito-v2.pdf` and `.txt` | Established localization, certifying-cycle equality chain, strictness calculation and uniform-ring baseline. Version 2, 11 June 2026; cited as a preprint. |
| `XuMeng2026` / S4 | Section II setup, Section III Corollary 3, Section V discussion | `literature/supervisor-supplement/xu-meng-2608.22934v1.pdf` and `.txt` | Unicyclic kinetic-refinement and rigidity comparison, not a proof premise. Version 1, 24 August 2026; cited as a preprint. |

Primary links: [Uhl–Seifert](https://arxiv.org/abs/1907.04260v1),
[Xu et al.](https://arxiv.org/abs/2507.08938v2),
[Kolchinsky–Ohga–Ito](https://arxiv.org/abs/2605.15884v2), and
[Xu–Meng](https://arxiv.org/abs/2608.22934v1).

S1's strict-positive stochastic wording is not used to claim all boundary
points come from a positive matrix. The paper defines its unrestricted
comparison domain and constructs the zero-diagonal companion explicitly.
S1's earlier ring-phase discrepancy is not propagated: the ring baseline is
attributed to S2 Eq. (S66). These convention issues are historical source
bookkeeping, not claimed as the new scientific result. The venue-only
Das–Green comparator in the supervisor's notes is not cited in the paper.

## Packaged exact replays

`repro/verify_symbolic.py` packages `audit/referee_replay.py`;
`repro/verify_rational.py` packages `audit/referee_fraction_check.py`.
Only the introductory documentation, output-directory CLI, JSON filenames,
workflow job/time metadata and output limitation wording were adapted.
The mathematical calculation statements were preserved. The exact old/new
hash map is in `evidence/write/replay-packaging.json`; hashes of original
files and the accepted source/audit bindings are also recorded in
`provenance.json`. Both originals remain unchanged.

The actual packaged replay outputs are in `repro/expected/`. The symbolic
route passes 19 exact checks. The standard-library rational route checks
all 28 quadratic coefficients by polarization and five linear slack
directions. The manuscript's coefficient statements are exact; numerical
parameter scans and failed searches in the historical research folder are
not proof inputs and are excluded from the handoff.

## Complete source dependency scope

The PDF depends on `main.tex`, `references.bib`, and the standard TeX
packages/style explicitly named in main.tex. There are no imported TeX
fragments, external figures, downloaded class files, or custom bibliography
styles. `build.py` stages identical copies in a new local directory; the
build record binds the copies to the authored sources. The reproducibility
scripts read no data and need only the documented Python environment.

The publication source snapshot also binds the author handoff, this source
map, provenance, reproducibility files, venue.json and every venue evidence
file. The submission-file list excludes the primary-paper cache, web-tool
captures, local audit reports, job records, and progress checkpoints.
