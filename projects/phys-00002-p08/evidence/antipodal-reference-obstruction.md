# Restricted obstruction for antipodal reference preparations

Proposer: job phys-00002-p08-research-babca3f8ba11, 2026-10-12 UTC.
This is a proposed exact partial result for fresh scientific review. It does not
resolve the unrestricted resource question in source.md and problem.md. No
independent referee has accepted it. The proof uses stable definitions and primary
inputs; neither checkpoint.md nor state.json is an argument or dependency.

## Statement and physical scope

Alice sends a complex qubit, with four preparation labels i=1,...,4. Bob has K
binary auxiliary settings and a four-labeled-outcome target. Preparations and all
effects are untrusted positive 2-by-2 operators; preparations have trace one and
each measurement sums to the identity. No entanglement assistance, sequential
instrument, trusted axis or additional message is present. Input-independent
shared classical randomness is allowed. The model is static, dimensionless and
exactly noiseless; there are no dynamical boundary conditions, units of energy or
perturbative/truncation errors.

Let the reference target be any extremal four-outcome qubit POVM

    T_i = alpha_i (I - r_i.sigma),
    alpha_i>0, |r_i|=1, sum_i alpha_i=1, sum_i alpha_i r_i=0,

whose four effects are linearly independent as Hermitian matrices. Assume the
FOUR REFERENCE preparations are precisely their matched kernel states

    rho_i = (I + r_i.sigma)/2, so Tr(rho_i T_i)=0.

Write the reference binary observables as

    B_(0|y)-B_(1|y) = beta_y I + d_y.sigma,
    |beta_y|+|d_y|<=1.

**Proposition.** Suppose span{d_y} has dimension at most two. For every real
linear witness on ALL auxiliary and target probabilities that attains its global
quantum maximum at this reference strategy, there is another admissible maximizing
strategy with the same auxiliary measurements and a target with at most three
nonzero effects. Consequently that witness cannot self-test the reference target,
even if it only aims to certify the target and makes no separate claim about the
preparations. In particular this applies to K<=2 projective auxiliaries, and also
to K<=2 arbitrary binary POVMs.

The reference-preparation hypothesis is essential to the present proof. It is a
natural restriction: these are exactly the state-exclusion references used by
the reproduced 2020/2024 protocols. The proposition does NOT rule out a protocol
using other reference preparations, nor does it settle minimal N, all K=2
protocols, nonlinear certification, or noisy robustness.

## 1. Completeness and extremality give a state basis

The four rho_i form a basis of real Hermitian 2-by-2 matrices. Indeed the effect
coefficient vectors alpha_i(1,-r_i) are independent, so (1,r_i) are independent.
Also, any THREE of the r_i are linearly independent. Otherwise those three lie
in a subspace of dimension at most two and, by positive-weight completeness,
the fourth is their linear combination. This contradicts the three-dimensional
span required by extremality. In particular no pair is antipodal, and no plane
through the origin contains more than two r_i.

## 2. All target coefficients have a supporting normal form

Use binary probability normalization to express an arbitrary linear witness as

    L = C0 + sum_(i,y) w_iy Tr(rho_i O_y)
             + sum_(i,j) c_ij Tr(rho_i E_j),

where O_y=B_(0|y)-B_(1|y), E_j is the target, and every w_iy,c_ij is real.
There is no restriction to diagonal target penalties in this definition.

Hold the reference states and auxiliary measurements fixed. Since the reference
strategy is a global maximizer, its target optimizes the finite measurement SDP

    maximize sum_j Tr(H_j E_j),  H_j=sum_i c_ij rho_i,
    subject to E_j>=0 and sum_j E_j=I.

