# Directionwise obstruction for bounded periodic phase perturbations

Proposer: phys-00003-p10-research-5adb4c33e8c2, 2026-10-12.
This is a proposed restricted analytic result. It neither determines the
unrestricted optimum nor has fresh-referee acceptance.

## Precisely quantified proposed result

Keep the single real-amplitude coherent field, fixed initial ground-state
qubit, oscillator units and qubit-only readout of problem.md and physics.json.
Let k0=1/sqrt(2). For every fixed L>0 and real bounded Borel L-periodic
function g that is not constant almost everywhere, consider the legal fixed
interaction

V_epsilon=exp[-i sigma_y (k0 Q+epsilon g(Q))], epsilon in R.

There exists epsilon0(g,L)>0 such that, for both signs and every
0<|epsilon|<epsilon0,

inf_{alpha in R} F_Q[rho_epsilon(alpha)] < 4/e.

The output is uniformly full rank in this neighborhood. Below we give an
explicit real-arithmetic remainder bound and one expression for epsilon0.
For constant g the QFI remains exactly 4/e: it is a fixed output rotation.

The quantifier order is essential: g and L are fixed BEFORE taking epsilon
small. There is no common radius over all g or all periods, no claim of
a norm-neighborhood maximum, no finite-strength/global no-go, and no claim
about a general joint unitary, nonplanar rotations, or estimation risk.
The all-real-alpha infimum is controlled analytically, not by a sampled grid.

## Legal model, exact derivative and first variation

Real k0 Q+epsilon g(Q) is self-adjoint on the usual Q domain, since g(Q)
is bounded and commutes with Q. Its exponential is a bounded unitary,
independent of alpha. In the basis fixed in problem.md, define mu=sqrt(2)alpha,
p0(y)=exp(-y^2)/sqrt(pi), A=exp(-1/2), D=2A and W=2sqrt(2/pi).
With the complex Bloch coordinate from evidence/research/derivation.md,

m_epsilon(mu)=integral p0(y) exp[i sqrt(2)(mu+y)]
                        exp[2i epsilon g(mu+y)] dy.

Its alpha derivative is the Gaussian-score integral with weight 2sqrt(2)y.
This expression is valid even for discontinuous Borel g: differentiate the
smooth Gaussian density at fixed x, not g. Dominated convergence is justified
by bounded phase factors and the integrable Gaussian score, uniformly in mu.

At epsilon=0, m0=A exp(i sqrt(2)mu), d0=m0'=2i A exp(i sqrt(2)mu),
so |d0|^2=4/e and Re(conj(m0)d0)=0. Let m1 and d1 be epsilon derivatives at
zero; explicitly m1=2i E[g(X)exp(i sqrt(2)X)] and
d1=4i sqrt(2) E[(X-mu)g(X)exp(i sqrt(2)X)].
The radial part of the full-rank QFI is second order. The first variation is

G(mu)=2 Re(conj(d0)d1)
     =16sqrt(2)A integral y p0(y) cos(sqrt(2)y) g(mu+y) dy.

Thus, uniformly in mu,
F_Q(mu,epsilon)=4/e+epsilon G(mu)+O(epsilon^2).
The quantitative uniform remainder and full-rank condition are proved below.

## Why every nonconstant periodic direction loses at some amplitude

Put kappa=2pi/L and c_n=L^(-1) integral_0^L g(x) exp(-in kappa x) dx.
The real first variation G is a convolution of bounded g with an integrable
smooth kernel; it is continuous and L-periodic. Its average is zero, since
the kernel y p0(y)cos(sqrt(2)y) is odd. Its Fourier coefficients for n>0 are

G_n=i C(n kappa)c_n, G_-n=-i C(n kappa)c_-n,
C(xi)=16 k0 exp[-1-xi^2/4]
               [xi cosh(k0 xi)-2k0 sinh(k0 xi)].

This calculation follows directly from
integral y p0(y) exp(i lambda y)dy=(i lambda/2)exp(-lambda^2/4).
It does not require pointwise convergence of the Fourier series of g.
Fubini is valid because g is bounded and the kernel integrable. The multipliers
decay as a Gaussian times a polynomial; G's differentiated Fourier series
therefore converge absolutely. For xi>0, put z=k0 xi. The bracket becomes
sqrt(2)[z cosh z-sinh z], positive because its derivative is z sinh z>0
and its value at zero is zero. Hence every C(n kappa) is strictly positive.

If G vanished identically, all nonzero Fourier coefficients of g would
vanish. Uniqueness of Fourier coefficients in L2([0,L]) would make g constant
almost everywhere, contrary to the premise. Thus G is nonzero, continuous,
and of mean zero. On a compact period it has min G<0<max G. Set
gamma=min(-min G,max G)>0.

