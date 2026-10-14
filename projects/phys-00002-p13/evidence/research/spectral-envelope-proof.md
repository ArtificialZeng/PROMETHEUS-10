# Sharp three-state large-affinity first-passage envelopes

Proposer: phys-00002-p13-research-2695f8811a9c, 2026-10-12. This stable evidence file contains the argument; mutable handoffs are not inputs. No independent referee acceptance is asserted. Inputs: problem.md; source-ledger.json and its retained Wampler–Barato primary PDF; evidence/reproduction/derivation.md and the two reconstructed generators; evidence/research/boundary-derivation.md for the checked cumulant reduction (the present proof also restates it).

## 1. Precise proposed result

For the positive-rate, time-homogeneous three-state ring of problem.md, at every finite affinity A >= log(64), the following are the independent sharp upper envelopes of its large-threshold scaled FPT skewness and scaled excess kurtosis. The threshold limit is taken at fixed rates first. Define

R=exp(A), eta=sqrt(R), d=(eta+1)/(eta-1), H=(R+1)/(R-1)=(d^2+1)/(2d).

Let p_S and p_K denote the unique positive roots of

P_S(p)=4(d^2-1)p^2+(12d^2-4)p-(d^2-1)^2,

P_K(p)=8(d^2-1)p^3+(-4d^4+24d^2-12)p^2+(2d^4+12d^2-6)p-(d^2-1)^2(d^2+1).

For p>0 put

t(p)=d*p*(2+p)/(1+2p)^2, zeta(p)=d^2*p^2/(1+2p)^3,

V(p)=H-2t(p),

N(p)=3H^2-1-6H*t(p)+6zeta(p),

Q(p)=3H*(5H^2-3)-12*(3H^2-1)*t(p)+12H*t(p)^2+24H*zeta(p).

Then

U_S(3,A)=sqrt(A)*N(p_S)/V(p_S)^(3/2),

U_K(3,A)=A*Q(p_K)/V(p_K)^2.

Both are attained by strictly positive finite rates, explicitly constructed in Section 5. Their optimizing spectra differ. These formulas are algebraic in d, with the explicit entropy-normalization factors sqrt(A) and A. The result is restricted to N=3 and A>=log64; it does not determine kink locations, small-affinity branches, other cycle lengths, or finite-threshold distributions. The original general problem remains unresolved.

At A=log64, P_S reduces, up to a positive factor, to 784p^2+4753p-128, and P_K to 76832p^3+246225p^2+283857p-16640. Supplementary decimal values are in spectral-envelope-values.json; exact defining equations govern the claim.

## 2. Symmetric tilted spectrum gives a global relaxation

Remove only the common physical time scale by taking the geometric mean of the backward rates as the inverse-time unit, so W=product(w_i)=1 and U=product(u_i)=R. All rates, eigenvalues and coefficient numbers below are expressed in that unit. The physical observables are invariant under restoring a common inverse-time scale.

As reconstructed directly and by the independent renewal route,

c2=sum(u_i+w_i),
c1=sum_{i<j}(u_i*u_j+w_i*w_j)+sum_i u_i*w_(i+1),
D=R-1.

The characteristic determinant at the half-affinity field is

det(sI-M)=s^3+c2*s^2+c1*s+C, C=(eta-1)^2,

where M is the real symmetric matrix with diagonal M_ii=-(u_i+w_(i-1)) and off-diagonal entries sqrt(u_i*w_i) on edge i. This follows either from the retained tilted determinant with exp(-Az)=exp(-A/2), or by expanding the symmetric determinant. The product of its three off-diagonal entries is sqrt(UW)=eta. The half-affinity tilted generator is diagonally similar to M: distribute the counting field first; the forward and reverse cycle products both equal sqrt(UW), which is the detailed-balance consistency condition for positive diagonal symmetrization.

For real x,

-x^T M x=sum_i (sqrt(u_i)*x_i-sqrt(w_i)*x_(i+1))^2.

This is strictly positive for x!=0: simultaneous vanishing would require product(u)=product(w), or all x_i=0. Thus all eigenvalues of M are strictly negative. Write them as -x1,-x2,-x3 with x_i>0. Their elementary symmetric coefficients obey

x1*x2*x3=C, c2=x1+x2+x3, c1=x1*x2+x1*x3+x2*x3.

Every physical rate vector therefore maps into the enlarged positive-spectral domain X_C={x_i>0: product x_i=C}. We need not classify every rate-space critical branch or prove that every point of X_C is physically realizable. We will maximize over this relaxation and then realize its maximum by physical rates.

The exact FPT formulas from the retained inverse-SCGF/renewal reconstruction are

t=D*c2/c1^2, zeta=D^2/c1^3,
S=sqrt(A)*(3H^2-1-6Ht+6zeta)/(H-2t)^(3/2),
K=A*[3H(5H^2-3)-12(3H^2-1)t+12Ht^2+24Hzeta]/(H-2t)^2.

