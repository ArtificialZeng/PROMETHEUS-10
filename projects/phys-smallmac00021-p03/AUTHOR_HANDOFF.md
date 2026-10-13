# Author handoff: breathing-kagome spectral-count Comment

Status: local draft ready for fresh release review and then substantive human
author review. No external submission is authorized or claimed.

## Core accepted claim

For the Fig. 3 interpolation of Geschner *et al.* at `t=0`, `t'=1`, the
author-raster-defined 15-site invariant corner component has

`chi(E,lambda)=(E-1)^2 P6(E,lambda) P7(E,lambda)`.

The coefficient gcd in `Q[E]` is exactly `(E-1)^2`, so 13 roots per corner,
counted with algebraic multiplicity, are nonconstant. The exactly checked
three disjoint N=20 components therefore give 39, not the 36 inferred from
the paper's count 12. This is a finite spectral-bookkeeping correction. It
does not change the source's conclusion that the zero mode is removable.

The manuscript also reports two accepted secondary results at their narrow
scopes: an exact absence of a finite single-sublattice kernel for the balanced
`t=0.1` deformation, and an exact N=20 opposite-mirror-parity crossing in the
recorded rational lambda bracket. The edge multiplier explains alternating
finite-size convergence only at controlled numerical level.

## Hardest checks to repeat

1. Compare the 15-site/17-edge list in `manuscript/main.tex` and
   `evidence/isolated-corner-polynomial.json` directly with the official PRB
   Fig. 3, not only with the archived author raster.
2. Run both central scripts in a disposable copy. Confirm the endpoint
   polynomials, all 122 nonzero bivariate coefficients, the coprime
   `lambda^11`/`lambda^12` witness, and both unused rational holdouts.
3. Run `scripts/certify_parity_crossing.py` and inspect the exact inertias and
   strict order reversal rather than relying on the approximately
   `3e-13` floating-point separation.
4. Check every manuscript statement against `claim.json`,
   `verification.json`, and the accepted referee report. In particular, keep
   algebraic root count distinct from distinct plotted curves, localized
   states, isolated eigenvalues, and bulk/topological invariants.

## Source map

- Corrected paper: C. K. Geschner, A. Y. Chaou, V. Dwivedi, and P. W.
  Brouwer, *Phys. Rev. B* **113**, 155151 (2026), DOI
  `10.1103/vfyz-74qy`; exact statement is in Sec. III immediately after Eq.
  (5), with the deformation in Fig. 3.
- Author preprint/source raster: arXiv:2412.20460v1 and
  `literature/2412.20460v1-source/figures/interpolation.png`.
- Earlier robustness baseline: M. A. J. Herrera *et al.*, *Phys. Rev. B*
  **105**, 085411 (2022), DOI `10.1103/PhysRevB.105.085411`.
- Exact central evidence: `evidence/isolated-corner-proof.md`,
  `evidence/isolated-corner-polynomial.json`, and the two central scripts.
- Independent scientific audit: `audit/science.md` and `audit/replay.log`.

## Venue fit and caveats

The working target is a *Physical Review B* Comment because PRB explicitly
defines that article type for corrections to specific PRB papers. The title
and abstract follow the current Comment guidance. The result is exact but
narrow; PRB may decide it does not meet its significance threshold. Current
guidance encourages contacting the original authors before submission. Venue
scope and AI-policy sources are recorded in `venue/aims-and-policy.md`.

Unresolved exclusions include the original general connectivity iff,
crossing uniqueness, small-flake overlap outside the verified N=20
decomposition, a complete corner-core/edge secular limit, thermodynamic
persistence, experimental realization, and any new topological phase claim.
Global priority and unpublished author calculations are not known.

## AI use and pending author decisions

Codex GPT-5.6-sol materially assisted source comparison, calculations, code,
verification, figure generation, and drafting. The draft discloses this use
under the current APS policy. The named author has not been represented as
having completed human verification.

Before submission, Xiaojian Zeng must confirm:

- authorship, the affiliation `PBC School of Finance, Tsinghua University,
  Beijing 100190, China`, and `xiaojianzeng@foxmail.com`;
- scientific correctness after personally reviewing and reproducing the
  central calculation;
- the official journal-version Fig. 3 mapping and any response from the
  original authors;
- the AI disclosure, ancillary-file plan, data-availability wording, and all
  redistribution permissions;
- that *Physical Review B* Comment remains the preferred venue and that the
  current policies have not changed.
