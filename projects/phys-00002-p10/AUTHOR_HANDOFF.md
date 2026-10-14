# Local manuscript handoff — human review required

Title: A balanced beam-splitter counterexample to the low-order Wigner–Rényi
vacuum bound.

This is a local draft prepared from the unchanged accepted scientific scope.
It is ready for a fresh release review, not external submission or publication.
The separate internal AI referee audit is not external peer review or human
author approval. The final local release, if its future audits pass, must retain
status draft_ready_author_review_required.

## Core claim and accepted boundary

The universal bound over all independent balanced beam-splitter product inputs
and all 0 < alpha < 1/2 is false. Independently prepare
psi=(20|0>+|2>)/sqrt401 on both modes and trace one output after balanced
lossless mixing. The exact output Wigner function is exp(-R) Q^2/pi,
Q=(401-2R+R^2/2+20sqrt2(x^2-p^2))/401. At alpha=1/4,
the full-plane integral is below 9.43718 and the vacuum integral is above
9.43892. This one witness disproves the original universally quantified claim.
There is no claim of an optimum, violating interval, sharp order boundary,
general asymptotic expansion, preparation robustness, loss stability or experiment.

The units and domain are [x,p]=i, hbar=1, natural logarithms and the entire dx dp
plane. Input support {0,2} and output support {0,2,4} are exact, not truncation
approximations. The retained state is positive as a partial trace, normalized
exactly, and has a nonnegative Wigner function including its zeros. The established
alpha>=1/2 and Shannon beam-splitter results are unaffected.

## Hardest checks for the author and release reviewer

Review the exact preparation and Fock/coordinate coefficient agreement, including
the four-photon output component. Audit the absolute-value chord for cells crossing
Q=0, weighted Cauchy bound, factor from angular symmetry and polar Jacobian,
directed pi/trigonometric/exponential operations and analytic infinite-plane tail.
The two implementations share the cell inequality and grid; their independence
comes from distinct physical reconstructions and integer versus Decimal arithmetic.
They are not two unrelated integration proofs. Lower interval endpoints for an
upper-bound expression are not physical-integral lower bounds.

Reproduce with the instructions in reproducibility/README.md and inspect the
displayed inequalities in manuscript/main.tex. Python arithmetic and the source
programs are the computational trust base. No formal proof assistant is used.

The current accepted evidence and scientific audit remain hash-bound by the
existing snapshot. Neither source.md nor any accepted evidence was changed.
The manuscript's evidence map is reproducibility/SOURCE_MAP.md. No argument
relies on mutable handoff files.

## Literature and target

The current original preprint remains arXiv:2411.05562v2; the September general
counterexample remains arXiv:2609.24670v1. The additional He and purity papers
are contextual references, not premises of the certificate. The literature check
is bounded and does not guarantee priority. Review the distinction between
general Wigner-positive counterexamples and the present exact product-input
preparation before submission. Details and current primary retrievals are in
venue/write-literature-and-scope.md.

Physical Review A, Regular Article, is a source-backed target within quantum
optics and quantum information science, supported by two close published papers.
The current scope and APS AI policy summary are supplied in
venue/aims-and-policy.md. The machine-readable venue.json and raw retrievals
remain in the local dossier. No journal quartile or acceptance prediction is made.

## Human authorship and AI decisions still pending

The supplied draft byline is Xiaojian Zeng, PBC School of Finance, Tsinghua
University, 100190, xiaojianzeng@foxmail.com. Confirm the byline, affiliation,
contact details, actual intellectual contributions and any collaborators.
The affiliation is not an automated institutional endorsement.

OpenAI Codex assisted with literature searches, candidate discovery, derivations,
code, computational checks and drafting. The current manuscript worker uses
gpt-6.1-sol under the recorded authorization; earlier exact model-version records
are incomplete. The draft describes actual AI-assisted checks and does not claim
human verification. APS requires substantive uses in methods/acknowledgments,
tool/version details, actual human direction and verification, review and refinement
of generated content, and applicable terms/rights checks. The policy status is
needs_author_judgment. Resolve those records and human scientific accountability
before any submission; do not replace them with automated approval language.

Decide the eventual data/code repository and access route. The draft states that
programs and reference data accompany the source package, without inventing a
repository URL. Confirm priority and bibliographic metadata, and obtain the fresh
citation, clean-build and every-page visual release audits. External submission
is not authorized by this job.

## Package and redistribution scope

publication.json explicitly selects manuscript TeX/Bib, this handoff and the
needed authored code/reference outputs/instructions. No downloaded third-party
paper, copied figure, private log, job tree, scientific audit tree, credential or
account data is selected for redistribution. The selected scripts and numeric
outputs are project-generated; primary papers are cited by bibliographic links.
No license, ownership transfer or completed human rights approval is invented.
The author must confirm the eventual license and final sharing decision.

The clean local PDF path and complete source list are in publication.json.
Actual build and replay logs stay in build/ for the fresh reviewer. Older local
manuscript/PDF/code artifacts are preserved under build/history/pre-write-bb985.
