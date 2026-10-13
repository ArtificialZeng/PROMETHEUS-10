# Author handoff: strict non-saturation of the seven-state witness

## Core claim

For the exact seven-state ensemble and prepare-and-measure witness of Patra,
Taoutioui, and Vertesi (arXiv:2609.13075v1, Sec. VI.D), the maximum over
two-qubit separable preparations and independent legal binary effects obeys
`Q_SEP < 3/4`. This is a computer-assisted exact result-note. The stronger
quantitative problem remains unresolved: the work gives neither `Q_SEP` nor a
certified decimal/rational upper bound below `3/4`.

## Hardest checks completed

1. The seven states and positive weights were independently reconstructed in
   two representations. Both give the exact frame `sum alpha_i P_i = I_4/4`,
   21 legal Helstrom effects, and unrestricted witness value `3/4`.
2. Equality in the Helstrom, dimension-four purity, and Cauchy-Schwarz bounds
   was reduced analytically to exact matching of all 21 target transition
   probabilities by seven product rays. This avoids assuming the Wigner
   property.
3. The six zero transitions were assigned exhaustively to local factors:
   `3^6 = 729` assignments, 26 surviving closures, 18 ordered patterns, and
   nine patterns up to factor exchange. Eight patterns have exact unit
   Groebner ideal over `Q(sqrt(7))`.
4. The only algebraic survivor forces a real Bloch Gram matrix with determinant
   `-27/16` and eigenvalue `-1/2`, so it is impossible.
5. A fresh scientific audit independently reconstructed the source, equality
   argument, enumeration, and Gram obstruction, and accepted precisely this
   restricted result-note scope. This remains AI review, not external peer
   review.

## Important caveats

- The published feasible value `0.74990679` was not independently regenerated
  in this project and is cited as the source's numerical lower bound.
- Compactness proves an existential positive gap but no robustness modulus.
  The draft must not be advertised as an experimental threshold.
- The claim is semi-device-independent only under a four-dimensional message
  assumption; it is not device independent.
- The witness concerns the seven-state extended ensemble, not direct
  certification of the original four-state subset by this witness alone.
- The source was only three days old at the literature check. No absolute
  priority claim is justified; repeat the search immediately before any public
  posting or submission.
- The immutable lead called the source section `IV.D`; the correct primary
  locator is `VI.D`. The draft uses the correct locator without changing the
  immutable source record.

## Source map

| Draft content | Scientific source/evidence |
| --- | --- |
| AES definition and minimal four-state context | Cai et al., Phys. Rev. A 103, 052432 (2021) |
| Prepare-and-measure self-testing context | Navascues et al., Phys. Rev. Lett. 131, 250802 (2023) |
| Seven states, weights, witness, `3/4`, and `0.74990679` | Patra et al., arXiv:2609.13075v1, Eqs. (29)-(33), Sec. VI.D |
| Exact frame and target baseline | `evidence/input-a.json`, `evidence/input-b.json`, `evidence/baseline.log` |
| Equality reduction and obstruction | `evidence/product-saturation-proof.md` |
| Executable exact certificate | `scripts/check_product_saturation.py`, `evidence/product-saturation-exact.log` |
| Accepted scope and limitations | `audit/science.md`, `audit/science.json` |
| Venue scope and current policy | `venue/aims-and-policy.md`, `venue.json` |

## Target and format

Provisional target: **Quantum Information Processing**, **Regular Article**.
The official scope covers theoretical quantum information and entanglement;
the regular-article format is more conservative than a Letter for this narrow
existential result. This is a fit assessment, not an acceptance or ranking
claim. The local TeX uses a portable article layout because the Springer Nature
class was not installed; migrate to the current publisher template if the
author approves this venue.

## AI use

OpenAI Codex using GPT-5.6 Sol assisted with topic development, source
reconstruction, exact symbolic code and calculations, literature searching,
scientific checking, and manuscript drafting. The manuscript contains an
explicit disclosure consistent with the checked journal guidance. The named
author has not yet approved the manuscript and must take responsibility for any
submitted version.

## Decisions required from the author

1. Confirm the author name, PBC School of Finance affiliation, postal code, and
   email shown in the draft; add ORCID if desired.
2. Read and approve every equation, the exact code, and the AI disclosure.
3. Supply final funding and competing-interest declarations.
4. Approve or change the target venue and convert to its current template.
5. Decide whether to post the exact checker and input in a public archive and
   add the permanent URL/DOI to the data statement.
6. Repeat the primary-literature and citation check close to submission.
7. Decide whether to pursue a quantitative stability/dual certificate before
   submission; that addition would require a new scientific audit.

External submission is not authorized by this handoff.
