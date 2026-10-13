# Author handoff

## Core claim

For the fixed full-Choi-rank GAD channel with `p=18/25`, `gamma=3/10`, and coarse
pairing `03|12`, every arbitrary-qubit-CPTP two-use current-bit controller obeys
`F_2^M <= 456/625`. The displayed retained-history unitary policy attains
`1831/2500`, so `Delta_2 >= 7/2500 > 0`. Since the policy classes coincide at one
use, the earliest possible depth is `n_*=2`.

## Hardest checks

- Exact full-rank/CPTP verification of the ordered GAD Kraus tuple.
- Hermitian trace-norm contractivity for arbitrary CPTP recovery, applied only after
  each hidden pair has been incoherently summed into the observed operation.
- Exact current-bit factorisation `Phi_2^M=C_2 o C_1`, the nonunital qubit formula
  `F_e=(1+Tr(T_2 T_1))/4`, and the Frobenius bound.
- Agreement of all-hidden-path and coarse-Liouville calculations for `1831/2500`.

## Caveats requiring author attention

The proof does not determine either exact optimum, the maximal advantage over all
instruments, any robustness radius, or an `n>2` optimum. The novelty screen is
bounded; broaden the partially observed quantum-control and citing/later-version
search before submission. Confirm the title, affiliation, address, email, funding,
competing interests, and journal choice. The current author details are user-supplied
draft metadata and do not imply institutional endorsement.

## AI involvement

OpenAI `gpt-5.6-sol` assisted topic formulation, literature discovery, scientific
derivation, code generation, verification, and drafting on 13--14 September 2026.
The manuscript includes an accurate declaration. A fresh model context accepted the
frozen scientific scope, but that is not external peer review. The named author must
independently inspect the proof, code, citations, wording, and journal policy before
assuming accountability or submitting.

## Source map

- Model and quantifiers: `problem.md`, `physics.json`
- Exact proof and input: `evidence/gad-global-bound.md`,
  `evidence/gad-global-input.json`
- Reproducible verifier: `scripts/verify_gad_global_bound.py`
- Independent audit: `audit/science.md`, `audit/independent_replay.py`
- Closest-source comparison: `evidence/prior-comparison.md`,
  `literature/arxiv-2402.18941v1-source-record.md`, and
  `literature/arxiv-quant-ph-0403092v1-source-record.md`
- Venue scope and policy: `venue/aims-and-policy.md`

## Target fit and status

The provisional target is a Regular Article in *Quantum Information Processing*.
Official scope and policy links are recorded in `venue/aims-and-policy.md`; ranking
was not verified. This package is a local draft for author review. No external
submission is authorised or claimed.
