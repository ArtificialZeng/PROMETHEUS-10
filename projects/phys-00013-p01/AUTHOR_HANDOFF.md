# Author handoff: exact pure-state contraction spectrum

This is a **local manuscript reviewed in a fresh release job and awaiting human scientific review**. It is not submitted, externally peer-reviewed, published, or editorially accepted. The named author and affiliation are supplied draft details and require confirmation.

## Core result and scope

For exactly three complex qubits with independent adjacent normalized Haar-SU4 gates, the nonzero principal cosines on stationary L2(CP7) are

`c_r = 6 / ((r+2)(2r+3)), r >= 0`.

The sole constant direction is r=0. Removing it gives one-pair norm 2/5 and ordered m-pair norm `(2/5)^(2m-1)` for every integer m>=1. Conjugation on End(Sym^k C8), with its physical Hilbert–Schmidt metric, truncates at floor(k/2); its nonfixed norm is zero at k=0,1 and 2/5 at every k>=2. The original all-PU8 question `c_*=1/2` remains unresolved. This is an accepted restricted result-note, not a resolution of the original problem.

The self-contained argument is manuscript/main.tex, with the compiled draft at build/review/main.pdf. Stable scientific derivations are evidence/research/all-degree-proof.md and evidence/research/probability-reconstruction.md. manuscript/SOURCE_MAP.md maps the manuscript's statements to stable accepted evidence and primary sources. The independent scientific audit is retained in audit/science.md/json and the original evidence digest is `82b26b52b00466157c8268694793c3f2709dba1ecaedd4e945725e90de2a5d4c`. No scientific input or source byte was changed by writing.

## Hardest checks for the author

1. Confirm that spectator completion preserves the exact raw gate product and that the endpoint orbit statistic is complete, including the SU4 determinant correction on the unused complement.
2. Check the conditional Schmidt-frame law, column-exchange polynomial filtration, complex matrix-ball density, and isotropic component-to-radial inversion. These establish the coefficient at every degree, not only the finite data.
3. Check the self-adjoint Jacobi argument and polynomial density in L2(w), which close the infinite-dimensional tail.
4. Check the positive-Gram unitarization of the coherent-symbol map and complete Cauchy branching. The physical Hilbert–Schmidt metric must not be replaced by Euclidean monomial coordinates.
5. Check the ordered-power exponent 2m-1 and whole identity subtraction, plus the distinctions between singular norm 2/5, product spectral radius 4/25, Hamiltonian gap 3/5 and equal random-edge gap 3/10.

The supporting k7/k8 calculations are exact and use two different constructions. The manuscript's table/algebra checks are recorded in evidence/write/manuscript-support-check.log and are not new source reproduction or a fresh referee. Finite data support the analytic derivation; they do not prove its infinite quantifiers. Reproduction instructions and the tested environment are in reproducibility/README.md and requirements.txt. Full regeneration must be run in a separate scratch directory, because original programs write scientific output files.

## Prior work and limits

The number 2/5 at the second moment, fourth-exterior-power 1/2 witness, induced purity marginal, complex Haar-corner law, three-qubit joint marginal distribution, Cauchy branching and orthogonal-polynomial technique are prior work. They are attributed to the corresponding checked primary sources. The restricted contribution is the complete local-circuit dynamical sequence, sharp stationary ordered contraction and all-symmetric-order transfer. Current primary metadata and bounded later-resolution/equivalence searches are saved in evidence/write/literature-recheck.md and its raw records. Exhaustive priority is not certified.

There is no all-representation upper bound, arbitrary-site or arbitrary-local-dimension extension, noisy/real-ensemble result, perturbative calculation, thermodynamic phase claim, new particle or experiment. Delta initial laws are outside the stationary L2 domain; no deterministic-initial-state total-variation mixing time is asserted.

## Journal and declarations

Physical Review A, Regular Article, is a proposed topical target based on current official scope, article types, and nearby published random-circuit spectral work. Its editorial significance threshold is not guaranteed. venue.json and venue/aims-and-policy.md preserve the current policy check. Ranking/indexing is unverified. No fee, account, submission server or publication action was accessed.

The workflow used OpenAI Codex systems for ideas, derivation, exact calculations, code, literature comparison, separate automated checking, figure code and prose. The paper discloses this substantive use, including AI-assisted figure rendering. There is no documented completed human scientific verification. This job's runner role metadata does not identify the exact model version; the author/supervisor must reconcile actual retained run records before finalizing a tool/version disclosure. No model name was fabricated. AI checks are neither external peer review nor human authorship.

APS requires human responsibility, review/refinement and substantive-use disclosure, including how authors directed and verified outputs. Thus AI policy status is **needs_author_judgment**, not certified compatibility. The author must review the actual workflow and tool terms, independently assess the science and priority, and decide whether authorship and submission are appropriate. Confirm Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190, China; and xiaojianzeng@foxmail.com. Supply accurate contributions, funding and competing-interests statements; none were invented. Any desired repository deposit, venue change or external submission requires separate authorization.

## Build, handover and next gate

The draft uses standard REVTeX 4.2 with an eight-entry bibliography. The first build's missing-figure race and font-cache diagnostics are retained in evidence/write/build-diagnostic.md and latexmk.log. Two later empty-directory builds are preserved: build/final with clean-build.log, and, after final wording changes, build/review with review-clean-build.log. The latter is the clean handoff build, with compiler log build/review/main.log. The generated bibliography and REVTeX note database are supplied as manuscript/main.bbl and manuscript/mainNotes.bib. The writer's rendered-page observations are saved separately; they do not accept the final visual audit.

publication.json enumerates manuscript dependencies and an explicit submission-file selection. The selection consists of project-authored manuscript/Bib/figure/reproduction files and generated exact inputs. It excludes downloaded third-party papers, literature caches, raw web captures, audit/job logs, mutable handoffs and credentials. This is a scope/redistribution check for a local bundle, not a guarantee that the current AI workflow meets every external publication term. No source ZIP is activated or externally uploaded by this writing job.

**Release review:** Job phys-00013-p01-release-a939565e3b33 rechecked the eight primary citations, complete dependency and submission-file scope, actual clean-build logs, all five freshly rendered PDF pages, and current PRA/APS scope and AI policy. The final PDF at build/review/main.pdf is an exact byte copy of the fresh empty-directory build/release-clean/main.pdf; the writer PDF and earlier manuscript snapshot are preserved in evidence/release. The nonfatal nameref label-definition and APS bibliography control warnings are documented in the build audit. No scientific input or accepted scientific digest changed.

The three separate reports are audit/citations.md, audit/build.md and audit/visual.md. The accompanying JSON records bind the actual PDF, manuscript sources and unchanged accepted scientific snapshot. Local activation is owned by the supervisor after the release gate passes. The source archive has not been created or delivered before that activation. The explicit25-file selection excludes third-party full papers and internal runtime files.

APS requires an accurate tool name/version and account of human direction/verification, and places nonresearch drafting use in acknowledgments. The current draft discloses substantive AI uses but is not certified as submission-compliant. Before submission, the author must confirm exact tool versions, complete and describe actual human review, check tool terms, and finalize the placement and wording of the disclosure. No completed human review is inferred from the local automated audits. Venue status remains needs_author_judgment and human approval remains pending.

**One next test:** the supervisor should run release_gate.py publish, followed by bundle.py make and bundle.py check, only after the actual release gate passes; deliver the resulting local draft for human scientific/authorship review. No external submission is authorized.
