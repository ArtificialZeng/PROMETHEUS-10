# Author handoff

## Draft status

This is a local, AI-assisted draft for author and specialist review. It has not
been submitted, peer reviewed externally, accepted, or approved by the named
author. The manuscript intentionally stays within the science snapshot accepted
for writing.

## Core claim

For the finite open extended-SSH chain
`T_N=(r I+S_N)^2`, with `r` in `[1/5,4/5]`, the collision-safe confluent pencil
has two closed positive Ritz energies. For every integer `N>=61`, the two exact
positive edge energies obey explicit uniform relative enclosures and have the
leading laws

`E_1 ~ (1-r^2) r^(N+1)/N` and
`E_2 ~ N (1-r^2)^3 r^(N-1)`.

A codimension-two min–max estimate places the third positive energy at or above
the bulk-band distance `(1-r)^2`; hence exactly four chiral in-gap levels occur
in the certified range.

## Hardest checks completed

- The four-state Gram and cross-Hamiltonian blocks were constructed exactly in
  a root-and-derivative basis; the nonzero root/derivative overlap is retained.
- A signed reversal of `r^(N+1) T_N^{-1}` was checked to equal a rank-two
  extension plus an explicitly summed triangular tail.
- The uniform endpoint inequalities at `N=61`, including `eta_61<0.413` and the
  strict in-gap energy cap, were checked by exact rational arithmetic.
- Forty exact-fraction implementation tests had zero failures.
- Independent 110-decimal spectra and a separately assembled generalized
  pencil agree at `r=1/3,1/2,3/4` and `N=8,12,20,40`.
- The accepted scientific review is in `audit/science.md`; it is an AI review,
  not external peer review.

## Caveats requiring author attention

- `N=61` is a sufficient uniform threshold, not an optimized one.
- The result excludes disorder, interactions, on-site terms, non-Hermitian
  hopping, experimental uncertainty, and phase-transition claims.
- General power-law-prefactored Bloch states and qualitative Toeplitz
  `k`-splitting are prior art. The priority claim is only the two explicit
  coefficients, this rank-two tail enclosure, and the exact four-level count
  for the fixed family. A specialist should still audit theorem-level overlap
  in the Toeplitz literature.
- The source paper is arXiv:2604.20561v1 as checked on 2026-09-14. Recheck for a
  later version before submission.

## Source map

- Frozen question and model: `source.md`, `problem.md`, `physics.json`.
- Primary source: `intake-evidence/primary-sources/phys-00020-p03-01-2604.20561v1.pdf`
  (do not redistribute automatically).
- Main derivation and validation: `evidence/confluent-derivation.md`,
  `evidence/confluent_analysis.py`, `evidence/check_confluent_exact.py`.
- Draft source: `manuscript/main.tex`, `manuscript/references.bib`, and
  `manuscript/edge_splittings.pdf`.
- Regeneration instructions and data: `reproducibility/README.md`,
  `reproducibility/generate_figure.py`, and
  `reproducibility/edge_splittings.csv`.

## Provisional target fit

`venue.json` records Physical Review B, Regular Article, as a plausible target
because the paper concerns a finite topological condensed-matter chain and PRB
publishes the relevant generalized-Bloch literature. Scope and AI policy were
checked against official APS pages on 2026-09-14. This is not a ranking or
acceptance claim.

## AI involvement

OpenAI Codex with the `gpt-5.6-sol` model assisted with topic development,
literature synthesis, derivation, code, verification, scientific review, figure
generation, and drafting. The manuscript contains an APS-oriented disclosure.
The prospective author must independently review the equations, prose,
citations, code, and figure, revise the disclosure if needed, and accept full
responsibility before submission.

## Pending author decisions

1. Confirm the name, affiliation, postal code, and email shown in the draft:
   Xiaojian Zeng; PBC School of Finance, Tsinghua University, Beijing 100190,
   China; xiaojianzeng@foxmail.com.
2. Decide whether the contribution and length justify PRB or another venue.
3. Commission a human specialist check of the Toeplitz and repeated-root
   priority boundary.
4. Review and approve every scientific claim and all AI-use disclosure text.
5. Choose a public repository and license for code/data if the paper is to be
   submitted, then update the data-availability statement.
6. Recheck the target journal's current scope, author instructions, and AI
   policy immediately before submission.
