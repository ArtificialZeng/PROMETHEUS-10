# Author handoff — qutrit unistochastic monoid draft

Status: local draft for author review; no external submission is authorized.

## Core claim

For every `U,V in U(3)` there is `W in U(3)` with
`B(W)=B(V)B(U)`, where `B(U)_ij=|U_ij|^2`. Equivalently, order-three
unistochastic matrices form a monoid. In the fixed complete-dephasing qutrit
model this gives equality of the full two-step channel and one-step channel
for every input and every finite reference extension.

## Hardest checks already performed

- `audit/science.md` records a fresh accepted reconstruction of the exterior
  certificate, CKM chord, concavity form, compactness extension, and physical
  channel scope.
- `evidence/exterior-triangle-orthostochastic-proof.md` and
  `code/exterior_triangle_orthostochastic.py` give the exact endpoint lemma.
- `evidence/qutrit-unistochastic-monoid-proof.md` and
  `code/exact_qutrit_monoid_proof.py` give the exact full proof and algebraic
  audit.
- `venue/successor-search.md` updates the bounded primary-source comparison
  through 2026-09-13. Search non-detection is not a priority guarantee.

## Scientific caveats

- The result is exactly dimension three. It does not extend to dimension
  four, where arbitrary product closure fails.
- The channel statement requires complete dephasing in one fixed basis before
  and after each unitary and discards the intermediate record.
- It does not assert `W=VU`, one-Hamiltonian implementation, bounded control
  cost, retained-record equivalence, an ancillary realization, or an
  experimental demonstration.
- Exact scripts audit identities and examples; the universal result rests on
  the analytic proof.

## Target and policy fit

`venue.json` selects Journal of Mathematical Physics, Research Article. Its
current scope and AIP AI policy are documented in
`venue/aims-and-policy.md`. The use is compatible in principle only with a
detailed disclosure and actual critical human review. The draft includes the
disclosure and does not claim the review has occurred.

## AI involvement

OpenAI Codex was used in topic/literature triage, proof exploration,
symbolic-check code, computational verification, source comparison, and
manuscript drafting. The author must verify the theorem, code, every citation,
the novelty description, and the disclosure wording. AI is not an author.

## Pending author decisions before any submission

1. Confirm the author name, email, PBC School of Finance affiliation, postal
   form, and institutional permission to use the affiliation.
2. Perform and document a genuine scientific review of the proof and exact
   scripts; revise or withdraw any statement that does not survive it.
3. Confirm the target journal and article type, and rerun the successor search
   if time has passed.
4. Supply the conflict-of-interest, funding/acknowledgment, and CRediT author
   contribution declarations.
5. Confirm the AIP AI disclosure with the exact product/model information
   available at submission time.
6. Choose licenses and a repository for code/data if they will be public, and
   verify supplementary-file and redistribution requirements.
7. Approve any external submission explicitly; none has been attempted.

## Source map

- Scientific question and domain: `problem.md`, `physics.json`
- Primary-source reconstruction: `source-ledger.json`, `reproduction.json`
- Accepted proof packet: `claim.json`, `verification.json`, the two proof
  files under `evidence/`, and `audit/science.md`
- Manuscript: `manuscript/main.tex`, `manuscript/references.bib`
- Reproduction: `REPRODUCIBILITY.md`, `reproducibility/requirements.txt`
- Venue and current comparison: `venue.json`, `venue/aims-and-policy.md`,
  `venue/successor-search.md`
