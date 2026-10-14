# Author handoff: exact single-use noisy rotation sensing

This is a local result-note draft prepared for human author review.
It has not been externally submitted, and human authorship approval is pending.
The supervisor's frozen scientific acceptance is retained unchanged; automated
acceptance is not external human peer review.

The core claim is limited to one fixed Bell probe, one untouched ancilla,
U_theta=exp(-i theta dot sigma), known depolarization lambda in [0,1],
uniform Cartesian volume on the radius-pi/4 ball, and one-third coordinate
squared error. The optimum over all physical joint POVMs and estimators equals
the Bayesian NH relaxation:

    R1(lambda)=CNH(1,lambda)=pi^2/80-4(1-lambda)^2[3/(2pi)-12/pi^3]^2.

A four-outcome rotated-Bell PVM attains it, implemented by a fixed system
rotation V0^dagger followed by a Bell measurement. Posterior estimates shrink
by 1-lambda. A normalized covariant sphere POVM is also optimal. The original
attainment question for all k=1,2,3,4 remains unresolved because k=2,3,4
have not been settled. No arbitrary-probe, adaptive or experimental optimum
is claimed.

The hardest author checks are the Choi trace/swap and sigma_y convention;
the Cartesian-volume radial weight; the NH dual affine equations over the
full complex Hermitian program; its positive Gram factorization; and the
fixed local rotation/Bell identity. Review Secs. II--IV and both appendices,
using `evidence/research/k1-attainment.md` and the stable source derivation.
`manuscript/source-map.md` maps each argument to these inputs. The supporting
operator in Appendix A proves physical optimality for all real estimates.
The exact NH certificate supplies the separate relaxation equality.
Numerical integrations and solver outputs are corroboration, not proofs or
certified numerical enclosures.

Current primary literature was rechecked before drafting. The direct source
still reports numerical near-attainment; the closely equivalent star-moment
phase-imaging work and the older local rotation construction are credited.
The priority search is bounded. The author should assess the exact construction
against those papers, rather than claim invention of Bell measurements,
covariance, posterior estimation or SDP duality.

The provisional target is Physical Review A, Regular Article, based on the
official quantum science/information scope, current article-type guidance and
the nearby Rubio/Dunningham PRA publication. The venue record is `venue.json`
and `venue/aims-and-policy.md`. Ranking is unverified. Fit does not guarantee
the significance threshold, editorial acceptance or any quartile.

OpenAI Codex substantially assisted with discovery/derivations, scientific
code, symbolic and numerical verification, literature comparison, figure
generation and writing. A separate AI context reconstructed and checked the
restricted science. The manuscript discloses this and pending human review.
The writer's role metadata does not expose the deployed model/version;
confirm actual discovery/review/writing tool versions from genuine runner
usage records before finalizing the APS disclosure. Do not infer them solely
from a preferred-model policy. The author must document their own direction
and scientific verification and confirm tool terms/rights. The current policy
status is needs_author_judgment. No completed human validation is invented.

Please confirm the supplied byline and contact details: Xiaojian Zeng;
PBC School of Finance, Tsinghua University, Beijing 100190, China;
xiaojianzeng@foxmail.com. No institutional endorsement or funding statement
has been inferred. No unrelated self-citations were added.

Reproducibility instructions are in `manuscript/REPRODUCE.md`; the wrapper
runs copies so frozen evidence is not overwritten. The explicit submission
file list in `publication.json` contains own manuscript/figure/code and
necessary project inputs/derivations. Full third-party papers, screenshots,
raw retrieval logs, job records and audit dossiers are excluded after a
file-by-file scope check. No external upload or publication is authorized.

The release worker checked current primary citations and accepted scope,
reproduced the analytic figure, rebuilt from an empty output directory,
and viewed every page. The final reviewed PDF is `build/release-clean/main.pdf`.
The release audits and their evidence stay in the local dossier. AI assistance
is stated at the analytic methods, figure caption, and acknowledgments;
actual versions and human verification remain pending, so this is not a
claim of complete APS submission-policy compliance.

Next gate: the supervisor checks and activates the local release and creates
and checks the explicit source bundle. Human scientific review, substantive
authorship, byline/affiliation confirmation, tool-rights and version disclosure,
and final author approval remain necessary before any external submission.
