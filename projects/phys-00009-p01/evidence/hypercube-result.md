# Two-particle relaxation crossover on homogeneous hypercubes

Proposed restricted result, research job phys-00009-p01-research-144fa92f3934.
This is stable scientific evidence, not a manuscript or referee acceptance.
The original all-graph/all-alpha/all-k degree-two conjecture remains unresolved.

## Statement and physical conventions

Let Q_D have vertex set (Z/2Z)^D, D>=1, with one undirected edge of
conductance c>0 for each coordinate flip. Use the immutable source's closed
SIP generator, with homogeneous dimensionless site parameter alpha_x=a>0.
Let lambda_1 and lambda_2 denote the one- and two-particle gaps. Then

    lambda_1 = 2 c a,
    lambda_2 = c min{2a, rho_D(a)},

where rho_D(a) is the smallest positive eigenvalue of the (D+1)-state
birth-death negative generator T_D(a). In Hamming-distance order d=0,...,D,
its downward jump rate is 2 d a + 2 1_{d=1}, its upward jump rate is
2(D-d)a, and its diagonal is their sum; off-diagonal entries are minus
these rates. Define

    a_D = (D-1) 2^{-(D-1)} integral_0^1 (1+u^2)^{D-1} du - 1.

For D=1,2,3, this number is respectively -1,-1/3,-1/15 and
lambda_2=lambda_1 for all a>0. For every D>=4 it is positive, and

    lambda_2 < lambda_1  iff  0<a<a_D;
    lambda_2 = lambda_1  iff  a>=a_D.

The recurrence

    a_(D+1) = (D^2 a_D + 1)/[(D-1)(2D+1)],  D>=2,

gives a_4=1/35, a_5=17/315, a_6=37/693, and D^2 a_D -> 1.
The latter is a limit of this two-particle crossover threshold, not a
thermodynamic phase-transition claim or a uniform many-particle theorem.

For D=4, rho_4(a) below the crossover is the smallest positive root of

    lambda^3 -(32a+2)lambda^2 +(304a^2+32a)lambda
                -768a^3-48a^2 = 0.

Thus a finite, exact change in the slowest two-particle mode occurs at a=1/35.
All displayed gaps with c=1 use that inverse-time unit. Multiplication by c
restores units; a_D does not depend on a common time rescaling.

## 1. Translation characters exhaust the two-particle space

For q in (Z/2Z)^D write chi_q(x)=(-1)^{q dot x}. Represent a two-particle
configuration by the unordered pair {x,y}, including x=y for a stack.
A function in translation-character q has the form

    f({x,y}) = chi_q(x) g(x+y),

with addition modulo two. The swap x<->y imposes
g(z)=chi_q(z)g(z), so g(z)=0 whenever chi_q(z)=-1. Conversely this condition
makes the expression well-defined. The translation group acts unitarily in
the homogeneous reversible measure, so its character spaces are orthogonal
and exhaust the occupation-function space. Their dimensions are 2^D for q=0
and 2^{D-1} for every q!=0, totaling
2^D+(2^D-1)2^{D-1}=2^D(2^D+1)/2, the occupation-space dimension.

Set c=1 until the last step. Direct substitution in the source jump rates
gives the negative-generator block B_q. On the allowed relative displacements:

* The diagonal is 2Da at z=0 and 2Da+2 1_{|z|=1} otherwise.
* If q_i=0 and z differs from zero, the transition to z+e_i has coefficient
  -2a, except that z=e_i gives coefficient -2(a+1) to zero.
* From zero to e_i with q_i=0 the coefficient is -2a.
* A coordinate with q_i=1 takes the relative displacement out of the allowed
  set, giving no off-diagonal block coefficient. Both particle contributions
  to that displacement vanish in this character space. Their departure
  rates remain in the diagonal.

These rules also follow at a stack: each of two particles leaves at rate a,
so the total departure rate is 2Da. No ordered-pair factor is omitted.

## 2. Every nontrivial translation character is bounded by 2a

