# PROMETHEUS-10 · Computational result

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

An inspectable archive of AI-assisted physics research. **93 PDFs are preserved; 90 canonical research entries are indexed.** Three earlier results covered by later, more general or stronger claims remain linked as historical versions and are not counted twice. “10” is the name of the original collection, not the current manuscript count.

These are research drafts requiring human scientific, priority and authorship review. Recorded proof/disproof classes refer to the precise frozen claim. Partial and computational results leave the original problem unresolved. Separate AI review contexts are internal checks, not external peer review or journal acceptance. The original channel-boundariness draft retains its historical binding-gate limitation.

Scientific statements and manuscript titles retain their source language. Navigation, status, usage and the original ten detailed descriptions are localized; quoted scientific claims are not silently translated or weakened.

[PROMETHEUS-10](../../README.md)

[Searchable full catalog](../../catalog.html) · [Semantic comparison and deduplication](../../SEMANTIC_DEDUPLICATION.md) · [Reproduction guide](../../reproducibility/README.md)

## Browse the four result classes

| | Canonical entries |
|---|---:|
| [Proof](../proofs/README.md) | **32** |
| [Disproof](../disproofs/README.md) | **18** |
| [Partial result](../partial-results/README.md) | **38** |
| [Computational result](../computational-papers/README.md) | **2** |

The supervised workflow checks primary sources, reconstructs equations independently, reproduces a published baseline, develops a bounded result, and uses a fresh internal referee before writing and release checks. Compact evidence-indexed handoffs and shared tools reduce repeated work; cached input is a subset of input, not additional usage. No unmeasured token savings or success rate is asserted.

## Computational result

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — Computational result · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | In some thermal relaxation models, a hotter preparation can relax faster. Conditions found in three levels need not govern larger systems. |
| **Result and original-problem scope** | A four-level positive-temperature detailed-balance witness survives independent 100- and 180-digit calculations while the tested three-level necessary predicates are excluded. |
| **Proposed contribution** | A concrete higher-dimensional mechanism tests the limits of reducing thermal relaxation to three-level diagnostics. |
| **Limitations / bottlenecks** | Computational paper; high precision is not directed-rounding certification or a general classification. The original question remains unresolved. |
| **PDF and source** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — Computational result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

The act of packaging grants no additional license to manuscripts, code or data. Consult the original author handoff and applicable rights. No submission, peer-review or acceptance is implied.
