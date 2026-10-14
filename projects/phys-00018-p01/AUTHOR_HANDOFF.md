# Author handoff: local finite-RNA noise tradeoff

This is a local draft for scientific author review and a fresh release
review. It has not been submitted or externally published.

## Contribution and limits

The draft develops only the accepted result-note: for the exact two-gene
CTMC with parent tuples (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1),
all bounded real whole-lattice cross-protein response functions satisfy
the 4/5 return contraction. For sup-unit responses, gains a,b>0 and
S=a^2U1+b^2U2>0, every
epsilon<min(1/max(a,b),S/(4480 max(a,b)^3)) gives at least one protein
Fano factor strictly above its own mean-matched baseline 3/2 or 4/3.
Both constant responses leave both baselines unchanged.

The result is computer-assisted and local in feedback amplitude. There is
no monotonicity, smoothness or finite-plateau assumption on the response
shapes. The original arbitrary-N, arbitrary-kinetics, strong-feedback
question is unresolved. No positive amplitude radius uniform over all
shapes is proved; rare-tail and nearly constant functions can make S small.
Constants and kinetic choices are not asserted optimal or experimentally
universal. Extra biochemical channels are outside the result.

## Hardest checks for the human author

1. Read the full-space generator argument and conditional Jensen step:
   U1>=W4/187272 and U2>=3W4/102400. Do not replace these with the earlier
   stronger, unproved W2 route.
2. Check that the count-zero Riesz residual includes the aggregated tail
   equation, and that the full fourth-to-sixth moment tails control omitted
   directions relative to injection. A small additive cutoff error alone
   would not establish the theorem.
3. Inspect true-law resolvent error enclosures and exact congruence signs,
   rather than floating eigenvalues. The caps 48/128 only generate witnesses.
4. Recheck the stationary envelope coupling with the parent's covariance
   with its own half-envelope retained. It supplies the 448 cubic remainder
   without assuming stationary differentiability.
5. Confirm the exact Fano identity uses actual regulated means and the
   finite-lifetime baselines, rather than the fast-RNA burst baselines.

The manuscript gives these arguments in its main text and appendices.
Stable scientific file locators and primary citation locations are in
evidence/write/citation-and-scope-map.md. The exact supplied-data replay
and optional full-regeneration commands are in reproducibility/README.md.
The writer actually performed supplied-certificate replay in an isolated
tree and regenerated the outward-rounded numerical table. The optional
new full-regeneration wrapper was not run during writing.

## Independent review and publication boundary

The scientific scope was accepted by referee job
phys-00018-p01-referee-cf577e001b71 against frozen evidence digest
6e614ddab2b31db8a85eb89c4bb9f1e0d69c3eb041f2ce8f7c35c68f16d3b0cf.
This was a fresh AI scientific review, not external peer review or human
author validation. The writer's exact replay is an additional arithmetic
check, not a new acceptance. A fresh release job must still review
citations, build logs, every rendered page and all dependency bindings.
No writer-produced final-audit acceptance record is supplied.

All original source and accepted scientific bytes are preserved. New
manuscript and source-package files are distinct publication inputs.
Mutable operational handoffs supply no scientific or publication premise.

## Venue and current AI policy

Suggested target: Physical Review E, Regular Article. Current publisher
scope includes statistical, biological, complex-system and computational
physics. The Regular Article format allows a full account with appendices.
The fixed-kinetics restriction may limit editorial interest; this draft
does not guarantee journal suitability or acceptance. Indexing/ranking
has not been verified. See venue.json and venue/aims-and-policy.md for
primary policy links and the checked article-type evidence.

APS permits AI assistance with research and writing with substantive
disclosure, human judgment and accountability. The present work used
OpenAI Codex for reasoning, literature synthesis, derivations, code,
automated checks and drafting; this is substantially more than polishing.
The paper discloses those uses and explicitly records pending human review.
The human author must review, refine and take responsibility before any
submission, document actual direction and checking, and confirm tool/model
versions and applicable terms. No completed human verification is invented.

The supervisor's authorized operating policy selected gpt-6.1-sol with
max reasoning after a bounded gpt-5.6-sol fallback. The current role record
does not authenticate the actual per-call model/version for all prior
phases. Reconcile the supervisor's execution/usage records before making
an exact multi-phase model disclosure. Missing execution details remain
unknown. Policy status is needs_author_judgment.

## Author decisions still pending

Confirm the supplied draft identity: Xiaojian Zeng; PBC School of Finance,
Tsinghua University, 100190; xiaojianzeng@foxmail.com. Confirm authorship,
affiliation/address formatting, contributions and responsibility.
Review the scientific argument and priority assessment, approve or revise
the AI disclosure, choose a final venue and decide on a public data/code
repository and licensing. There is no public repository identifier yet.
No human approval, external communication or submission occurred here.

## Source selection and redistribution

The proposed source bundle explicitly lists the authored TeX/Bib,
generated table, handoff, reproducibility scripts/environment and the
necessary original calculation code and exact data. No downloaded
third-party paper, publisher-page cache, job transcript, mutable handoff
or credential is selected. The local source map retains third-party
locators so the reviewer can inspect the preserved private literature
cache separately. No third-party figure is reproduced. Imports of NumPy,
SciPy and system TeX packages do not bundle those packages.

The scope check establishes a suitable local source selection; it does
not replace the author's rights, licensing or AI-terms judgment.