The dual minimizes Tr(Lambda) over Hermitian Lambda subject to Lambda-H_j>=0
for each j. This is the direct Lagrange dual of the displayed primal: the
Lagrangian is Tr(Lambda)+sum_j Tr[(H_j-Lambda)E_j]. The primal is strictly
feasible at E_j=I/4, and the dual is strictly feasible at Lambda=t I for
sufficiently large finite t. The finite-dimensional SDP therefore has attained
strong duality (Slater's condition). In particular an optimal Lambda exists.

Complementary slackness gives

    Lambda-H_j>=0,  Tr[(Lambda-H_j)T_j]=0.

For positive matrices, zero trace of the product implies that their supports
are orthogonal. T_j has rank one and its kernel is the support of rho_j.
Thus the entire dual slack must be

    Lambda-H_j = k_j rho_j,  k_j>=0.

Expand the common Hermitian Lambda uniquely in the state basis,
Lambda=sum_i l_i rho_i. Comparing coefficients gives the NECESSARY form

    c_ij = l_i - k_j delta_ij.

This is an equality of the witness coefficients, established using the reference
states. It remains valid when the witness is evaluated on ANY other states.
Target completeness then reduces its entire target contribution to

    sum_(i,j) c_ij p(j|i,target) = sum_i l_i - sum_i k_i p(i|i,target).

Hence even arbitrary coefficients on all sixteen target probabilities reduce
to common row shifts plus nonnegative exclusion penalties at this reference.
This is stronger than assuming a two-stage witness from the start.

## 3. At most two preparations contribute nontrivially to the auxiliaries

Hold all measurements fixed and optimize the i-th preparation over the Bloch
ball. Let u_i=sum_y w_iy d_y. By the normal form and sum_j alpha_j r_j=0,
its state-dependent Bloch vector is

    g_i = u_i - k_i b_i = u_i + k_i alpha_i r_i,

where b_i=-alpha_i r_i is the target's Pauli coefficient. A unit Bloch vector
r_i maximizes g_i.s over |s|<=1 exactly when g_i=tau_i r_i with tau_i>=0,
including tau_i=0. Therefore

    u_i = (tau_i-k_i alpha_i) r_i.

Every nonzero u_i is parallel to r_i and lies in span{d_y}. By Section 1,
the active set A={i:u_i!=0} contains at most two labels. For all other states
the auxiliary contribution is independent of the state, provided the auxiliary
measurements are kept fixed. The scalar beta_y terms are also preserved by
keeping those measurements fixed. This conclusion does not assume that the
individual w_iy vanish, or that the binary settings are independent/projective.

## 4. Construct an inequivalent target at exactly the same score

If A={a,b}, put

    s=|r_a+r_b|,  q=(r_a+r_b)/s,  A0=1/(2+s).

Section 1 gives 0<s<2. Choose one inactive label c and let d be the other.
Define

    E'_a=A0(I-r_a.sigma),  E'_b=A0(I-r_b.sigma),
    E'_c=A0*s(I+q.sigma), E'_d=0.

These effects are positive. Their scalar weights sum to A0(2+s)=1 and
their vector coefficients sum to -A0(r_a+r_b)+A0*s*q=0, so sum E'_i=I.
Keep the active preparations r'_a=r_a,r'_b=r_b, choose r'_c=-q, and choose
any state for label d. Then p'(i|i,target)=0 for all four i.

If A={a}, choose an inactive c and use the projective target

    E'_a=(I-r_a.sigma)/2, E'_c=(I+r_a.sigma)/2,
    E'_j=0 for the other labels,

with r'_a=r_a and r'_c=-r_a. Again all diagonal target probabilities vanish.
If A is empty, the same construction with arbitrary a,c and any unit r_a
works, since no state has a nonzero auxiliary u_i.

In every case the active auxiliary contributions are unchanged, the inactive
ones remain zero, the binary scalar terms are unchanged, the row-shift term is
constant, and every target penalty is zero. Thus L'=L at the global maximum.
The replacement has at least one zero effect, whereas the reference has four
nonzero independent effects. It is inequivalent under every common unitary or
antiunitary transformation, even if outcome permutations were additionally
allowed. Fixed labels have been preserved in the construction.

If one were to impose nonzero effects artificially, split E'_c in the two-active
case into two positive proportional effects on the inactive labels and use the
same kernel state for both; this gives four nonzero but dependent effects at the
same score. Such an extra premise is not needed in the project's admissible set.

The alternative is already a single admissible branch. Allowing shared
randomness cannot remove it. A linear functional has the same supremum on a
strategy set and on its convex hull, and this branch attains the reference's
global maximum. This proves the proposition.

## Verification and relation to the original question

The argument is analytic for EVERY extremal four-outcome qubit target, EVERY
coefficient array, and EVERY auxiliary collection with Bloch span at most two,
subject to the matched antipodal reference states. It relies on ordinary
finite-dimensional SDP duality, positivity and completeness, not a finite scan.
The exactly checked matrix normal-form spaces and all active-index alternatives
for a tetrahedron and an unequal-weight extremal target are in
evidence/n4k2_exact_checks.py, evidence/n4k2-exact-checks.log and
evidence/n4k2-exact-check-summary.json. They are same-worker proposer checks,
not a second scientist or a fresh referee. Exact algebra introduces no numerical
tolerance or approximation remainder.

The previous local-nullspace route was also completed at the tetrahedron with
two coordinate auxiliaries. Its singular tangent does not continue at fixed
statistics: see evidence/n4k2-linearization-derivation.md and the exact logs.
No step of the proposition depends on that differential calculation.

Closest source comparison and limits on novelty: evidence/research-prior-comparison.md.
Primary baseline references are the unchanged source-ledger.json and
supervisor-inputs/povm-primary/2406.08661v1.pdf (Sections III, IV, VI), and
supervisor-inputs/povm-primary/Tavakoli-2020-published.pdf (noiseless method and
Eqs.13–15). A reduced-resource protocol outside the matched state-exclusion
reference class remains possible in this analysis. The original status is
unresolved; this proposed lower bound is restricted, and is not a resolution-paper.
