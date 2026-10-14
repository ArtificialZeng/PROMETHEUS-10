# Canonical tangent structure used to choose a discriminating test

This is a stable research derivation for pass 1, not a publication candidate. It uses the exact physical model in problem.md and the reproduced canonical coefficient construction in evidence/reproduction/derivation-a.md. No derivation is taken from a mutable checkpoint.

Write Q=sqrt(P) tensor sqrt(P), K0[(i,r),(j,s)]=Qij delta(r,i)delta(s,j), and U(t)=exp(i t H) on R=S=C^4 for a fixed Hermitian 16-by-16 H. For strictly positive P with det(sqrt(P)) nonzero, Q has rank four and the left/right Schmidt supports of K0 are exactly the logical flag subspaces r=i and s=j. The full physical marginal stays exactly fixed for every real t by auxiliary unitarity.

The first derivative of the coefficient matrix is

dK[(i,r),(j,s)] = i Qij H[(r,s),(i,j)].

Its logical-to-logical compression has only the diagonal auxiliary entries H[(i,j),(i,j)], which are real. Thus that compression is purely imaginary times real Q. Since the entropy gradient on the occupied support is real in this basis, the first entropy derivative at t=0 vanishes. Cross-support terms do not change occupied eigenvalues at first order either.

The first-order block between BOTH null Schmidt spaces is

A[(i,r),(j,s)] = i Qij H[(r,s),(i,j)], with r != i and s != j.

Standard finite-dimensional singular-value perturbation about a rank-four matrix gives newly emerging squared singular values t^2 sigma_k(A)^2 + o(t^2). Consequently when A is nonzero their entropy contribution is -t^2 log2(t^2) ||A||F^2 + O(t^2). The combined entropy contribution of the occupied eigenvalues has no linear term and changes by O(t^2); individual degenerate eigenvalues may split linearly. A generic fixed direction therefore has a positive small-t logarithmic contribution. This local statement cannot exclude a finite-distance witness or the exceptional A=0 directions. Boundary tables and det(sqrt(P))=0 are excluded from this rank-four derivation.

For positive P, A=0 exactly when every off-diagonal H entry connects labels with the same i or the same j (or is zero). The allowed Hermitian space has real dimension 16 + 2*(4*6 + 4*6)=112: diagonal entries and the row/column edges of a four-by-four label array. It contains local auxiliary-unitary gauge directions. These exceptional directions have no first-order new Schmidt amplitudes and need a separate entropy-curvature test.

The numerical test in flat_tangent_curvature.py evaluates the finite-difference Hessian on these 112 directions at two step sizes, saves its matrices and probes its minimum-eigenvalue direction. A materially negative eigenvalue, followed by a legal negative entropy-gap probe, would motivate certification. Near-zero gauge eigenvalues are not witnesses; a positive finite numerical Hessian is not a universal or rigorous lower bound.
