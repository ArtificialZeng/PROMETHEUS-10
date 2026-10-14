# Proposer derivation: the five-photon resonance and the indexed upper bound

Job phys-00003-p07-research-8876169a864b, 2026-10-12. This is a restricted result for the exact unbiased self-adjoint Rabi operator, not a resolution of the joint universal conjecture or referee acceptance. The Hamiltonian, units, parity and boundary conditions are those of problem.md and physics.json. All arguments below use omega=1. For general omega use G=g/omega, d=Delta/omega and e=E/omega. Delta reversal exchanges parity sectors.

## Statements to be checked by a fresh referee

(A) For every 0<g<=1/10 and -1<=c<=1, set Delta=5/2-(5/4)g^2+c*g^4. Then the infinite plus-parity operator satisfies E_2^+<5/2-g^2.

(B) On the particular fourth-order tuned curve Delta=5/2-(5/4)g^2-(5/64)g^4, let x=5/2-g^2 and kappa=sqrt(120)/64. The levels are indexed as E_2^+ and E_3^+, and

|E_2^+-(x-kappa*g^5)| <= g^6/3,

|E_3^+-(x+kappa*g^5)| <= g^6/3,

uniformly for 0<g<=1/10. In particular x-E_2^+ >= kappa*g^5-g^6/3>0, and the same-parity doublet gap belongs to [2*kappa*g^5-(2/3)g^6,2*kappa*g^5+(2/3)g^6]. This curve is tuned through g^4 only: exact stationarity or the exact minimum-gap curve is NOT asserted.

At g=0 the weak indexed inequality holds by diagonal sorting, but the strict inequality and doublet splitting vanish. Neither the opposite-parity bound nor the universal same-parity spacing bound is established here. A same-parity gap is not automatically a dipole-allowed spectral line.

## A. Uniform window: finite trial space, exact polynomial sign

Write t=g^2, x=5/2-t, q_n=n+(-1)^n Delta-x. Compress H_+-x to sites 0,...,7 to obtain A8. Its determinant depends only on offdiagonal squares (n+1)t. Let D_0=1,D_1=q_0 and D_(n+1)=q_n D_n-n*t D_(n-1). No finite matrix is being identified with the full spectrum: it is a legal finite-Fock trial space for min-max.

Put u=c+5/64, so |u|<=69/64. Exactly det(A8)=t^4 P(t,u), with P(0,u)=-768u^2 and the next term t*(-45/2+119u+320u^2). All coefficients of P are recorded in feshbach-bounds.json and independently reconstructed by the matching expansion in check-feshbach.py. They are rational.

For T=1/100 and U=69/64, let p_jk be the coefficients of u^j t^k. Define

A=768-sum_{j>=2,(j,k)!=(2,0)} |p_jk| T^k U^(j-2),

B=sum_{j=1} |p_1k| T^(k-1),

C=45/2-sum_{j=0,k>=2} |p_0k| T^(k-1).

There are no other t^0 terms. Exact rational arithmetic gives A>764, B<120, C>22. For 0<t<=T,

P(t,u)<=-764u^2+120t|u|-22t
          <=(120^2/(4*764))*t^2-22t<0.

Thus A8 has an odd number of negative eigenvalues and no zero eigenvalue. Its two-dimensional coordinate subspace spanned by sites 1 and 3 is strictly negative: q_1=-4+(9/4)t-c*t^2<0 and q_3=-2+(9/4)t-c*t^2<0, and those sites have no direct edge. Therefore A8 has at least two, hence at least three, negative eigenvalues. A corresponding three-dimensional finite-Fock subspace has all Rayleigh quotients strictly below x. Min-max for the full compact-resolvent operator proves E_2^+<x without any truncation-error inference or assumption about tail eigenvalues.

## B. Exact two-state Schur complement at the tuned curve

Fix c=-5/64. Let P project on sites 0 and 5; Q splits into M=sites1,...,4 and T6=sites6,...,infinity. At E=x define R=M(x)^(-1) and r6=<6|(T6-x)^(-1)|6>. The Feshbach matrix F(E)=PHP-E-PHQ(QHQ-E)^(-1)QHP has entries at x

