# Author handoff: restricted hypercube relaxation result

This is a local draft for author review. A fresh release reviewer has checked
the four cited primary records, rebuilt from empty auxiliaries, and viewed
all seven final PDF pages. Supervisor release activation is still pending;
no external submission or publication has occurred. The scientific workflow accepted
the frozen result-note scope; that AI-assisted review is not external peer
review or human scientific verification.

## Core claim and boundaries

For conservative SIP with exactly two particles on every finite Boolean
hypercube Q_D, homogeneous dimensionless a>0 and common edge conductance
c>0, lambda2=c min(2a,rho_D(a)). The distance-chain rates are
downward 2da+2 1_{d=1} and upward 2(D-d)a. The exact threshold is
(D-1)2^{-(D-1)} integral_0^1(1+u^2)^{D-1}du-1. A slower two-particle
separation mode occurs precisely below it for D>=4; a4=1/35, the stated
recurrence holds for D>=2, and D^2 a_D tends to one.

The original all-graph/all-positive-alpha/all-k lambda_k=lambda2 conjecture
remains unresolved. No result at k>=3, heterogeneous cube, different edge
weights, reservoirs, experimental data or thermodynamic phase transition
has been derived. Prior one-particle failure and prior two-particle
relative-coordinate methods are explicitly credited.

## Hardest checks for the human author

1. Verify translation-character exhaustion and the unordered-pair swap
   condition; pay particular attention to stack versus distinct-pair weights.
2. Reconstruct the nonzero-character block bounds and the >=4a nonradial
   zero-character bound in the actual reversible norm. Radial lumping by
   itself does not prove the full gap.
3. Check the rank-one determinant sign, cube diagonal resolvent, and the
   integration-by-parts threshold. The D=4 polynomial convention is
   det(lambda I-T), whereas the general comparison uses det(T-2a I).
4. Audit the unique-crossing argument using eigenvalue simplicity and the
   large-a limit; no unproved monotonicity of rho_D(a)/a is assumed.
5. Check the recurrence and contraction proof of the threshold limit.

The stable scientific argument is evidence/hypercube-result.md. The
accepted scientific statement is claim.json and the frozen snapshot is
audit/snapshot.json. The independent reconstruction and report remain
audit/referee-derivation.md and audit/science.md. The original source.md,
scientific inputs and accepted audit bytes were preserved by the writer.

## Source map and bounded novelty

- Kim--Sau 2024: known gap comparisons and the log-concave identity;
  DOI 10.1214/24-AAP2085. No novelty is assigned to those results.
- Kim--Sau 2026: exact model/measure Eqs. (2.1)--(2.2), monotonicity
  Eq. (2.7), conjecture Eq. (1.7), directional small-diffusivity Theorem 2.3
  and prior one-particle failure; DOI 10.1007/s00220-026-05728-9,
  arXiv:2412.01489v2. Do not import the experimental HTML numbering.
- Caputo--Quattropani--Sau 2026: exchange-model resolution and distinct
  open SIP/BEP problem, Sec. 1.4.6; arXiv:2609.10450v1.
- Carinci--Giardina--Redig 2017: prior exact two-particle relative-coordinate
  method on the line; arXiv:1711.11283v2.

Current primary versions and later-resolution screens were rechecked
before drafting; evidence/write-literature-assessment.md indexes actual
raw returns. No matching full-gap finite-a all-D hypercube formula was
located in the bounded search. Global priority is unproved. Human literature
review and, if appropriate, consultation with specialists remain advisable.

## Venue and author decisions

Proposed target: Journal of Statistical Physics, Original Paper. Its
current aims and actual nearby SIP article support the assessed scope;
see venue.json and venue/aims-and-policy.md. Ranking/indexing are unverified.
The current guidelines require disclosure beyond copy editing, prohibit
LLM authorship and require actual human accountability and final agreement.
venue.json therefore records needs_author_judgment and pending approval.

The user-supplied draft name, affiliation and email were used:
Xiaojian Zeng; PBC School of Finance, Tsinghua University, Beijing 100190,
China; xiaojianzeng@foxmail.com. Please confirm these details and authorship.
No institutional endorsement or ORCID was inferred. The author must supply
truthful funding and competing-interest statements, choose any repository
and code license, approve the AI declaration, and decide whether this
contribution and venue are appropriate. No no-funding/no-conflict assertion
has been invented. The current pending-review sentence in the AI disclosure
must be updated only after actual human review and approval.

## AI use, reproducibility and local release

OpenAI Codex was involved in exploration, analytic derivations, code,
symbolic/numerical checks, literature comparison and writing. Separate
AI-assisted reconstruction is documented; it does not erase possible shared
errors or constitute external review. The draft accurately discloses this
scope and does not say the human author verified the work.

See reproducibility/README.md for actual environment, disposable-copy
replay, the exact central checker, baselines, figure generation and a clean
LaTeX build. The figure uses 80-digit illustrative eigenvalues and exact
rational thresholds, with observed precision/comparison checks. Numeric
plots are not scientific certificates.

The submission list was checked to exclude full third-party papers,
raw web retrievals, logs, audit material and mutable checkpoint/state files.
No final distribution license or external submission is authorized here.
Fresh release review used build/release-clean/main.pdf and its actual final
compiler/BibTeX logs, dependency recorder and seven rendered page images.
The hash-bound citation, build and visual reports are audit/citations.md,
audit/build.md and audit/visual.md in the local dossier. Workflow records
mentioned here are intentionally excluded from the submission archive;
the manuscript and included stable proof are self-contained. The supervisor
must pass the final release gate before local activation and then make/check
the selected-file bundle. Only a local author-review draft is authorized.

One next test: after the supervisor's final gate and local activation, verify
the handoff bundle hashes, then perform actual human scientific, authorship
and policy review before considering any external submission.
