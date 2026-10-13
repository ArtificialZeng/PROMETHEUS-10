# Author handoff

## Draft status

This is a local `result-note` draft. It has not been submitted, peer reviewed,
or approved by the named author. The author details currently shown are Xiaojian
Zeng, PBC School of Finance, Tsinghua University, Beijing 100190, China,
xiaojianzeng@foxmail.com; all details require confirmation.

## Core accepted claim

For the subdivided star `T_q` with `q` ordinary leaves at `C` and the two
additional edges `C--A--B`, the coefficient-one unnormalized Hamiltonian

`H_s=-sum_e (|00>+s|11>)(<00|+s<11|)_e`

has `Delta(T_q,s)>1-s^2` for exactly `q=1,...,6` and every real `0<s<1`.
The universal tree conjecture and equality classification remain unresolved.

## Hardest checks

- The local term is rank one with norm `1+s^2`; it is not a normalized
  projector.
- Both excitation channels are controlled: the largest odd eigenvalue and the
  second-largest even eigenvalue.
- For `q=2,...,6`, all spin-charge blocks are included with multiplicity; their
  dimensions sum to `2^(q+3)`.
- Every possible target crossing lies among 171 exact resultant-root
  neighborhoods. Rational root bounds and Weyl enclosures are strictly positive
  on all of them, and each `q` has a positive exact reference margin.
- The full-basis numerical replay is only corroborative; it is not presented as
  the continuous-parameter proof.

## Caveats requiring author attention

- The cutoff `q<=6` is arbitrary and is the main significance/venue risk.
- Nothing is proved for `q>=7`, arbitrary trees, cyclic or weighted graphs,
  normalized edge projectors, `s=1`, or a thermodynamic limit.
- The result does not create a new general Quantum Max-Cut algorithm.
- The bounded literature check supports candidate novelty only, not priority.
- A permanent public code/data repository and identifier have not been chosen.
- The declaration of interests, funding, author contributions, author details,
  and final data statement require human confirmation.

## AI-use disclosure

OpenAI Codex with the `gpt-5.6-sol` model assisted with problem development,
literature-search support, derivations, code generation and execution,
same-machine checking, and drafting. The current IOP policy was checked and the
draft includes a detailed disclosure. Because the use extends beyond simple
language editing, venue compatibility and the exact final wording require the
author's judgment. Do not state that a human verified the work until that review
has actually occurred.

## Target fit

The provisional target is *Journal of Physics A: Mathematical and Theoretical*,
article type Paper. Its current scope covers computational/mathematical methods,
quantum simulation and eigenvalue problems. This is a plausible topical match,
not an acceptance forecast. The author should decide whether to submit this
finite result or first seek an all-`q` extension.

## Source map

- Model and source normalization: `source.md`, `source-ledger.json`,
  `reproduction.json`.
- Analytic `P_4` proof: `evidence/path4-exact-analysis.md`.
- Block reduction: `evidence/subdivided-star-analysis.md`.
- Exact finite-range proof: `evidence/subdivided-star-continuum-analysis.md`,
  generator, JSON packet and checker.
- Accepted scientific-scope review: `audit/science.md`.
- Venue evidence: `venue/aims-and-policy.md`.
- Manuscript: `manuscript/main.tex` and `manuscript/references.bib`.
