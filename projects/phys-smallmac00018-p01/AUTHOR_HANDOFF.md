# Author handoff: exact indirect-gap boundary at flux one third

Status: local draft ready for fresh release audit and human author review. Nothing has
been submitted or published.

## Core accepted claim

For the frozen clean noninteracting Hamiltonian, the one-third and two-thirds global
indirect gaps are identical. With

`r_c = sqrt((69 - 11 sqrt(33))/8)`,

the common gap is positive for `1/2 <= r <= r_c` except on the direct lines
`m = +/-sqrt(3) r`. For `r_c < r <= 2`, it is negative exactly in
`m_-(r) < |m| < m_+(r)`, with the two exact parametric boundary branches stated in
the manuscript. Those branches contain distinct conduction and valence momenta and
meet the direct segments at algebraic cusps. The isolated-band Chern tuple is
`(+1,-2,+1)` inside the direct lines and `(0,0,0)` outside them. Direct-band topology
is explicitly kept separate from fixed-filling insulation.

## Hardest checks already completed

- Two independently constructed Bloch representations agree under an explicit DFT
  convention map, and the undeformed spectrum/Chern benchmark was reproduced.
- Root monotonicity in `cos(kappa)` reduces every global extremum to `kappa=0` or
  `pi`; the operator spectral reflection proves equality of the two filling gaps.
- A chemical-potential sign theorem and degree-three Fejer--Riesz factorization turn
  the global boundary into exact Fourier coefficient matching.
- Independent Laurent reconstruction derives the primitive `X,V` relation without
  importing the first reduction.
- Rational Sturm sequences classify the unique `E>=1` sector, prove the cusp and
  branch monotonicity, isolate the nonphysical stationary root, assign the two band
  roots, and exclude all division/exceptional sectors.
- A fresh scientific referee replay accepted the frozen claim at its full stated
  scope. That replay is an AI audit, not external peer review.
- The manuscript phase figure is a deterministic evaluation of the exact equations;
  its generator reproduces four accepted boundary-value pairs before writing output.

## Source and reproducibility map

- Manuscript: `manuscript/main.tex`; bibliography: `manuscript/references.bib`.
- Compiled draft: `build/main.pdf`; compiler log: `build/main.log`.
- Figure/data generator: `manuscript/generate_phase_diagram.py`; vector figure:
  `figures/phase_diagram.pdf`; samples: `data/phase_boundary.csv`.
- Instructions/environment: `manuscript/REPRODUCIBILITY.md` and
  `manuscript/requirements.txt`.
- Exact scientific checks: the five listed scripts in `scripts/`, with the central
  certificate in `scripts/certify_global_boundary.py` and clean-room reconstruction
  in `scripts/verify_laurent_reconstruction.py`.
- Accepted claim and audit: `claim.json`, `audit/science.json`, and
  `audit/science.md`.
- Venue/policy evidence: `venue.json` and `venue/aims-and-policy.md`.

## Venue fit and caveats

Physical Review B, Regular Article, is a plausible target because its current scope
includes electronic structure and topological states, and the full proof benefits from
the unrestricted Regular Article format. This is not an editorial recommendation or
acceptance prediction. Ranking status is unverified.

The result is limited to the infinite clean single-particle model. It does not cover
interactions, disorder, trapping, boundaries, finite size, calibration, or a many-body
thermodynamic transition. SymPy exact arithmetic is computer assistance, not a formal
proof-assistant verification. The representation-aware literature search supports only
bounded candidate novelty; a broader human priority search remains necessary.

## AI disclosure

The draft discloses that OpenAI Codex, identified at the available service granularity
as a GPT-5-based agent accessed in September 2026, assisted with problem formulation,
literature synthesis, derivations, verification code, numerical replay, figure code,
and writing. It states the exact and independent computational checks and does not claim
completed human verification. APS policy was checked on 2026-09-14 and permits such use
only with substantive disclosure and human accountability.

## Decisions required from the author before submission

1. Confirm author name, sole-author status, PBC School of Finance affiliation, Beijing
   postal code 100190, and `xiaojianzeng@foxmail.com`.
2. Read and independently check the central algebra, code outputs, physical wording,
   and every citation; obtain any additional expert review judged necessary.
3. Broaden the literature search, especially gauge-equivalent period-three mass
   representations, and revise novelty wording if an identical boundary is found.
4. Confirm that the exact Codex/model-version wording and service terms satisfy the
   APS policy then in force; revise the disclosure to describe the author's actual
   verification after that verification occurs.
5. Decide whether Physical Review B remains the target and whether a one-column
   preprint or reformatted two-column source should be handed to the journal.
6. Approve the data-availability wording and the exact public repository/archive to be
   cited, if any. No repository URL has been invented in this draft.
7. Request a fresh citation, clean-build, and every-page visual audit after any change.

The submission bundle intentionally excludes downloaded third-party articles, browser
records, job logs, credentials, and internal audit dossiers. Only authored manuscript,
figure, code, and data files needed for review and reproduction are selected.
