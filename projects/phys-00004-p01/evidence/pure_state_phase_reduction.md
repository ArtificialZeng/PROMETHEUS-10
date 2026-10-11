# Exact reduction used by the two-use search

This note concerns the frozen two-use GADC problem only.  It does not prove
additivity.

## Mixed inputs reduce to pure inputs

For fixed `gamma, eta`, define

\[
 F(\rho)=\mathcal W(\Phi_{\gamma,\eta}^{\otimes2}(\rho),H_2).
\]

Ergotropy is convex because

\[
 \mathcal W(\omega,H)=\max_U\operatorname{Tr}
 [\omega(H-U^\dagger H U)]
\]

is a pointwise maximum of linear functions of `omega`.  Composition with the
linear channel preserves convexity.  A convex continuous function on the
compact energy-ball spectrahedron has a maximizer at an extreme point.

Every extreme point of

\[
 \{\rho\succeq0:\operatorname{Tr}\rho=1,
   \operatorname{Tr}(\rho H_2)\le 2e\}
\]

has rank one.  Indeed, if `rank(rho)=r>=2`, the real vector space of Hermitian
perturbations supported on `supp(rho)` has dimension `r^2>=4`.  There is a
nonzero supported Hermitian `X` satisfying `Tr X=0` and, when the energy
constraint is active, also `Tr(X H_2)=0`.  For sufficiently small positive
`epsilon`, both `rho+epsilon X` and `rho-epsilon X` remain positive and
feasible.  If the inequality is slack, choose `epsilon` small enough to
preserve the slack.  Thus such a `rho` is not extreme.  Consequently a search
over all pure states covers the full complex mixed-state optimization, though
a finite search still cannot certify the universal inequality.

## Only one phase can be gauged neither locally nor globally

The GADC is covariant under the energy-diagonal qubit rotations
`R(alpha)=diag(1,exp(i alpha))`, and these rotations commute with the
Hamiltonian.  A global phase and the two local rotations therefore transform
every two-qubit pure state, up to zero-amplitude limits, to

\[
 |\psi\rangle=\sqrt{p_0}|00\rangle+\sqrt{p_1}|01\rangle
 +\sqrt{p_2}|10\rangle+e^{i\delta}\sqrt{p_3}|11\rangle,
\]

where all `p_j` are nonnegative and sum to one.  The invariant phase is
`delta=phi_00+phi_11-phi_01-phi_10` modulo `2 pi`; local covariance cannot
remove it.  At actual per-cell energy `e`, all populations are represented by

\[
 p_3\in[\max(0,2e-1),e],\quad p_1+p_2=2(e-p_3),\quad
 p_0=1-2e+p_3,
\]

plus one split parameter for `p_1,p_2`.  This is the six-variable search
domain `(gamma,eta,e,p3-split,p1-split,delta)` used in
`search_complex_two_qubit.py`.

## Spectral-diameter form of the remaining inequality

If the two-use output eigenvalues are ordered
`lambda_max >= lambda_2 >= lambda_3 >= lambda_min`, its passive energy for
levels `(0,1,1,2)` is

\[
 \lambda_2+\lambda_3+2\lambda_{\min}
 =1-\lambda_{\max}+\lambda_{\min}.
\]

Writing `D=lambda_max-lambda_min` and using the exact two-use output-energy
law gives

\[
 \mathcal W(\Phi^{\otimes2}(|\psi\rangle\langle\psi|),H_2)
 =2[(1-\gamma)e+\gamma\eta]-1+D.
\]

Let `x_e` be the one-use optimizing excitation from Eqs. (58)--(59), and let

\[
 r(x)=\sqrt{(1-2\eta\gamma)^2+
 4\gamma(1-\gamma)(2\eta-x)x}.
\]

The desired upper bound at the actual input energy is therefore exactly

\[
 D\le r(x_e)-2(1-\gamma)(e-x_e).                 \tag{R}
\]

In the unsaturated regime `x_e=e`, this reduces to `D<=r(e)`.  Product inputs
at the one-use optimum saturate the corresponding bound.  Establishing (R)
over the reduced pure-state domain, with all eigenvalue-order branches
controlled, is the concrete analytic next test.

## Exact phase-dependence checks

The statement following Eq. (75) of arXiv:2305.16803v4 that the two-use output
spectrum is phase-independent is false as written.  At
`gamma=1/2, eta=1/4`, the two inputs

\[
 |\psi_+\rangle=(1,1,1,1)^T/2,\qquad
 |\psi_-\rangle=(1,1,1,-1)^T/2
\]

have identical populations and energy.  Direct exact application of the
printed one-cell map gives output purities

\[
 \operatorname{Tr}\sigma_+^2=625/1024,\qquad
 \operatorname{Tr}\sigma_-^2=417/1024.
\]

Their spectra therefore differ.  The characteristic polynomials are also
recorded by the executable search evidence.

The phase can even raise ergotropy while populations are held fixed.  For the
ADC point `gamma=1/2, eta=0`, take populations
`(1/10,1/20,1/20,4/5)` and put phase `delta` only on the last amplitude.
For `delta=0` and `delta=pi/3`, respectively, the exact characteristic
polynomials are

\[
 {(5\lambda-1)
 (2000\lambda^3-1600\lambda^2+(325-20\sqrt2)\lambda-16)\over10000},
\]

and

\[
 {(5\lambda-1)
 (2000\lambda^3-1600\lambda^2+(325-10\sqrt2)\lambda-16)\over10000}.
\]

Both outputs have energy `17/20`.  High-precision roots give ergotropies
approximately `0.296423880240299` and `0.305395155861315`, so deleting the
invariant phase is not an equality-preserving pointwise reduction.  Neither
state beats the product-code benchmark; this corrects the scope of the old
numerical search but does not resolve the frozen additivity claim.
