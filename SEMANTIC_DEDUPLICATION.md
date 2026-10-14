# Semantic result comparison

The current index preserves **93 manuscript PDFs and their source packages**. It presents **90 canonical research entries**: 32 proofs, 18 disproofs, 38 partial results and 2 computational results. Classification follows the recorded frozen scope, not the strength of a title. These are drafts requiring human author review; the original boundariness manuscript retains its historical binding-gate limitation.

Deduplication compares the original question, physical model, premises, quantifiers, observable and actual result. PDF hashes are used only for artifact integrity. Neither full-PDF text similarity nor a shared internal project number is a semantic equivalence test. The two machines' IDs remain separate: `phys-smallmac…` is the upstream collection, `phys-…` the original and subsequent big_mac collection.

## Earlier results covered by a later entry

| Earlier preserved manuscript | Canonical entry | Why it is not counted independently |
|---|---|---|
| [phys-smallmac00008-p02](projects/phys-smallmac00008-p02/paper.pdf) | [phys-smallmac00014-p11](projects/phys-smallmac00014-p11/paper.pdf) | The full-Choi-rank qubit recovery equality for two uses is included in the later all-positive-integer-use result, under the same fresh minimal environment, fixed full four-outcome measurement and recovery conventions. |
| [phys-smallmac00014-p03](projects/phys-smallmac00014-p03/paper.pdf) | [phys-smallmac00015-p01](projects/phys-smallmac00015-p01/paper.pdf) | The symmetric three-state weak-Fourier-drive inequality is the N=3 specialization of the complete-K_N weak-drive theorem. Neither statement establishes a finite-amplitude bound. |
| [phys-smallmac00015-p06](projects/phys-smallmac00015-p06/paper.pdf) | [phys-smallmac00016-p01](projects/phys-smallmac00016-p01/paper.pdf) | The same two-use ordered GAD instrument, `03\|12` bit and parameter point are used. The later exact current-bit optimum and history policy strengthen the earlier gain certificate and add a certified parameter rectangle. Together with equality at one use, this includes the earlier onset witness. |

The earlier PDFs, code, IDs, source statements and provenance remain unchanged. Their links appear inside the canonical entry; the searchable catalog can include all earlier versions. This is navigation and accounting, not a replacement of a scientific review or a claim that the earlier work has no value.

## Related work retained separately

| Pair | Distinction |
|---|---|
| [big_mac purification curvature](projects/phys-00004-p09/) / [small_mac purification local minimum](projects/phys-smallmac00022-p01/) | All positive nonproduct binary tables with pathwise positivity and no common neighborhood versus a full U(16) local neighborhood at r=1/2. Neither complete recorded statement contains the other. Global additivity remains unresolved. |
| [big_mac two-hub EPR family](projects/phys-00035-p01/) / [small_mac small subdivided stars](projects/phys-smallmac00022-p03/) | Different graph families, size quantifiers and deformation regimes: k≥100 in an endpoint scaling versus q=1…6 for all 0<s<1. Neither proves the all-graph conjecture. |
| [two genes with finite RNA lifetimes](projects/phys-00018-p01/) / [three-species feedback ring](projects/phys-smallmac00010-p02/) | Different state spaces, number of species, noise baselines and controlled remainders. A shared noise-tradeoff theme does not make these the same result. |
| [nonreciprocal current large deviations](projects/phys-00030-p01/) / [three-port noise/entropy bound](projects/phys-00032-p01/) | Different target inequality, observable and hypothesis set. A large-deviation counterexample is not a noise/entropy theorem. |

## Version and novelty boundaries

- Each local project contributes one current qualified PDF. Older Landau, Ising and EPR scopes remain in their local archives; they are not uploaded as additional independent achievements under fresh IDs.
- The first ten manuscripts are now included in the same four global classes. Historical display numbers and upstream collection maps remain in the unchanged history for traceability.
- `phys-00002-p02` retains the recorded novelty reassessment concerning arXiv:2609.38836v1. This synchronization does not establish priority or turn it back into an open task.
- A fresh accepted proof without a completed manuscript and release is not uploaded as a finished PDF. The paused Gaussian joint candidate stays in the local research workflow until its writing and fresh release checks finish.
- Unknown equivalence is not silently merged. Future intake must compare against both machines' original questions and complete claim scopes before starting another research task.

The machine-readable comparison is [semantic-relations.json](reproducibility/semantic-relations.json). The full scope index is [portfolio.json](reproducibility/portfolio.json) and the [searchable catalog](catalog.html).