No perturbative expansion in A or optimization approximation is involved: these are derivatives through cumulant order four at zero Laplace field. They are the scaled excess kurtosis convention, not ordinary kurtosis or a steady-state current cumulant ratio.

On X_C, the identity

c1^2-3C*c2=((x1*x2-x1*x3)^2+(x1*x2-x2*x3)^2+(x1*x3-x2*x3)^2)/2 >=0

gives 0<t<=D/(3C)=d/3. For A>=log64, 1<d<=9/7, hence

V=H-2t >= (3-d^2)/(6d)>0.

Consequently the relaxation never introduces a zero/negative variance denominator in this claimed interval. This restriction is essential; no extension into smaller affinities with an invalid relaxed denominator is asserted.

## 3. The relaxed maxima exist away from infinity

If a sequence in X_C escapes every compact subset, its largest coordinate L tends to infinity along a subsequence. Since the other two coordinates have product C/L,

c1 >= L*(x_j+x_k) >= 2sqrt(C*L) -> infinity.

Thus zeta->0, and bounded t has a subsequential limit in [0,d/3]. For zeta=0 the derivatives with respect to t are

d(S/sqrt(A))/dt=[3(H^2-1)-6Ht]/(H-2t)^(5/2),
d(K/A)/dt=24[H(H^2-1)-(2H^2-1)t]/(H-2t)^3.

Their respective maxima over the larger interval 0<=t<H/2 occur at

t_S^0=(H^2-1)/(2H), t_K^0=H(H^2-1)/(2H^2-1).

For 1<H<=65/63 both lie below 1/3<=d/3. Indeed each is increasing in H; their upper values are 128/4095 and 16640/282303. These statements follow by elementary differentiation (for t_K^0 the derivative numerator is 2H^4-H^2+1>0). Thus any escaping sequence has S or K bounded by the corresponding zeta=0 maximum.

Now choose a repeated spectral pair x1=x2=r, x3=q=C/r^2 and p=q/r=C/r^3. Direct substitution gives exactly t(p),zeta(p) in Section 1. On p in (0,1),

t'(p)=2d*(1-p)/(1+2p)^3>0,

so t(p) runs from 0 to d/3. For each observable choose p with t(p)=t_S^0 or t_K^0, respectively. Its zeta(p) is strictly positive, and both observables increase strictly with zeta at fixed t:

partial S/partial zeta=6sqrt(A)/V^(3/2)>0,
partial K/partial zeta=24AH/V^2>0.

This repeated-root point strictly exceeds the respective boundary-at-infinity maximum. Continuity, the uniform lower bound on V, and the above escape analysis therefore show that each relaxed supremum is finite and attained at a finite interior point of X_C. If a maximizing sequence were unbounded it would contradict the strict witness; bounded positive-product sequences have compact positive subsequences.

## 4. All relaxed maximizers have a repeated root; the roots above are global

The map (c1,c2)->(t,zeta) has nonzero Jacobian for c1>0. At a local maximum on the two-dimensional X_C its differential cannot have rank two: otherwise a tangent direction could hold t fixed and increase zeta. The coefficient map on X_C has rank two whenever the x_i are all distinct. To see this without fitting, dependence of dc1 and dc2 on the product-constrained tangent space implies multipliers lambda,mu such that

x_i*(c2-x_i-lambda)=mu for every i.

Subtracting the i,j equations gives (x_i-x_j)*(x_k-lambda)=0. If all three are distinct this requires lambda equal to all three roots, a contradiction. Also dc2 can vanish on the tangent space only at the triple-equal point. Hence every relaxed maximizer has at least two equal roots and is on the p-family (the triple-equal case is p=1).

Symbolic differentiation gives the exact factorizations

2V*N'-3N*V'=3*(p-1)*P_S(p)/(d*(2p+1)^5),
V*Q'-2Q*V'=6*(p-1)*P_K(p)/(d^2*(2p+1)^6).

The signs of these expressions are the signs of the derivatives of S/sqrt(A) and K/A, respectively, since the omitted denominators are positive. For x=d^2 in (1,81/49], every nonconstant coefficient of P_S and P_K is positive, and the constant is negative. For P_K the potentially delicate coefficient is -4x^2+24x-12>0, already positive throughout 1<=x<=3. Thus both polynomials are strictly increasing for p>=0 and have a unique positive root.

Section 5 proves these roots are smaller than p_uniform<1. It follows that each observable increases on (0,p_*), decreases on (p_*,1), and increases on (1,infinity). Therefore p=1 is a local minimum and the only possible finite interior maximum along this family is p_*. By Section 3 a relaxed global maximum must exist at a finite point, and by the rank argument it must be on this family. Its value is consequently exactly the p_* expression in Section 1. This excludes all unequal-root critical branches and all noncompact limits without assuming a reflection ansatz captures every rate optimizer.

