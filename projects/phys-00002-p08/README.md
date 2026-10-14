# phys-00002-p08

**A resource obstruction for qubit measurement self-testing with matched kernel preparations**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

Reweighting all probabilities at the established four matched-exclusion-state reference cannot reduce auxiliary settings from three to two. Any such reduced-resource protocol must depart from those reference preparations or change the physical resources/premises. The obstruction addresses target-only certification, not merely separate state self-testing.

## Original question

自检验四结果单比特测量，能否减少制备和辅助测量数量？

## Frozen scientific scope

For any extremal four-outcome complex-qubit reference POVM with four matched pure kernel-state preparations, and any binary auxiliary collection whose reference observable Bloch vectors span a space of dimension at most two, every real linear functional on the complete prepare-and-measure probability table that is globally maximized at that reference has an admissible maximizing realization with the same auxiliary measurements and a target having at most three nonzero effects. Thus no such witness self-tests the four-outcome target, even when only the target is to be certified. This includes two projective auxiliaries and two arbitrary binary POVMs. The reference kernel-state restriction is essential to the claimed scope; the unrestricted resource conjecture remains unresolved.

## Proposed contribution and limitations

Necessary supporting-witness normal form c_ij=l_i-k_j delta_ij with k_j>=0 for arbitrary target probability coefficients at any four matched kernel-state reference; using it, a universal explicit <=3-nonzero-effect same-score target replacement whenever the auxiliary Bloch span has dimension<=2. Includes arbitrary binary POVMs and zero auxiliary-state-gradient cases; original unrestricted minimality remains unresolved.

Fresh primary screen2026-10-12UTC before legacy extension:2406.08661v1/current official record;2020 publisher fulltext;2306.07248v5 including official2025-11-01 revision;2306.00730v4;2603.01802v1;2503.13282v2/current2026-07-01 revision. Exact-ID and minimal/two/four-outcome/antipodal/state-exclusion/lower-bound searches. No equivalent result identified in checked passages; bounded screen, incomplete forward-citation coverage, no proof of priority or unrestricted openness. Novelty/significance remain for fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
