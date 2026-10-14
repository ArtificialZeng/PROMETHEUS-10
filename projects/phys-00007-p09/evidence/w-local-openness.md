# Local robustness of commuting-reflection encoding near W3

Proposed restricted result, 2026-10-12; proposer job
phys-00007-p09-research-d982a4bee65c. This is a referee packet, not acceptance.
The universal source conjecture remains unresolved.

## Statement

There exist epsilon>0 and C<infinity such that every normalized complex
three-qubit pure-state ray at distance less than epsilon from [W3] admits
a commuting-reflection local encoding using the triangle graph basis.
More precisely choose the phase with <W3|psi> positive and write
psi=(W3+eta)/sqrt(1+||eta||^2), <W3|eta>=0. An encoder change of basis
V(theta)=exp(-i sum_jk theta_jk sigma_jk/2) V0 can be chosen with
||theta|| <= C ||eta||^(1/3). The exponential factorizes over qubits;
V0=q^tensor3 is the published W solution. This bound is anchored at W;
it does not assert a globally continuous or pairwise Holder encoder selection.
Local-unitary covariance extends existence to an open neighborhood of the
entire local-unitary W orbit. No explicit numerical epsilon or C is claimed.

On the particular legal normalized state path
psi(t)=(W3+t delta)/sqrt(1+13t^2), delta=V0^dag O V0 W3,
O=K1K2K3-2(K1+K2+K3), there is an exact branch through V0 with
theta=s v1+O(s^2), t=(40ab/39)s^3+O(s^4).
It therefore has theta=v1 (39t/(40ab))^(1/3)+O(|t|^(2/3)), with the real
cube root. No C1 branch through this V0 follows the same state path.

## Inputs and conventions

The primary results used are Theorem 6 and Proposition 7 of
Pauwels--Guhne, arXiv:2608.21185v1. The source PDFs/text, independently
reconstructed GHZ/W benchmarks and convention map are indexed by
source-ledger.json, reproduction.json and evidence/reproduction-report.md.
The exact local differential calculation is in research-rank-report.md,
w_jacobian.py and w-jacobian.json in this directory.
Nothing in this argument uses checkpoint.md or state.json as an input.

W3=(001+010+100)/sqrt3; positive a,b satisfy a^2=(3+sqrt3)/6,
b^2=(3-sqrt3)/6, so ab=1/sqrt6. q=i(bY+aZ), standard Y=iXZ.
K1=XZZ, K2=ZXZ, K3=ZZX. All parameters, amplitudes and moments are
dimensionless. No dynamical or physical-coupling expansion is present.
Series below are convergent local-coordinate Taylor expansions of exact
finite-dimensional unitary functions, with analytic remainders.

## Six-constraint elimination

Let F be the six expectations of K1,K2,K3,K1K2,K1K3,K2K3 in V(theta)psi.
Use theta=N u+B y, where the three columns of N are
v_h: X_j=0, Y_j=sqrt2 delta_jh, Z_j=2-5 delta_jh,
and B spans the six X_j,Z_j controls, with no Y controls.
These nine columns are independent because the Y part of N is invertible.
The exact J_B=d_y F at (u,y,eta)=(0,0,0) is nonsingular. With rows
K1,K2,K3,K1K2,K1K3,K2K3 and columns Z1,Z2,Z3,X1,X2,X3, its determinant
is -16 sqrt3/6561. The three single moments have diagonal Z derivative
2ab/3; pair moments have X derivative sqrt2/3 on the two participating
qubits and zero on the other qubit. This also gives an explicit inverse.

The real analytic implicit-function theorem gives a unique analytic
y=Y(u,eta) in a neighborhood of the origin, satisfying F=0.
Y(0,0)=0 and d_u Y(0,0)=0 because J N=0. Define the real scalar
R(u,eta)=<V(Nu+B Y(u,eta))psi(eta)|O|V(Nu+B Y(u,eta))psi(eta)>.
All seven nonidentity stabilizer moments vanish iff F=0 and R=0.
This is equivalent to eight equal graph probabilities and hence an encoding.

The linear theta derivative of O vanishes for every control, as certified
in w-jacobian.json. Its Hessian on N is zero. Thus R(u,0) has no terms
of degrees zero, one or two. Its cubic homogeneous term is

C3(u)=ab[-(80/3) sum_j u_j^3
          +40 sum_{j!=k} u_j^2 u_k -160 u1 u2 u3].

This full polynomial is obtained in w_cubic.py by explicit ket expansion
and ten unisolvent rational samples of a degree-three homogeneous polynomial;
elimination verifies invertibility of the interpolation system. Five extra
exact holdouts are checked, including u=(1,1,1), where the cubic vanishes.
Homogeneous degree three follows from H linear and L quadratic in u;
interpolation is consequently complete at this degree, not a fitted ansatz.