## 5. Strictly positive physical realization for every claimed affinity

Put y=R^(1/6)>=2, so eta=y^3. The uniform-rate half-affinity spectrum has

r0=y^2+y+1, q0=(y-1)^2, p_uniform=q0/r0.

Substitution into the two derivative polynomials gives

P_S(p_uniform)=8*(y^2-y+1)^3*G_S(y)/[(y-1)^4*(y^2+y+1)^4],

G_S=y^6-3y^4+2y^3-3y^2+1,

P_K(p_uniform)=8*(y^2+1)*(y^2-y+1)^4*G_K(y)/[(y-1)^6*(y^2+y+1)^6],

G_K=2y^8-y^7-8y^6+9y^5-8y^4+9y^3-8y^2-y+2.

For v=y-2>=0 the exact expansions are

G_S=v^6+12v^5+57v^4+138v^3+177v^2+108v+21,

G_K=2v^8+31v^7+202v^6+725v^5+1562v^4+2049v^3+1566v^2+603v+72.

Every coefficient is positive. Since P_S,P_K are increasing, their roots obey 0<p_*<p_uniform<1. Set

r=(C/p_*)^(1/3), q=C/r^2.

Then r>r0 and r-q>3y: r-C/r^2 is strictly increasing, and equals 3y at r0. There is a unique k>y satisfying

2k+eta/k^2=r-q,

because the left side equals 3y at k=y, has derivative 2-2eta/k^3>0 above y, and tends to infinity. Let h=eta/k^2; then h*k^2=eta and h+2k=r-q. All h,k,q,r are finite and positive, and r-2k=h+q>0.

Here are explicit positive edge rates in the W=1 time unit. With B=r*(r-2k), E=r+(eta-1)k, F=eta*r-(eta-1)k, set

u0=(eta/k)*E/B, w0=B/E,
u1=k*F/E,         w1=k*E/F,
u2=eta*B/F,      w2=F/(k*B).

Their products are exactly U=eta^2=R and W=1. Also E>0 and F=eta*(r-k)+k>0, so no irreversible edge or inadmissible limit is used.

To verify their spectrum, let a=sqrt(h*k) and b=(sqrt(h),sqrt(k),sqrt(k)). Define T with diagonals -r+h,-r+k,-r+k, symmetric off-diagonal a on edge 0 and k on edge 1, and entries eta*a forward / a/eta reverse on edge 2. The positive row-null-vector components, with first component 1, are

l1=a*E/B, l2=a*F/B.

The last two equations l^T T=0 follow by solving a 2x2 system of determinant B. The first follows from det T=0: the symmetric companion M0=-rI+b*b^T has spectrum (-r,-r,-q), determinant of -M0=r^2*q=C, and twisting the cycle changes det(-T) by -(eta-1)^2=-C. Equivalently this first equation is the exact polynomial identity checked in spectral-envelope-check.py under 2k^3-(r-C/r^2)k^2+eta=0.

The column generator diag(l)*T*diag(l)^(-1) then has precisely the six rates displayed above and zero column sums. Its half-affinity symmetric matrix has the same diagonals and off-diagonals a,k,a as M0, since u0*w0=u2*w2=eta/k=h*k and u1*w1=k^2. It therefore realizes c2=2r+q and c1=r^2+2rq, so its actual FPT observables equal the relaxed maxima. This proves both the global physical bounds and sharpness for every A>=log64.

## 6. Checks, interpretation, and limits

spectral-envelope-check.py verifies exact derivative identities, the symmetric determinant/positive quadratic form, the coefficient inequality, the two positive-coefficient expansions, the reflection-family rank factorization, and all rate products/escape diagonals under the defining polynomial. It also independently replays rational positive-rate samples against the existing renewal recurrence and evaluates the algebraic optimizers at increasing precision, with rational fixed-affinity rate approximants checked by both the direct determinant and independent renewal. These computations corroborate, rather than replace, the analytic global proof.

Physically the bound limits the asymmetry and excess tails of entropy-threshold timing distributions in dissipative three-step cycles. The attaining mechanism is degeneracy of two decay eigenvalues of the half-affinity tilted generator, not an exceptional point: this matrix is real symmetric and diagonalizable. The finite-affinity sharp values replace a numerically optimized branch on the stated interval; neither a fixed-time-current ratio nor irreversible enzymatic cycle-time bounds is interchangeable with this observable. The rates remain positive and probability conserving, with no extra edges, driving or resetting. The exact cumulant order is four; no all-order statement is needed.

The full historical question and kink positions remain unresolved by this packet. Numerical stationarity, all distinct-rate numerical optima, and exploratory Hessians are not certificates; the spectral relaxation plus explicit realization is the central argument. Literature comparison and priority limitations are separately recorded in pass2-literature-recheck.md. Fresh referee reconstruction of the positivity/global-maximization/realization argument is the next test, not self-acceptance.
