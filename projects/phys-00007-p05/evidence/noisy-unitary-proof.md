# Exact solution of the frozen two-qubit noisy-unitary SDP

Proposer job phys-00007-p05-research-6ead7b830b3f, 2026-10-12.
This is a proposed resolution requiring a fresh referee, not an acceptance.
Definitions and convention map are in problem.md and
evidence/reconstruction-and-baseline.md. Primary inputs are indexed by
source-ledger.json. All operators below use the grouped X=RA A,Y=RB B order.

## Statement

For every U in U(4) and every p in [0,1], put P=|u><u|, where
u[ra,a,rb,b]=U[2a+b,2ra+rb]/2, rho=Tr_X P, L=Tr sqrt(rho).
Then the frozen state and TP-constrained channel SDPs obey

    s(Omega)=t(Omega)=(1-p)L^2+p/4,
    S_infty[A|B]_N=-log2((1-p)L^2+p/4)-1.

An explicit common optimizer is

    Q_*=(1-p)L sqrt(rho)+(p/16)I_4.

This covers complex unitaries, all degeneracies, rank deficiencies, and endpoints.
It concerns the specified fully depolarizing replacer and single-use min-entropy;
it asserts neither a general mixed-unitary identity nor a capacity or finite-
temperature theorem. The sqrt is of the PURE-unitary reduction rho, not of
Tr_X Omega. Replacing it by the latter is generally unjustified.

## 1. Pure projector plus scalar identity: matching exact witnesses

This intermediate calculation is not claimed to be a new entropy theorem.
For any unit vector in C^4 tensor C^4, write its Schmidt decomposition as

    |u>=sum_(i=1)^r a_i |x_i>|y_i>, a_i>0, sum a_i^2=1.

The Schmidt phases are absorbed into x_i; L=sum a_i and
sqrt(rho)=sum a_i |y_i><y_i|. Let Pi=sum |y_i><y_i|,
w=sum |x_i>|y_i| and

    W=|w><w|+(I_X/4) tensor (I_Y-Pi).

Then W>=0, Tr_X W=Pi+(I-Pi)=I_Y, Tr W=4, and
<u|W|u>=L^2. This is an admissible STATE dual witness, also a lower bound
for the constrained channel primal because it bounds every state-feasible Q.
For a=1-p>=0 and b=p/16>=0, its objective on Omega=aP+bI is
aL^2+4b. No channel-dual derivation is needed.

Take Q=aL sqrt(rho)+bI. It is PSD and has trace aL^2+4b.
The slack is a[I_X tensor L sqrt(rho)-P]. For any vector z, set
z_i=<x_i y_i|z>. Weighted Cauchy-Schwarz gives

    |<u|z>|^2=|sum a_i z_i|^2
              <= L sum a_i |z_i|^2
              <= <z|I_X tensor L sqrt(rho)|z>.

The final inequality uses that, for each y_i, the complete X norm is at
least its component along x_i. Thus the slack is PSD, including zero
Schmidt values without taking an inverse. Weak duality now gives

    s(aP+bI)=aL^2+4b.

The rank-complement term in W is essential when r<4: omitting it would
lose (4-r)b from the dual objective and fail to certify noisy rank-deficient
cases. At p=1 Q=bI, W still works, and s=1/4. At p=0 this reduces to
the known pure-state formula from KRS2009.

## 2. Q_* obeys the conditioning-channel marginal

Unitary U implies Tr_B rho=I_RB/2 and Tr_RB rho=I_B/2. These follow respectively
from the full reference marginal I_RA,RB/4 (trace preservation) and the
full output marginal I_A,B/4 (unitality), followed by tracing the other qubit.

A direct proof of the qubit lemma used in source Appendix D Lemma 9 follows.
Any two-qubit LMM density operator has the Pauli representation

    rho=(I tensor I + sum_ij T_ij sigma_i tensor sigma_j)/4,

