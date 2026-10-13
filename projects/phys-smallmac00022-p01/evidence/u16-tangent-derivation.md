# Minimal-split complex tangent analysis at `r=1/2`

## Scope

This record treats the minimal ancillary split `(d_A',d_B')=(4,4)` at the
single exact parameter value `r=1/2` and von Neumann order `alpha=1`.  It gives
an exact tangent-space/stationarity decomposition and controlled numerical
evidence for the fixed-rank Hessian.  It does **not** prove local minimality,
global additivity, or anything about larger ancillary splits.

Write a flag label as `x=(I,J)` and an output flag basis vector as `y=(a,b)`,
with every index in `{0,1,2,3}`.  Let

`C = ([[r,1],[1,1]]/sqrt(3+r^2)) tensor 2`.

Across `AA':BB'`, the coefficient matrix of a flag unitary `W` is

`M(W)_(I,a),(J,b) = C_(I,J) W_(a,b),(I,J)`.

At `W_0=I_16`, only rows `(I,I)` and columns `(J,J)` are occupied, and their
active `4 x 4` block is `C`.  At `r=1/2`, `C` is nonsingular and every entry is
strictly positive.

## Exact split of all 256 real tangent directions

Let `K*=-K` and `W(t)=I+tK+O(t^2)`.  If `P` and `Q` project onto the active
row and column spaces, respectively, then the normal-normal first variation is

`[(1-P) M'(0) (1-Q)]_(I,a),(J,b) = C_(I,J) K_(a,b),(I,J)`

for `a != I` and `b != J`.  Positivity of all `C_(I,J)` shows that this block
vanishes exactly when `K` has no off-diagonal entry joining two points of the
`4 x 4` flag grid whose two coordinates both differ.

Thus the first-order fixed-rank kernel consists of:

- 16 imaginary diagonal generators;
- 24 unordered edges sharing `I`, with two real generators per complex edge;
- 24 unordered edges sharing `J`, again with two real generators per edge.

Its real dimension is `16+2(24+24)=112`.  The remaining 72 unordered grid
pairs have both coordinates different and supply `2*72=144` support-opening
directions.  The dimensions sum to `256=dim_R U(16)`.  The script constructs an
orthonormal anti-Hermitian basis and verifies these counts and the normal-block
zeros directly.

## Stationarity

Put `rho(t)=M(t)M(t)*`.  On the positive support of `rho(0)`, the only possible
active-active part of `M'(0)` comes from a diagonal generator
`K_(I,J),(I,J)=i theta_(I,J)`.  It gives

`rho'(0)_(I,I') = i sum_J C_(I,J) C_(I',J)
                         (theta_(I,J)-theta_(I',J))`.

This is purely imaginary and antisymmetric after removal of the prefactor `i`,
whereas `log rho(0)` is real symmetric.  Their trace pairing is zero.  Rook-edge
directions give only active-normal blocks at first order, and both-coordinate
edges give a normal-normal variation of `M` but no first-order variation of
`rho` paired with its active support.  Since `Tr rho'(0)=0`,

`d S(rho(t))/dt |_(t=0) = -Tr[rho'(0) log_2 rho(0)] = 0`.

For support-opening directions the entropy is not twice smooth at the rank
boundary, but its one-sided first derivative still vanishes by the asymptotic
formula below.  This establishes directional stationarity for all 256 real
directions; it is not a second-order local-minimum theorem.

## Proved gauge modes and no others removed

Every pair `X,Y in u(4)` generates a local-ancilla gauge tangent

`K = X tensor I_4 + I_4 tensor Y`.

The corresponding product path `(exp(tX) tensor exp(tY)) W_0` changes the left
reduced state only by a local `A'` conjugation and traces a local `B'` unitary,
so its entropy is exactly constant.  The map `(X,Y) -> K` has the one-dimensional
kernel `(i c I,-i c I)`, hence its image has real dimension `16+16-1=31`.
Its diagonal part is precisely the seven-dimensional family
`theta_(I,J)=x_I+y_J`; arbitrary branch phases are not projected away.

The computation represents these 31 directions inside the 112-dimensional
kernel, checks rank 31, and diagonalizes only the orthogonal 81-dimensional
quotient.

## Fixed-rank Hessian calculation

For a kernel generator `K`, the script uses the exactly unitary Cayley path

`W_K(t)=(I-tK/2)^(-1)(I+tK/2)`,

which has the same first and second jet as `exp(tK)`.  It evaluates the entropy
of the four positive Schmidt weights, forms symmetric second differences, uses
coarse/fine Richardson extrapolation, and obtains mixed entries by quadratic
polarization.  The generator basis is orthonormal in
`Re Tr(K*L)`, so the reported eigenvalues are in bits per squared unit tangent
parameter.

At coarse/fine pairs `(2e-3,1e-3)` and `(1e-3,5e-4)`, respectively, the quotient
minimum is

`0.159148977465060` and `0.159148970359836`,

and the quotient maximum is about `1.57318519`.  The two quotient Hessians
differ by `5.55e-8` in operator norm.  The unprojected matrix has exactly 31
eigenvalues within `2e-6` of zero; their small signed spread and the gauge
residual are at the finite-difference scale.  No additional numerical zero or
negative quotient direction was found.  The full cluster list, whose
multiplicities sum to 81, is in `evidence/u16-tangent.log`.

The weakest mode is, to numerical resolution, entirely in the nine-dimensional
nonfactorizable phase quotient.  A separate 100-decimal implementation directly
forms the `4 x 4` reduced matrix for the double-centered phase table.  Its
positive finite entropy differences shrink from `3.18e-5` bits at `|t|=0.02`
to `1.24e-7` bits at `|t|=0.00125`, and its symmetric curvature converges to
`0.15914898`.  A factorizable phase changes the entropy by only `1.1e-101` bits
at the same precision.  This independently checks the weakest discovered
direction, but is not an interval enclosure of the entire Hessian.

## Support-opening asymptotic

For `N(K)=(1-P)M'(0)(1-Q) != 0`, standard singular-value perturbation of the
block matrix with nonsingular active block gives new Schmidt weights

`lambda_l(t)=t^2 s_l(N)^2+O(|t|^3)`.

Consequently,

`S(rho(t))-S(rho(0)) = -t^2 log_2(t^2) ||N||_F^2 + O(t^2)`.

The displayed leading term is positive and dominates the bounded quadratic
term for every fixed direction with `N != 0`.  Therefore each such fixed
direction increases the entropy for all sufficiently small nonzero `t`.
This does not by itself give a uniform neighborhood estimate as `||N|| -> 0`.

For the normalized real edge joining `(0,0)` to `(1,1)`, the exact coefficient
is

`||N||_F^2=(C_00^2+C_11^2)/2
          =0.0147928994082840236686390532544...`.

An independent 100-decimal direct `16 x 16` partial trace along the exact Givens
rotation gives positive entropy differences from `1.31e-4` bits at `t=0.02`
to `1.86e-7` bits at `t=0.000625`; the ratio to the logarithmic leading term
decreases toward one, as expected when the bounded `O(t^2)` term is divided by
the slowly growing logarithm.

## What remains

The numerical quotient gap is not yet an interval-certified eigenvalue bound.
Even such a bound must be combined with a uniform remainder estimate that
controls mixed paths whose opening component tends to zero with `t`.  These are
the next obligations for a local-minimum theorem in the `(4,4)` split.  Larger
ancillary splits and global two-copy additivity remain completely unresolved.

