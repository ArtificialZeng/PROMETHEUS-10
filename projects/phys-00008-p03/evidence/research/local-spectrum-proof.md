# Exact local spectrum and a conditioning obstruction for the n=4 iterator

Proposer job: phys-00008-p03-research-4c9b863a737b. This is a restricted analytic result submitted for fresh review, not a solution of the original almost-sure question.

## Definitions and statement

View arrays x=(x_ij) in C^(4 x 4 x 4) as a real Euclidean space E of dimension 128, with inner product Re sum_ij <x_ij,y_ij>. Let R be the arrays whose four row squares are unitary, and C the arrays whose four column squares are unitary. The source recurrence F is one principal-root row normalization followed by one principal-root column normalization. Near a QLS both steps are well-defined and equal the nearest-unitary polar projections P_R and P_C, so F=P_C P_R. This equivalence is already derived in evidence/reproduction/reconstruction.md. The original normalization, indices and post-column maximum row Frobenius residual e are those of problem.md.

For any real theta, put c=cos(theta), s=sin(theta), u=c e_0+s e_1, v=-s e_0+c e_1, and define

Q(theta) =

    e_0  e_1  e_2  e_3
    e_1  e_0  e_3  e_2
    e_2  e_3  u    v
    e_3  e_2  v    u.

Every row and column is an orthonormal basis, as is checked directly using c^2+s^2=1. Thus Q is a legal exact rank-one measurement array and F(Q)=Q. The array is a simple block deformation; no new QLS construction or equivalence classification is claimed.

Claim A. On the real 64-dimensional space T_C(Q), the derivative D F(Q) has characteristic polynomial

    z^16 (z-1)^32 [z-(1+c)/2]^8 [z-(1-c)/2]^8.

Multiplicities combine when roots coincide. For sin(theta) != 0 the largest eigenvalue strictly below one is (1+|cos(theta)|)/2. At theta=0 mod pi, the spectrum consists of 0 (24) and 1 (40). At cos(theta)=0 it consists of 0 (16), 1/2 (16) and 1 (32). These are linearized tangent dimensions, not dimensions of a proved nonlinear solution manifold.

Claim B. For every q in (0,1), delta in (0,1) and eta>0, there exist theta in (0,pi/2) and an array x in C with 0<||x-Q(theta)||_F<eta, such that e(F(x))>q e(x)>0. All eight Gram matrices inverted during this one full cycle have spectra in [1-delta,1+delta]. In particular their condition numbers are at most (1+delta)/(1-delta). No uniform one-cycle residual factor strictly below one exists over these arbitrarily well-conditioned inputs. No upper bound of one on the nonlinear residual ratio is asserted. This statement concerns a proposed performance bound, not a counterexample to source convergence.

## Derivative from the defining equations

For a unitary square A and a perturbation H, expand

    [(A+hH)(A+hH)^dagger]^(-1/2)(A+hH)
      = A + h (H-A H^dagger A)/2 + O(h^2).

The expansion follows by differentiating the Hermitian principal inverse square root at I: (I+hB)^(-1/2)=I-hB/2+O(h^2). Therefore the row and column derivatives are orthogonal tangent projectors L_R and L_C, and D F(Q)=L_C L_R. Its restriction to T_C equals L_C L_R L_C, which is self-adjoint, positive semidefinite and bounded above by I. This is standard projection geometry, also explicitly stated in Lewis–Malick (2008), Lemma 2.1 and equation (11); the new calculation below is the spectrum for this array.

At this real array the real and imaginary perturbations separate. A column tangent vector is written, column by column, as A_j K_j where A_j is Q's j-th column square. Real K_j is skew symmetric (six generators per column); an imaginary tangent vector is i A_j S_j for real symmetric S_j (ten generators per column). Thus the sectors have dimensions 24 and 40. Use one coordinate for each upper-triangular generator (a,b), a<b for K, a<=b for S, with generator entries (a,b)=1 and (b,a)=-1 or +1. Off-diagonal generators have squared norm 2 and diagonal symmetric generators squared norm 1.

Applying the formula (H +/- A H^T A)/2 to rows and columns in this basis gives the following complete block decomposition. The rational-function reconstruction, all generator labels, every block entry and every determinant are also preserved in exact-family-spectrum.json and generated without SVD by exact_family.py.

| Sector | One-dimensional blocks [1] | Two-dimensional blocks | Eight-dimensional blocks |
|---|---:|---:|---:|
| Real skew generators | 0 | 4 | 2 |
| Imaginary symmetric generators | 16 | 4 | 2 |

The four two-dimensional pairs, in either sector, are [(0,0,1),(1,0,1)], [(0,2,3),(1,2,3)], [(2,0,1),(3,0,1)] and [(2,2,3),(3,2,3)]. Each block is (1/2)[[1,-1],[-1,1]] in the real sector and (1/2)[[1,1],[1,1]] in the imaginary sector, with eigenvalues 0 and 1. Each eight-dimensional block has the form

    D_8 = [[I_4/2, B], [B^T, I_4/2]],

