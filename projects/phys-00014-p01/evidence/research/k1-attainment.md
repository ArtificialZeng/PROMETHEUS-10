# Exact k=1 measurement and NH certificates

Proposer job: `phys-00014-p01-research-f15bfc274f9b`.
This is a restricted result submitted for a fresh referee, not acceptance.
The frozen original asks about k=1,2,3,4; only k=1 is settled here.
Inputs are the stable `evidence/reproduce/source-input-derivation.md`,
`input-a.json`, `input-b.json`, and `exact-input-map.json`. The prior,
channel, factor-swap and Pauli conventions remain those in `source.md`
and `problem.md`. No mutable handoff supplies a derivation.

## Claim and conventions

For the fixed single Bell probe, Cartesian-volume prior on the radius
a=pi/4 ball, known 0<=lambda<=1 and risk E[||hat(theta)-theta||^2]/3,

    R_1(lambda) = C_NH(1,lambda) = pi^2/80 - 4(1-lambda)^2 q^2,
    q = 3/(8a) - 3/(16a^3) = 3/(2pi) - 12/pi^3.

The optimization is over all physical joint POVMs on the system and
untouched ancilla and all finite-second-moment estimators. There is no
probe optimization, unbiasedness, adaptive-use or k>1 assertion.

Use the source spin basis |0>,|x>,|y>,|z> and rephase each spin-one
column as |tilde(i)>=-i|i>. Its vector is
v(theta)=cos(r)|0>+sin(r) sum_i n_i|tilde(i)>.
This is a basis change only. In these real coordinates, with E_ab the
matrix units, P0=E_00 and P1=sum_i E_ii,

    Gamma0 = A P0 + B P1,
    Gamma_i = Q F_i,       F_i=E_0i+E_i0,
    A=(1-lambda)C+lambda/4,
    B=(1-lambda)(1-C)/3+lambda/4,
    Q=(1-lambda)q,
    C=1/2+3/(4a)-3/(8a^3),   A+3B=1.

A,B are strictly positive even at lambda=0. The moment sign follows
by conjugating the reproduced iQ(E_0i-E_i0) with
diag(1,-i,-i,-i), rather than replacing the physical parameter by -theta.

## A four-outcome projective measurement

Let s_j be (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1). Define

    |e_j> = (|0> + sum_i s_ji |tilde(i)>)/2,
    M_j=|e_j><e_j|,       hat(theta)_j = 2Q s_j.

These four vectors are orthonormal: 1+s_j dot s_l is 4 for j=l
and zero otherwise. Thus M_j>=0 and sum_j M_j=I_4. The measurement
is independent of lambda, while the estimator depends on the known noise.
The actual source/computational-basis vectors are
(W S diag(1,-i,-i,-i)) e_j, with W,S from the reproduced input map.
They are physical vectors on the two-qubit system-ancilla Hilbert space.
Each vector is maximally entangled: its coefficient matrix is proportional
to (I-i sum_i s_ji sigma_i), whose product with its adjoint is 4I.
No locality or implementation by a specific apparatus is assumed.

More explicitly, put U0=(I-i(sigma_x+sigma_y+sigma_z))/2. For the
listed outcomes, U0^dagger U_j is respectively I, i sigma_y,
i sigma_z, i sigma_x. The PVM can therefore be implemented by applying
the fixed single-qubit U0^dagger on the encoded subsystem followed by a
standard Bell-basis measurement (with the indicated label permutation).
This is a mathematical circuit identity, not a claim of an experiment.

Tr(Gamma0 M_j)=(A+3B)/4=1/4, and
Tr(Gamma_i M_j)=Q s_ji/2. Consequently the estimator displayed is
exactly the posterior mean, with squared norm 12Q^2 at every outcome.
The Bayes risk equals the prior risk minus the posterior mean-square
gain divided by three: pi^2/80-4Q^2.

The finite PVM's first-moment operators are commuting completions of the
star operators. With {i,j,l}={1,2,3},

    X_i^tet=2Q(F_i+E_jl+E_lj),
    (X_i^tet)^2=4Q^2 I,   [X_i^tet,X_j^tet]=0.

The spin-one completion terms have zero overlap with every Gamma_i;
they make a common projective measurement possible. They do not make
the individually optimal SLD operators commute or saturate the SLD bound.
The covariant sphere has different first/second moment operators but
the same optimal risk. The reproduced SLD expression gives the exact
incompatibility gap

    R_1-C_SLD = 8B Q^2/(A+B)>0 for lambda<1,
    C_SLD = pi^2/80-4Q^2/(A+B).

Both sides coincide at lambda=1. This is a finite Bayesian precision
statement, without a local-unbiased or asymptotic interpretation.

The estimates stay in the prior ball. Since
q=E_r[r sin(r)cos(r)]/3 <= E_r[r]/6 = a/8,
their norm 2sqrt(3)Q is at most sqrt(3)a/4<a. This uses the specified
radial density 3r^2/a^3; no Haar measure is substituted.

## A normalized SO(3)-covariant continuum measurement

For n on the unit sphere with probability measure dOmega/(4pi), take

    dM(n)=|m(n)><m(n)| dOmega/(4pi),
    m(n)=|0>+sqrt(3) sum_i n_i|tilde(i)>,
    hat(theta)(n)=2sqrt(3)Q n.

Spherical first and second moments give integral dM=I_4. The probability
density is A+3B=1, and its posterior mean is the displayed estimator.
Its risk is again pi^2/80-4Q^2. The tetrahedral PVM is a finite optimal
alternative, not a replacement of the continuous prior by four atoms.