a=Delta-x-t*R_11,

b=5-Delta-x-5t*R_44-6t*r6,

F_05=+sqrt(120)*g^5/det(M(x)).

The sign follows from (M^-1)_14=-sqrt(24)*g^3/det(M) and the minus in the Schur complement. Changing the phase of site5 reverses this sign without changing eigenvalues. We use the positive Jacobi edges throughout.

The middle inverse is finite and exact. R_11 is computed backwards as r4=1/q4, r_n=1/[q_n-(n+1)t*r_(n+1)] for n=3,2,1; R_44 is computed forwards as l1=1/q1,l_n=1/[q_n-n*t*l_(n-1)] for n=2,3,4. The signs q1,q3<0 and q2,q4>0 ensure the inverse recursion denominators alternate in the same signs, so all are nonzero in the stated range.

## C. Infinite-tail and resolvent estimates

For the tail beginning at site N, apply g*sqrt(k)<=epsilon*k+t/(4epsilon) and 2|v_n*v_(n+1)|<=|v_n|^2+|v_(n+1)|^2 to every edge. The absolute edge form is bounded by its full-chain row sums <=2epsilon*n+epsilon+t/(2epsilon). Using n>=N and diagonal n+(-1)^n Delta>=n-|Delta| gives the closed quadratic form lower bound

b_N=(1-2epsilon)N-|Delta|-epsilon-t/(2epsilon).

At N=6, epsilon=1/32, b6-x=19/32-(55/4)t+(5/64)t^2>0. Hence T6-x is positive. For N=9 the same estimate gives b9-x=109/32-(55/4)t+(5/64)t^2>0. (Both use Delta>0.) These estimates are uniform and control the actual infinite operator, not matching cutoffs.

The positive resolvent tail at site9 has 0<r9<=1/(b9-x). Positivity and successive one-site Schur complements give bounds

r8L=1/q8, r8U=1/[q8-9t/(b9-x)],

r_nL=1/[q_n-(n+1)t*r_(n+1)L],

r_nU=1/[q_n-(n+1)t*r_(n+1)U], n=7,6.

Here q8>=79/10, q7>=2, q6>=5 and b9-x>=3. Hence r8U<=1/(79/10-3/100)<1/7, r7U<=1/(2-8/(700))<1, and q6-7t*r7U>=5-7/100>0. All denominators are strictly positive. Thus r6L<=r6<=r6U and bL=5-Delta-x-5tR44-6t*r6U <= b <= bU with r6L instead. The exact rational functions a,bL,bU,det(M) are in feshbach-bounds.json.

Here is a separate resolvent estimate needed for energy dependence and level indexing. For |E-x|<=1/1000, write QHQ-E=D_E+V_Q. On the middle sites |(D_E)_nn|>=19/10; on tail sites n>=6 the diagonal is positive and >=n/4. These inequalities follow directly from Delta in [2.48749,2.5] and x in [2.49,2.5]. The signs on middle sites are -,+,-,+. The matrix V_Q D_E^-1 has absolute row and column sums <2/5, uniformly in this energy strip.

For the finite middle rows the sum is <=(4g)/(19/10)<2/5. For the tail column at n>=7, the sum is <=4g(sqrt(n)+sqrt(n+1))/n, decreasing with n, and at n=7 it is <24g/7<=12/35. For a tail row at n>=7 it is <=4g[sqrt(n)/(n-1)+1/sqrt(n+1)], decreasing with n, and at n=7 is <4g[1/2+3/8]<=7/20 (using sqrt7<3 and 1/sqrt8<3/8). At the boundary n=6 the row is <=4g*sqrt7/7<6/35 and the column <=4g*sqrt7/6<1/5. Missing edges to P only reduce these sums. The Schur norm test therefore gives ||V_Q D_E^-1||<=2/5. The Neumann inverse and |D_E^-1|<=10/19 imply

||(QHQ-E)^(-1)|| <= (10/19)/(1-2/5)=50/57<1.

The row/column estimates define bounded V_Q D_E^-1 on l2 despite unbounded V_Q; the inverse maps into D(N), since D_E is linear in N up to bounded diagonal terms. This establishes the legitimate inverse of the self-adjoint Q compression.

