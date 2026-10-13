# Author handoff: exact signed-sum spectral locus

## Draft status

This is a local `result-note` draft for author review. It has not been submitted,
peer reviewed externally, or accepted by a journal. The original combined problem
remains unresolved because no uniform Pauli-algebra canonical-mode construction is
claimed.

## Core accepted claim

For every real `(a,b,c,d,e,f)`, the spectrum of

`H = a Z_2 + b Y_1 X_2 + c X_1 Y_2 + d Z_1 Y_3 + e Y_1 X_3 + f Z_3`

is, with multiplicity, a three-mode signed-sum spectrum if and only if

`c d (a^2-f^2)(b^2-e^2) = 0`.

The accepted scope is spectral only. The six real hyperplanes include every zero,
degenerate, and intersection stratum. The off-locus certificate is the exact constant-
coefficient residual

`-64 c^2 d^2 (a-f)(a+f)(b-e)(b+e)`.

## Hardest checks already completed

- Two independently derived `8 x 8` Hamiltonians agree in all 64 symbolic entries.
- The all-equal source benchmark is reproduced exactly and numerically.
- A characteristic-polynomial route and a separate Pauli-trace/Newton replay obtain
  the same factorized obstruction.
- Chiral symmetry `Gamma=Y_1Y_2Y_3` reduces real sufficiency to an eight-linear-factor
  identity and supplies explicit nonnegative energies for both ordered spectral
  relations.
- A fresh referee accepted this exact restricted claim while explicitly rejecting any
  implication of uniform structural CAR modes or scalable simulation.

## Caveats requiring author attention

- The literature search was bounded. The author should repeat priority and related-
  work checks, especially for arXiv:2012.07857, 2305.15625, 2310.19897, 2508.05789,
  and 2509.09092 and their latest versions.
- The paper must continue to distinguish signed-sum spectral representability from a
  useful Pauli/local canonical-fermion construction.
- The symbolic factorization and the ordered-magnitude reduction should be checked by
  the author line by line before submission.
- Physical Review A / Regular Article is a plausible current target, not a verified
  editorial fit or acceptance prediction. A narrower mathematical-physics journal may
  be preferable after human assessment.
- The draft author identity needs confirmation: Xiaojian Zeng; PBC School of Finance,
  Tsinghua University, Beijing 100190, China; xiaojianzeng@foxmail.com.
- The APS AI disclosure must be reviewed and approved by the author. It presently
  records substantive OpenAI Codex (`gpt-5.6-sol`) assistance without claiming prior
  human verification.

## Source map

- Primary model and published limit: `literature/arxiv-2012.07857v2-primary-excerpt.md`
- Frozen problem and conventions: `problem.md`, `physics.json`
- Independent reproduction: `reproduction.json`, `evidence/source-reconstruction.md`
- Exact result: `evidence/spectral-locus-proof.md`,
  `evidence/general-characteristic.log`, `evidence/spectral-locus-check.log`
- Fresh referee: `audit/science.md`, `audit/replay.log`
- Manuscript and references: `manuscript/main.tex`, `manuscript/references.bib`
- Regeneration: `reproducibility/README.md`
- Venue evidence: `venue/aims-and-policy.md`

## Redistribution scope

The proposed submission bundle contains only project-authored TeX, BibTeX, the
project-authored figure, source code, requirements, regeneration instructions, and
this handoff. It excludes downloaded third-party papers, the short local primary-source
excerpt, credentials, and the `jobs/`, `audit/`, and `release/` runtime trees. This
file-level scope was checked for the local bundle; journal licensing and final upload
choices remain the author's responsibility.

## Pending author decisions

1. Confirm the scientific proof and bounded novelty claim.
2. Confirm author name, affiliation, address, and email.
3. Approve or revise the target venue and Regular Article type.
4. Approve the AI-use disclosure and data/code availability statement.
5. Decide whether the illustrative obstruction-slice figure improves the paper.
6. Authorize any future external submission separately; none is authorized here.
