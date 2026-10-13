# Author handoff

## Core claim

The draft proves that the exact unrestricted complex fermionic Gaussian rank of
`(|0000>+|1111>)^{tensor 2}/2` is four. The accepted scope is one finite
eight-mode target. It excludes no border-rank or approximate-rank decomposition
and makes no claim for three or more copies or asymptotic simulation complexity.

## Hardest checks

- The analytic reduction uses parity, nonzero Chevalley pairing to obtain a
  transverse pure-spinor pair, and the exhaustive 15-case `GL(8)` normal form.
  These steps deserve independent specialist inspection.
- The target flattening rank is exactly 78 (one nonzero 78-minor and 50
  independent right-null vectors).
- Eleven normal forms have all-specialization rank at most 74. Four have rank at
  least 83, including separate `a-b` and `a+b` minors for the exceptional
  `(q,i)=(0,4)` component.
- The generator and replay programs are separately implemented, but both should
  still be run by the author in a clean environment before submission.

## Source map

- Model, original conjecture, known four-term upper bound, and restricted lower
  bound: Cudby--Strelchuk, arXiv:2307.12654v4.
- Precise conventions and exclusions: `problem.md` and `physics.json`.
- Human-readable proof: `evidence/clifford-rank-gap-proof.md`.
- Exact certificate and replay: `evidence/clifford-rank-gap-certificate.json`,
  `scripts/certify_clifford_rank_gap.py`, and
  `scripts/replay_clifford_rank_gap.py`.
- Independent scientific audit and physical-Majorana replay:
  `audit/science.md` and `audit/referee_replay.py`.
- Manuscript: `manuscript/main.tex` with `manuscript/references.bib`.

## Venue and policy

Physical Review A, Regular Article (Quantum Information Science), is the current
provisional target. Its verified scope and the June 2026 APS AI policy are
summarized in `venue/aims-and-policy.md`. This is a scope match, not an acceptance
or ranking prediction. No indexing or quartile claim was verified.

The draft discloses substantive use of registered OpenAI Codex workers using
model identifier `gpt-5.6-sol` with reasoning effort `ultra` in research, code,
verification design, literature synthesis, and drafting. Before submission, the
author must check the current policy again, independently review and refine the
entire manuscript, run the code, and adjust the disclosure to truthfully describe
the completed human verification. Do not claim that review has occurred until it
has.

## Pending author decisions

1. Confirm the author name, affiliation, postal code, and email shown in the draft.
2. Decide whether PRA remains the preferred venue and whether the exact JSON
   certificate and both scripts should be supplied as Supplemental Material or
   through a durable public repository.
3. Obtain a human specialist review of the spinor transversality and normal-form
   arguments and a broader final priority search.
4. Review every citation, the AI-use disclosure, and the data-availability text.
5. Approve or revise the title, exposition, and submission package. External
   submission has not been authorized or performed.

## Redistribution scope

The proposed handoff bundle contains only authored TeX/Bib/Markdown, project code,
the project-generated exact JSON certificate, and an environment record. It does
not include downloaded third-party papers, browser captures, private job logs, or
credentials. This limited file selection was used for the redistribution check in
`publication.json`.
