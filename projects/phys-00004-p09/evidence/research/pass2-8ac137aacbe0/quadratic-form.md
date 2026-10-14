# Entropy quadratic form and its sign

Scope: P has strictly positive entries and det(sqrt(P)) is nonzero. Let
M_ij=sqrt(p_ij), Q=M tensor M, G_L=Q Q^T, G_R=Q^T Q. Entropy uses bits.
The coefficient matrix at t=0 has occupied 4 by 4 block Q and twelve null
directions on each side. The auxiliary unitary is exp(i t H), H Hermitian.
Scientific inputs: problem.md; evidence/reproduction/derivation-a.md;
evidence/research/pass1-ed42e17e0d25/tangent-obstruction.md. This calculation
does not take an argument from a mutable checkpoint.

For the 112-dimensional exceptional space (no first-order null-to-null block),
write its diagonal as real d_ij, and its off-diagonal entries as
X_ri^(j)=H[(r,j),(i,j)] for r!=i and
Y_sj^(i)=H[(i,s),(i,j)] for s!=j. Each X^(j),Y^(i) is Hermitian with zero
diagonal; these entries and d uniquely determine H.

The coefficient blocks to second order are

    K(t) = [ Q+t D+t^2 E   t B+O(t^2) ]
           [ t C+O(t^2)      O(t^2)    ],

where D=i F, F=Q elementwise-multiplied by d,
E_ij=-(Q_ij/2)(d_ij^2+sum_r!=i |X_ri^(j)|^2+sum_s!=j |Y_sj^(i)|^2),
B[i,(j,s)]=i Q_ij Y_sj^(i) and C[(i,r),j]=i Q_ij X_ri^(j).
The occupied-to-occupied term in H^2 is its diagonal at (i,j); hence the
second-order entropy coefficient has no cross terms between d,X,Y.

Put f(x)=-x log2 x and T=D Q^T+Q D^dagger. If G_L has eigensystem
(lambda_a,v_a), then the coefficient of t^2 in S(K K^dagger) is

    c(H) = Tr f'(G_L)(E Q^T+Q E^dagger+D D^dagger+B B^dagger)
           + Tr f'(G_R) C^dagger C
           + (1/2) sum_ab L_ab |(v^dagger T v)_ab|^2,

    L_ab=(f'(lambda_a)-f'(lambda_b))/(lambda_a-lambda_b),
    L_aa=f''(lambda_a)=-1/(lambda_a ln 2).

At repeated eigenvalues the continuous diagonal limit applies, so the
formula is basis independent in the degenerate eigenspace. The C term comes
from coupling the positive spectrum to the left null subspace: each positive
eigenvalue obtains the shift <v|Q C^dagger C Q^T|v>/lambda. New Schmidt
weights are O(t^4) here and contribute o(t^2) to entropy. Thus this is a
finite second derivative, unlike generic directions with positive t^2 log(1/t^2).

The first derivative vanishes: T is purely imaginary Hermitian while f'(G_L)
is real symmetric. Unitarity preserves normalization at all t. The +1 in
f' cancels in the total quadratic coefficient.

## Controlled-rotation blocks

