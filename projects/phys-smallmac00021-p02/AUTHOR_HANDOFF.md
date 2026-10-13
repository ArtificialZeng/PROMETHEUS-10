# Author handoff

## Core claim

Within the reproduced co-propagating short-wave, cubic-order
constant-vorticity capillary--gravity model, the unrestricted real
dispersion-plus-resonance system has exactly two total-sign-related frequency
sheets. On either sheet the cubic numerator has an exact rational form, and
for every distinct positive pair (k1,k2) there is exactly one positive
r=g/sigma at which it vanishes. The physical positive-frequency sheet has
negative vorticity at that zero.

The original full-Euler/higher-order question remains unresolved; the article
is a scoped result note, not a full resolution.

## Hardest checks already completed

- The cubic numerator was reconstructed term by term from the primary
  arXiv-v1 Hamiltonian and independently replayed by the scientific referee.
- A no-squaring derivation proves completeness of the two real sheets.
- Exact symbolic identities prove the rational C formula and quartic
  factorization; positivity and endpoint signs prove uniqueness.
- Adversarial back-substitution covered near-equal, strongly separated, and
  ordinary integer wave-number pairs, plus the N=0 boundary.
- The accepted science snapshot passed the release gate before drafting.
- Martin--Basu (2021) was mapped equation by equation and is credited for the
  positive-sheet resonance magnitude and capillary negative-root uniqueness.
- Constantin--Kartashova--Wahlén (2010) was added as the closest
  pure-capillary coupling-coefficient antecedent, as requested by the fresh
  referee.

## Caveats requiring author attention

- Zero cubic coupling does not imply no transfer at higher order or in the
  full Euler equations.
- The finite-depth multiplier, counter-propagating/noncollinear triads,
  dissipation, detuning, stability, and experimental accessibility are not
  covered.
- Formula-error statements are deliberately restricted to the inspected
  arXiv v1; the publisher equation rendering was not accessible.
- The literature search was bounded and cannot establish global priority.
- The journal AI policy requires author-led scholarly judgment and human
  accountability. This draft involved material generative-AI work and is
  currently marked needs_author_judgment; it must not be submitted as-is.

## Source map

- Model and cubic coefficient:
  'intake-evidence/primary-sources/phys-00021-p02-01-1911.05213v1.pdf'
- Accepted proof:
  'evidence/resonance-classification.md'
- Independent referee report and replay:
  'audit/science.md', 'audit/replay.log'
- Closest-prior comparisons:
  'evidence/martin-2017-comparison.md',
  'evidence/martin-basu-2021-comparison.md',
  'audit/novelty-search.md'
- Reproducible checker:
  'scripts/resonance_classification.py',
  'evidence/resonance-classification.log'
- Manuscript:
  'manuscript/main.tex', 'manuscript/references.bib'

## Venue fit

The proposed venue is the Journal of Mathematical Fluid Mechanics as a
standard original research article. Its official scope covers rigorous
mathematical fluid mechanics, and the closest 2017 precursor appeared there.
No ranking claim was verified. The standard local article class should be
converted to the current Springer Nature template if the author chooses this
venue.

## Decisions pending from Xiaojian Zeng

1. Verify every derivation, citation, source-version caveat, and numerical
   illustration personally; revise or reject the scientific framing.
2. Confirm name, PBC School of Finance affiliation, Beijing 100190 address,
   and xiaojianzeng@foxmail.com.
3. Supply accurate funding, competing-interest, and contribution statements.
4. Decide whether the level of AI involvement is compatible with the intended
   venue after consulting the current editor/policy; revise the declaration.
5. Decide whether to target JMFM and, if so, adopt its current LaTeX template.
6. Do not submit externally until a fresh release audit and the author's own
   review are complete.
