# Author handoff: local result-note

Title: **A resource obstruction for qubit measurement self-testing with matched
kernel preparations**. This is a local draft for author review. It has not been
submitted or externally peer reviewed. Author identity, affiliation and email
are supplied draft details requiring confirmation: Xiaojian Zeng; PBC School of
Finance, Tsinghua University, 100190; xiaojianzeng@foxmail.com.

## Core result and limits

Exactly four reference preparations are the matched pure kernel states of a
nonzero rank-one extremal four-outcome complex-qubit target. Every real linear
witness on all auxiliary and target probabilities, globally maximized at that
reference, has an inequivalent same-score maximizing target with at most three
nonzero effects if the reference binary-observable Bloch span has dimension at
most two. The auxiliary measurements are unchanged. Arbitrary binary biases,
degenerate settings, zero preparation gradients and input-independent shared
randomness are included.

The supporting normal form is c_ij = ell_i - k_j delta_ij, k_j >= 0. It is a
necessary consequence of measurement optimization, not an assumed witness
ansatz. The alternative is positive and complete. Its zero effect proves
inequivalence under common unitary/antiunitary transformations or relabeling.
The score is preserved; the full table need not be. The original unrestricted
resource-minimality question remains unresolved. No N>=4 bound, nonlinear/noisy
theorem, new protocol or experimental result is claimed. The setting is static,
dimensionless and exactly finite-dimensional; no perturbative or tail estimate
is applicable.

## Hardest scientific checks

Review the state-basis and every-triple independence implication of extremality
and positive completeness. Reconstruct the primal/dual measurement SDP, strict
feasibility, dual attainment and rank-one complementary slackness. Check that
the coefficient identity is numerical and persists when states change. In
preparation optimization, allow zero gradients and signed parallel multipliers.
Verify all zero/one/two-active replacements, binary scalar biases, legal zero
effects and the single-branch shared-randomness counterexample.

The universal proof is in manuscript/main.tex, Section 3, and the unchanged
stable derivation evidence/antipodal-reference-obstruction.md. Exact supporting
checks are evidence/n4k2_exact_checks.py. The current isolated replay under
reproducibility/runs/exact/ completes the same 22 model/active-set checks with
exact score differences zero. It is a software/algebra replay, not another
scientific acceptance. The scientific workflow's separate referee phase is an
AI-context review, not external peer review or completed human validation.

## Source map and novelty

The closest primary sources are Tavakoli et al. (2020), DOI
10.1126/sciadv.aaw6664, noiseless Eqs. (6)–(7), and Drótos et al. (2024), DOI
10.1088/1367-2630/ad4e5c, arXiv:2406.08661v1, Sections III–IV and VI. The
exact proposed difference is the necessary all-target-coefficient normal form
and an inequivalent target maximizer for target-only certification. Standard
SDP duality and preparation-span optimization are not claimed new.

Later versions actually checked: semi-SIC 2306.07248v5 (2025 revision), universal
2306.00730v4, photonic 2603.01802v1 and Bell-scenario 2503.13282v2. Book
bibliographic metadata and official Boyd/Vandenberghe Slater slides were checked.
Source details, locations and retrieval limits are
evidence/write-64f056228bbb/literature-review.md. Manuscript citation keys map
directly to the versioned URLs/DOIs in manuscript/references.bib. No equivalent
restricted result was identified in this bounded screen; priority is not guaranteed.
The original source.md and all accepted scientific evidence remain byte-identical.

## Venue and AI use

Proposed target: Quantum Information Processing, Regular Article. Its subject
scope fits. Ranking/indexing are unverified. The current policy assessment is
**needs_author_judgment**, with the actual oversight issue described in
venue/aims-and-policy.md. Disclosure alone does not make this autonomous workflow
compliant. Substantial AI participation included ideas/arguments, source checks,
code, algebra, science auditing and text. The named author must undertake genuine
scientific reconstruction and determine authorship responsibility, permissible
oversight and venue eligibility. No human-led scientific work is invented here.
Per-job exact model/usage provenance is a supervisor record; this packet makes
no invented model-version or billing statement.

Confirm funding, conflicts, contributions, identity/affiliation, manuscript
content, repository availability, licensing and any eventual submission. These
declarations are pending. No author approval has been assumed or requested as
part of this bounded writing job.

The journal page contains conflicting abstract lengths. The current main
abstract follows its 150–250-word instruction. If the 80–100-word instruction
applies, an alternative is:

> We study linear self-testing of extremal four-outcome qubit measurements with
> four reference preparations matched to the target effect kernels. Every witness
> globally maximized at such a reference admits an inequivalent maximizing target
> with at most three nonzero effects when the auxiliary observable Bloch span has
> dimension at most two. Measurement duality forces an exclusion-penalty coefficient
> form; preparation optimality then permits an explicit replacement. The result
> includes arbitrary binary auxiliaries and shared randomness. It gives a resource
> obstruction within this reference class, while unrestricted minimality and noise
> robustness remain unresolved.

## Reproduction and next review

See reproducibility/README.md for tested isolated checking and clean-build
commands. Full third-party PDFs/renderings and raw caches are not selected for
redistribution. The source packet includes only authored manuscript/code,
instructions and scientific replay outputs. Public references are cited by
identifier and URL.

The fresh release job of 12 October 2026 checked all six cited sources and
version attributions, the complete source dependencies, a clean-directory
rebuild, and all six rendered pages. The rebuilt PDF is
build/release-708e9b8f0919/main.pdf; its extracted text agrees with the earlier
writer build. The final release records bind this PDF and the current source
snapshot. These checks do not supply human scientific validation or establish
the venue's AI-policy compatibility, which remains needs_author_judgment.

One next test for the author is to reconstruct the restricted argument,
especially complementary slackness and the explicit same-score replacement,
and assess the actual research workflow against the venue policy before any
submission. Authorship, declarations and final approval remain pending.
The supervisor performs local activation and creates/checks the selected
handoff bundle after a ready release return. Any central scientific change
requires a fresh science review; publication-only edits require a new manuscript
snapshot and affected release reviews. No external submission is authorized.
