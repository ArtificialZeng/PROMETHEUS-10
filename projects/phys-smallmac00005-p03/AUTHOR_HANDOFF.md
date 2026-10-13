# Author handoff

## Core result

The draft proves, for the spinless homogeneous-field magnetic Laplacian on the
unit disk and eigenvalues counted with multiplicity,

`mu_3(b) <= lambda_1(b)` for every `b > 0`.

The new argument covers `0 < b <= 4`: a positive Dirichlet comparison function
gives a piecewise lower bound, while two fixed trial states plus one of two exact
`b=2` crossing states give a three-dimensional Neumann trial space. The
published Pauli-counting specialization supplies `b > 4`.

## Hardest checks and source map

- Dirichlet ground-state representation and lower bound:
  `manuscript/main.tex`, Lemma 2.1; accepted derivation in
  `evidence/variational-proof.md`.
- Four trial-state identities, sign factorizations, and min--max step:
  `manuscript/main.tex`, Section 3; executable replay in
  `evidence/verify-variational-identities.py` with recorded output
  `evidence/variational-identity-check.log`.
- Imported radial-ground, exact-crossing, and high-field statements:
  Lotoreichik (2025), Section 5, DOI 10.1007/s11005-025-01901-8.
- High-field counting input: Fournais et al. (2025), Proposition 2.1,
  DOI 10.1215/00127094-2024-0029.
- Frozen scientific scope and independent AI replay:
  `claim.json`, `verification.json`, `audit/science.md`. These are internal
  review records, not substitutes for human or external peer review.

## Caveats and author decisions

The proof is only for the unit disk, constant field, spinless operator,
Dirichlet versus magnetic-Neumann realizations, and the third-versus-first
comparison. It does not extend to general convex domains, higher indices,
variable fields, Robin data, or Pauli spin coupling.

Before any submission, the named author must independently verify every proof
step and citation, repeat a broader priority search, confirm the supplied name,
affiliation, postal code, and email, provide accurate funding and competing-
interest statements, choose or confirm the target venue and article type, and
approve the AI declaration. No human approval is recorded yet.

## Venue fit and AI-use warning

`venue.json` records Letters in Mathematical Physics as a plausible research-
article target because its current scope covers mathematical physics and it
published the closest predecessor. The ranking is unverified. Current Springer
Nature guidance requires disclosure and human accountability. AI assistance here
included proof search, code, literature triage, scientific review, and drafting,
not merely copyediting, so `ai_policy_status` is `needs_author_judgment`. The
draft must not be submitted unless genuine author-led review makes the use and
disclosure compliant with the policy then in force.

## Redistribution and package contents

The proposed submission bundle contains only the original TeX/Bib draft, this
handoff, reproducibility instructions, project-generated verification code/log,
and an environment record. It deliberately excludes downloaded journal PDFs,
browser captures, internal job/audit files, and credentials. The journal asks
authors to upload LaTeX sources without subfolders; flatten filenames at actual
submission time after resolving collisions and rechecking the compiled PDF.