Let m=|q|>=1 and let r=D-m be the number of coordinates with q_i=0.
The active q-coordinates of an allowed z have even parity and are fixed
under the off-diagonal moves in B_q. If those m bits are all zero, the
corresponding component is

    B_0 on Q_r + 2ma I.

Here B_0 on Q_r is itself the translation-invariant two-particle block on
the r-dimensional cube. It has nonnegative spectrum and a zero eigenvalue
because it is the restriction of a reversible Markov negative generator.
For r=0 take it to be the one-dimensional zero operator. On any nonzero
even-parity pattern of the m bits there is no zero or unit displacement,
so the component is

    2a Laplacian(Q_r) + 2ma I.

Both components have spectrum bounded below by 2ma. In particular all
nonzero-character eigenvalues are >=2a, and the characters with m=1 attain
2a. This proves the exact inherited one-particle branch and prevents a
non-radial translation character from invalidating the claimed minimum.

## 3. Within q=0 only a radial mode can lie below 2a

B_0 acts on all relative displacements z. It is reversible with weights
w(0)=(a+1)/a and w(z)=1 for z!=0: detailed balance on 0<->e_i is
w(0)2a=w(e_i)2(a+1). Coordinate permutations preserve this measure and
the generator. Let R be the radial subspace, functions of |z| alone.
Its orthogonal complement consists of functions whose sum on every Hamming
shell is zero, and in particular f(0)=0 and sum_{|z|=1}f(z)=0.

On that complement the weighted norm equals the ordinary counting norm,
and the operator identity is

    B_0 f = 2a Laplacian(Q_D) f + 2 1_{|z|=1} f.

The extra column at z=0 annihilates f(0); the z=0 row agrees because the
unit-shell sum is zero. These functions also have zero counting mean.
The ordinary cube Laplacian has gap 2, from its Walsh eigenvalues 2|q|.
Consequently their Rayleigh quotients are at least 4a. This is an exact
quadratic-form bound, not an eigensolver observation.

On R the negative generator is precisely T_D(a), with the jump rates stated
above. All its rates between neighboring distances are positive; it is a
finite irreducible reversible birth-death chain. Combining the nontrivial
character bound, the non-radial q=0 bound, and the exact m=1 eigenvalue gives
lambda_2=min{2a,rho_D(a)} for every D and a>0.

## 4. Exact finite-a threshold

Let R_D be the radial cube Laplacian: diagonal D, downward coefficient -d
and upward coefficient -(D-d). Its eigenvalues are 2j, j=0,...,D. Then

    T_D(a)/(2a) = R_D + a^{-1} e_1(e_1-e_0)^T.

The matrix M=R_D-I is invertible. The determinant lemma at the competing
one-particle eigenvalue 2a yields

    det(T_D(a)-2a I)
       = (2a)^{D+1} det(M) [1 + h_D/a],
    h_D=(e_1-e_0)^T M^{-1}e_1.

To evaluate h_D, let v=M^{-1}e_1. Its zero-distance row is
(D-1)v_0-Dv_1=0, hence h_D=v_1-v_0=-v_0/D. On the full cube, e_1 is the
indicator of the unit shell, equal to Adj(Q_D) delta_0. With
L=Laplacian(Q_D), Adj=D I-L, so

    v_0 = (D-1)G_D - 1,
    G_D = [(L-I)^{-1}]_{00}
        = 2^{-D} sum_{j=0}^D binomial(D,j)/(2j-1).

The final expression follows from the normalized Walsh characters; none of
the denominators vanish. Therefore -h_D=[(D-1)G_D-1]/D. Integration by parts
of ((1+u^2)^D-1)/u^2 gives

    G_D = -1 + D 2^{-(D-1)} integral_0^1 (1+u^2)^{D-1} du,

which proves -h_D=a_D with the formula in the statement. The determinant
at 2a can thus vanish at a positive a only at a=a_D, and its zero there is
simple as a function of a.

