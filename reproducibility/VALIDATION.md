# Validation record

Validation date: **2026-10-12**. Ten projects; **26 selected computation commands returned zero**, and all ten manuscripts compiled successfully from fresh copies. Scientific outcome markers were also inspected as described below. This is a packaging/reproduction check, not a new peer review or comprehensive novelty audit.

| Project | Fresh check outcome |
|---|---|
| phys-00002-p01 | 256/320-bit interval runs reported rank_two_fixed_a_local_optimality_certified=true; independent check verification_passed=true. Global assertions remain false/unresolved. |
| phys-00002-p02 | Eight named configurations plus 128 held-out configurations; exact identities and SOCP/SDP diagnostics met verifier criteria. Numerical agreement is corroboration of the manuscript proof. |
| phys-00002-p06 | All eight witness checks printed PASS, including detailed-balance predicates, late-time order reversal and precision stability. Not an interval-certified general theorem. |
| phys-00002-p15 | Fixed-gap probe failure_count=0; trace-bound stress checks passed within floating tolerance. Near-closing-gap uniformity is not claimed. |
| phys-00003-p01 | Exact quotient, independent Wick comparison, baseline and convention-map checks printed PASS. Polynomial scope remains restricted. |
| phys-00004-p01 | Coefficient, exact quadratic proof and representation/baseline commands reported pass. Baseline calculation alone does not establish two-use additivity. |
| phys-00004-p02 | Standard-library rational certificate status PASS, without floating-point sign decisions. |
| phys-00005-p01 | Two representations and comparator recovered 62 edges, tau=1673/1192 and delta=-81/2384; status exact_counterexample_verified. |
| phys-00006-p01 | Three exact symbolic checks printed PASS, including independent equal-marginal memory witness audit. |
| phys-00007-p01 | Symbolic replay printed PASS. This does not remedy the historical submission-bundle binding failure. |

## Environment and limits

- Python 3.12.14, macOS; scientific dependency versions are pinned in the root requirements. The local replay used the existing environment and existing python-flint 0.9.0 installation. A fresh pip installation and Linux/Windows have **not** been tested.
- Each run operated on a copied project. Published benchmark scripts and supporting evidence are included where selected by the original project package; the runner shows exactly what was executed.
- The four-measurement replay initially failed because source.md was absent from the old submission list. Adding the unchanged file fixed the failure without weakening hash validation.
- Clean TeX compilation completed for all ten. Final logs had no detected undefined citations/references, missing-character or overfull-box warnings. Three projects (phys-00002-p06, phys-00002-p15, phys-00004-p01) retain a nameref label-definition warning.
- Rebuilt PDFs were not substituted for the archived PDFs. This pass did not repeat a new page-by-page visual science release review. The original archived PDFs all match the original release-manifest SHA-256 digests.
- The archived draft phys-00007-p01 remains historically blocked at evidence/manuscript binding. No queue or gate state was changed.
- Exact certificates and numeric diagnostics have different evidential scope; see each PDF and the five-language tables.

Full commands, durations and build invocations: [validation-results.json](validation-results.json). Package edits: [portability-changes.json](portability-changes.json).

## README packaging checks

All five README files rendered to Markdown-derived HTML with ten details/summary sections and eleven tables each; all README local links resolve. A live browser click/visual test was not completed: browser policy rejected local file URLs, and the headless browser dependency was unavailable. No bypass or browser installation was attempted. The preview HTML is not included in the public package.
