# Author handoff

## Core claim

The complete three-state, two-harmonic local-detailed-balance model specified in the
manuscript is a computer-assisted counterexample to the heterogeneous-prefactor
multistate phase bound conjectured as Eq. (36) by Degünther, Koyuk and Seifert. The
outward-rounded certificate proves `A>0`, `B>0`, and `A-k0,min*B<0`; since
`k0,min=1`, this is a disproof on the source's required positive phase branch.

## Hardest checks already performed

- An exact periodic, normalized C1 cubic comparison path has its continuum residual
  enclosed on 2,097,152 subboxes at 256-bit Arb precision.
- An analytic Dobrushin contraction bound converts the residual into a uniform error
  bound for the unique exact periodic state.
- Exact-in-form Fourier integration with outward rounding encloses both observables.
- A 4096-segment, 320-bit replay certifies the same signs.
- A fresh referee reconstructed the source convention, obtained matching floating
  centers from independently written full-state LSODA relaxation and one-period
  integration, checked the integration-by-parts form of `A`, and reran the Arb
  certificate at a third partition and precision.

## Caveats

The work does not give a replacement bound or classify the violating region. The
literature screen was bounded and does not prove priority. The interval proof and the
source equation mapping require human line-by-line review, followed by ordinary peer
review. The author details below have not been confirmed during this automated job.

## Source map

- Model, phase, two-state theorem, and conjecture: Degünther--Koyuk--Seifert,
  arXiv:2112.02888v1, Eqs. (1)--(4), (31)--(36), Appendix B; journal DOI
  10.1088/1742-5468/ac59ad; official VOR handle `11682/18621`.
- Later conjectural status: Julius Degünther's 2024 University of Stuttgart thesis,
  Eq. (3.30) and surrounding text; handle `11682/15137`, DOI
  `10.18419/opus-15118`.
- Exact witness and proof: `evidence/counterexample-parameters.json`,
  `evidence/certify_counterexample.py`, and the two certificate JSON files.

## Target and policy

JSTAT is a plausible target for a standard research paper because its official scope
covers statistical physics and the closest predecessor appeared there. IOP's current generative-AI policy permits
disclosed assistance but requires critical author revision, checked references, and
human responsibility. Because AI assisted with reasoning, code, computation, audit,
and drafting, policy compatibility remains an author judgment. No ranking was verified
and no editorial fit or acceptance is claimed.

## AI use

OpenAI Codex using GPT-5.6 Sol (OpenAI) assisted with literature support, reasoning,
code, interval calculation, an independent AI audit, and drafting. The manuscript
discloses this. The human author must inspect and approve the disclosure and all
underlying work; no claim of completed human verification is made.

## Pending author decisions

1. Confirm name, affiliation, postal code, email, authorship eligibility, and order:
   Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190;
   xiaojianzeng@foxmail.com.
2. Perform a broader priority search and verify every bibliography entry against the
   primary record.
3. Re-run the certificate in a clean environment and audit the Dobrushin and residual
   arguments line by line.
4. Decide whether JSTAT is the intended venue and confirm its policy at submission time.
5. Confirm the four proposed JSTAT-list keywords: Stochastic thermodynamics,
   Dynamical processes, Exact results, and Stationary states.
6. Critically revise the prose and approve the final scientific and AI-use statements.

External submission is not authorized and has not occurred.
