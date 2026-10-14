# Double reconstruction of the new probability input

The all-degree argument needs a Haar orthonormal two-frame V=(u,v) in C4 and a rank-two projector P. The decisive input is the law of B=V*PV, not a non-Hermitian corner spectrum. The published truncation formula is primary-truncation-excerpt.md. Both reconstructions below derive B's density from the physical Haar model without using computed moment answers. They share this agent, complex-volume conventions and standard polar integration, and do not count as a fresh referee.

## A. Haar-Stiefel constraint and square polar integration

Write V vertically as(Q,H), with Q,H complex2×2 matrices. Haar frame measure is the unique left/right unitary-invariant measure on V*V=I, so its ambient representation is proportional to delta(Q*Q+H*H-I)dQ dH. For a square complex p×p matrix H, polar integration gives dH=const. dS dU, S=H*H>0: the usual determinant power det(S)^(n-p) is zero because n=p. Integrating over H at fixed Q therefore gives a constant on Q*Q<I. This derives the N=4,n=m=2 specialization of source Eq.(38) directly. Passing Q to B=Q*Q again has determinant exponent zero. Thus B is uniform in Cartesian Hermitian volume on0<B<I.

In eigenvalue coordinates this is p(s1,s2)=6(s1-s2)² on the unit square, with independent Haar U2 eigenvectors. The factor is normalized by exact integration. Since z=u*Pu-v*Pv=B11-B22, conditional on the eigenvalue difference δ, z is uniform on[-δ,δ]. This gives p_z(z)=1-3z²+2|z|³. Spectator SU2 rotations imply isotropy of(a-b)/2, and inversion gives p_R(R)=12R²(1-R), R=|a-b|/2.

## B. Gaussian frame and a linear Hermitian change of variables

Let G be a4×2 matrix of independent standard complex Gaussian entries, partitioned into two square blocks G1,G2. V=G(G*G)^(-1/2) has Haar Stiefel law by left unitary invariance. Put W_i=G_i*G_i. Independently each positive Hermitian W_i has Wishart density const. exp(-Tr W_i), with determinant exponent n-p=0. Define S=W1+W2 and B=S^(-1/2)W1 S^(-1/2). It follows exactly that B=V*PV for the first-two-coordinate projector.

At fixed S, W1=S^(1/2) B S^(1/2), and the Hermitian2×2 congruence Jacobian is(det S)^2. To see this directly, diagonalize S=(s1,s2): the coordinates B11,B22,ReB12,ImB12 scale by s1,s2,sqrt(s1s2),sqrt(s1s2), whose product is(s1s2)^2. Unitary conjugation has unit Jacobian. The map(W1,W2)→(S,W1) has unit Jacobian, and the full map(S,B)→(S,W1) is triangular in S and B. Thus the joint density factors into exp(-Tr S)(det S)^2 dS times dB on0<B<I. Integration over S leaves the same uniform Hermitian matrix law, independently reconstructing the essential input.

The two routes agree under the exact convention B=Q*Q=V*PV and z=B11-B22. They do not identify B's eigenvalue gap with the original reduced-Bloch radius without justification: equality of their z laws together with isotropy determines the Bloch-radius law. This is the important convention map.

## Exact checks and source baseline

probability_check.py verifies the four-coordinate congruence Jacobian, both unordered density normalizations, component-to-radial inversion and general-r moment formula. It writes probability-input-a.json, probability-input-b.json and probability-comparison.log from actual symbolic checks. The stored probability inputs are concise defining formulas; the derivations above establish their source/physical meaning. The published2×4 purity density is independently reconstructed from the normalized complex Gaussian state/Wishart eigenvalue formula and transformed to t in all-degree-proof.md; analytic-check.log verifies normalization, mean2/3 and exact agreement with source Eq.(8).

No experiment, Monte Carlo fit, approximate probability law or invented source table enters the result. The radial formula is exact at the specified complex N=4,p=2 dimensions only.
