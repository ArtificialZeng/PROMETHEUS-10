# Author handoff

## Draft status and core claim

This is a local `resolution-paper` draft for author review, not a submission or
publication. In the finite open Sierpinski--Hanoi model, restricted to the
canonical all-cycle-`+1` single-particle sector, the two depth-five spectral
landmarks are exact transverse crossings at `J=+/-1/3` and source
`lambda=1/6`. Their unique nonzero continuation is
`J_k=+/-3^(-(k-3)/2)`, with multiplicity
`(3^(k-2)+1)/2` per eigenvalue sign and exact scale ratio `1/sqrt(3)`.
On the fixed intervals `[1/4,1/2]` and its negative, the tracked minimum is
zero only at `k=5`; moving windows centered on `J_k` have zero minima at every
depth.

## Hardest checks completed

1. The primary v2 paper was reconstructed at its normalization, orientation,
   cycle-sector, finite-boundary, and local-field conventions. Two independent
   graph constructions reproduce the complete depth-five source spectrum.
2. The all-depth proof fixes the inherited copy holonomies and the quotient
   macrocycle sign before Schur elimination. A direct finite-class gauge check
   and fresh-referee graph construction challenged this step.
3. The rational corner response was lifted to a division-free three-polynomial
   recurrence that retains the cycle-flat factors. Full direct characteristic
   polynomials at depth six agree at held-out rational couplings.
4. The flat-locus induction gives the complete residual factor, not a numerical
   fit. Exact arithmetic checks the depth-five and depth-six multiplicities;
   independent direct spectra extend through depth seven.
5. The fixed-window correction was separately replayed with exact coefficient
   arithmetic. Numerical eigensolvers are used only as corroboration.

The accepted scientific audit is in `audit/science.md`; the paper-facing proof
is `manuscript/main.tex`. The clean draft is `build/main.pdf`.

## Source and reproducibility map

- Defining primary source and conventions: `source-ledger.json`,
  `evidence/source-reconstruction.md`.
- Input reconstruction and source-spectrum baseline: `reproduction.json`,
  `evidence/input-a.json`, `evidence/input-b-independent.json`.
- Exact depth-five factorization: `evidence/exact_k5_degeneracy.py`,
  `evidence/check_exact_k5.py`, and their JSON certificates.
- Signed recurrence: `evidence/cycle_schur_pass3.py`,
  `evidence/check_cycle_schur_pass3.py`, and the frozen recurrence records.
- All-depth scaling and direct depth-six replay:
  `evidence/flat_crossing_scaling_pass4.py` and
  `evidence/check_flat_crossing_scaling_pass4.py`.
- Fixed-window bound: `evidence/fixed-interval-gap-salvage-result.md`.
- Figure and tabulated data: `manuscript/generate_figures.py` and
  `manuscript/data/crossing_data.csv`.
- Exact commands and environment: `manuscript/README.md` and
  `manuscript/requirements.txt`.

## Scope and caveats that must remain explicit

- No result is claimed for another cycle sector, a physical fermion-parity
  projection, a many-body gap, an experiment, or a thermodynamic phase
  transition.
- The three-scalar recurrence is not claimed minimal, and no universal
  characteristic-polynomial-only no-go theorem is claimed.
- The literature search is bounded. The prospective author should repeat it
  with the databases available to them before making a priority statement.
- The direct higher-depth spectra are checks, not the all-depth proof.

## Venue and policy fit

`venue.json` records Quantum as a plausible original-research target. Its
official scope includes theoretical quantum science and the defining model was
published there, but the journal's significance threshold is high and fit does
not predict acceptance. Quantum requires an arXiv quant-ph posting or
cross-listing for submission; none has been made. Its current author guidance
requires detailed AI-use disclosure. The draft includes a broad disclosure and
does not say that the prospective author has already verified the work.

## AI involvement and pending author decisions

A large language model contributed to topic development, literature screening,
derivations, code, symbolic and numerical work, checks, figure generation, and
drafting. Before any submission, Xiaojian Zeng must independently review and
correct the primary-source reconstruction, proofs, code, computations,
bibliography, figure, disclosure, author name, affiliation, email, and venue
fit, and then explicitly assume responsibility.

The author must also decide or supply: final title and venue; contribution and
AI-use statement; funding and acknowledgments; conflicts; code/data license and
public archive; arXiv category and license; and whether the result meets the
target venue's significance threshold.

## Redistribution check

The proposed submission bundle contains only newly authored manuscript files,
the generated figure/data, handoff and reproducibility instructions, and
project-generated code/certificates. It excludes downloaded third-party PDFs,
the source-figure raster, job records, audit logs, credentials, and browser
records. External submission remains unauthorized.