up to replacing B by -B or P B, where P reverses four coordinates. These replacements preserve the singular values. For the first real block the ordered generator labels (column j, generator a,b) are

    (0,0,2), (0,1,2), (1,0,3), (1,1,3),
    (2,0,2), (2,0,3), (3,1,2), (3,1,3),

and

    B = [[-c/2,  s/4,  s/4,     0],
         [-s/4,     0, -c/2, -s/4],
         [-s/4, -c/2,     0, -s/4],
         [    0,  s/4,  s/4, -c/2]].

For the second real block the labels are

    (0,0,3), (0,1,3), (1,0,2), (1,1,2),
    (2,1,2), (2,1,3), (3,0,2), (3,0,3),

and its B is P B. The two imaginary blocks have the same respective labels and -B, -P B. The sixteen one-dimensional imaginary blocks are the diagonal symmetric generators, each eigenvalue one. The eight remaining generators in either sector are paired into the four stated two-dimensional blocks. This accounts for every coordinate, with no truncation.

To diagonalize D_8, decompose R^4 into the two orthogonal spans of

    e_0-e_3, e_1-e_2;   and   e_0+e_3, e_1+e_2.

On the first span B is diag(-c/2,c/2). On the second it is (1/2)[[-c,s],[-s,-c]], whose singular values are both 1/2. Hence B has singular values 1/2 (twice) and |c|/2 (twice). The eigenvalues of D_8 are 0 (twice), 1 (twice), (1+c)/2 (twice) and (1-c)/2 (twice), with coinciding values combined. Adding the block counts proves Claim A. No fitted polynomial or degree assumption enters this argument.

The independent symbolic check sets t=tan(theta/2), c=(1-t^2)/(1+t^2), s=2t/(1+t^2), constructs all tangent generators directly, and factors the exact block determinants over Q(t). It obtains precisely the stated characteristic polynomial and zero exact difference. This parameter covers all real theta except theta=pi mod 2pi, which the direct c,s derivation includes. Floating-point Jacobians and central differences are only supplementary checks.

## Residual obstruction and admissible curves

Fix theta in (0,pi/2), lambda=(1+cos(theta))/2<1, and take a nonzero eigenvector E in T_C with D F(Q) E=lambda E. Let

    B_i(E)=E_i A_i^dagger + A_i E_i^dagger,
    alpha=max_i ||B_i(E)||_F,

where A_i and E_i are the row squares. We must have alpha>0: otherwise E is also in T_R, so L_R E=E and L_C E=E, forcing D F(Q)E=E and contradicting lambda<1.

There is an analytic column-unitary curve x(h) through Q with tangent E. Explicitly write the j-th column tangent as A_j K_j, K_j skew Hermitian, and replace that column square by A_j exp(h K_j). Then

    x(h)=Q+hE+O(h^2),
    F(x(h))=Q+h lambda E+O(h^2),
    e(x(h))=|h| alpha+O(h^2),
    e(F(x(h)))=|h| lambda alpha+O(h^2).

The maximum of the four norms does not obstruct these expansions: each has the displayed leading norm, and there are only finitely many. Consequently e(F(x(h)))/e(x(h)) tends to lambda as h tends to zero through nonzero values.

Given q<1, choose theta>0 small enough that lambda>q. By continuity, for all sufficiently small nonzero h, the ratio exceeds q, e(x(h))>0, and ||x(h)-Q||<eta. At Q all row Gram matrices and all post-row column Gram matrices equal I. Their spectra vary continuously with h, so reducing |h| further places all of them in [1-delta,1+delta], ensuring legality. This proves Claim B, including its quantifiers. It establishes no infinite-time bad basin.

## Physical and scientific limits

The entries and residuals are dimensionless finite-dimensional measurement-array quantities. Q(theta)'s rows define exact CPTP measurement channels; nearby column-normalized x generally has incomplete rows and is not called an exact measurement array. The iteration is a classical numerical constructor. Claim B says that a Gram-condition monitor alone cannot promise a uniform strict one-cycle progress factor, even near valid exact arrays. Near theta=0 the linearized slow factor is 1-theta^2/4+O(theta^4); this is not an established all-time iteration complexity law.

The 48 old capped misses and five 5000-cycle survivors were all later finite 1e-6 hits in the saved experiments. Their local numerical spectra explain slow rates in the checked regimes, but they do not prove the conjecture, a Gaussian probability statement, nonlinear local convergence, integrability of the neutral directions, or a universal rate. General manifold convergence theorems cannot be invoked here without their extra hypotheses: T_R and T_C each have dimension 64 in ambient dimension 128 and have a nonzero intersection, so ambient transversality fails. Novelty and independent scientific acceptance remain for a fresh referee.
