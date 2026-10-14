# Exact diagnostic reductions, research pass 1

These are stable supporting derivations, not a frozen scientific candidate or
referee acceptance. Source: the immutable source.md, problem.md, final JPA
Eqs. (8),(19),(41), and PRL supplemental Eq. (S3). No rounded value of psi_0
enters the analytic statements below.

## Legendre conversion

Write d=sigma/(k_B J)>0, t=d/(2 psi)>0, c=J coth(t), and a=J/c=tanh(t).
Extend B(j) continuously to [-c,c], using 0 log(0)=0, and set B=+infinity
outside. Differentiation gives

    B'(j)=log[(c+j)/(c-j)]-log[(c+J)/(c-J)]
         =2 atanh(j/c)-2t,
    B''(j)=2c/(c^2-j^2)>0.

For every finite real s the maximizing current is strictly interior:

    j_B(s)=c tanh(t+s/2).

Direct substitution (or the conjugate of binary relative entropy) gives

    H_psi(s)=B*(s)
            =2c log[cosh(s/2)+a sinh(s/2)]
            =2J coth(t) log[cosh(t+s/2)/cosh(t)].

Thus H(0)=0, H'(0)=J, and H''(0)=J/sinh(d/psi), as required by the
source noise inequality. B is proper closed convex. The physical real CGF
is convex; at finite positive temperature it is smooth wherever its
defining energy integral exists. Fenchel inequalities alone suffice for
the counterexample direction: if chi(s)<H(s), then

    I(j_B(s)) >= s j_B(s)-chi(s)
               =B(j_B(s))+H(s)-chi(s)>B(j_B(s)).

Conversely, if I<=B throughout (-c,c), continuity of B and the interior
maximizer yield chi>=H (using chi=I* for the closed physical CGF).
If chi>=H for all s, conjugating gives I<=B. A single CGF gap therefore
certifies a rate-function violation at a stated interior current, without
assuming that the saddle of chi equals the saddle of H.

## Fixed reversed-mean test that avoids a Legendre saddle

For every psi>0, -J is strictly inside the stipulated domain because c>J.
Direct simplification gives

    B_psi(-J)=2J log[(c+J)/(c-J)]
             =4Jt=2sigma/(psi k_B).

The exact conservative infimum bound psi_0>=1/2 is proved in
r1-exact-psi-control.md. Consequently B_psi0(-J)<=4sigma/k_B.
With the explicit real field s=-24, Fenchel's inequality gives

    I(-J)>=24J-chi(-24).

A certified positive value of the LINEAR residual

    Delta=24J-chi(-24)-4sigma/k_B

therefore directly disproves the frozen original bound at the known current
j=-J, with strict margin at least Delta. No approximate psi, minimizer of
the physical rate function, or unknown psi-dependent current is needed.
All three rates must still be integrated/enclosed for the same legal finite
physical sample. This exact reduction makes the next certification test
cheaper than solving a Legendre saddle or enclosing a nonlinear H.

## Three-terminal cyclic algebraic family

Order reservoirs as (0,1,2), occupations (x,z,y), and

    P=[[0,0,1],[1,0,0],[0,1,0]].

Outgoing lead 0 receives incident lead 2. Extracted counts are X=n_0-n_2.
Their single-energy MGF, both from the source determinant and elementary
independent Fermi occupations, is

    G(s)=(1-x+x exp(s))(1-y+y exp(-s)),
    J_0=x-y, J_1=z-x, J_2=y-z, sum J_i=0.

Let ell(u)=log[u/(1-u)]=(mu-E)/(k_B T). Actual all-reservoir entropy
in units k_B per energy-channel attempt is

    e=ell(x)(x-y)+ell(z)(z-x)+ell(y)(y-z)
     =D(y||x)+D(x||z)+D(z||y),

where D is binary relative entropy. This follows by telescoping reservoir
binary entropies, exactly as PRL (S3). It is not event reversal entropy.
For fixed 0<y<x<1, the z-dependent part is strictly convex, since each
relative entropy is strictly convex in its corresponding argument, and
has its unique minimizer in (y,x), solving

    (z-x)/(z(1-z))+ell(z)-ell(y)=0.

For a fixed energy E0, any interior occupations can arise from the same
finite chemical potentials mu_i=E0+k_B T ell(f_i), with a common T>0.
Finite-width integration must use these fixed parameters, not independently
chosen occupations at each energy. P at one energy is only an algebraic
diagnostic until a stationary finite-width scattering realization is supplied.

## Longer cycles as a separate diagnostic

For L>=3, order (x,z_1,...,z_{L-2},y) and use the forward cyclic permutation.
The counted marginal still depends only on x,y, but the total entropy is
D(y||x)+D(x||z_1)+...+D(z_{L-2}||y). A sufficiently gradual path can
reduce the latter sum as L grows. This observation is a lead, not a claim
that any finite admissible scatterer violates the frozen bound.
