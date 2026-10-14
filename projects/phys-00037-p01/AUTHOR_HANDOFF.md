# Author handoff: local draft requiring review

## Core result and scope

The manuscript proves only the accepted three-mode second variation for
Bravyi's complete unrestricted qubit/Majorana attenuation channel:
`0 <= b6 <= ... <= b1 < 1`, at `g=|+++>`. All fourteen real pure-state
gradient entries vanish, the Hessian is positive semidefinite, and its
Gaussian-normal cross block is zero. The two-dimensional normal span is
`span_R{|-+->, i|-+->}`. In the stated normalized chart,
`H_Im >= H_Re >= 2 b1^2 (1-b1^2)^4 / (65 ln 2)`.
For `b1>0` both normal curvatures are positive; at `b1=0` the map is
depolarizing and all derivatives vanish. The entropy and coordinate curvature
are in bits. No noise-parameter perturbation or tail truncation is used.

The original global/all-n entropy conjecture remains unresolved by this work.
The result includes zero/repeated smaller attenuations, and excludes b1=1,
strict nonlinear local minimality along Gaussian zero modes, distant minima,
higher modes and new capacity formulas. The Gaussian family includes linear
Majorana generators. Do not impose definite parity or claim an isolated-
fermion SSR-limited communication rate for the unrestricted qubit input.

## Hardest checks for the human author

Read the normalized-density second variation and resolvent prefactor in
Sections 3-4; omitting the normalization term gives the wrong Hessian.
Check the full complex Gaussian tangent rank and flip-support selection
argument, including repeated eigenvalue divided differences. Check the
analytic worst-f reduction, all finite Bernstein degrees and the positive
4/5 slice. Verify the factor 2/(65 ln 2) in the conservative integral bound.
The manuscript uses Bravyi's Gaussian minimum only on the Gaussian tangent,
and never assumes its all-input conjecture.

The exact portable checker regenerated and matched all 37,320 rational
coefficients, 192 source matrix entries in each of two constructions,
tangent rank 12, 384 CP flip-support identities, and the published one- and
two-mode rational spectra. Twenty-nine floating Hessian checks are included
only as convention diagnostics. Generic libraries and primary-source
conventions are shared; code agreement cannot replace mathematical review.

## Materials and reproduction

The manuscript is `manuscript/main.tex`, with `manuscript/references.bib` and
the portable `manuscript/build.py`. `supplement/README.md` gives complete
commands and environment versions; `supplement/SOURCE_MAP.md` identifies
the checked primary versions and exact source loci. The source supplement
contains the complete witness plus generating and two replay implementations.
It is network-free and does not need the downloaded paper cache. Its witness
is byte-identical to the accepted one; ports change paths and labels only.

The local writer portability results are saved separately as
`evidence/write-a1b7a981ff57-portability.json` and its actual log. These are
writer checks, not a new scientific acceptance. The original scientific
snapshot and the fresh science referee report are preserved unchanged.
The concise mutable checkpoint is not a derivation or publication dependency.

## Venue, priority and pending author decisions

The source-backed local target is Quantum Information Processing, original
paper; see `venue.json` and `venue/aims-and-policy.md`. The scope is plausible,
but no editorial-interest guarantee or ranking/indexing claim is made.
The current official AI policy requires **author judgment**, because this
project involved AI-origin analytic work and autonomous internal checks.
Compatibility cannot be asserted by a disclosure alone. The author must
decide whether the documented research process can satisfy publisher policy.
The journal's guidance on unpublished references also requires attention:
checked author preprints are cited explicitly, without inventing final
publisher-body verification. Confirm or revise that presentation before
submission, keeping checked source versions traceable.

Confirm the supplied author name (Xiaojian Zeng), affiliation (PBC School of
Finance, Tsinghua University, Beijing 100190, China) and email
(xiaojianzeng@foxmail.com). Confirm who can take intellectual accountability,
provide a real human contribution statement, and confirm funding and
financial/nonfinancial interests. No absent funding or interests are presumed.
Independently assess priority and significance; current exact-claim searches
are bounded and cannot prove exhaustive novelty or present openness.

## AI disclosure and remaining review

OpenAI Codex contributed to ideas, derivation, code, exact checks, literature
screening and writing. A separate Codex session reconstructed the accepted
science and performed an internal audit. This is not external peer review,
and the human has not yet verified all content. The paper says so explicitly.
The exact model/runtime identifiers are not asserted by this writer; use
the supervisor's real routing/usage records when preparing a final declaration.
Do not infer them from a tool name or invent completed human supervision.

The selected source files contain original project TeX/Bib/code and the
project-generated exact witness. Third-party full papers, web caches, job
records and private logs are excluded from submission selection. This scope
check is not a copyright transfer or final authorship approval.

A fresh release job must still verify material citations, scope and policy,
perform its own clean build and every-page inspection, and validate the
portable submission selection. This writer has not created final audit
acceptances, activated a release, submitted externally or claimed publication.
