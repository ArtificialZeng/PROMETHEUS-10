# Endpoint manuscript source and dependency map

The scientific claim is the unchanged claim.json result-note, original_status=unresolved. The accepted88-file snapshot remains the sole scientific scope. The new manuscript does not bind checkpoint.md or state.json, directly or through its evidence records.

| Manuscript item | Stable source/evidence | Portable reproduction |
| --- | --- | --- |
| Hamiltonian, Pauli identity, known star law and original Conjecture3 | literature/2602.03605v1.pdf,20/23/24; source-ledger.json S1 | Certificate local ket/Pauli equality and complete four-qubit star |
| Minimum-field degree comparison | literature/2607.14401v1.pdf,2; source-ledger.json S2 | Intrinsic field d_i eta/4 stated explicitly |
| Separate added-field theorem | literature/2607.10765v1.pdf,12; source-ledger.json S3 | Context only, not an imported exact family formula |
| Sharp leaf-bound gap in prior art | literature/2609.26802v2.pdf,30-31; source-ledger.json S4 | Context only |
| Uniform half bound | literature/2610.09485v1.pdf,21; source-ledger.json S5 | Context only |
| Normalized positive parent objective | literature/Ju-Nagda-2025-published.pdf,24:2-24:3; source-ledger.json S6 | H_1=-2Q convention, no endpoint gap assertion |
| Established orbit/double-star methods | Wong2026 Waterloo MMath thesis section3.3/Theorem13/Example2; current primary title and sections in evidence/write-e8b228-current-web-5.json | Bibliographic entry WongThesis2026; not claimed as new |
| Full star-spin envelope, all N tail, internal N2 Weyl bound, full-gap interpretation | evidence/research-p4-full-gap-derivation.md | Explicit proof in manuscript/endpoint.tex; symbolic star determinant in certificate |
| Correct auxiliary C orientation labels | Frozen proof's norm is unchanged; manuscript derives actual spectra | Certificate auxiliary_C_characteristic_polynomials |
| Source-Pauli rational quotients and continuous box bounds | evidence/research-p4-pauli-branch-replay.py/json/log | reproducibility/endpoint_certificate.py/json builds without cached inputs |
| Complete root anchors | evidence/research-p4-root-anchor.py/json/log | Certificate anchors with every root and multiplicity |
| Direct original-model quotient checks | evidence/research-p3-independent-replay.py/json/log | Complete physical intertwiners at k3, s3/5, transcription checks only |
| Outward-rounded manuscript anchor table | Same exact rational anchor values | reproducibility/make_endpoint_table.py, manuscript/endpoint-anchors.tex |

The executable supplement recreates the accepted matrices, characteristic polynomials, derivative/residual bounds, root anchors and margin constants exactly. The writer comparison and fresh-directory replay are separate portability checks, not referee acceptance. The current primary recheck is evidence/write-e8b228-literature-recheck.md and refreshed readings in evidence/write-e8b228-primary-readings.txt.

Compilation dependencies are manuscript/main.tex (entry point), manuscript/endpoint.tex (complete paper), manuscript/tree-family.tex (native TikZ graph), manuscript/endpoint-anchors.tex (generated table), and manuscript/references.bib. System LaTeX packages are not local source dependencies. No old leaf-example or small-s table is imported. The build uses -no-shell-escape and a recorder file so the local dependency set can be inspected.

The curated submission_files contain the complete authored TeX/Bib/TikZ/table, portable certificate/code/reference data, README, requirements and author handoff. Raw third-party source fulltexts, web responses and audit/job/operational records are local dossier inputs and are excluded from that public supplement. Old files remain preserved in the project and archive.
