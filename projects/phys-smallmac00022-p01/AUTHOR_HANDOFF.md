# Author handoff — local result-note draft

This package is a local draft for scientific and authorship review.  It has
not been submitted externally, and no venue acceptance or ranking is claimed.

## Core accepted claim

For the diagonal state `rho_r` at exact `r=1/2`, base-2 von Neumann order,
and the fixed minimal ancillary split `(d_A',d_B')=(4,4)`, the
product-canonical two-copy purification is a strict local minimum modulo the
local ancillary `U(4) x U(4)` orbit over the full complex `U(16)` flag
manifold, including support-opening directions.

The original global question remains unresolved.  The draft proves no global
minimum in `U(16)`, no statement for larger ancillas or other `r`, and no
additivity result.

## Hardest checks already represented in the dossier

1. The complete 256-real-dimensional tangent splits exactly into a
   112-dimensional first-order fixed-rank kernel and 144 support-opening
   directions.  The ancillary orbit has dimension 31, leaving an exact
   81-dimensional quotient basis.
2. `evidence/certify_u16_hessian.py` evaluates the analytic entropy Hessian
   with 320-bit Arb balls and certifies all 81 interval LDL pivots of
   `H-(159/1000)I` as positive.  The binary64 eigenvalue is diagnostic only.
3. The opening map has exact least squared scale `5/338`.  The proof uses a
   Schur complement, rank-four approximation bound, local slice coordinates,
   and the `-tau log_2(tau)` tail to control mixed rank-opening paths uniformly.
4. A fresh AI referee independently reconstructed the tangent dimensions,
   gauge quotient, source baseline, finite-difference Hessian, and opening
   scale, then replayed the interval certificate.  This is not external peer
   review and does not replace human verification.

## Source map

| Manuscript content | Primary supporting files |
| --- | --- |
| Model, one-copy spectrum, prior result | `problem.md`, `reproduction.json`, bound arXiv v1 PDF in `intake-evidence/primary-sources/` |
| Tangent and gauge classification | `evidence/u16-tangent-derivation.md`, `evidence/analyze_u16_tangent.py` |
| Interval Hessian theorem | `evidence/u16-local-minimum-proof.md`, `evidence/certify_u16_hessian.py`, `evidence/u16-hessian-certificate.log` |
| Precision and path diagnostics | `evidence/u16-hessian-precision-replay.log`, `evidence/u16-high-precision.log` |
| Accepted scientific scope | `claim.json`, `audit/science.md` |
| Venue scope and AI policy | `venue/aims-and-policy.md`, `venue.json` |

The downloaded third-party source PDF is evidence only and is deliberately
excluded from the handoff submission file list.

## Target fit

The proposed venue is *Quantum Information Processing*, Regular Article.  Its
official scope explicitly covers theoretical quantum information and
entanglement.  A Regular Article is a more honest fit than a Letter for this
single-parameter, dimension-specific result.  This is a topical match, not an
acceptance recommendation.  Ranking and indexing were not verified.

## AI use and policy boundary

AI contributed substantively to the research question, derivations, code,
literature checks, calculations, verification, AI referee replay, and writing.
The manuscript discloses that role and does not list AI as an author.  Current
Springer Nature policy requires human-led judgment, verification, and
accountability.  The venue status is therefore `needs_author_judgment` until
the named author conducts an independent review and approves the paper and
declaration.

## Decisions and reviews still required from the author

- Confirm the name, affiliation, postal address, and email on the title page.
- Independently check the theorem, especially the spectral Hessian formula,
  interval LDL logic, slice-coordinate step, and logarithmic tail inequality.
- Run or commission an independent code and citation review; the AI referee is
  not peer review.
- Decide whether the local contribution is significant enough for the target
  venue and whether broader literature searching is needed given the recency
  of arXiv:2608.28897v1.
- Complete author-contribution, funding, and competing-interest declarations.
- Approve or revise the AI declaration under the policy current on the actual
  submission date.
- Decide where to deposit code/data and provide a permanent identifier.
- Approve all submission files and any external submission.  None is
  authorized or performed by this job.

## Build and reproduction

Follow `manuscript/README.md`.  The expected draft is `build/main.pdf` and the
compiler record is `build/main.log`.  The rigorous run must end with
`certificate=PASS`; floating-point diagnostic agreement is not a substitute.