For the decisive line u=s e1 the second-order complementary controls are
c=(13 sqrt3 ab,0,0,-4 sqrt3 ab,0,0,-4 sqrt3 ab,0,0)
in the X1,Y1,Z1,X2,Y2,Z2,X3,Y3,Z3 ordering. Write H=v1.sigma/2 and
L=c.sigma/2, z=V0 W3. The coefficients of the rotated ket are
z1=-i H z,
z2=-i L z-H^2 z/2,
z3=-(HL+LH)z/2+i H^3 z/6.
The true third-order Y correction contributes only a linear derivative of O,
which is zero; it cannot change C3. The exact coefficient on this line is
c0=-80ab/3 !=0. A separately coded operator calculation in
check_w_cubic_exact.py verifies all seven zero coefficients through order two
and this cubic, using
-i <[H,[H,[H,O]]]> /6
 - <[H,[L,O]]+[L,[H,O]]> /2.
It conjugates the operators back into the original W basis and neither imports
the ket-series script nor reads its output. Shared radical arithmetic and source
constants remain a common dependency; this is proposer verification only.

## Uniform sign argument: arbitrary complex perturbations

Fix the two unused kernel coordinates to zero and set r(s,eta)=R(s e1,eta).
Real analyticity implies r(s,0)=c0 s^3+O(s^4). Choose a small fixed rho>0
within the implicit-function neighborhood such that
|r(s,0)-c0 s^3| <= |c0| |s|^3/2 for |s|<=rho.
On a smaller compact product neighborhood smooth dependence on the fourteen
real components of eta yields a uniform finite L>=1 with
|r(s,eta)-r(s,0)| <= L ||eta||.
Choose A=(4L/|c0|)^(1/3). For d=||eta||>0 sufficiently small,
s_+=A d^(1/3), s_-=-A d^(1/3) both lie within rho, and
|r(s_+/-,0)| >= 2 L d. Their signs are opposite, and the perturbation bound
preserves those signs. The intermediate-value theorem gives s_* between
s_- and s_+ with r(s_*,eta)=0. At d=0 choose s_*=0.
All six eliminated equations hold exactly along this interval. Therefore
theta=N e1 s_*+B Y(s_* e1,eta) solves all seven moment equations exactly.
Taylor bounds on the analytic Y give ||Y(s e1,eta)|| <= C1(s^2+d),
so ||theta|| <= C d^(1/3) after shrinking the neighborhood.
The phase-fixed chart covers every ray near W, with no real-amplitude
restriction. The finite constants and radius exist by local analyticity;
they have not been computed. The result is exact local existence, not a
truncated numerical solution or a guaranteed practical convergence algorithm.

## Explicit source path and nonsmooth compensation

Exact calculation gives <W|delta>=0, ||delta||^2=13, and
d_t <V0 psi(t)|O|V0 psi(t)> at t=0 equals 26.
Eliminating the six regular moments leaves this t derivative unchanged because
the theta derivative of O is zero. Hence r_path(s,t)=26t+c0 s^3
+O(s^4+|t||s|+t^2). The analytic implicit-function theorem applied in t gives
t=T(s), T(s)=-(c0/26)s^3+O(s^4)=(40ab/39)s^3+O(s^4).
T'(s)=3(40ab/39)s^2+O(s^3)>0 for nonzero small s; T is strictly increasing
across zero and covers a full two-sided t interval. Inverting it produces the
stated real cube-root branch and encoder asymptotics. Conversely any C1
encoder path through V0 has zero missing-moment control contribution at first
order, and cannot cancel 26t. Thus the earlier smooth-continuation obstruction
is compatible with exact encodability: cubic local-control response compensates
the linear state perturbation with a cube-root control displacement.

## Physical consequence and scope

This establishes robustness of a full eight-message distinguishable basis under
arbitrary small complex pure-state perturbations of W, within one fixed connected
graph and the restricted commuting-reflection class. The eight encoders are
V(theta)^dag K^s V(theta). Every Pauli tensor K^s has at most an overall sign
times local Hermitian involutions; distribute that sign into one local factor.
Conjugation by product SU2 preserves those properties and global commutation.
Vanishing seven moments gives Gram I8. A joint projective decoding measurement
distinguishes the messages. No LOCC decoding, ancillas, entangling encoders,
noise tolerance for mixed states or experiment is asserted.

This does not settle arbitrary three-qubit states far from W. It provides no
finite certified radius, global algorithm, uniqueness, optimum control cost or
continuous encoder choice over all nearby states. The exponent is an upper bound
for some nearby encoder, not a global optimum over other encoders/graphs.
The flat cubic on the symmetric kernel line is explicitly allowed by the proof;
only the nonzero one-dimensional cubic is needed.

## Literature and next test

The current primary page still lists arXiv:2608.21185v1 and the same conjecture.
The checked benchmark gives W itself, not an all-complex neighborhood proof;
the 2023 real-state unrestricted-LU construction has a different encoder class.
Current retrievals/searches are preserved in research-pass2-web.json and
research-pass2-literature.json. No verified successor result was located; this
does not establish priority and unpublished work/complete forward citations
remain a limitation. The precise novelty comparison is in prior-comparison-pass2.md.
The next decisive test is fresh-referee reconstruction of the source inputs,
the one-line cubic and the uniform sign argument, with particular attention to
third-order regular elimination, arbitrary complex-state coverage and whether
this open-neighborhood result already follows from an accessible prior result.
