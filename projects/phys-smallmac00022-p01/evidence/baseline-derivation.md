# Source-led reproduction derivation

Primary locator: Negari and Baghali Khanian, arXiv:2608.28897v1,
Eqs. (C1)--(C7), especially (C3)--(C5).

In the source logical bases `(0_L,1_L)` and `(0_R,1_R)`, direct
transcription of (C3) gives

`C_r = [[r,1],[1,1]]/sqrt(D)`, with `D=3+r^2`.

Therefore the left marginal is

`C_r C_r^T = [[1+r^2,1+r],[1+r,2]]/D`,

which is (C4).  Its trace is one and its determinant is
`(1-r)^2/D^2`, so its two eigenvalues are

`lambda_pm = (1 +- sqrt(1-4(1-r)^2/D^2))/2`.

Theorem 1 in the same primary source proves that the canonical purification
is globally optimal among all purifications of a classical two-qubit state.
Combining that theorem with the independently reconstructed spectrum gives
(C5): `E_P^(alpha)(rho_r)=S_alpha(sigma_r)` for `0<=alpha<=infinity`.
The computation here reproduces the decisive coefficient, marginal, spectrum,
and entropy at the frozen witness point; it does not claim a new proof of
Theorem 1.

For the two-copy witness, reconstruction A takes `C_r tensor C_r` and changes
only its `(00_L,00_R)` entry from `+r^2/D` to `-r^2/D`, as in (C7).
Reconstruction B starts instead from the four classical probabilities, builds
the full physical-plus-flag ket branch by branch, and explicitly traces the
physical `B` and flag `B_prime` indices.  It never reads A's matrix or output.
The convention map and observed agreement are recorded in
`evidence/input-comparison.log`.