## Continuum physical-risk dual certificate

Let H=(1/3) integral p(theta)||theta||^2 rho(theta) d^3theta, so that
Tr H=pi^2/80. The loss operator for an arbitrary real estimate t is

    F(t)=H+(||t||^2 Gamma0-2 sum_i t_i Gamma_i)/3.

Define D=-12B Q^2 P0-(4/3)A Q^2 P1 and Y=H+D. By rotational
covariance it suffices to take t=r z, with r=||t||. The matrix F(t)-Y
has a 0,z block

    (1/3) [[A r^2+36B Q^2, -2Qr],
           [-2Qr, B r^2+4A Q^2]],

and two transverse diagonal entries (B r^2+4A Q^2)/3.
Its block determinant is exactly

    A B (r^2-12Q^2)^2/9,

because A+3B=1. Diagonal entries are nonnegative, so the matrix is
positive semidefinite for every r>=0, not just a radius grid or the prior
ball. Integrating Tr[(F(t)-Y)dM(t)]>=0 gives risk >=Tr Y
=pi^2/80-4Q^2 for every POVM and estimator. At r=2sqrt(3)Q the
block has kernel (1,sqrt(3)), giving complementary slackness with the
sphere measurement and with all four tetrahedral outcomes. This argument
does not need full rank of each individual encoded state.

## Exact NH dual certificate (not inferred from physical optimality)

Block indices i,j=1,2,3 are parameter indices; a,b=1,2,3 label the
spin-one coordinates within each 4-dimensional Hilbert block. Define
the 12 by 12 Hermitian matrix K by

    K_ij = (A/3) delta_ij P0
         + (B/3)(delta_ij P1 + E_ij - E_ji).

On parameter space tensor spin-one space write
|omega>=sum_i |i> tensor |i>, Pi_tr=|omega><omega|/3,
and Pi_as=(I-Swap)/2. Then exactly

    K = (A/3) I_3 tensor P0 + B Pi_tr + (2B/3) Pi_as,

where the last two operators are supported only on spin-one Hilbert
coordinates. Thus K>=0. Set x=2Q, X_i=x F_i, and stack X vertically.
The 16 by 16 NH dual matrix is

    Z = [[K, -K X], [-X^dagger K, X^dagger K X]]
      = [I; -X^dagger] K [I, -X] >= 0.

It obeys the exact source-program dual affine conditions

    Z_ii=Gamma0/3,
    Z_ij+Z_ji=0 for i<j<=3,
    Z_i4+Z_4i=-2 Gamma_i/3.

Indeed (K X)_i=x((A/3)E_0i+B E_i0), and the last equality uses
A+3B=1 and x=2Q. Moreover

    Z_44=x^2(3B P0+(A/3)P1),
    Tr Z_44=x^2(A+3B)=4Q^2.

For completeness, weak duality follows directly by tracing Z against
the feasible source Schur matrix [[L,X_primal],[X_primal^dagger,I]]:

    objective - (pi^2/80-Tr Z_44)
       = Tr(Z [[L,X_primal],[X_primal^dagger,I]]) >=0.

Hermitian block symmetry L_ij=L_ji makes the off-diagonal K coefficients
cancel. The Hermitian X_primal blocks give the first-moment coefficients
shown above. Thus the dual proves C_NH>=pi^2/80-4Q^2 independently of
the physical-risk certificate. This is an exact PSD factorization, with
no solver tolerance or eigenvalue threshold.

Conversely any physical POVM with real finite estimates supplies a feasible
NH moment pair X_i=integral t_i dM and L_ij=integral t_i t_j dM:
its full Schur matrix is the integral of
[t_1 I;t_2 I;t_3 I;I] dM [t_1 I,t_2 I,t_3 I,I]. The tetrahedral
measurement above therefore gives C_NH<=pi^2/80-4Q^2. Alternatively
the sphere moments give the explicit covariant primal

    X_i=2Q F_i,
    L_ij=4Q^2 delta_ij P0
         +(12Q^2/5)(delta_ij P1+E_ij+E_ji).

Its Schur complement has zero spin-zero sector and, on parameter tensor
spin-one space, eigenvalues 0 on trace and antisymmetric tensors and
24Q^2/5 on symmetric traceless tensors. Thus it is PSD for every Q.
The primal objective is exactly pi^2/80-4Q^2.

## Endpoints, scope and closest prior work

At lambda=0 the individual outputs are rank one, but the measurement,
moment pair and both certificates remain valid. At lambda=1, Q=0,
all estimates are zero and both optima equal the prior risk. No limiting
full-rank theorem or perturbative approximation is invoked.

Bia/Gagatsos arXiv:2607.15398v1 supplies this rotation model and numerical
near-attainment. Albarelli/Branford/Rubio arXiv:2511.16645v4 / Quantum
10,2192 supplies the quadratic POVM optimality framework (Appendix B)
and the closely equivalent star-moment phase-imaging example (Sec.4.1,
Eqs.58-59). The latter is explicitly numerical regarding NH attainment,
so the star representation and optimality framework themselves are prior
work. The proposed delta is a finite physical measurement and exact
primal/dual saturation for k=1 across the full depolarization interval.
This dossier does not assert priority beyond the bounded recorded search,
does not generalize to arbitrary moment matrices, and leaves k=2,3,4
and the frozen original unresolved. Fresh source, correctness, novelty
and significance review is required before any manuscript.
