# Exact reduction for the tight subdivided-star family

## Scope and notation

Let `T_q`, `q>=1`, be the tree with ordinary leaves
`L_1,...,L_q`, centre `C`, and two further vertices `A,B`, with edges

\[
  C L_i\quad(1\le i\le q),\qquad CA,\qquad AB.
\]

Thus `T_q` has `n=q+3` vertices and degree sequence
`(q+1,2,1,...,1)=(n-2,2,1,...,1)`.  Put `t=s^2` and work with

\[
 K_s=-H_s=\sum_{e}|\phi_s\rangle\langle\phi_s|_e,
 \qquad |\phi_s\rangle=|00\rangle+s|11\rangle .
\]

If `mu_e`, `mu_o` are the largest eigenvalues of `K_s` in the even and
odd sectors and `nu_e` is the second-largest even eigenvalue, the two
required margins are

\[
 M_o=\mu_e-\mu_o-(1-t),\qquad
 M_e=\mu_e-\nu_e-(1-t).
\]

The full all-`q`, all-`0<t<1` sign problem remains open below.  The new
exact results here are a complete leaf-spin reduction, a recursion among
its nonsymmetric blocks, and a proof that `M_o>0` and `M_e>0` for every
fixed `q` in a punctured neighbourhood of `t=0`.

## Leaf-spin decomposition

Permutations of the `q` ordinary leaves commute with `K_s`.  On those
qubits, the only non-diagonal operators that occur are the collective
raising and lowering operators `J_+` and `J_-`; the diagonal part is a
function of the Hamming weight.  The ordinary-leaf Hilbert space therefore
decomposes into spin

\[
 j=q/2-r,\qquad 0\le r\le\lfloor q/2\rfloor,
\]

with multiplicity

\[
 d_{q,r}=\binom qr-\binom q{r-1}
 \quad (\binom q{-1}:=0).
\]

For one copy of the spin-`j` space, use the orthonormal basis
`|c,a,b;k,r>`, where `c,a,b` are the bits at `C,A,B` and
`r<=k<=q-r` is the physical ordinary-leaf Hamming weight.  Retain only
states with

\[
 c+a+b+k\equiv p\pmod2
\]

in parity block `p`.  Denote the resulting real symmetric matrix by
`B^(p)_(q,r)`.  Its diagonal is

\[
 q-k\quad(c=0),\qquad tk\quad(c=1),
\]

plus `1` when `c=a=0`, `t` when `c=a=1`, `1` when `a=b=0`, and
`t` when `a=b=1`.  Its only off-diagonal entries are

\[
\begin{aligned}
 |0,a,b;k,r\rangle &\longleftrightarrow |1,a,b;k+1,r\rangle,
 &s\sqrt{(q-r-k)(k-r+1)},\\
 |0,0,b;k,r\rangle &\longleftrightarrow |1,1,b;k,r\rangle,
 &s,\\
 |c,0,0;k,r\rangle &\longleftrightarrow |c,1,1;k,r\rangle,
 &s.
\end{aligned}
\]

These formulas follow directly by applying `sum_i |phi_s><phi_s|_(C,L_i)`
and the standard spin-`j` matrix element of `J_+`; the last two lines are
the edges `CA` and `AB`.  Consequently the complete parity characteristic
polynomial factors exactly as

\[
 \chi_p(x)=\prod_{r=0}^{\lfloor q/2\rfloor}
   \det(xI-B^{(p)}_{q,r})^{d_{q,r}}.                 \tag{1}
\]

This is a polynomial-size reduction of the `2^(q+2)` dimensional parity
block.  Because a nonnegative top-parity eigenvector can be averaged over
leaf permutations without vanishing, the largest eigenvalue in either
parity occurs in `r=0`.  The second even eigenvalue is exactly

\[
 \nu_e=\max\left\{\lambda_2(B^{(0)}_{q,0}),
      \max_{1\le r\le\lfloor q/2\rfloor}
      \lambda_1(B^{(0)}_{q,r})\right\},             \tag{2}
\]

where eigenvalues in (2) are ordered decreasingly.

There is a second exact reduction, special to bipartite graphs, that is
hidden if one records parity alone.  Give `L_i,A` sign `+` and `C,B`
sign `-`.  The integer staggered occupation

\[
 Q=N_L+n_A-n_C-n_B=k+a-c-b
\]

commutes with every edge term.  The only off-diagonal transition is
`00 <-> 11`; every edge joins one `+` and one `-` vertex, so its two
occupation changes cancel.  Also

\[
 (k+a+c+b)-Q=2(c+b),
\]

so Hamming parity is exactly `Q mod 2`.  Equivalently, flipping the qubits
on `C,B` maps the model to a number-conserving rank-one edge Hamiltonian
and maps `Q` to particle number minus two.

For fixed `r` and `Q`, `k=Q-a+c+b` is fixed by the three core bits.
Every `(r,Q)` block therefore has dimension at most eight, independently
of `q`.  Thus (1) can be sharpened by factoring every
`det(xI-B^(p)_(q,r))` over its allowed charges.  The exact implementation
checks that these charge blocks have dimension at most eight and that
their product recovers each reduced characteristic polynomial.  In
particular, the even ground root lies in the seven-state `(r,Q)=(0,0)`
component for `q>=2`; the numerically leading odd component is the
eight-state `(0,1)` component for `q>=3`, with smaller boundary blocks at
`q=1,2`.  Fixed-size charge blocks, rather than exponential
diagonalization, are therefore the natural objects for the remaining
Sturm or continued-fraction comparison.

