# Author handoff — local draft, human review required

**Core result.** Every fixed finite n≥3 and real q outside {-1,1}:
near the embedded sharp witness A_q, the optimized unaveraged response
g_q has a Morse–Bott maximum c(q). The local equality manifold has
dimension 4n−2, its full negative normal Hessian spectrum is explicit,
and a tubular Taylor argument gives a two-sided quadratic deficit and
a bound for every complex second operator B. The auxiliary q=1/2
two-level equality identity is not the main novelty claim.
The original unrestricted global conjecture remains unresolved.

Manuscript: manuscript/main.tex and manuscript/references.bib.
Current local PDF: build/write-final-20261013/main.pdf (eight pages).
The complete source layout and reproducibility commands are in
reproducibility/README.md. The analytic spectrum is an equation table;
there is no external figure dependency or quota-driven plot.

## Hardest checks for the human author

Read the entire proof and confirm the signed-b branch for q<-1;
the simple top eigenvalue and gaps; the smooth reducing-two-plane
geometry; all real and imaginary spectator Hessian blocks; the
matrix-unit support extension to arbitrary finite n; and the normal
Taylor integral controlling the full remainder. The negative-q
spectator multiplication form is negative semidefinite, with top
eigenvalue at most zero. The manuscript incorporates that correction.
Do not propagate the inaccurate intermediate q||C||_F^2 estimate
from the preserved proposer proof into later versions.

The Hessian is measured in real Frobenius-orthonormal coordinates at
the unnormalized A_q, whose squared norm is R. Check this convention
before applying the response coefficients to calibrated operators.
The physical response is success-weighted on a subnormalized control
state. Normalized postselection adds a success-probability denominator.
The parameter q is a signed observable weight, not a probability,
jump rate, or particle statistic; no GKLS generator is inferred.

## Limits and value

There is no explicit neighborhood radius, global inequality, uniform
large-n/parameter limit, excluded-point geometry, experimental claim,
or new universal relaxation-rate result. No later primary resolution
or matching local theorem was identified in the bounded current
screen. Absence of a search hit does not certify openness or priority.
The missing effective radius limits finite-error applications.

The accepted scope adds a full-dimensional neighborhood, including
full-rank nonnormal spectator-coupled perturbations, beyond the prior
normal-A and two-level bounds. Exact normal susceptibilities and the
true curved saturation geometry are the proposed contribution.

## Source map

- Response reference (BibTeX key ckos2022response):
  arXiv:2208.10005v1, Eq. (4), Theorem 1, Lemma 1 and the sharp witness
  on PDF pages 3–5,8. The published article is LAA 656 (2023), 158–166,
  DOI 10.1016/j.laa.2022.09.022; the full journal body was not compared
  with the author preprint, and the bibliography says which was used.
- ckos2022norm: arXiv:2202.11520v2, the distinct squared-norm problem.
- nobori2026: arXiv:2608.03897v1, Theorem 1.1, Section 3 and
  Proposition 3.1, the recent related q≥0 norm bounds.
- muratore2024: arXiv:2409.00436v1, the already proved universal
  maximal relaxation-rate bound; it is credited rather than claimed here.

The stable scientific arguments are evidence/research/all-q-local-stability.md
and evidence/research/n2-equality-and-local-maximum.md. These preserved
files belong to the accepted scientific evidence; they were not rewritten.
The current manuscript gives a self-contained corrected argument.
All supplied exact programs and their scientific logs are listed in
publication.json and reproducibility/README.md. Original source.md
is byte-for-byte preserved. checkpoint.md and state.json are handoff
files and are not scientific or manuscript inputs.

## Venue and author decisions

Proposed target: Quantum Information Processing, Regular Article.
The current official scope, article type and LLM policy were checked;
the source-backed comparison is venue/aims-and-policy.md.
Ranking and indexing remain unverified. The analytical emphasis may
make LAA an alternative, but current LAA author/scope pages could not
be fully retrieved. No external contact or submission has occurred.

Confirm the supplied draft name **Xiaojian Zeng**, affiliation
**PBC School of Finance, Tsinghua University, 100190**, and email
**xiaojianzeng@foxmail.com**. Confirm authorship eligibility, scientific
responsibility, actual intellectual contribution, affiliation, funding,
competing interests, archive and code license. Review and edit the
paper and choose the final journal before any submission.

OpenAI Codex participated in literature screening, idea generation,
derivations, symbolic code, calculations, scientific checks and writing.
The manuscript discloses this. Neither the automated checks nor the
fresh internal science referee establish completed human review or
external peer review. The journal’s human-accountability requirement
therefore remains a real pending decision; ai_policy_status is
needs_author_judgment, not an invented author approval.

The local packet excludes third-party full papers, screenshots,
literature caches, raw web observations and private workflow logs.
Its redistribution scope was checked, but actual public distribution
and licensing remain subject to author approval. The downstream fresh
release job still needs citation, clean-build and every-page visual
audits. This handoff does not assert those independent acceptances.
