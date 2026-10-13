# Author handoff

## Core claim

For the fixed two-qubit XYZ GKSL generator with
`gamma=3/5`, `Delta=2/5`, and `Gamma>0`, the complete nonstationary spectral
gap obeys

```text
g(73/10) > 3/2 > 1 > g(8).
```

The independently reproduced largest positive Liouvillian exceptional point
is `Gamma_cr=8`. Therefore 8 is not a global spectral-gap maximizer. The draft
does **not** locate the global maximizer or claim that every finite-time quench
relaxes faster at 73/10.

## Hardest checks already represented in the dossier

- Two independent constructions of the 16-by-16 generator agree exactly after
  the explicit vectorization permutation.
- The source parity factors, `Gamma_cr=8`, and the size-two Jordan defects at
  `Gamma=8` were reproduced exactly.
- A parity-block Hurwitz certificate gives strict stability after the
  `3/2` shift at `Gamma=73/10`.
- A separate full-matrix recursive Routh replay gives zero shifted
  right-half-plane roots at `73/10` and two at `8`.
- A fresh scientific referee accepted only this restricted result-note scope.

## Source map

- Frozen claim and scope: `claim.json`, `problem.md`, `physics.json`.
- Primary model and baseline: `source-ledger.json`, `reproduction.json`, and
  `intake-evidence/primary-sources/phys-00020-p01-01-2412.13674v2.pdf`.
- Exact proof and data: `evidence/rational-counterexample-proof.md`,
  `evidence/rational-counterexample-certificate.json`, and
  `evidence/rational-counterexample-independent.json`.
- Independent referee reconstruction: `audit/science.md`, `audit/replay.log`.
- Bounded novelty comparison: `evidence/prior-comparison.md`,
  `audit/novelty.md`.
- Rebuild instructions: `REPRODUCIBILITY.md`.

## Venue fit and caveats

The provisional target is a Regular Article in *Physical Review A*, whose
current scope includes quantum science and fundamental concepts. The closest
model paper was published there. This is a topical-fit assessment, not a claim
of sufficient editorial significance or likely acceptance. A Regular Article
was chosen because the exact result is narrow and benefits from full
reproducibility detail; the manuscript is not framed as a Comment on the
source's distinct specified-quench result.

The priority search was bounded and cannot exclude all unindexed or later
work. The ordinary Liouvillian gap controls an asymptotic exponent but not
every finite-time relaxation metric. The correct microscopic relation is
`{sigma_z tensor sigma_z, L}=0`; parity of the dissipator, rather than a
commutator of those two operators, yields the superoperator block split.

## Pending author decisions

1. Confirm the author name, affiliation, postal code, and contact email used in
   the draft; no institutional endorsement is implied.
2. Independently check the model transcription, Routh--Hurwitz argument,
   source comparison, and every citation before approving scientific content.
3. Decide whether the result is substantial enough for the proposed venue or
   should first be strengthened by a certified global optimizer.
4. Review and approve the explicit AI-use disclosure against the policy in
   force on the actual submission date.
5. Decide whether and when to submit. No external submission has been made or
   authorized by this write job.
