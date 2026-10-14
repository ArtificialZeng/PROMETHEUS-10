# Candidate restricted result: local optimality at the coherence threshold

Job: `phys-00015-p01-research-a873439075b5`. This is a proposer derivation awaiting a fresh referee. It is not a proof of the frozen all-heterogeneous problem. The finite searches are not premises of the argument.

## Exact statement and physical interpretation

Fix any integer n>=5, put t=tan(pi/n), and consider a uniform nearest-neighbor ring with clockwise/counterclockwise rates u=c(1+t), d=c(1-t), c>0. Its leading conjugate pair has b/a=1. There exists a neighborhood of this ring in the space of strictly positive cycle rates modulo common time rescaling such that every rate tuple in that neighborhood with b/a>=1 obeys

    Y := sigma*a/b^2 >= Y_*(n) := (1+t^2)*atanh(t)/t > 1.

Equality occurs only for the uniform ring at b/a=1, up to common time scaling. In particular, at fixed b/a=1 the uniform ring is a strict local minimizer of entropy per spectral period. We give the full positive second variation for arbitrary small heterogeneous edge flows and stationary probabilities. Orientation reversal gives the corresponding backward-biased statement.

All neighborhoods here depend on n. No explicit radius, uniform-in-n neighborhood, global minimum, result at arbitrary distance from the uniform ring, or solution of source.md is asserted. The main nontrivial assertion is constrained local optimality and its response tensor. Merely preserving Y>1 in some neighborhood would already follow by continuity and is not claimed as the contribution.

The physical model is the finite autonomous positive-rate single cycle in problem.md. Entropy is in k_B=1 units and natural logarithms; rates, a,b,J,sigma have units inverse time. The proof uses exact finite-dimensional perturbations, no continuum approximation, hidden states or truncated infinite operator.

## Coordinates that cover every nearby legal rate tuple

In a clockwise-current neighborhood J>0. Divide all rates by J, selecting a time unit in which the stationary edge current is one. Let pi be the positive stationary distribution and define

    g_i = pi_(i+1) d_(i+1)/J > 0,
    u_i/J = (g_i+1)/pi_i,   d_i/J = g_(i-1)/pi_i.

These formulas also generate all positive pi,g inputs: the forward and backward edge flows are g_i+1 and g_i, so their difference is one on every edge and the generated distribution is exactly stationary. Conversely, stationary current conservation gives these equations for every nearby cycle. This is a smooth coordinate chart after removal of common rate scale. Reversing the cycle treats J<0.

Choose zero-mean real vectors h,p and write

    g_i = g exp(m+h_i),
    pi_i = exp(p_i)/sum_j exp(p_j),
    sum_i h_i = sum_i p_i = 0.

The single real variable m is the mean log backward flow; h,p each supply n-1 independent heterogeneous directions. The backward generator Q=R^T has rates (g_i+1)/pi_i and g_(i-1)/pi_i. Its stationary entropy rate in the selected time unit is exactly

    sigma=A=sum_i log(1+1/g_i).

These inputs are finite, positive and irreducible for all finite coordinates. The observable Y is independent of the time unit.

## The uniform point, spectral leadership and analytic constraint

At h=p=m=0, pi_i=1/n and Q is circulant. Let theta=2*pi/n, f_l(i)=exp(i*l*theta*i)/sqrt(n), and

    lambda_l=n[(g+1)(exp(i*l*theta)-1)+g(exp(-i*l*theta)-1)].

For g>0 the l=1,n-1 pair is simple, is the only leading nonzero pair, and is separated from other nonzero eigenvalues by strict cosine ordering. These statements are direct Fourier identities, consistent with the inherited published baseline. The positive imaginary member has b=n*sin(theta), a=n*(2g+1)*(1-cos(theta)), and

    q=b/a=cot(pi/n)/(2g+1).

Thus q=1 means g=(1-t)/(2t)>0 since n>=5 gives 0<t<1. Near each finite-n point, the simple eigenvalue continues real analytically and its leading gap remains positive. This follows from the nonzero characteristic-polynomial derivative and the implicit function theorem; no assumption about arbitrary heterogeneous degeneracies is needed for this local result.

The derivative with respect to m is

    lambda_g=-2*n*g*(1-cos(theta))<0,

and q_m=b*lambda_g/a^2<0. The implicit function theorem therefore eliminates m as a real analytic function m(h,p;q) near q=1. Translation invariance makes the first variation in zero-mean h,p vanish; hence m(h,p;1) also has no linear term. The fixed-q cost is stationary in every heterogeneous tangent direction.

## Deriving the second variation

