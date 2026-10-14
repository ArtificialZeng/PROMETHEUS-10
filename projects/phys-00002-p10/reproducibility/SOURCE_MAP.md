# Formula and program map

The manuscript reports one exact physical state and a computer-assisted strict
full-plane integral comparison at alpha=1/4. Its support, density matrix,
Wigner square, analytic cell moments and tail formulas are explicitly displayed.

| Manuscript component | Supplied program or data | Role |
| --- | --- | --- |
| Exact finite-support product input, joint output and reduced density matrix | evidence/alpha-quarter-witness-exact.py | Checks given creation-map/partial-trace coefficients and applies the Fock/Laguerre Weyl transform |
| Hermite wavefunction and exact Q(sqrt2) coefficient equality | evidence/alpha-quarter-witness-exact.py and .json | Algebraic equality and exact normalization |
| Independent coordinate partial trace; vacuum and one-photon nodal baselines | reproducibility/independent_replay.py | Gaussian coordinate and Fourier moments, without importing the Fock checker |
| Cauchy/chord cell inequality and analytic weighted moments | evidence/alpha-quarter-jensen-enclosure.py | Directed 40-digit Decimal evaluation on the displayed grids |
| Decimal pi and elementary-function enclosures | evidence/alpha-quarter-enclosure.py | Arithmetic helper imported by the Decimal polar calculation; its unrelated benchmark main routine is not run |
| Decimal rows of the manuscript table | evidence/alpha-quarter-jensen-enclosures.json | Actual recorded analytic upper-bound evaluations, including their entire tails |
| Integer outward arithmetic and separate tail bound | reproducibility/independent_replay.py | 35-digit integer interval implementation of the shared inequality |
| Integer table row, exact rational endpoints and nodal counts | reproducibility/independent-enclosure.json | Evaluated upper-bound expression and vacuum comparison |
| Repeated execution without overwriting reference evidence | reproducibility/run_all.py | Scratch-copy runner and post-calculation comparisons |

The portable integer script is copied from the accepted coordinate reconstruction
and interval implementation. Its only changes are its descriptive header and
output filename (independent-enclosure.json). The physical equations, grid,
arithmetic and proof inequalities are unchanged. Its reference numeric output
is identical to the accepted calculation. Re-running it is reproduction, not
a new independent review.

All polynomial comparisons are exact. The table contains upper bounds only,
and every upper includes a Gaussian-polynomial bound on the unbounded exterior.
The source literature fixes the entropy, beam-splitter and quadrature conventions;
no external paper is needed as a data file during calculation.

Primary references used for context are linked in manuscript/references.bib:
Van Herstraeten and Cerf, arXiv:2411.05562v2 and Physical Review A 112, 062207;
Van Herstraeten, Cerf and Chabaud, arXiv:2609.24670v1;
He, arXiv:2609.13312v2;
Qian and Gagatsos, arXiv:2601.16898v2 and Physical Review A 114, 022408.
The first proposes the restricted low-order extension, the next two concern
general Wigner-positive states, and the last gives Shannon purity criteria.
This package does not redistribute their full texts or figures.
