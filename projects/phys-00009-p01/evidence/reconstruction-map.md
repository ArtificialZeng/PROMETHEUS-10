# Independent SIP input reconstruction and conventions

This is a source reproduction derivation for job phys-00009-p01-reproduce-407d9b181782. It does not establish the open many-particle gap identity. No derivation relies on checkpoint.md or state.json.

The primary journal source is Kim-Sau, DOI 10.1007/s00220-026-05728-9. Eq. (2.1) specifies every ordered jump, Eq. (2.2) the stationary law, and Eq. (3.7) the reversible Dirichlet form. The actual primary returns are preserved in evidence/reproduce-model-dirichlet-tool-return.json and evidence/reproduce-versions-scope-form-tool-return.json. The current author preprint is arXiv:2412.01489v2. PDF/journal labels are used throughout; the experimental arXiv HTML labels differ.

## A: occupation jumps

In a fixed total-particle sector k, enumerate all weak compositions eta of k in ascending lexicographic order. Functions are column vectors. For eta'=eta-delta_x+delta_y, x!=y, A sets

    L_A[eta,eta'] = c_xy eta_x (alpha_y+eta_y),
    L_A[eta,eta] = -sum_{eta'!=eta} L_A[eta,eta'].

The graph sum is ordered. There is no factor 1/2 in L. The x=y terms vanish and are excluded. Empty departure sites never evaluate an inadmissible destination. All coefficients are supplied by the primary equation; this is an assembly from a fully specified generator, not inference of an unavailable matrix.

A calculates unnormalized weights w_k(eta)=product_x (alpha_x)_{eta_x}/eta_x! using the finite rising product, then divides by Z_k=(A_tot)_k/k!, A_tot=sum_x alpha_x. This is exactly the primary Gamma quotient by the Gamma recurrence.

## B: the reversible quadratic form in another representation

B independently enumerates occupancies using a descending Cartesian product and sum filter. Its local weights are calculated by the recurrence w_x(0)=1 and w_x(m)=w_x(m-1)(alpha_x+m-1)/m. Both k and k-1 probabilities are normalized by explicitly summing their weights, without using A's output or closed-form normalization. The normalization identity follows independently by multiplying the formal power series (1-t)^(-alpha_x) and comparing the coefficient of t^k in (1-t)^(-A_tot). All alpha are positive; the finite-sector weights and masses are positive.

For each zeta with k-1 particles and each graph edge x<y, let

    eta=zeta+delta_x, eta'=zeta+delta_y,
    q(zeta;x,y) = [k/(A_tot+k-1)] mu_{k-1}(zeta)
                 c_xy (alpha_x+zeta_x)(alpha_y+zeta_y).

Here q is an unoriented configuration-edge conductance. Derivation: Eq. (2.2) gives

    mu_k(zeta+delta_x)/mu_{k-1}(zeta)
      = [Z_{k-1}/Z_k] (alpha_x+zeta_x)/(zeta_x+1),
    Z_{k-1}/Z_k = k/(A_tot+k-1).

Multiplying by (zeta_x+1)c_xy(alpha_y+zeta_y) yields q. Repeating with x and y exchanged yields the same q, proving detailed balance. Every allowed occupation jump has a unique zeta, and the two directions in Eq. (3.7) cancel its factor 1/2. Therefore

    E(f) = sum_{zeta, x<y} q(zeta;x,y) [f(eta)-f(eta')]^2
         = f^T K_B f,

where K_B is assembled by adding q*(e_eta-e_eta')*(e_eta-e_eta')^T. B never uses A's rates, states, mass vector or matrices. Its generator reconstructed from the form is L_B=-M_B^(-1)K_B, M_B=diag(mu_B). The primary form and measure, the algebraic derivation and independently implemented recurrence are the actual independence; copying files or comparing hashes would not suffice.

## Explicit map

Let p(i) be the B index of the same occupancy as A index i. Let P have P[i,p(i)]=1, so f_A=P f_B. Then

    L_A = P L_B P^T,
    M_A = P M_B P^T,
    -M_A L_A = P K_B P^T,
    H_A = -M_A^(1/2) L_A M_A^(-1/2)
        = M_A^(-1/2) (P K_B P^T) M_A^(-1/2).

H is the real symmetric operator similar to -L; its null vector is sqrt(mu), not the constant vector except for uniform mu. The smallest positive eigenvalue has inverse-time units. Forward probability evolution uses L^T and has the same eigenvalues. The exact comparison checks all entries, all mass components and every configuration edge after permutation. No numeric tolerance is used for these comparisons.

## Physical admissibility and baseline scope

The finite graph is undirected and connected, c>=0 and c_xx=0, alpha>0 and total occupancy k is conserved. There are no reservoirs or boundary creation, and no continuum or perturbative approximation. Rates are nonnegative; K is a sum of positive edge forms. Connectivity plus positive alpha makes the occupation graph connected, hence constants are the unique zero mode. This gives a finite reversible Markov relaxation problem, not an empirical particle prediction.

For the three-site unit path alpha=(1,1,1), the independently written one-particle negative generator in site order is

    [[1,-1,0],[-1,2,-1],[0,-1,1]],

with eigenvectors (1,1,1), (1,0,-1), (1,-2,1) and eigenvalues 0,1,3. Published Eq. (1.2), together with gap_{k+1}<=gap_k in Eq. (2.7), implies gap_k=1 for every k>=1 in this known regime. We reproduce the k=1,2,3 instances by exact characteristic polynomials and rational real-root isolation. This is not a new theorem for arbitrary parameters.

A second published check uses the complete graph with unit conductances and alpha=(1/2,2/3,3/4), A_tot=23/12. Eq. (3.5), Eq. (3.8) and Proposition 3.1/Eq. (3.9) give eigenvalues j*(A_tot+j-1), j=0,...,k, with multiplicities binomial(n+j-2,j) (multiplicity one for j=0). For n=3 these multiplicities are j+1. The exact expected values through k=3 are 0,23/12,35/6,47/4. This published instance checks heterogeneous weights below one without extending the conjecture. The weighted four-site family is an input-convention diagnostic only, with no target gap claim.

The same agent wrote both constructions using the same source and case specifications. They have separate algorithms, state enumeration, normalization and code and read no shared computed answers. This is weaker than a fresh referee reconstructing the source; no referee acceptance is claimed.
