# Proposer argument: the two endpoint formulas at every order

Job phys-00036-p01-research-0c81f16dc975. This is a candidate proof for fresh scientific review, not referee acceptance. The claimed scope is exactly the undeformed Conjecture 2.7 of Schouten--de Leeuw, arXiv:2604.27189v2, printed p.21 / PDF p.22, with Definition 2.4 on printed p.17 / PDF p.18. It makes no long-range perturbative, thermodynamic or experimental assertion. The original source.md is preserved. All arguments are here in this stable file; checkpoint.md and state.json supply none.

## 1. Assumptions, notation and the claim

Let V be any finite-dimensional complex space and let R(u,v) be a matrix formal power series at (0,0), satisfying the source Yang--Baxter equation, R(u,u)=P, and R12(u,v) R21(v,u)=I. An analytic input is included by its formal Taylor series. The two-site flip is P. The homogeneous periodic transfer is

    t_L(u)=tr_a R_aL(u,0)...R_a1(u,0),  U_L=t_L(0).
    Q_k^(L)=partial_u^(k-2)(t_L(u)^(-1)t_L'(u))|0.

All derivatives are raw derivatives, including their factorials. Put C(u)=P R(u,0), so C(0)=I. Define the open ordered product on sites 1,...,n,

    G_n(u)=C_(n-1,n)(u)...C_12(u),    G_1=I,
    F_n=G_n^(-1)G_n',                B_n=G_n'G_n^(-1).

A superscript interval on F or B denotes the same product on that interval. Let r=k-2. We prove that, for every k>=2 and every L>=k, the cyclic sums of

    a_k = partial_u^r(F_k - F_(k-1)^[2,k])|0,
    b_k = partial_u^r(B_k - B_(k-1)^[1,k-1])|0

are both Q_k^(L). We then prove their local equivalence to any k-site density of the prescribed charge by explicitly identifying the kernel of cyclic summation. Thus the conclusion is the source's exact I tensor m - m tensor I equivalence, not equality of spectra or just commutation.

## 2. Exact reduction of the algebraic block formulas

Write S_n(u)=R_1n(u,0)...R_12(u,0) and U_n=P_1n...P_12. Moving the flips to the left gives

    U_n^(-1) S_n(u)=G_n(u).                         (2.1)

For completeness this is an induction: S_n=P_1n C_1n S_(n-1), U_n=P_1n U_(n-1), so U_n^(-1)S_n=(U_(n-1)^(-1)C_1n U_(n-1))(U_(n-1)^(-1)S_(n-1)). The cyclic permutation U_(n-1) sends site n-1 to site 1, hence its conjugation changes the first C to C_(n-1,n), with the ordering of its two tensor slots preserved. The base n=2 is C_12. Since U_n is constant, S_n^(-1)S_n'=F_n. Taking the n=k and shifted n=k-1 differences is therefore exactly the LEFT source block formula, with all lower-support positions retained.

Braiding normalization gives, in fixed ordered tensor slots,

    R_ij(0,u)=R_ji(u,0)^(-1)=P_ij C_ij(u)^(-1).     (2.2)

For T_n(u)=R_1n(0,u)...R_(n-1)n(0,u), moving its flips to the left instead gives

    T_n(0)^(-1)T_n(u)=C_12(u)^(-1)...C_(n-1,n)(u)^(-1)=G_n(u)^(-1).  (2.3)

Indeed a factor C_in^(-1) is conjugated by all the flips to its right; P_(i+1)n sends its second slot from n to i+1 and all subsequent flips leave its slots unchanged. Their residual order is i=1,...,n-1. Consequently

    -T_n(u)^(-1)T_n'(u)=-G_n (G_n^(-1))'=G_n'G_n^(-1)=B_n.        (2.4)

The smaller right block occupies sites 1,...,k-1. Thus b_k is exactly the RIGHT source block formula, including its single overall minus. Varying a singleton leg by u is precisely the source D on that leg. No difference-form assumption is used.

## 3. An exact transfer unfolding with a regular factor

Introduce commuting independent formal bookkeeping variables z_1,...,z_L and

    X_L(z)=U_L^(-1) tr_a R_aL(z_L,0)...R_a1(z_1,0).

This auxiliary multivariable series is only a generating device; it is not asserted to be a new commuting family of inhomogeneous physical transfers. On z_1=...=z_L=u it equals U_L^(-1)t_L(u). Associate variable z_j to the directed nearest-neighbour edge (j-1,j), indices modulo L.

If z_1=0, R_a1=P_a1. The identity tr_a(A_a P_a1)=A_1, when A acts trivially on physical site 1, replaces the auxiliary tensor slot by site 1 and gives

    X_L(0,z_2,...,z_L)=C_(L-1,L)(z_L)...C_12(z_2).  (3.1)

Equation (2.1) is valid with a separate variable in each factor and supplies the final equality. The same formula holds with a cut at any j for which z_j=0: cyclically rotate the monodromy to put P_aj last and use the same trace identity. Partial-trace cyclicity is legitimate for this rotation because the entries of a factor acting on site j commute with the physical entries of the other factors, which act on different sites. The normalized zero product is always the same U_L.

More generally restrict the active variables to any proper subset S of the L edges. Cutting at an edge outside S, equation (3.1) expresses X_L restricted to S as the product of the C factors for S, in descending path order. Connected components of S are proper intervals. Different components have disjoint physical site supports, so their products commute. Hence

    X_L|S = product_(components I of S) G_I(z).     (3.2)

The choice of an inactive cut does not affect this product: changing the cut cyclically reorders only the mutually commuting disconnected components. This exact restriction identity, rather than an approximation to an infinite product, is the essential transfer input.

## 4. Rooted connected coefficients and the finite-order bound

Write Y_j=X_L^(-1) partial_(z_j) X_L and Z_j=(partial_(z_j) X_L) X_L^(-1). For a coefficient with monomial z^alpha in Y_j or Z_j, define its ROOTED edge support to be

    S(alpha,j)={i:alpha_i>0} union {j}.

The root must be included even when alpha_j=0: differentiation can remove its sole power. A coefficient of total degree r has at most r+1 edges in this support. If r<=L-2 this is always a proper subset, so (3.2) applies to its computation. Restricting variables outside S to zero commutes with differentiating in z_j, and determines the coefficient exactly.

If S is disconnected, let I be its component containing j. Differentiating (3.2) and multiplying by the inverse, using the disjoint-support commutation of the components, gives

    (X_L^(-1) partial_j X_L)|S=G_I^(-1) partial_j G_I,
    ((partial_j X_L) X_L^(-1))|S=(partial_j G_I)G_I^(-1).

These expressions contain none of the variables in the other components. Since each non-root edge of S has a strictly positive exponent, the proposed coefficient must therefore be zero whenever S is disconnected. Every surviving rooted coefficient of degree r is supported on a connected proper interval of at most r+1 edges. This establishes locality with no commuting-transfer or Yang--Baxter assumption yet. It also supplies the finite-size control: at order r=k-2 and L>=k, no rooted support can wind around all L edges.

Now put all variables on a fixed open interval of k-1 edges equal to u and sum the rooted derivatives on that interval. Its left form is F_k(u), and its right form is B_k(u). At degree r=k-2, subtracting the left form for the interval with its first edge removed cancels exactly the rooted coefficients whose support omits that first edge. To see this without confusing roots with monomial exponents, consider each root j separately: for j different from the removed edge and exponent zero at that edge, the restricted coefficient is the same smaller-product coefficient; for root at that edge it has no smaller-product counterpart. The surviving connected intervals have their leftmost edge at the first edge. Their maximal length is k-1, so none extends beyond the product used.

There is exactly one leftmost edge for every connected proper interval on the directed cycle. Translating this anchored expression to every edge counts every surviving rooted coefficient once. The identical argument for the right form removes the last edge and anchors at the rightmost edge. Therefore, for every L>=k, with tau denoting cyclic translation,

    sum_(n=0)^(L-1) tau^n(a_k) = partial_u^r(X_L(u)^(-1)X_L'(u))|0,  (4.1)
    sum_(n=0)^(L-1) tau^n(b_k) = partial_u^r(X_L'(u)X_L(u)^(-1))|0.  (4.2)

The factor r! from coefficient extraction is the same on both sides. In the smallest case k=2, rooted support consists only of its root edge and G_1'=0; the argument includes this case and L=2. For every k, it includes the minimal periodic length L=k. Scalar and lower-range coefficients remain in the connected/rooted expansion and are not projected away.

## 5. Where integrability is used

For the physical uniform diagonal X_L(u)=U_L^(-1)t_L(u), the left form is exactly t_L(u)^(-1)t_L'(u). The Yang--Baxter equation implies [t_L(u),t_L(v)]=0, as used explicitly by the source around Eq.(2.24). In particular [t_L(u),t_L'(u)]=0 and [U_L,t_L(u)]=0. Thus X_L and X_L' commute, and the right form X_L'X_L^(-1) is the same as the left form. Equations (4.1)--(4.2) are therefore both the specified Q_k^(L). This step, rather than the regular-factor unfolding alone, is needed to identify the right endpoint with the prescribed left logarithmic derivative. Braiding normalization was needed in (2.2); regularity in (3.1).

## 6. From all-length cyclic sums to the exact local gradient

Here is the finite-dimensional kernel argument, including its constructive witness. Choose a basis of End(V) consisting of I and trace-zero matrices E_alpha (dimension one is the scalar-only case). Expand a k-site matrix D in the resulting tensor-word basis. Separate the all-I scalar word. Every other word has a unique core w of length m<=k obtained by removing leading and trailing I factors; the first and last letters of w are non-I. Its embeddings in k slots have coefficients c_0,...,c_(k-m), where c_a multiplies I^tensor a tensor w tensor I^tensor(k-m-a).

Take any periodic L>2k. The cyclic translates of a core w have a unique exterior interval of identities longer than any interior identity interval of w. Consequently different cores cannot mix in the tensor-word expansion of the cyclic sum, and the L placements of each core give distinct basis words. The cyclic sum of D vanishes if and only if its scalar coefficient is zero and

    sum_(a=0)^(k-m) c_a=0                           (6.1)

for every core. When m=k, this forces its only coefficient to zero. For m<k set, in a (k-1)-site matrix M, the coefficients of the corresponding core embeddings to

    d_a=-sum_(b=0)^a c_b,   0<=a<=k-m-1.           (6.2)

Then I tensor M - M tensor I has coefficients -d_0=c_0, d_(a-1)-d_a=c_a at interior positions, and d_(k-m-1)=c_(k-m) at the last position, the last equality following from (6.1). Summing over cores constructs M with

    D=I tensor M - M tensor I.                     (6.3)

For dimension one the zero cyclic sum already forces D=0. Thus this kernel statement holds for every finite local dimension. Conversely (6.3) telescopes on every periodic chain.

Let q_k be any k-site representative of the prescribed source charge, meaning its cyclic sum is Q_k^(L) for all L>=k. Applying (6.3) to a_k-q_k and b_k-q_k, using (4.1)--(5), proves both of the source's local equivalences. In particular a_k itself provides a consistent k-site representative, without having to calculate or choose a boost-normalized one.

## 7. Scope and evidence limits

This argument claims the complete all-R/all-k undeformed identity. The source hypotheses suffice; no difference form, Hermiticity, spectral eigenbasis, local dimension two, finite-order ansatz or thermodynamic limit is imposed. Physical Hermitian observables still require their model-specific real energy scale and odd-charge i convention; the proof concerns the raw dimensionless algebraic charges only.

The k=4,5 nonlinear-XXX evidence in research-reparam-derivation.md, research-reparam-comparison.json and research-reparam-test.log checks signs, factorials, lower charges and exact gradient witnesses. Those finite computations do not establish the universal quantifiers; sections 2--6 are the all-order argument. Additional generic-matrix tests attack the regular-factor and connected-coefficient steps without falsely treating a non-Yang--Baxter matrix as an admissible counterexample. A fresh referee must independently reconstruct the primary formulas, inspect the rooted-support cancellation and cyclic-sum kernel argument, and assess novelty. Proposer verification is not that acceptance.
