# Stable independent input B and convention map

Reproduction job phys-00027-p01-reproduce-e7d47effda86, 13 October 2026.
This is a source reconstruction, not an embedding classification or novel result.
Primary source: literature/2405.11216v3.pdf, PDF p2 Eqs. (4),(6), p3 RHS
Eq. (12) and Eqs. (13)-(15). PDF pp3 and 6 were rendered and inspected;
the inspected renders are primary-p3.png and primary-p6.png in this directory.
Equation numbers here follow the PDF, not the HTML rendering.

## Separate derivation

The antisymmetric component is defined by Eq. (6), and the symmetric
Werner-Holevo component by the RIGHT side of Eq. (12). The latter's
displayed Kraus prefactor and counting convention are not taken as a
normalization input. The source explicitly specifies the matrices
E_mn+E_nm and -i(E_mn-E_nm) in Eq. (4) and Eq. (11); no missing matrix is
inferred from an abstract or text summary. The diagonal orthonormal
matrices below are Eq. (5)'s diagonal matrices divided by sqrt(2).

Let F be the tensor swap on C^d tensor C^d, and Omega=sum_i |i,i>.
With J(T)=sum_ij E_ij tensor T(E_ij), J(id)=|Omega><Omega|,
J(trace(.)I)=I_(d^2), J(transpose)=F. Thus the two noise components give
J(W_minus)=(I-F)/(d-1)=2 P_minus/(d-1) and
J(W_plus)=(I+F)/(d+1)=2 P_plus/(d+1).
These identities derive the normalization from the explicit definitions.

Put t=1-x-y. The independently assembled spectral representation is

    J_B=t |Omega><Omega| + 2x/(d-1) P_minus + 2y/(d+1) P_plus.

All vectors below have norm one, and the associated matrices have unit
Frobenius norm. Under |Q>>=sum_i,a Q_ai |i,a>, choose Q0=I/sqrt(d),
S_ij=(E_ij+E_ji)/sqrt(2), A_ij=(E_ij-E_ji)/sqrt(2), i<j, and
D_m=(sum_(i=0)^(m-1) E_ii-m E_mm)/sqrt(m(m+1)), m=1,...,d-1.
The A_ij differ from the primary Hermitian -i(E_ij-E_ji) matrices by
a phase i and a normalization sqrt(2); phases cancel in K X K^dagger.
The S_ij and D_m span symmetric traceless matrices. Identity is the
remaining symmetric direction. The complete d^2-dimensional basis is
orthonormal; its cardinalities are 1, d(d+1)/2-1, and d(d-1)/2.

The unnormalized Choi eigenvalues are

    lambda0=d*t+2y/(d+1),
    lambda_s=2y/(d+1), multiplicity d(d+1)/2-1,
    lambda_a=2x/(d-1), multiplicity d(d-1)/2.

Input B constructs each Kraus matrix as sqrt(lambda)*Q. In particular,
K0=sqrt(t+2y/[d(d+1)]) I. It does not assign sqrt(lambda/d)*Q to a
trace-preserving Kraus map: those are the normalized Choi-state weights,
not the channel Kraus weights. The normalized Choi state is J_B/d, and
its eigenvalues are lambda/d. This distinguishes the two normalizations.

## CP/TP and full support as INPUT properties

For x>0,y>0,t>=0 all three eigenvalues are strictly positive, even at
t=0. Hence J_B is positive definite with rank d^2 throughout the frozen
domain, and the input channel is completely positive, including on
entangled inputs. This says nothing about a homogeneous generator.

Partial trace over the OUTPUT tensor factor gives I: Tr_out(|Omega><Omega|)=I,
Tr_out(P_plus)=(d+1)I/2, Tr_out(P_minus)=(d-1)I/2. Equivalently
sum K^dagger K=I. The channel is also unital. The weighted Kraus construction
is Hermiticity preserving. The exact matrix-unit comparison checks all
complex-linear inputs, rather than only real density matrices.

## Explicit A-to-B map

Input A is transcribed separately from PDF p3 Eq. (14):
t X+c Tr(X)I+b X^T, c=x/(d-1)+y/(d+1), b=y/(d+1)-x/(d-1).
Its Choi expression is J_A=t |Omega><Omega|+c I+b F. Since
P_plus=(I+F)/2 and P_minus=(I-F)/2, J_A=J_B for every d>=3 and
every legal x,y. This comparison is made after, not as an input to,
the separate implementations.

Both use zero-based local indices: primary |m> is local |m-1>.
The Choi tensor order is INPUT then OUTPUT, row (i,a)=i*d+a,
column (j,b)=j*d+b. The column-stacked superoperator uses

    S_(a+d*b,i+d*j)=J_(i*d+a,j*d+b).

There is no adjoint in this reshuffle. The map transpose is complex
linear, while Kraus adjoints include conjugation. Partial transpose of
J would define another convention and is not substituted here.

## Actual independence and limits

One agent wrote both implementations. B imports no A code, reads no A
JSON or cached matrix, uses its own basis constructor, derives its map
from Choi spectral vectors, and separately transcribes Eq. (28)'s input.
Both necessarily share the primary paper, model parameters, computational
basis, and this agent's mathematical interpretation. This is independent
representation/implementation, weaker than fresh-agent reconstruction.
The comparison script may load both only after they have been generated.
No claim of referee acceptance or independent human review is made.

## Physical scope and units

Finite M_d(C), all d>=3, all complex operators, x>0,y>0,x+y<=1;
no spatial boundary, thermodynamic limit, data fitting, approximation,
or perturbative expansion. x,y and the channel spectrum are dimensionless.
The target generator has time^-1 units; with hbar=1, H has time^-1
and jumps have time^-1/2. Observation time is T=1 by unit choice.
This reproduction does not impose covariance or a logarithm branch on
any prospective generator. Full Choi support does not imply invertibility
of the channel as a superoperator. No generator has been inferred.