For a path h_i(epsilon)=epsilon*h_i, p_i(epsilon)=epsilon*p_i first hold m=0, and expand Q=Q0+epsilon*Q1+epsilon^2*Q2/2+O(epsilon^3). Denote h_(i-1) by hprev. The two outgoing rates have derivatives

    (Q1)_i,i+1 = n[g*h_i-(g+1)*p_i],
    (Q1)_i,i-1 = n[g*hprev-g*p_i],
    (Q2)_i,i+1 = n[g*h_i^2-2*g*h_i*p_i+(g+1)*(p_i^2+mean(p^2))],
    (Q2)_i,i-1 = n[g*hprev^2-2*g*hprev*p_i+g*(p_i^2+mean(p^2))].

Diagonal entries are minus their sum; these coefficients follow by differentiating the defining rates, including the softmax normalizer. At l=1, lambda'=0. Put B_j=F^* Q_j F, with F the unitary Fourier matrix. The simple-eigenvalue second derivative is

    lambda''=(B2)_11 + 2*sum_(l!=1) (B1)_1l*(B1)_l1/(lambda_1-lambda_l).

This follows by solving (Q0-lambda_1)v'=-Q1*v, with f_1^*v'=0, and projecting the twice-differentiated eigen-equation. It does not require Hermiticity of Q; Q0 is diagonalized by the unitary Fourier basis.

Restoring fixed q=1 means m(epsilon)=m''*epsilon^2/2+O(epsilon^3), where

    m''=-(Re(lambda'')+Im(lambda''))/lambda_g.

The affinity and Y second derivatives are consequently

    A''=g/(g+1)^2 * sum_i h_i^2 - m''*n/(g+1),
    Y''=Y0*(A''/A0-Im(lambda'')/b0),
    A0=n*log((g+1)/g), b0=n*sin(theta), Y0=A0/b0.

For reference, the Fourier matrix elements used to reduce the sum are

    (B1)_lm = n*g*[exp(i*m*theta)-1
                    + exp(-i*(l-m)*theta)*(exp(-i*m*theta)-1)]*hhat_(l-m)
                - lambda_m*phat_(l-m).

Here lambda_m denotes the m-th Fourier eigenvalue; the mean-flow derivative is lambda_g (named lg in the scripts). Only l=1+k,1-k contribute for a single real spatial Fourier mode k. Products of different mode indices average to zero, so the real Hessian separates into mode blocks. Cyclic translation gives the same cosine/sine diagonal coefficients and the skew phase coupling below.

## Closed blocks and exact positivity

For 1<=k<n/2 set v=tan(pi*k/n), x=t^2 and L=log((1+t)/(1-t))=2*atanh(t). Then v>=t. Write

    h_i=Hc*cos(k*theta*i)+Hs*sin(k*theta*i),
    p_i=Pc*cos(k*theta*i)+Ps*sin(k*theta*i).

In the variable order (Hc,Hs,Pc,Ps), the second derivative is the quadratic form with real symmetric matrix

    [ hh   0   hc   hs ]
    [ 0   hh  -hs   hc ]
    [ hc -hs   pp    0 ]
    [ hs  hc    0   pp ].

The coefficients can be written compactly using

    S=L*(1-x)^2+2*t*(1+x),
    D_+-=(1-x)^2*(v+-2*t)^2+4*t^4*v^2+t^2*(1+6*x-3*x^2),
    D=D_+*D_-,
    Ph=2*t^2*(1+x)*[L*(1-x)^2*(3*x-1)+2*t*(1+x)^2]
                  +(v^2-t^2)*(5*x^2-2*x+1)*S,
    Pc_poly=L*t^2*(3-x)*(1-x)*(1+x)-2*t^3*(x^2-6*x+1)
                  +v^2*[L*(1-x)*(1+x)*(3*x-1)+2*t*(7*x^2-2*x-1)],
    Pd=2*t^2*(1+x)*[4*t^2*(1+x)-L^2*(1-x)^3]+(v^2-t^2)*S^2.

Then

    hh=t*(1+x)*(1+v^2)*Ph/[(1+t)^2*D],
    pp=(1+t)/(1-t)*hh,
    hc=-t*(1+x)^2*Pc_poly/[(1+t)*D],   hs=v*hc,
    hh*pp-hc^2-hs^2=t^2*(1+x)^2*(1+v^2)*Pd/[(1-t)*(1+t)^3*D].

Direct substitution in the two-mode eigenderivative above yields these rational expressions. scripts/research_symbolic_curvature.py performs that symbolic reduction over Q(t,v,L); scripts/check_curvature_sign.py verifies the alternate factorizations exactly. Neither script turns finite sampled signs into a universal sign assertion.

