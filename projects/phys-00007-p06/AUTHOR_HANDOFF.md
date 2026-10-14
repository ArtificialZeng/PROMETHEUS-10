# Author handoff — local draft, 2026-10-12

The draft proves t5=sqrt(3/8) in the original single-copy five-pure-state
model in C^5, permitting dependent states and zero POVM effects. The exact
rank-three family has all squared overlaps m for 3/8<m<2/5 and a physical
dual of trace s eta>0. Equal-prior exclusion error is at least s eta/5.
The boundary is excludable: this is an infimum approached from above.

Hardest checks for human review: the D identity and parameter positivity;
both physical-projector Schur complements; finite-step loss control;
the distinction between a Hilbert-space dual and a Gram-label witness;
the embedding in C^5; and the published sufficient bound including equality.
The accepted fresh internal AI referee record is audit/science.md, with
independent replay audit/replay.py and audit/replay.log. This is not external
peer review. Stable proposer proof: evidence/five-state-proof.md.

Source map:
- manuscript Section 1 and lower bound: Johnston–Russo–Sikora, Quantum 9,
  1622 (2025), Corollary 5.4, Eq. (2), Section 6; preserved publisher
  PDF in supervisor-inputs/antidist-primary/Johnston-2025-published.pdf.
- follow-up comparison: arXiv:2609.17411v1, Section 1.1 and Section 3;
  accepted excerpts in literature/research-current-web.json and
  literature/research-section3-web.json; writing recheck in venue/.
- new construction and certificate: evidence/five-state-proof.md;
  manuscript Sections 2–4 express only the accepted scope.
- supplementary exact checks: evidence/verify-five-state-certificate.py
  and evidence/five-state-verification.log; regeneration in reproducibility/.

Quantum is the proposed original-research venue: exact state-exclusion
scope and the directly related Quantum article support fit. Official scope
and AI policy are documented in venue/aims-and-policy.md. Rankings are
unverified; editorial suitability and publication are not guaranteed.

Codex contributed to ideas, proof development, exploration, calculations,
code, searches, internal verification and writing. The manuscript says so.
The author must review and decide whether to adopt the work and disclosure;
no completed human contribution or approval is asserted.
Confirm Xiaojian Zeng, PBC School of Finance, Tsinghua University, 100190,
and xiaojianzeng@foxmail.com.
No n>=6 threshold, exact optimum-error, noise-robustness or experimental
claim is established.

The explicit submission file list excludes third-party PDFs, literature
captures, queue/job logs, and audit records. Included text/code are authored
project artifacts; the original proof is paraphrased into self-contained
manuscript equations and primary-source findings are attributed.
No third-party code or figures are copied; SymPy is a dependency, not bundled.
Human rights and authorship confirmation remains pending.

Next step: fresh release-role citation, clean-build and every-page visual
review. Do not submit externally without separate authorization.
