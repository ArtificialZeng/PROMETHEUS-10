# Author handoff

## Local status

This is a local `draft_ready_author_review_required` package for a fresh
release audit.  It has not been submitted, peer reviewed, accepted, or
approved by the named author.  The accepted science snapshot remains the
exact resolution-paper claim reviewed in `audit/science.md`.

## Core result and scope

For the dimensionless magnetic Laplacian
`(-i nabla - b(-y,x)/2)^2` on every concentric annulus `{a<r<1}`, with
`0<a<1`, `b>0`, no independently added harmonic Aharonov--Bohm flux, and the
same boundary type on both circles, the globally ordered spectra counted with
multiplicity satisfy

`mu_3(A_a,b) <= lambda_1(A_a,b)`.

The claim is exact and full-scope for that frozen model.  It does not cover
nonconcentric holes, other boundary conditions, nonuniform fields, an added
harmonic flux, many-body physics, or experiment.

## Hardest checks for the author

1. Recheck the small-field derivative factorization in equations (8)--(10),
   including the sign transfer from `H'''<0` through three integrations and
   the `c=1` endpoint.
2. Recheck that the high-field integer-window dichotomy is exhaustive and
   that both complement branches preserve strict inequalities at `a=1/4`,
   `b=6`, and integer-window endpoints.
3. Verify the logarithmic-mean estimate and the transverse width bound in the
   thin-ring branch, including all normalization factors.
4. Confirm from the primary source that the homogeneous-field Dirichlet disk
   ground is radial; this is the only source premise used in the Barta step.
5. Repeat the literature search before any submission.  The existing novelty
   screen is bounded and is not a priority guarantee.

## Source map

| Manuscript content | Bound project sources |
| --- | --- |
| Frozen model, units, gauge, boundary data, multiplicity | `problem.md`, `physics.json`, `claim.json` |
| Primary disk baseline and radiality premise | `source-ledger.json`, `literature/lotoreichik-2025-published.pdf`, `evidence/baseline.log` |
| Exact universal proof | `evidence/universal-annulus-ordering-proof.md` |
| Independent symbolic/rational checks | `scripts/check_universal_annulus_ordering.py`, `evidence/universal-annulus-ordering-check.log` |
| Fresh scientific review | `audit/science.json`, `audit/science.md`, `audit/replay.log` |
| Bounded novelty comparison | `evidence/universal-annulus-prior-comparison.md`, `evidence/triage-readiness.md` |
| Journal aims and current AI policy | `venue.json`, `venue/aims-and-policy.md` |
| Article and build | `manuscript/main.tex`, `manuscript/Fig1.tex`, `manuscript/references.bib`, `build-release/main.pdf` |

## AI involvement and policy caveat

Generative AI contributed to literature triage, proof-strategy exploration,
code, adversarial verification, the proof-derived schematic, and drafting.
The manuscript discloses that scope and does not list AI as an author.  The
target publisher's current guidance requires human-led scholarly judgment,
verification, and accountability.  The present AI scientific audit is not a
substitute for those duties; `venue.json` therefore records
`needs_author_judgment`.

## Pending author decisions

- Confirm the spelling, affiliation, postal address, and email currently
  shown as Xiaojian Zeng; PBC School of Finance, Tsinghua University, Beijing
  100190, China; xiaojianzeng@foxmail.com.
- Independently validate the theorem, citations, figure, and prose, and decide
  whether to take responsibility for a submitted version.
- Supply accurate funding and competing-interest declarations.  None were
  inferred in the local draft.
- Approve or revise the AI-use declaration after checking the policy again at
  the actual submission date.
- Decide whether *Letters in Mathematical Physics*, longer Research Article,
  remains the preferred target.  Fit is source-backed but acceptance and
  ranking are not claimed.

## Reproducibility and redistribution

Regeneration steps and tested versions are in
`manuscript/REPRODUCIBILITY.md`.  The handoff selection contains only authored
TeX/Bib/figure source, this handoff, the reproducibility guide, and the
accepted checker.  It excludes the downloaded primary-source PDF, runtime
jobs, audit logs, credentials, and release internals.  A fresh release worker
must still audit every citation, perform a clean build, and visually inspect
every PDF page before local activation.
