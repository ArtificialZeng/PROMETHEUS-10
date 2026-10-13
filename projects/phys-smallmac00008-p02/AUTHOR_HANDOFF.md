# Author handoff

## Core result

For every full-Choi-rank qubit CPTP channel, under two identical memoryless
uses, a fresh minimal four-dimensional environment per use, one fixed
orthonormal environment measurement used twice, all outcomes retained, and the
specified polar-unitary recoveries, the separately optimized full-history and
current-record Bell entanglement fidelities are equal.

The physical message is optimization-level, not pointwise: history can improve
the fidelity for a fixed measurement, but the determinant-maximizing
measurement family always contains a commuting-positive-part point where the
gap vanishes.

## Hardest checks already performed

- The source's rank-three `U(3)` control was reconstructed in two independent
  representations, giving `F1=3/4` and both two-use values `5/8`, with every
  branch retained.
- The Takagi convention was mapped explicitly from column mixing to the
  environment row-mixing convention, including `V=U^T` and the full-rank
  `T O P` maximizing family.
- The new `O(4)` lemma was proved using a quaternionic balanced two-plane and
  centered-ellipse argument. Exact symbolic identities and degenerate cases
  were independently replayed by the accepted referee.
- The pointwise determinant and commutator-gap identities, TP/Choi
  admissibility and sixteen fresh full-rank end-to-end examples were replayed
  independently. The frozen scientific audit accepted the exact restricted
  claim; this remains AI review, not external peer review.

## Caveats

- No claim is made for more than two uses, adaptive or step-dependent bases,
  general POVMs, nonminimal environments, higher dimensions, imperfect
  detectors, delayed control, or arbitrary current-record CPTP controllers.
- The theorem does not resolve the source's all-step Conjecture 9.
- The bounded novelty search found no equivalent result, but was not an
  exhaustive priority search. The publisher version of the 2024 source was not
  compared word-for-word with arXiv v1.
- The target journal and policy were checked on 2026-09-13, but ranking and
  indexing were not verified.

## Source map

| Manuscript component | Main supporting records |
| --- | --- |
| Protocol and frozen quantifiers | `source.md`, `problem.md`, `physics.json` |
| Published control and conventions | `reproduction.json`, `evidence/source-reconstruction.md`, `evidence/baseline.log` |
| Takagi optimizer | `evidence/takagi-o4-analysis.md`, Laustsen--Verstraete--van Enk primary excerpt |
| Orthogonal-frame lemma | `evidence/o4-rank-one-proof.md`, exact replay script/log |
| Full theorem and limits | `verification.json`, accepted `audit/science.md` and independent replay |
| Novelty boundary | `evidence/primary-priority-comparison-pass3.md`, `audit/novelty-search.md` |
| Venue and AI policy | `venue.json`, `venue/aims-and-policy.md` |

## Target fit

The provisional target is *Quantum Information Processing*, Regular Article.
Its current scope includes theoretical quantum information and quantum error
correction, and it published the directly preceding 2024 work. Current journal
and Springer Nature guidance require disclosure and human accountability for
substantive LLM use. Because AI contributed to the derivation, computation,
checking and writing, compatibility remains a human policy judgment; no
submission is authorized.

## Decisions required from the author

1. Verify the theorem, every proof step, physical interpretation, code output
   and citation against the primary sources; obtain any additional expert
   review considered necessary.
2. Confirm the author name, affiliation, postal address and email, and supply
   ORCID if desired. The listed affiliation is not an automated institutional
   endorsement.
3. Decide whether the work and AI-assisted workflow meet the journal's current
   human-led authorship policy; revise and approve the AI declaration.
4. Supply/approve funding, competing-interest, data/code repository and author
   contribution statements before submission.
5. Recheck current venue scope, article type, policy and submission formatting;
   decide whether to use the journal's production template.
6. Extend the literature search, especially post-2024 citations and synonymous
   matrix-analysis formulations, and compare the publisher version of the
   source if available.

External submission, author approval, peer review and editorial acceptance are
all pending.