For a->infinity the positive eigenvalues of T_D(a)/a tend to 4j,
j=1,...,D, since T_D(a)/a->2R_D. Thus every positive radial eigenvalue is
larger than 2a for sufficiently large a. At every positive a the radial
birth-death eigenvalues are real, simple and continuous. If a_D<=0, none can
cross 2a and rho_D(a)>2a for all a>0. If a_D>0, exactly one can cross and it
must be the first positive eigenvalue: a higher one cannot reach 2a while
the first remains above it, and a prior crossing would require another
positive zero of the determinant. Simplicity of the determinant zero forces
a sign change. Hence rho_D(a)<2a below a_D, equals 2a at a_D, and is greater
than 2a above a_D. This supplies the full iff statements, not just existence
of a radial eigenvalue below a single-particle comparison.

Put H_m=2^{-m} integral_0^1(1+u^2)^m du. Integration of the derivative of
u(1+u^2)^m yields H_m=[1+m H_(m-1)]/(2m+1). Substitution into
a_D=(D-1)H_(D-1)-1 proves the stated recurrence. Direct values at D=1,2,3,4
give the negative thresholds and a_4=1/35; the recurrence then proves
positivity for every D>=4.

For the large-D limit set b_D=D^2 a_D. Its recurrence is

    b_(D+1)=q_D(b_D+1),
    q_D=(D+1)^2/[(D-1)(2D+1)] -> 1/2.

For D>=6, 0<q_D<=4/5, which first bounds b_D uniformly. The identity
b_(D+1)-1=q_D(b_D-1)+(2q_D-1), with q_D->1/2, then implies b_D->1 by a
contraction estimate with a vanishing inhomogeneous term. This proves the
threshold asymptotic without numerical fitting.

## 5. Four-dimensional polynomial and exact checks

The radial characteristic polynomial at D=4 is

    lambda (lambda-8a)
      [lambda^3-(32a+2)lambda^2+(304a^2+32a)lambda-768a^3-48a^2].

At lambda=2a it is 96a^4(35a-1), consistent with the general threshold.
The exact checker compares full rational occupation matrices from direct
jumps and an independently assembled incidence form. It verifies character
intertwiners, their ranks, the radial lump and exact polynomial/root ordering
at D=3,a=1/100 and D=4,a=1/100,1/35,1/10,1. It also checks the determinant,
Green-function, integral and recurrence threshold identities at D=1,...,16.
The all-D proof above, rather than this finite list, establishes the quantifiers.

Actual code and outputs: evidence/research_hypercube_check.py,
evidence/research-hypercube-checks.json,
evidence/research-hypercube-symbolic-checks.json and
evidence/research-hypercube-check.log. The checker and proof have the same
proposer; their agreement is not independent referee acceptance.
The earlier evidence/research-cube-radial-diagnostic.json contains an unchanged
substitution diagnostic caused by differing SymPy symbol assumptions. Its
at_2a field is not used as a certificate. The explicit-symbol calculation in
the final checker replaces that failed diagnostic and records a real identity.

## Scope and physical consequence

Below a_D a translation-invariant pair-separation observable relaxes more
slowly than every one-particle observable. Above a_D the two-particle gap is
an inherited one-particle mode. The exact dimension-dependent boundary and
D^2 a_D limit quantify a finite-diffusivity crossover in this established
attractive Markov model, beyond the prior directional a->0 existence statement.
The radial reduction includes checks that all excluded symmetry sectors lie
higher; mere lumping would only have supplied an upper bound.

No k>=3 gap identity follows from this result. By the published monotonicity,
lambda_k<=lambda_2<lambda_1 below a_D for k>=2, so one-particle reduction of
the full conservative SIP is certainly impossible there. For a>=a_D the
full many-particle gap may still be smaller; it is not determined here.
The new result is restricted to homogeneous hypercubes and exactly k=2,
with a stated threshold limit. It neither proves nor disproves the original
universal equality lambda_k=lambda_2, and makes no empirical or new-particle claim.