For a trigonometric polynomial
g(x)=g0+sum_{n>=1}[a_n cos(n kappa x)+b_n sin(n kappa x)],
this same filter reads
G(mu)=sum_{n>=1} C(n kappa)[b_n cos(n kappa mu)-a_n sin(n kappa mu)].
The single sine direction reproduces exactly the separately checked coefficient
in evidence/research/derivation.md and perturbation-check.json.

## Explicit uniform full-rank and quadratic-remainder control

Let M=sup_x |g(x)| (any finite upper bound suffices), M>0. Set

h=(1-A)/4, beta=(1+A)/2, delta=1-beta^2>0,
K=4 W^2(1+h)^2+4 D W+4(beta W+D)^2/delta.

For a=|epsilon| with a M<=h, |exp(2i epsilon g)-1|<=2aM gives
|m_epsilon-m0|<=2aM and |d_epsilon-d0|<=2aMW.
Thus |m_epsilon|<=A+2h=beta<1 and 1-|m_epsilon|^2>=delta uniformly in mu.
The pointwise SLD/Bures convention is consequently regular throughout this
neighborhood; the rank caveat of the original unrestricted problem is avoided.

The exact real-exponential Taylor remainder is
|exp(2i epsilon g)-1-2i epsilon g|<=2a^2 M^2.
It implies

m_epsilon=m0+epsilon m1+r_m, |r_m|<=2a^2 M^2,
d_epsilon=d0+epsilon d1+r_d, |r_d|<=2a^2 M^2 W,
|m1|<=2M, |d1|<=2MW.

Expanding the tangential contribution gives the uniform estimate

abs(|d_epsilon|^2-D^2-epsilon G)
 <= a^2 M^2[4W^2(1+h)^2+4DW].

Indeed the terms involving r_d and d0 are bounded by 4DWa^2M^2,
and |epsilon d1+r_d|<=2aMW(1+aM)<=2aMW(1+h).
Using Re(conj(m0)d0)=0, the exact Lipschitz differences instead give

abs(Re(conj(m_epsilon)d_epsilon))
 <=2aM[(A+2aM)W+D] <=2aM(beta W+D).

The nonnegative radial QFI term is therefore at most
4a^2 M^2(beta W+D)^2/delta. Combining the two parts proves

abs(F_Q(mu,epsilon)-4/e-epsilon G(mu)) <= K M^2 epsilon^2

for every real mu whenever aM<=h. These inequalities are analytic; numerical
constants are not needed for the theorem and no floating-point certificate
is substituted for them.

Choose
epsilon0=min[h/M, gamma/(2 K M^2)].

For positive epsilon evaluate at an amplitude realizing min G; for negative
epsilon evaluate at one realizing max G. Both give

inf_alpha F_Q <=4/e-gamma |epsilon|+K M^2 epsilon^2
              <4/e-(gamma/2)|epsilon| <4/e.

This completes the stated directionwise obstruction, for arbitrary fixed
bounded periodic Borel perturbations, including discontinuities. Constant
parts of g can be subtracted by a fixed output rotation; this can tighten M
without altering G or QFI.

## Physics consequence and limits

The published quadrature coupling's 4/e performance cannot be improved by
turning on any one fixed weak periodic phase profile along the same sigma_y
axis. The loss mechanism is a nonconstant zero-mean first-order sensitivity
ripple whose Fourier transfer has no nonzero-frequency nulls. Multiharmonic
cancellation cannot remove that ripple for a nonconstant fixed profile.
This excludes a substantial perturbative design route within the same physical
readout model. A possible improvement must bypass this restricted conclusion,
for example by finite strength or a profile changing singularly with its
strength. No existence of any such improvement is asserted.

The response multipliers become small at low and high frequencies, so this
proof gives no frequency-independent radius. Smooth retuning of the linear
coefficient k=k0+O(epsilon) has zero first-order effect because the known
linear QFI is stationary at k0; the same directional loss follows by a
uniform Taylor expansion. This observation is explanatory, not an additional
quantified claim in the proposed packet.

Primary prior, exact baseline and source conventions are documented in
source-ledger.json and evidence/reproduction/derivation.md. The initial
sinusoidal representations, symbolic Gaussian-score cross-check, full-period
double-precision tests, held-out high-precision tests and finite discovery
search are saved in evidence/research/. They support and attack the derivation;
the infinite-dimensional/all-amplitude conclusion rests on the analytic proof.
Fresh independent reconstruction, novelty and significance review are required.
