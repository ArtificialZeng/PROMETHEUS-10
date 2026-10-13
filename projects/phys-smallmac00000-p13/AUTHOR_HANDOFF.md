# Author handoff

**Local manuscript for author review.** Release audit reports are in
`audit/citations.md`, `audit/build.md` and `audit/visual.md`. Local
activation is reserved to the supervisor. No
external submission, journal acceptance, human scientific approval,
SCIE indexing or ranking is asserted. The result is a restricted
`result-note`; the original dissipation-profile classification remains
unresolved.

The draft author metadata follows the explicit current workflow:
**Xiaojian Zeng; PBC School of Finance, Tsinghua University, 100190;
xiaojianzeng@foxmail.com.** Please confirm these details and the relevant
authorship criteria before any use outside this local workflow. Their
inclusion does not constitute institutional endorsement or completed
human author approval. Funding, competing interests, author contribution
declarations and any future submission decision remain unconfirmed.

## Core result and strongest checks

The finite open XX spin model, local end baths and dephasing convention
are fully stated in the article. With odd centered chains, kappa/J=4,
mu=1/2, eta/J=5, and gamma_0/J=c/N or c/(N-1), each fixed finite c>0 has
stationary natural-occupation spacing tending to 1/(36+4c), and central
orbital IPR tending to 51/125. Stationarity comes first. Dimensional c
must be divided by J. The spectrum concerned is that of the equal-time
covariance, not the many-body state or any relaxation generator.

The hardest checks for the author are the second-eigenvalue interlacing
index, the two-dimensional sine subspace, the endpoint residual sign
and normalization, and the residual-to-vector-to-IPR inequalities.
Pointwise convergence of matrix entries is insufficient because the
far-edge diagonal variation stays finite. The article supplies the
finite-size arguments and keeps the original source's current
normalization qualification explicit in Appendix A.

The accepted internal scientific review is `audit/science.md`, tied to
`audit/science.json` and the unchanged `audit/snapshot.json`. This was a
fresh AI context with its own exact-spin and integer/rational spectral
checks; it was not human review or external peer review, and correlated
model errors remain possible. No claim is made that the author has
verified its conclusions. Scientific changes require fresh review.

## Files and reproduction

- `manuscript/main.tex`, `references.bib`, `main.bbl`, `figures/convergence.pdf`
  and `finite-size-table.tex` form the portable article source.
- `manuscript/repro/README.md`, `reproduce.py`, `data.json`, `requirements.txt`
  and `environment.json` document and regenerate the numerical illustration.
- `manuscript/build.py` builds into a new empty local directory and retains logs.
- `evidence/write-65fbc7ab9205/manuscript-source-map.md` maps each equation,
  plotted value and citation to accepted scientific evidence or primary sources.
- `publication.json` specifies the local build PDF and the exact source and
  handoff file lists. The release job used
  `build/final-release-1281c1befa6a/main.pdf`; final audit JSON records bind
  the exact reviewed sources and PDF. The source map and dependency update
  is `evidence/release-1281c1befa6a/release-preparation.md`.

The writing-phase numerical reproduction checked all 24 existing cases;
maximum spacing/IPR differences from the reference were 2.92e-16 and
7.22e-16. The maximum zero-vector residual was 2.50e-16. Four largest-size
cases also used an 80-digit recurrence and an alternate QR calculation.
Finite-size errors are much larger: at N=2561 the spacing differs from
its limit by about 1.6% or 4.1% for c=1/2 or 2. These precision diagnostics
are not interval enclosures. No new parameter search or central result
was introduced in the writing phase.

## AI involvement and policy decisions

AI tools contributed substantially to formulation of the restricted
question, analytic argument discovery, code, numerical calculations,
literature searching/comparison, internal checks and drafting. The
current worker is an OpenAI Codex GPT-6-based assistant; exact deployed
model revisions for every historical research/checking pass are not
established by the scientific evidence inspected in this writing job.
They must not be invented. The manuscript's Acknowledgements discloses
the substantive Codex assistance without claiming completed human
verification. Before external use, supply the complete actual model and
version details required by the selected venue and critically review
the text, calculations and bibliography yourself. The disclosure must
not be reduced to grammar assistance.

JSTAT's official scope and **standard research paper** route were
checked; `venue.json` and `venue/aims-and-policy.md` record the evidence.
Its policy allows some disclosed AI uses but requires author critical
revision, reference verification, detailed tool/model/version disclosure
and rights assessment. This draft therefore has
`ai_policy_status=needs_author_judgment` and human author approval pending.
No account privacy/training settings or contractual terms were inspected
or changed. Policy compliance cannot be inferred from an internal
scientific acceptance. The current AI audit was internal development,
not a journal reviewer service or an external report.

## Scope and transfer

The known resistance law, tridiagonal moment structure and imaginary-
impurity orbital are explicitly attributed. Novelty support is bounded;
the author should assess whether the finite-total-noise joint limit has
sufficient independent interest for the target journal. No general
defect threshold, XY extension, off-center result, protected memory,
experimental observation or reverse-order limit has been established.

The handoff selection contains only locally authored article/code/data
and this handoff. Downloaded third-party papers, primary-page captures,
private job logs and internal scientific reports are excluded from the
submission file list. No license on third-party material is granted by
this package; author rights and final publication license remain for
the author. The local handoff bundle is not yet a journal upload archive:
JSTAT requires main.tex at its root and separate supplements. No cover
letter, funding declaration, human-approval statement or repository DOI
has been fabricated.

The release pass repaired two malformed odd-size limit subscripts and
moved the figure panel labels clear of plotted curves. No scientific
input or numerical data changed. The final clean build has seven pages;
each was visually inspected. All five citations were checked against
primary sources, and the portable reproduction reran all 24 cases.
The code still uses one numerical thread and the same recorded environment.

One next test: the supervisor should run the bound release check, locally
activate the PDF, then make and check the explicit handoff bundle. The
archive checker needs that activated manifest and cannot certify a bundle
that has not yet been made. Human scientific and authorship review, the
model/version inventory, and venue-policy/rights decisions remain pending
before any external use. Scientific changes require fresh independent
review; manuscript changes require a renewed snapshot and affected release
audits.
