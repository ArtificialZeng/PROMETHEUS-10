# Author handoff

**Local draft:** Arbitrarily clustered hot spots on bridgeless quantum graphs.
**Author supplied for this draft:** Xiaojian Zeng; PBC School of Finance,
Tsinghua University, 100190; xiaojianzeng@foxmail.com.
Please confirm the authorship, exact affiliation and contact details.
They are supplied draft details, not an institutional endorsement.

## Core result and hardest checks

The accepted scope is the resolution of Kennedy-Rohleder Conjecture 8.9 in its
no-bridge metric-multigraph meaning. For each integer m>=4, the uniformly doubled
split tree has diameter one, simple
mu2=[atan(1/sqrt(2m+1))/h]^2, h=atan(1/sqrt(m))/pi, and exactly 2m
global extreme vertices with diameter 6h. The explicit finite ceiling choice
makes that diameter strictly below every epsilon>0.

The author should reconstruct three decisive steps: complete spectral ordering
and simplicity before doubling; the two-sided operator-domain map retaining all
added DD interval sectors; and the opposing-copy interior distance case needed
for the true graph diameter. The proof is exact at every finite m>=4.
Diagnostic numerics are not rigorous interval enclosures.

## Scope, attribution and review status

The tree family and uniform doubling are established prior art. The focused
delta is the fully controlled no-bridge conjecture consequence. Literature
coverage is bounded and no exhaustive priority assertion is made.
Parallel edges, articulation vertices, symmetry ties, increasing total length
and increasing degree are permitted. No fixed-volume, bounded-degree,
vertex-biconnected, Euclidean-domain or experimental conclusion follows.

An independent AI scientific referee accepted the unchanged claim. This is
neither external peer review nor completed human author review. The fresh release
review checked both primary references, rebuilt the article without old auxiliaries,
and visually inspected all seven pages. Its reports are audit/citations.md,
audit/build.md and audit/visual.md in the local dossier. The supervisor must
validate and activate the local draft and create the selected-file bundle before
delivery. Human scientific review and final policy judgment remain pending.
External submission has not been authorized or attempted.

## Scientific and primary-source map

| Draft material | Stable scientific evidence / primary source |
| --- | --- |
| Construction and exact spectral/metric proof, Sections 2-5 | evidence/research-pass1-proof.md, Sections 1-6 |
| Standard operator and conventions | evidence/operator-reconstruction.md; physics.json |
| Published pumpkin/split-tree baseline | evidence/published-baseline.md; reproduction.json; evidence/input-a.json and evidence/input-b.json |
| Full matching, exact identities, interior geometry diagnostics | evidence/research-pass1-check.py; evidence/research-pass1-input.json; evidence/research-pass1-results.json; evidence/research-pass1-metric-pairs.json |
| Original question, tree family, definition of doubly connected | Kennedy-Rohleder, https://arxiv.org/html/2003.14335v4, Sections 4.2, 6.2, 8.2; DOI 10.3934/cpaa.2021095 |
| Known uniform doubling operation | Kennedy, https://cm.episciences.org/13945/pdf, Section 4.3; DOI 10.46298/cm.12380 |
| Fresh primary versions and bounded later-resolution screen | write-evidence/literature-recheck.md and its five raw source records |
| Manuscript-to-evidence scope | write-evidence/scope-map.md |

No scientific argument or publication input depends on a mutable handoff.

## Target and AI disclosure

Proposed target is CPAA, as an original research paper. Its current public scope
covers analysis and differential equations, and it published the exact predecessor.
See venue.json and venue/aims-and-policy.md. Indexing and rank are unverified.
The journal fit is a reasoned topic match, not an acceptance forecast.
The plain article class may need the journal's current submission template.

OpenAI Codex contributed to literature screening, ideas, proof development,
code, internal checking, drafting and the TikZ schematic. The declaration in the
PDF says so and states that human scientific review and approval remain pending.
The primary publisher policy requires disclosure and human accountability;
ai_policy_status is needs_author_judgment. Approve or revise the declaration
only after substantive human review, and recheck the current policy before submission.

## Pending author decisions

1. Verify the exact proof, prior-art relationship and novelty coverage.
2. Confirm author identity, affiliation, contact details, and any real funding or conflicts.
3. Decide on the journal/article type and current template, and assess the AI declaration.
4. Authorize any eventual external submission separately, after fresh release review.

Build instructions are in manuscript/BUILD.md; diagnostic regeneration instructions
are in REPRODUCIBILITY.md. publication.json selects own TeX/Bib/TikZ, these handoff
instructions, and necessary authored code/data. It excludes third-party full papers,
raw website captures and private execution logs from the submission selection.
The reviewed clean PDF is build/release-clean-fbdfab0dc4b5/main.pdf; after local
activation the supervisor's deliverable is release/main.pdf. The author must
assess the proof and disclosure before any external submission.