The independent full computational-basis construction in
`analyze_subdivided_stars.py` verifies (1), coefficient for coefficient
over `QQ` at `s=2/5`, for both parities and every `1<=q<=6` (full parity
degrees through 256).  This finite replay checks the implementation; the
displayed collective-spin argument establishes (1) for arbitrary `q`.

## Exact recursion for nonsymmetric sectors

Write `k=r+k'` and `q'=q-2r`.  The collective matrix element becomes

\[
 \sqrt{(q'-k')(k'+1)},
\]

while the ordinary-edge diagonal becomes `q'-k'+r` for `c=0` and
`tk'+tr` for `c=1`.  All core-edge entries are unchanged.  Hence

\[
 B^{(p)}_{q,r}\cong
 B^{(p-r\ {\rm mod}\ 2)}_{q-2r,0}
 +rD_C(t),                                           \tag{3}
\]

where `D_C(t)=|0><0|_C+t|1><1|_C`, restricted to the indicated parity
space.  Charge `Q` on the left becomes `Q-r` in the smaller block.
Equation (3) is an exact identity, not an eigenvalue fit.  It
reduces every potential nonsymmetric competitor in (2) to a smaller
symmetric problem with a positive but non-scalar central field.  The code
checks (3) entry by entry for all sectors through `q=12`.

## Exact small-`s` splitting

At `s=0`, `K_0` is diagonal and counts edges whose endpoints are both
zero.  Its even maximum is the all-zero state with eigenvalue `q+2`.
Writing `K_s=K_0+sV+s^2W`, ordinary second-order perturbation theory gives

\[
 \mu_e=q+2+A_e(q)t+o(t),\qquad
 A_e(q)=\frac{q}{q+1}+\frac1{q+2}+\frac12.           \tag{4}
\]

Indeed, flipping the two endpoints of an ordinary edge, `CA`, or `AB`
costs respectively `q+1`, `q+2`, or `2` zero-zero edges; there are `q`
ordinary edges.  The `W` expectation in the all-zero state vanishes.

The odd maximum of `K_0` is `q+1`.  Its eigenspace is spanned exactly by
the singleton-one states at the `q+1` degree-one vertices
`L_1,...,L_q,B`.  There is no first-order matrix inside this space and no
`W` diagonal contribution.  Summing the two-step paths through `V` gives
the following exact second-order matrix:

\[
\begin{aligned}
 (E_2)_{L_iL_i}&=\frac{q-1}{q}+\frac1{q+1}+\frac12,\\
 (E_2)_{L_iL_j}&=\frac1q\quad(i\ne j),\\
 (E_2)_{L_iB}&=0,\qquad (E_2)_{BB}=1.
\end{aligned}                                       \tag{5}
\]

For example, the three terms in the first line arise from flipping a
different ordinary edge, `CA`, or `AB`, whose intermediate denominators
are `q`, `q+1`, and `2`.  The symmetric ordinary-leaf eigenvalue of (5) is

\[
 A_o(q)=\frac{2(q-1)}q+\frac1{q+1}+\frac12,          \tag{6}
\]

which exceeds the terminal value `1` for `q>=2` (and ties it for `q=1`).
Thus

\[
 \mu_o=q+1+A_o(q)t+o(t).                             \tag{7}
\]

Combining (4) and (7) with the target `1-t` yields

\[
 M_o(t)=
 \frac{q^2+3q+4}{q(q+1)(q+2)}\,t+o(t).              \tag{8}
\]

The coefficient is strictly positive for every integer `q>=1`.  The
second-even gap equals `2` at `t=0`, so `M_e(0)=1` and remains positive by
continuity.  Therefore, for every fixed `q`, there exists `epsilon_q>0`
such that the subdivided star obeys both strict inequalities for
`0<t<epsilon_q`.  For `q=1`, the earlier exact `P4` calculation proves the
strict statement on the entire interval.

The `1/q` decay of the coefficient in (8) explains the previously tight
case `q=4`, `s=1/10`: its leading prediction is `0.002666...`, close to
the exact isolated margin `0.0026339496...`.  This is an explanation of
the near-star obstruction, not an extrapolation proof.

## Interior scout and remaining obstruction

Using (1)-(2), a double-precision held-out scan covered all `1<=q<=64`
(`4<=n<=67`) at 43 points from `s=0.01` through `s=0.9999`, for 2752
family/parameter cases.  Both margins were positive at every sampled
point and the first excitation was always odd.  For every `q>=2` the odd
top was in `(r,Q)=(0,1)`.  The second even level was always in `r=0`: it
was the next `Q=0` root for `q=1,2` and the `Q=2` Perron root for every
sampled `q>=3`.  The smallest sampled actual margin was approximately
`1.5630e-6` at `q=64,s=0.01`.  These floating-point observations are
discovery evidence only.

The remaining analytic task is now sharply reduced: prove on `0<t<1`
that

\[
 \lambda_1(B^{(0)}_{q,0})-\lambda_1(B^{(1)}_{q,0})>1-t
\]

and that every competitor in (2) lies at least `1-t` below the even top.
Equation (3) suggests a comparison/continued-fraction induction, but a
positive nonscalar field cannot simply be replaced by a scalar bound
without losing the required strict constant.  No all-interval theorem or
counterexample is claimed in this pass.