with real T: Hermiticity makes expectations of these Hermitian observables real.
By real singular-value decomposition choose proper rotations O1,O2 in SO(3)
so O1 T O2^T is diagonal. If an SVD rotation has determinant -1, move its
reflection into a sign of the corresponding diagonal entry; this gives proper
rotations with signed diagonal entries. SU(2) implements all proper rotations
on Pauli matrices. Therefore local qubit unitaries transform rho to

    rho_d=(I+sum_i d_i sigma_i tensor sigma_i)/4.

XX, YY and ZZ commute, and the four Bell vectors form a common eigenbasis.
Consequently sqrt(rho_d)=sum_j sqrt(lambda_j) |Bell_j><Bell_j|. Each Bell
projector has either one-qubit marginal I_2/2, whence

    Tr_B sqrt(rho)=(L/2)I_RB,
    Tr_RB sqrt(rho)=(L/2)I_B.

Local-unitary conjugation preserves these scalar marginals. Repeated or zero
lambda_j do not alter the argument: choose the Bell basis in every eigenspace,
and the positive square root is basis independent. This fact is explicitly
prior work (source Lemma 9); it is restated to make the proof self-contained.
It does not assert that every arbitrary eigenbasis in a degenerate space is Bell.

Thus Tr_B Q_*=[aL^2/2+2b]I_RB=(Tr Q_*/2)I_RB. Q_* is feasible for t,
so s<=t<=Tr Q_*=s. This proves the entire frozen all-U,all-p equality.

## 3. Separate structural proof by finite correlated signs

This addresses the precise pending research test independently of the formula.
Choose a local-unitary Bell eigenbasis y_1,...,y_4 for rho. For positive
lambda_i let x_i=(I tensor <y_i|)u/sqrt(lambda_i), giving orthonormal x_i.
Complete them arbitrarily for zero lambda_i. Then
u=sum_i sqrt(lambda_i) x_i tensor y_i, with zeros included.
For each of the 16 independent sign vectors epsilon in {+1,-1}^4 define

    V_X(epsilon)=sum_i epsilon_i |x_i><x_i|,
    V_Y(epsilon)=sum_i epsilon_i |y_i><y_i|.

Both are unitaries; their tensor product fixes u exactly, since epsilon_i^2=1.
It also fixes the scalar identity, hence fixes Omega for every p. Conjugating
any feasible I tensor Q>=Omega preserves feasibility with Q replaced by
V_Y Q V_Y†. The 16-term average is PSD, has the same trace, and equals

    Qbar=sum_i <y_i|Q|y_i> |y_i><y_i|.

Every y_i is maximally entangled between RB and B, so Tr_B Qbar=Tr(Q)I/2.
Thus every state-feasible objective value is channel-feasible after averaging.
The minimum is attained (finite-dimensional PSD trace-bounded compactness),
so s=t. Zero lambda, p=1 and degeneracies cause no exception. V_X and V_Y
are proof operations on grouped spaces; they need not be physically local gates
on the individual ports or allowed thermodynamic transformations.

## Physical inference and limitations

The additional TP restriction carries zero objective penalty for this family,
and the white-noise dependence is explicitly affine for 2^(-H_min), rather
than for the entropy itself. If L^2=kappa in [1,4], the channel entropy crosses
zero at p=(kappa-1/2)/(kappa-1/4); this is only a min-entropy sign threshold,
not an entanglement-breaking threshold. The bounds follow from sum a_i^2=1
and Cauchy-Schwarz, giving L between 1 and 2. Identity/CNOT/SWAP have
kappa=1,2,4 and recover the baseline formulas exactly.

The decisive additional step beyond the source's noiseless Proposition 10 and
square-root marginal lemma is a common primal/dual pair for scalar white noise,
or equivalently the explicitly constructed correlated-sign dephasing. Existing
qubit normal forms and generic SDP symmetrization are not claimed as discoveries.
Global priority remains subject to the bounded comparison in
evidence/research-prior-comparison.md and fresh independent referee review.