No complement eigenvalue lies in the strip. The middle negative inertia is two by continuation from g=0 (the same estimates hold for a homotopy reducing only V_Q to zero); the tail is positive. Thus QHQ-E has precisely two negative eigenvalues throughout the strip.

## D. Certified remainder and root localization

For a rational function f(t)=p(t)/q(t) with q(0)>0, a certified upper bound on |f| for 0<=t<=T is

sum |p_k|T^k / [q_0-sum_{k>=1}|q_k|T^k],

provided the denominator is positive. Exact algebra and this coefficient bound, applied to a/t^3,bL/t^3,bU/t^3 and (1/det(M)-1/64)/t, give

|a|<=g^6/10, |b|<=g^6/10,

|F_05-(sqrt120/64)g^5|<=g^7/5.

The actual bounds are approximately 0.068738,0.075021 and 0.064947 in the respective normalizations; the decimal values are diagnostic only. By the row-sum norm bound, with J=[[0,1],[1,0]],

||F(x)-kappa*g^5*J|| <= g^6/10+g^7/5 <= (3/25)g^6.

All rational arithmetic assertions are saved in feshbach-symbolic.log; no fitted coefficient is used.

The complement inverse is analytic in the strip, and

F'(E)=-I-PHQ(QHQ-E)^(-2)QHP,

-I-11g^2 I <= F'(E) <= -I,

since ||QHP||^2=11g^2 and the resolvent norm is <1. Ordered eigenvalues of F therefore decrease at slopes between -(1+11g^2) and -1 in the finite-difference/min-max sense. At x-1/1000 both are positive, and at x+1/1000 both are negative, since ||F(x)|| <= kappa*g^5+(3/25)g^6<1/1000. Each ordered eigenvalue has one root; the Schur inertia identity with the complement's two negative levels labels these roots E_2^+ and E_3^+.

Let lambda be the corresponding ordered eigenvalue of F(x), and h=E-x. Monotonicity gives |h|<=|lambda| and |h-lambda|<=11g^2|h|. Weyl's 2x2 bound gives |lambda-(+/-kappa*g^5)|<=(3/25)g^6. Consequently

|h-(+/-kappa*g^5)| <= [3/25+11g(kappa+(3/25)g)]g^6
 <= [3/25+(11/10)(11/64+3/250)]g^6
 = (128905/400000)g^6 < g^6/3.

 Since kappa>17/100 and g/3<=1/30, the lower-level upper-bound margin is positive. This establishes statement B including the indexing and a uniform O(g^6) remainder.

## Meaning and limits

The fifth-order coupling sqrt(5!)/64 is already in primary multiphoton literature. This derivation does not claim discovery of that coefficient or of a new resonance. The proposed difference is a rigorous explicit finite coupling range, remainder and sorted level-index certificate that can decide the Lanuza indexed bound where second- and fourth-order diagonal margins cancel. The full original claim is still unresolved. Novelty and significance require fresh referee comparison. Raw retrievals and comparison are in this directory and in pass2-current-retrieval.json. No mutable handoff file supplies any step of this argument.

## Arithmetic replay and diagnostic point certificates

The checker reconstructs det(A8) by the determinant expansion over the 34 matchings of the eight-site path. An occupied edge e contributes -(e+1)t; an unmatched vertex contributes q_n. Products and sums of Fraction bivariate polynomials give the full 73-coefficient polynomial without calling Sympy or the generator recurrence.

At selected rational g and Delta the checker additionally uses a head of 80 sites. For a rational endpoint z below the tail form bound b80, the infinite-operator count below z is bounded between negative inertia of A80-z and of A80-z-[80g^2/(b80-z)]|79><79|. This follows by the positive-tail Schur complement, whose omitted scalar resolvent is between zero and 1/(b80-z). Equal bounds certify the full count. Integer determinant Sturm signs and a separate Fraction LDL calculation check both finite inertias. The root brackets use rational upper/lower enclosures of sqrt120 verified by squaring. These point checks validate implementations and branch labels; the continuum and g->0 assertions rely on the uniform proof above.
