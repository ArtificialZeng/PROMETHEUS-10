# Author handoff: product-profile narrow beams

This local draft gives only the accepted fixed-configuration product-profile narrow-beam result-note. For the full homogeneous three-dimensional Landau-Maxwell equation, the actual initial derivative is p^-2 sum_j w_j C_j+O(p^-1), each C_j<=-45/(14a_j^2), and sum_j w_j C_j<=-45/14. It is therefore negative for sufficiently small p. The general monotonicity problem remains unresolved.

The manuscript sources are manuscript/main.tex and manuscript/references.bib. The current PDF and build log are identified in publication.json. The previous Gaussian/fixed-standardized-shape manuscript and publication-stage records were preserved under evidence/write-beams/previous-manuscript/; old release audits do not review this new text. A fresh release job must check citations, source dependencies, the clean build and every PDF page before local activation. No external submission has occurred or is authorized.

## Scope and hardest checks

The accepted scientific snapshot is 69a5b9a5108295a4fdecc12f4262ea7d9dee4bd5f0f57b4d795dd5bb9923efa6. Its 151 files and the original source were rehashed before writing; the accepted scientific files have not been modified. This is internal automated scientific review, not external peer review or completed human verification.

The author should especially review:

- The original collision first variation, with both density factors and both score factors differentiated. The covariance is not frozen along the dynamics.
- The general product-profile partner average and the term B_j*Ibar-6*I_j, whose cancellation requires both normalized label sums. The redistributed C_j is not an isolated-beam physical derivative.
- J_R>=I_R^2+S_3^2/(4I_R), JP*U4>=14, the skewness square completion and the use of Jensen after sum w_j*a_j=1.
- The exact whole-mixture mass, mean and energy, the distinction between actual profile variances and base Gaussian variances, and the p-dependent center correction.
- The physical cores, unequal-variance posterior bounds, polynomial lower bounds and full-space Gaussian tails that transfer component calculations to the mixture.
- The fixed-p affine rotation/noise representation, covariance self-consistency and weighted raw-derivative estimates that identify the actual initial right derivative.

The stable proof is evidence/research-pass4/product-pair-and-sign-derivation.md. manuscript/SOURCE_MAP.md maps every part of the article to stable proof/code and primary versions. Portable exact checks are in repro, with actual writing-stage replay output in build/write-beams-replay/receipt.json. The code validates algebra, not all analytic hypotheses. No unsuccessful numerical scan is used as proof.

## Limits and priority

Centers, weights, profiles, widths, beam count and gaps are fixed as p tends to zero. Only local transverse-longitudinal product factors are covered. The actual-mixture theorem assumes positive polynomial-Gaussian factors; the leading functional inequality alone has the broader finite-moment/integration-by-parts scope. There is no explicit uniform finite-p threshold, sharp constant, correlated-profile result, rough-data extension, positive-time statement or Boltzmann/Coulomb transfer.

Current primary versions, exact claim sections and later-resolution searches were rechecked on 14 October 2026. Tabary v5 and Silvestre v1 remain the located exact neighbors; no matching later resolution or identical beam criterion was found in a bounded screen. This does not certify absolute priority. Older Villani 1998/2000 fulltext equivalence and implications of known representations remain author review priorities. Standard information inequalities, heat identities and stochastic representation are attributed and not claimed as independently new.

## Author and AI decisions

Draft details supplied for this workflow are Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190, China; xiaojianzeng@foxmail.com. The author must confirm authorship, affiliation and contact details; no institutional endorsement is inferred.

OpenAI Codex substantially participated in derivations, symbolic code, literature search, internal checks and drafting. The manuscript discloses that involvement and that human scientific review remains pending. AI agreement may share errors. The author must independently examine the argument and sources and assume responsibility before any submission; no such review is claimed to have happened.

Proposed target: Kinetic and Related Models, original research paper. The current official scope and nearby Landau/Fisher-information articles support subject fit, not editorial interest or acceptance. The current AIMS policy requires generative-use disclosure and human accountability and prohibits artificially creating core research data. This is an analytic calculation with exact symbolic checks, but the extent of generative assistance requires author judgment; venue.json therefore retains needs_author_judgment. Ranking/indexing/quartile are unverified. Confirm final venue policy, rights, funding/conflict statements and format before considering submission.

## Redistribution and next test

The submission list selects only original manuscript/BibTeX, source map, this handoff, reproduction instructions, original portable code and exact calculated outputs. It excludes downloaded third-party full papers, raw web records, private logs and workflow metadata. No third-party image, experimental data, system package or mutable handoff is bundled. This is a local artifact-scope redistribution check; human authorship and submission-rights approval remain pending.

One next test: a fresh release reviewer must independently check the exact frozen manuscript's citations, policy, complete source scope, clean compiler log and all rendered pages, rerun the structural gate, and only then consider hash-bound local activation and bundling. External submission still requires human authorization.
