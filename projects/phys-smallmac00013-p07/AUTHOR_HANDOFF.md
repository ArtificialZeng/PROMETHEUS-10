# Author handoff

## Core claim

For every integer n at least 2 and formal r,

    [t^3] X^O_{2n}(r,t)
      = r(1+(n-2)r^2) X^O_{2n-2}(r,1)

in Z[r]. This is the full formal-r identity conjectured in BFK
arXiv:2309.08446v2, Eq. (8.33), under that paper's OSASM normalization.

## Hardest checks already performed

- The accepted science audit independently reconstructed the decisive BFK
  source equations and the low-Laurent last-column signs.
- The binomial congruence T(-r/2) was simplified independently and gives a
  centred skew kernel supported only between opposite index parities.
- Pfaffian minor summation leaves two column sets; the exceptional set has a
  two-index parity imbalance and its Pfaffian vanishes.
- Exact definition-only and source-Pfaffian implementations agree through
  published baselines and on the reserved order-16 test.

These are AI-assisted checks, not external peer review or human approval.

## Caveats and scope

- The result is finite-size and exact. It makes no thermodynamic-limit,
  free-energy, phase-transition or experimental claim.
- The literature search is bounded. It does not exclude simultaneous,
  unindexed or unpublished work after the checked BFK version.
- No proof-assistant formalization was performed.
- The manuscript author line and supplied details (Xiaojian Zeng; PBC School
  of Finance, Tsinghua University, 100190; xiaojianzeng@foxmail.com) require
  confirmation by the author.

## AI use and target-journal policy

OpenAI Codex model gpt-5.6-sol with reasoning effort ultra assisted with
literature discovery, the central derivation, exact code, an independent audit
in a separate context, and manuscript drafting. This is disclosed in the
acknowledgements. IOP's current policy expressly covers disclosed AI text and
literature assistance but does not expressly classify central AI-assisted
mathematical derivation. Before submission, the author should critically
rederive the proof, verify every reference and code output, approve the
disclosure, and seek journal guidance if needed.

## Source map

- Definitions and original conjecture: BFK v2, Eqs. (8.2), (8.10), (8.11),
  (8.32), (8.33); local extract in
  literature/bfk-2309.08446v2-primary-extract.md.
- Accepted proof record: evidence/all-n-proof.md.
- Independent audit: audit/science.md and audit/replay.log.
- Exact checkers and data: code/ and the files listed in
  REPRODUCIBILITY.md.
- Venue scope and policy: venue/aims-and-policy.md.

## Target fit and pending decisions

The provisional target is Journal of Physics A: Mathematical and Theoretical,
article type Paper, because its current scope explicitly includes physical
combinatorics and integrable systems. Ranking is unverified and no acceptance
claim is made.

Before any submission, the author must decide or confirm:

1. authorship, affiliation, email and any coauthor contributions;
2. proof correctness and priority after an updated literature search;
3. funding, competing-interest and data/code repository statements;
4. the target journal and whether its editor accepts the disclosed degree of
   AI assistance;
5. final reference metadata and journal-specific formatting.

No external submission is authorized or has been made.
