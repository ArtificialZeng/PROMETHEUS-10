# Proposer proof: nondegenerate two-qubit diagonal-discord monotonicity

Job phys-00004-p05-research-cb17bca630d9, 2026-10-12. This is a proposed exact resolution of the target in problem.md, pending a fresh referee. It does not claim acceptance or priority. Primary source S1 is the preserved arXiv:1708.09076v2, Section II Eq. (8), Section III Conjecture 1. The published isotropic proof uses channel/dephasing commutation; the argument below requires only that the channel image of the dephased input is fixed by the output dephasing. Numerical scans are supplementary attacks, not the proof.

## Statement

Let rho be any density operator on C^2 tensor C^2, and E any unital CPTP map on the first factor. Suppose rho_A and E(rho_A) are nondegenerate. Write Phi=E tensor id, rho'=Phi(rho), and let Delta and Delta' be the fixed linear pinching channels in the input and output marginal eigenbases, respectively. Then

    S(Delta' rho') - S(rho') <= S(Delta rho) - S(rho).

All entropies and quantum relative entropies use base two. There is no marginal-gap lower bound, full-rank hypothesis, semigroup assumption, restriction to real or X states, or perturbative truncation. Only this two-qubit statement is submitted. The reasoning also works for finite spectator dimension, but that enlargement is not needed for this claim.

## 1. Exact compatibility of the comparison state

Write rho_A=a P_+ + b P_- with P_++P_-=I, a+b=1 and a!=b. Let A=E(P_+). Unitality and linearity give E(P_-)=I-A and

    rho'_A=b I+(a-b) A.

Nondegeneracy of rho'_A means that A is nondegenerate, and its spectral projections Q_+,Q_- are exactly those defining Delta' (possibly interchanged). Thus E(P_+) and E(P_-) are diagonal in this basis. The pinched input has the block form

    tau=Delta rho=P_+ tensor B_+ + P_- tensor B_-,
    B_s=<s|rho|s> >=0.

Therefore sigma=Phi(tau)=A tensor B_+ +(I-A) tensor B_- obeys

    Delta' sigma=sigma.                                      (1)

Moreover sigma_A=rho'_A, since Delta preserves rho_A. This is a compatibility statement for this input/output pair; it does NOT assert Delta' rho'=Phi(Delta rho). In particular, it is consistent with S1's explicit noncommuting Hadamard example.

An independent coordinate derivation is useful for checking (1). Let rho_A=(I+g n.sigma)/2, g>0, ||n||=1. A unital qubit map sends Bloch vectors by a real matrix M. Put m=Mn; nondegenerate output implies m!=0. Images of P_s=(I+s n.sigma)/2 are (I+s m.sigma)/2, diagonal along m/||m||. Every tensor coefficient row of tau is proportional to n, so its channel image is proportional to m and is fixed by output pinching. Neither coordinate proof requires M to be diagonal or invertible.

## 2. Pinching relative-entropy identity and supports

Use D(x||y)=Tr[x(log_2 x-log_2 y)] on supp(x) subset supp(y). For any fixed orthogonal pinching L and any density operator y with L(y)=y and supp(x) subset supp(y),

    D(x||y)=D(x||Lx)+D(Lx||y).                              (2)

To verify it for positive definite y and Lx, log y and log(Lx) are block diagonal and L is self-adjoint for the trace pairing. Thus Tr x log y=Tr Lx log y and Tr x log(Lx)=Tr Lx log(Lx); subtracting the three definitions proves (2). Rank deficiency causes no exception: y's kernel projector is block diagonal, so supp(x) subset supp(y) implies supp(Lx) subset supp(y). Also x <= k Lx for k pinching blocks, which ensures supp(x) subset supp(Lx). Restrict logs to the relevant supports, or regularize y by (y+epsilon I)/(1+epsilon d), apply the finite-dimensional trace argument, and take epsilon down to zero. Entropies are continuous in finite dimension and the finite-support relative entropies converge. Hence (2) remains valid with the stated supports.

For our two-block Delta, rho <= 2 tau: writing N=(P_+-P_-) tensor I gives tau=(rho+N rho N)/2, so 2 tau-rho=N rho N>=0. Positivity of Phi gives rho'<=2 sigma. Consequently every relative entropy needed below is finite, including rank-deficient states and channels on the boundary of the CPTP tetrahedron.

## 3. Contractivity and conclusion

Quantum relative entropy obeys data processing under every CPTP map (the same standard contractivity premise used by S1, Theorem 1). Apply it to the pair (rho,tau), not to a nonlinear state-dependent dephasing map:

    D(rho'||sigma) <= D(rho||tau)=S(tau)-S(rho).

By (1), apply (2) with x=rho', y=sigma, L=Delta':

    D(rho'||sigma)
       = S(Delta' rho')-S(rho') + D(Delta' rho'||sigma)
       >= S(Delta' rho')-S(rho').

Combining these inequalities proves the statement. In particular the exact loss splits into two nonnegative terms:

    D_diag(rho)-D_diag(rho')
      = [D(rho||tau)-D(rho'||sigma)] + D(Delta' rho'||sigma).

The first is data-processing loss and the second is the mismatch between channel-image comparison state and pinched output. Equality requires both terms to vanish. No equality classification is claimed.

## 4. Domain and significance

This resolves the source.md universal inequality for all its admissible two-qubit inputs and unital single-use qubit channels. It does not define diagonal discord at degenerate marginals, prove monotonicity for arbitrary distance substitutions, or establish the source's separate isotropic/commuting classification conjecture. Nondegenerate output is essential to identify its unique pinching basis in Step 1. An arbitrarily small positive gap is allowed by the exact argument. No finite scan substitutes for this quantifier.

The physical implication is that entropy-based diagonal discord cannot grow under the specified local unital noise, even if the local measurement basis moves and channel/dephasing commutation fails. This justifies the proposed resource monotonicity in that domain, without requiring a dynamical embedding. It does not assert monotonicity under nonunital noise or any conclusion about optimized discord.

## 5. Adversarial self-review and literature limitations

Checked possible failure points: E(P_+)+E(P_-)=I relies on unitality, not merely TP; output basis follows because a-b!=0 and rho'_A nondegenerate; E(Delta rho) and Phi(rho) have the same marginal; pinching is fixed separately for each state while DPI uses the linear CPTP Phi; relative entropy orientation is rho first and comparison state second; support inclusion follows from the pinching inequality and positivity. Noncommutation is permitted and the correction term has the nonnegative sign shown above.

S1 proves isotropic/semiclassical cases and labels the general qubit case Conjecture 1. Fresh exact-claim and proof-specific searches are preserved in evidence/research-web-recheck.json. No later resolution was identified. This is a bounded priority check, not an exhaustive citation audit. Novelty and correctness must be independently assessed by the fresh referee; no author acceptance is implied. The argument is special to entropy/relative entropy; the broader distance-family statements are not inherited.
