# Author handoff — local draft, 2026-10-12

Status: draft_ready_author_review_required. No external submission or author approval has occurred. The writing job prepares this for a fresh release review; it does not provide that review.

Core claim: for every two-qubit state and local unital CPTP qubit channel, entropy-based one-sided diagonal discord is nonincreasing if the measured marginal is nondegenerate before and after the channel. This is the accepted frozen resolution-paper/proved scope, not the entire broader published conjecture. Rank-deficient global states and arbitrarily small positive gaps are covered. The exact loss splits into data-processing loss and comparison-state mismatch.

Hardest checks for human review: E(P-)=I-E(P+) uses unitality; the affine output marginal identifies the comparison state's output block algebra; fixed pinching rather than nonlinear state-to-basis assignment is used in relative-entropy reasoning; singular-state support inclusions follow from rho<=2 Delta rho and positivity. Equality classification, degenerate marginals, arbitrary distances, larger spectator dimensions and nonunital channels are not claimed. Independently accepted AI scientific review is in audit/science.md; it is not external peer review.

Source map: manuscript/main.tex and manuscript/references.bib cite primary S1 (Liu/Takagi/Lloyd, J Phys A 52 135301, DOI 10.1088/1751-8121/ab0774; arXiv1708.09076v2, Eq8, Eq11, Corollary4, Conjecture1) and S2 (Liu/Hu/Lloyd, PRL118 060502, DOI 10.1103/PhysRevLett.118.060502; arXiv1606.03723v4). Stable proof evidence/monotonicity-proof.md. Standard ingredients/common-eigenbasis observation are credited; only their application is the contribution. Current bounded search found no later exact resolution; priority is not guaranteed. See write/literature-check.md.

AI: OpenAI Codex assisted ideas, proof development/checking, code, literature discovery and manuscript text; a separate AI session checked the argument with independent code. Underlying model version was not independently recorded. The draft methods and acknowledgement statements honestly say human review remains pending. Do not substitute the publisher's completed-review template before that review occurs.

Target: Journal of Physics A: Mathematical and Theoretical, Paper, because quantum correlations/open systems are in scope and the source conjecture appeared there. Editorial significance is not guaranteed. Current policy permits disclosed research/drafting use conditionally on human validation; venue.json uses needs_author_judgment. Ranking/SCIE/quartile are unverified. See venue/aims-and-policy.md. The author must critically revise prose, inspect source references, verify calculations and accept responsibility before submission.

Confirm author details: Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190; xiaojianzeng@foxmail.com. No institutional endorsement is implied. Confirm address spelling, affiliations, authorship eligibility, funding/conflicts and data/repository plans. No self-citation quota applied.

Reproduction: reproducibility/README.md and requirements.txt; existing code/data are own synthetic outputs. The submission list contains own TeX/Bib/proof/replay code/data and this handoff, but no downloaded third-party papers, raw web captures, internal acceptance reports or mutable handoffs. Downloaded sources remain preserved in the local dossier. Human approval is required before choosing a public supplement or journal submission.

Next test: a fresh release reviewer checks citation attribution and source dependency closure, rechecks the actual clean compiler log, and renders/inspects every PDF page. Human scientific/authorship review remains required thereafter.