All denominator factors are positive on 0<t<1,v>=t: 1+6*x-3*x^2>0 for 0<x<1, so each D_+- is strictly positive. Also S>0 and 5*x^2-2*x+1=5*(x-1/5)^2+4/5>0.

The elementary integral inequality atanh(t)<t/(1-t^2), valid for 0<t<1, gives L<2*t/(1-x). For Ph at v=t, if 3*x>=1 positivity is immediate. If 3*x<1, its bracket is strictly larger than

    2*t*[(1+x)^2-(1-x)*(1-3*x)]
        =4*t*x*(3-x)>0.

Its v^2 slope is positive, so Ph>0 for every v>=t. For Pd at v=t,

    L^2*(1-x)^3 < 4*t^2*(1-x) < 4*t^2*(1+x).

Its v^2 slope S^2 is positive, so Pd>0 as well. Thus hh>0 and the displayed Schur determinant is strictly positive. The four-dimensional Hessian block is positive definite (equivalently its two-dimensional complex Hermitian block is positive definite).

If n is even, k=n/2 is a Nyquist mode: sine vanishes and the two Fourier signs coincide. Direct alias counting in the eigenderivative doubles the generic cosine coefficients in the v->infinity limit. The two-dimensional real block is diagonal because hc,hs tend to zero, with

    hh_Nyquist=2*t*(1+x)*S/[(1+t)^2*(5*x^2-2*x+1)]>0,
    pp_Nyquist=(1+t)/(1-t)*hh_Nyquist>0.

There is no k=0 heterogeneous mode because h,p have zero mean. Consequently the complete tangent Hessian is positive definite for every fixed n>=5. All aliased and conjugate modes are included.

## From the Hessian to the neighborhood statement

At fixed q=1 this finite-dimensional analytic function is stationary and has a positive definite Hessian on the entire 2(n-1)-dimensional heterogeneous tangent space. Taylor's theorem therefore gives a strict local minimum, with equality only at h=p=0. No explicitly computed error radius is needed for this existential finite-n statement; an explicit finite perturbation guarantee would require a remainder bound and is not asserted.

Along the uniform family at general q near one,

    Y_unif(q)=2*atanh(q*t)/[q*sin(theta)].

Its derivative is positive for q>0 with q*t<1, since z/(1-z^2)-atanh(z)>0 for z in (0,1) (differentiate, or integrate its positive derivative). By continuity, the derivative of the heterogeneous constrained-chart cost with respect to q is still positive in a sufficiently small neighborhood of (h,p,q)=(0,0,1). For q>=1 in a product neighborhood, lowering q to one at fixed h,p lowers Y and remains in the local chart. Combine this with the fixed-q strict minimum to obtain the stated local minimum on the eligible side q>=1.

At q=1, Y_*(n)=(1+t^2)*atanh(t)/t>1. Equality in the local minimum requires h=p=0 and q=1, leaving only common rate scale. Rates stay positive, the exact stationary law stays normalized, and the leading pair remains simple and spectrally isolated in the selected neighborhood. The result covers every leading member of that conjugate pair. It makes no claim about distant Jordan points or degeneracies, or about n->infinity interchange with perturbation size.

## Verification and limits

216 finite Fourier blocks (n=7,8,9,10,11,12,18,24,50, applicable q=1,1.5,2) were checked numerically as discovery diagnostics in evidence/research-local-variation.json and .log. At q=1 the least tested eigenvalue was 0.0024883694645669 at n=50; these numbers do not prove the all-n sign. Direct finite differences with the coherence constraint independently restored agree with the eigenderivative formula on five nontrivial directions. The observed finite-difference errors decrease initially with step size and ultimately reach cancellation error. No extra significant digits or interval interpretation is attached to those tests.

Independent same-worker algebraic replay differentiates the full defining generator and solves a bordered eigenvector system at n=6, including generic cosine, sine-coupled and Nyquist directions, in scripts/check_local_variation_exact.py. Its actual results are in evidence/research-exact-local-replay.json and .log. This is representational verification, not a fresh referee or acceptance. The rigorous all-n sign conclusion rests on the explicit inequalities and Fourier reduction above.

The original universal question remains unresolved. The 30,000 natural-rate/flow and 12,000 inverse-coordinate searches found no eligible violation; this negative numerical search is only the motivation for examining the local extremum. A current-frequency proof shortcut is unsupported: evidence/research-frequency-bridge-example.json numerically exhibits an eligible leading pair with b/(2*pi*J)>1 while Y>1, so that shortcut cannot be assumed. This auxiliary observation is not submitted as a new disproof of a published claim.

Closest-prior-work comparison and bounded priority coverage are in evidence/research-prior-comparison.md. The candidate theorem does not derive the current-free entropy bound from an affinity-only sector inequality and does not replace the exact spectral observable by a phase current.
