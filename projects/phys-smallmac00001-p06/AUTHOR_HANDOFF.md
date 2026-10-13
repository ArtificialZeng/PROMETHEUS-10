# Author handoff: local draft requiring review

The local manuscript is **A missing spectral arc at finite cycle affinity in
four-state Markov generators**. Its accepted scope is a `resolution-paper`
disproving the frozen spectral-set equality at B = log(3)/2. This means the
specified equality is false; it does not mean the entire attainable spectral
region has been classified. The draft has not been externally submitted,
editorially accepted, or approved by the human author.

## Core result and why it matters

For all sufficiently small positive delta, every four-state generator with
escape rates at most one and all oriented cycle-product bounds satisfies

    |Im lambda| <= 1/2 - delta/2 + delta^2/4,
    delta = -1 - Re lambda.

The explicit compressed companion point

    Lambda(delta) = -1 - delta + (i/2)sqrt(1 - 2 delta + 3 delta^2)

violates that bound, yet its uncompressed preimage is an eigenvalue of an
unrestricted generator with escape rate exactly one. The exclusion holds
even in the larger compact class, so every excluded point is separated from
its spectral union by a positive, existential distance. The physical
consequence is a missing set of normalized decay–frequency pairs at fixed
driving, caused by triangle constraints opened when chords are added to a
biased square.

## Scientific review priorities

1. Independently check the source Theorem 3 and its SM3/SM5 equality chain,
   including arbitrary finite generators, admissible winding, and the
   strict Jensen step. These imply the full-class endpoint rigidity.
2. Check the slack signs, exact logistic coordinates, and uniform Taylor
   remainder in Section 4. The proof allows all four escape deficits and
   unused mean affinity. It does not assume a smooth feasible family.
3. Check the coercive bootstrap in Section 4.2 and the triangle estimates
   on zero-chord faces in Section 5.1. They are what turn a quadratic
   calculation into a universal local exclusion.
4. Check compact globalization and the exact-rate companion. No global
   equality of exact-alpha and bounded-alpha stochastic spectral unions
   is needed, and no finite scan is treated as a proof.

The actual fresh scientific referee accepted the unchanged claim. This was
an AI review in a fresh context, not external peer review or human review.
The writer replayed the packaged algebra: 19 symbolic checks, all 28
Gaussian-rational quadratic coefficients, and five slack directions pass.
The original referee code and records remain intact. Detailed provenance
is in manuscript/source-map.md and manuscript/provenance.json.

## Limits that must remain in any submitted version

- Eta is existential, without a numerical value or distance enclosure.
- The upper coefficient 1/5 is not proved sharp or attainable.
- The original test point at companion parameter t = 1/2 remains undecided.
- No complete boundary, general inclusion theorem for the compressed
  region, larger-state theorem, or experimental prediction is supplied.
- The finite-dimensional model is exact. The local expansion has a uniform
  remainder; it is not an uncontrolled perturbative model truncation.
- Novelty comparisons concern the four checked primary works. No exhaustive
  priority search or journal-acceptance guarantee is asserted.

## Draft identity and declarations needing confirmation

The supplied draft identity is **Xiaojian Zeng**, **PBC School of Finance,
Tsinghua University, 100190**, **xiaojianzeng@foxmail.com**. Confirm the exact
affiliation format, corresponding-author details, authorship eligibility
and consent before any external action. The displayed affiliation is not
an automated institutional endorsement. Funding, conflicts of interest,
authorship contributions and a public repository/license have not been
declared on the author's behalf and require actual author decisions.

## AI use and provisional journal target

OpenAI Codex provided substantive assistance in topic development,
mathematical reasoning, calculation/code, source checks, internal review,
and drafting. The current writing environment identifies GPT-6; exact
deployed model/version records for preceding stages are not established in
this writing packet. The acknowledgement says this explicitly and does
not pretend that the human author verified the work. Before submission,
confirm the complete tool/model/version disclosure and critically revise
the manuscript and every reference after personal review.

The provisional target is **Journal of Physics A: Mathematical and
Theoretical**, article type **Paper**. Its official scope includes
nonequilibrium systems, stochastic processes, network theory and
mathematical physics. Uhl and Seifert's directly relevant 2019 paper is
published there. Fit is an editorial inference. The ordinary full-paper
category is used without padding to a usual length; the final article type
remains the author's decision. [Official scope and article types](https://publishingsupport.iopscience.iop.org/journals/journal-of-physics-a-mathematical-and-theoretical/about-journal-physics-mathematical-theoretical/).

The official policy requires critical human revision of AI-generated text,
disclosure of model/version/use in acknowledgements, and author checking
of references. It does not make an AI context a human author or journal
referee. Its provisions on research use, references and rights require
judgment for this extensively assisted draft; `ai_policy_status` remains
`needs_author_judgment`. [IOP generative AI policy](https://publishingsupport.iopscience.iop.org/questions/generative-ai-tools/).

SCIE/indexing and JCR/CAS/SJR system, year, category and quartile are
**unverified**. No ranking or indexing claim should be added without a
matching authoritative database check.

## Files and next review

Read manuscript/main.tex and the PDF path in publication.json. The clean
build procedure is manuscript/build.py; manuscript/README.md and
manuscript/repro/README.md give actual regeneration commands. No figures
are needed for this analytic argument. The explicit submission_files list
contains authored sources, documentation, code and exact outputs. It
excludes all downloaded third-party papers, private logs and browser data;
no public license grant has been made automatically.

The fresh release job `phys-smallmac00001-p06-release-b89f118e9c8c` rechecked all four primary citations, rebuilt in a new directory, and viewed all ten rendered pages. The final compiler log contains no warnings or unresolved citations/references. Both packaged exact replays match their expected outputs. Current release reports and digest bindings are in `audit/citations.*`, `audit/build.*` and `audit/visual.*` in the local dossier. The release worker preserves all 79 accepted snapshot files, including the historical checkpoint.

**One next test:** the supervisor runs the final structural check, local `release_gate.py publish`, then `bundle.py make` and `bundle.py check` against the exact audited PDF and listed sources. This creates only a local author-review package. The human author must then review the proof and each reference, confirm identity/model disclosure and policy/rights decisions, and authorize any later external action separately. External submission remains unauthorized.