Define W_ij=Q_ij [Q f'(G_R)]_ij. For each unordered row pair i<u, let
z_j=X_ui^(j). Its contribution is z^dagger L^(i,u) z, where

    L^(i,u)=diag(Q_i) f'(G_R) diag(Q_i)
            +diag(Q_u) f'(G_R) diag(Q_u)-diag(W_i+W_u).

It has zero row sums because f'(G_L)Q=Q f'(G_R). For Q=M tensor M,
log G_R=log(M^T M) tensor I+I tensor log(M^T M).
A positive off-diagonal entry of a positive-definite two by two matrix
implies a strictly positive off-diagonal entry of its logarithm, by the
two-eigenvalue divided-difference formula. Therefore f'(G_R) has strictly
negative off-diagonal entries exactly on the two-bit square's edges, and
zero entries between Hamming-distance-two vertices.

Consequently L^(i,u) is a connected weighted graph Laplacian:

    c_X(i,u)=sum_{j<k} -f'(G_R)_jk
                     (Q_ij Q_ik+Q_uj Q_uk) |z_j-z_k|^2 >= 0.

Equality requires z constant across j, precisely a local R-unitary gauge.
The column-controlled Y blocks have the transposed expression using G_L;
they are likewise nonnegative with only the local S-unitary gauge kernel.
This accounts for 72 strictly positive real directions after gauge removal.

## Phase block: exact sum of squares

Here M=[[x,y],[z,w]] has strictly positive real entries and x^2+y^2+z^2+w^2=1.
Set

    J=xyzw, u=xy+zw, v=xz+yw, du=xy-zw, dv=xz-yw,
    Delta=xw-yz, delta=sqrt(1-4 Delta^2),
    a=(1+delta)/2, b=(1-delta)/2,
    kappa=ln(a/b)/delta=2 artanh(delta)/delta.

Both single-copy Gram matrices have eigenvalues a,b. Strict positivity and
Delta!=0 imply 0<delta<1: their off-diagonal entries are positive, excluding
a=b, and their determinant Delta^2 is positive, excluding b=0. In particular
kappa>2, since artanh(delta)>delta for 0<delta<1.

Let z_A1,z_A2,z_B1,z_B2 denote the binary signs (-1) to the corresponding
binary label. Define row characters chi_1=z_A1, chi_2=z_A2,
chi_3=z_A1 z_A2, and column characters eta_1=z_B1, eta_2=z_B2,
eta_3=z_B1 z_B2. Modulo phases depending only on the row or only on the
column, the phase matrix has the unique representation

    d=(1/4) sum_{r,s=1}^3 alpha_rs chi_r eta_s.

This is an orthonormal real basis for the nine-dimensional phase quotient.
For binary signs z_A,z_B define

    r1(z_A,z_B)=alpha_11+alpha_13 z_B+alpha_31 z_A+alpha_33 z_A z_B,
    r2(z_A,z_B)=alpha_22+alpha_23 z_B+alpha_32 z_A+alpha_33 z_A z_B,

    Bplus=uv(alpha_12+alpha_21)
          +u dv(alpha_13+alpha_23)+v du(alpha_31+alpha_32)
          +2 du dv alpha_33,

    Dphase=J sum_{i,j=0}^1 p_ij [r1((-1)^i,(-1)^j)^2
                               +r2((-1)^i,(-1)^j)^2]
           +(1/2) Bplus^2.

Let O be any real orthogonal eigenvector matrix of M M^T, with its first
column corresponding to a. Write R=F Q^T-Q F^T and

    zeta=[(O tensor O)^T R (O tensor O)]_(01,10).

The phase coefficient is exactly

    c_phase=( kappa Dphase + (kappa/2-1) zeta^2/(ab) )/ln 2.       (P)

No numerical fit is used in this identity. The following derivation and the
exact coefficient expansion in check_phase_identity.py establish it.

Put g=M M^T, K=g tensor I+I tensor g. The spectrum of Q Q^T is
a^2,ab,ab,b^2, and log(Q Q^T)=log(g) tensor I+I tensor log(g).
Let Ptop,Pmid,Pbottom project onto a^2, the two-dimensional ab eigenspace,
and b^2, respectively. Put Psum=Ptop+Pbottom and

    S=Ptop/a+Pbottom/b=(2I-Pmid-K)/(2ab).

For the phase block let R2=F F^T-(1/2)[(Q elementwise d^2)Q^T
+Q(Q elementwise d^2)^T]. Its trace vanishes. The logarithmic divided
differences between distinct eigenvalue groups, divided by kappa, are 1/a,
1/b and 2. The within-Pmid divided difference is 1/(ab). Accordingly

    c_phase ln 2 = kappa Aphase-zeta^2/(ab),

    Aphase=-Tr K R2-Tr S R Pmid R^T-Tr Psum R Psum R^T,
    zeta^2=(1/2)Tr Pmid R Pmid R^T.

Expansion gives Aphase=Dphase+zeta^2/(2ab), yielding (P).
To check this expansion exactly without symbolic eigenvectors or logarithms,
use

    Pmid=(delta^2 I-(2g-I) tensor (2g-I))/(2 delta^2).

The program works over QQ[x,y,z,w] with four independent unnormalized
amplitudes and normalizes by N=x^2+y^2+z^2+w^2. It verifies all 45 symmetric
coefficients in the displayed nine-dimensional basis after clearing the
explicit denominator. symbolic-phase-identity.json and its actual log record
45 zero polynomials and complete coverage. The denominator is nonzero on
the stipulated physical domain. This is exact algebra supporting the proof;
it is not a fresh scientific referee acceptance.

All terms in (P) are nonnegative. If Dphase=0, the positive probability
weights force r1=r2=0 for all four sign pairs. Thus
alpha_11=alpha_22=alpha_13=alpha_23=alpha_31=alpha_32=alpha_33=0.
The remaining condition Bplus=0 gives alpha_21=-alpha_12, because u,v>0.
On this last direction, writing alpha_12=h, direct multiplication of the
two-by-two Schmidt-basis matrices gives

    zeta^2=4 h^2 ab u^2 v^2/delta^2.

For example, the cross term z_A1 z_B2/4 has coefficient matrix
(Z M) tensor (M Z)/4; in the Schmidt basis its (01,10) minus (10,01)
entry is proportional to b-a. The transposed cross term has opposite sign.
Here the squared off-diagonal matrix elements of Z in the left and right
Gram eigenbases are 4v^2/delta^2 and 4u^2/delta^2. These identities give
the displayed zeta square independently of eigenvector sign conventions.
It is positive for h!=0. Since kappa>2, c_phase=0 therefore forces every
alpha to vanish. The phase quotient is strictly positive definite.

## Exact scope and consequence

The phase sector has 16 real dimensions and seven local phase gauge
directions. Each of the six row-controlled pairs has two constant gauge
directions (real and imaginary), as does each column-controlled pair.
The local auxiliary-unitary gauge has dimension 7+12+12=31, agreeing with
dim U(4)+dim U(4)-1. The quotient of the exceptional 112-dimensional
space therefore has 112-31=81 real dimensions: nine phase directions and
72 controlled-rotation directions, all with strictly positive c(H).

For every fixed H in this exceptional space outside the local gauge,
S(AR;t)=2 h2(a)+c(H)t^2+o(t^2) with c(H)>0. For every fixed H outside
this space, the earlier null-to-null calculation instead gives a positive
leading -t^2 log2(t^2)||A||_F^2 term. Thus every fixed non-gauge Hermitian
generator increases entropy for sufficiently small nonzero t in the stated
auxiliary split. Pure local generators leave entropy invariant exactly.

This result concerns derivatives and each fixed exponential-unitary path.
It does not supply a quantitative common neighborhood for all paths, a
global entropy lower bound, or any result for larger auxiliary splits.
It excludes boundary probability tables and det(M)=0 from this calculation.
It does not prove the original additivity claim. No experimental or
asymptotic resource-rate improvement is asserted.
