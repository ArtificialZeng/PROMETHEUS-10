# Author handoff

## Status

This is a local `result-note` draft ready for fresh release review and human
author review. It has not been submitted, peer reviewed, accepted, or
published. External submission is not authorized by this workflow.

## Core scientific claim

For the no-dagger three-output Bell functional `I3` in Eq. (6) of
arXiv:2606.21362v3, every tensor-product strategy of arbitrary local dimension
with three-output projective measurements satisfies `I3 <= 4`. The maximally
entangled qutrit strategy stated in that source attains 4. Equivalently, the
supplemental 35-word certificate gives an exact rank-16 noncommutative SOS for
`4*1-I3` over `Q(omega)`.

The draft does not claim equality rigidity, self-testing, robustness,
uniqueness of the optimal behavior, device-independent randomness, or the
first-family conjecture for `d>3`.

## Hardest checks

1. **Operator convention.** The article uses the no-dagger convention of the
   defining paper's main-text Eq. (6). Its appendix convention is related only
   after Bob's outcome inversion. The qutrit witness and certificate were both
   checked in the stated no-dagger convention.
2. **Exact coefficient identity.** The supplied verifier reduces every one of
   the 1,225 Gram products and compares the entire reduced-word dictionary for
   `W^dagger conjugate(Y) W = 4*1-I3`; the mismatch count is zero.
3. **Exact positivity.** Pivoted cyclotomic `LDL^dagger` arithmetic gives 16
   positive rational pivots and a 19-dimensional remainder whose entries are
   exactly zero. Floating-point optimization and eigenvalues are not accepting
   evidence.
4. **Independent audit.** A fresh referee replay used different field
   coordinates and a 70-by-70 rational realification, reproducing the exact
   identity, PSD rank, and qutrit value before accepting the bounded claim.

## Source map

- `manuscript/main.tex`: self-contained article and AI-use disclosure.
- `manuscript/references.bib`: cited-source metadata.
- `evidence/exact-sos-certificate.json`: machine-readable exact certificate.
- `evidence/verify_exact_sos_independent.py`: independent certificate replay.
- `REPRODUCIBILITY.md`: environment and exact replay/build commands.
- `audit/science.md`: accepted scientific referee report and limitations.
- `evidence/prior-comparison.md`: bounded primary-source comparison; it is not
  an absolute priority proof.
- `venue/aims-and-policy.md`: dated official-source check for journal scope and
  AI policy.

## Target fit and caveats

The provisional target is a Physical Review A Regular Article because PRA's
official scope includes foundations of quantum mechanics and quantum
information. Editorial significance and acceptance are unassessed. Ranking
was not verified. The venue and article type remain the author's decision.

The defining source is a recent 2026 preprint. The literature comparison was
bounded to the defining version and directly adjacent primary sources, so the
manuscript makes no absolute novelty or priority claim. Any later version or
new paper should be checked immediately before submission.

## AI use

OpenAI Codex (`gpt-5.6-sol`) was used substantively for literature synthesis,
scientific reasoning, exact-algebra code development and debugging, and
manuscript drafting. The system was directed to preserve the Bell-operator
convention and to require exact identity and positivity checks. An independent
implementation replayed those checks. The AI system is not an author; the
named human author remains responsible for deciding whether the work is
correct and suitable for submission. The manuscript contains a disclosure
drafted to match the APS policy checked on 2026-09-15.

## Pending human decisions

- Confirm the author name, affiliation, postal form, and email currently shown
  as Xiaojian Zeng; PBC School of Finance, Tsinghua University, Beijing 100190,
  China; `xiaojianzeng@foxmail.com`.
- Personally read the defining paper and the full manuscript, rerun the exact
  verifier, and inspect every page of the PDF.
- Recheck all citations and the defining preprint's latest version immediately
  before submission.
- Decide whether PRA and the Regular Article format are appropriate, and obtain
  any institutional or coauthor approvals that apply.
- Approve or revise the AI disclosure after checking current journal policy,
  applicable OpenAI terms, privacy, rights, and third-party permissions.
- Confirm that the two original supplemental files may be redistributed and
  select any license requested by the journal or repository.

The current clean build command and expected replay are documented in
`REPRODUCIBILITY.md`.
