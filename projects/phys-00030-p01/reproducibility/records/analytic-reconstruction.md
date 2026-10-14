# Independent analytic reconstruction for the frozen finite counterexample

Referee job: phys-00030-p01-referee-db03e016c43e. The parameters and quantifiers are those of the current frozen claim. This reconstruction uses the primary equations and the stable evidence; it uses no checkpoint, state file, owner verdict or discovery module.

## Source conventions and physical input

JPA final (19) counts extraction from reservoir alpha. Differentiating its determinant at zero field gives f_alpha minus the outgoing-row occupation sum, hence J_alpha = f_alpha - sum_beta |S_alpha,beta|^2 f_beta per energy channel. JPA (26) gives the same single-channel marginal. Conditional on the incoming selected-mode occupation being one or zero, the outgoing selected mode has binary occupation with expectation fixed by the corresponding row of S. Thus

    p_plus = f_0 sum_(b!=0) |S_0b|^2 (1-f_b),
    p_minus = (1-f_0) sum_(b!=0) |S_0b|^2 f_b,
    M(s) = 1+p_plus(exp(s)-1)+p_minus(exp(-s)-1).

The incoming diagonal Fermi ensemble is an incoherent mixture of occupied sets. The probability of an outgoing occupied set of equal size is the squared determinant of the corresponding scattering submatrix. Summing these nonnegative Slater probabilities independently supplies the same p_plus, p_minus, all reservoir currents and original determinant. This is the route implemented in audit/referee-replay.py, without importing discovery code. The count is X=n_in,0-n_out,0, in {-1,0,1}.

The semi-infinite lead surface equation is t^2 g^2-(E-2t)g+1=0. Its retarded root inside the band is [E-2t-i sqrt(E(4t-E))]/(2t^2). The outgoing Bloch solution has E=2t-2t cos(k) and g=-exp(ik)/t. The two were independently compared at all high-precision replay points. The contacts have Gamma(E)=-Im Sigma(E)>0. The finite sample has only real branch/contact couplings and the Hermitian core i Gamma_c(P-P^T); it is a stationary, normal, number-preserving Hamiltonian. The lead band is [0,40000] epsilon. There are exactly three thermal reservoirs, each at T_ref>0 and with the specified finite chemical potential.

For G=(E-H-Sigma P_outer)^-1, G-G^dagger=-2i Gamma G P_outer G^dagger. Consequently S=I-2i Gamma G_outer is unitary. Nonsingularity in the open band follows from the imaginary quadratic form: a null vector must vanish at all absorbing outer sites, and the nonzero branch couplings successively force its amplitudes through every branch and core to vanish. Bound modes outside the propagating band have no extensive steady reservoir flux. A stationary bound-mode occupation can be chosen.

The filter hoppings use the w/4 convention visually reconstructed from PRL (22)-(25). The witness contacts are exact tight-binding contacts, with the stated outer onsite compensation, rather than the published wide-band baseline. Thus the documented literal JPA dot-coefficient discrepancy changes neither the source counting formula nor physical admissibility of this independently specified Hamiltonian.

Particle conservation and elastic energy conservation imply, at common temperature,

    sigma/k_B = sum_a (mu_a-E0) J_a / epsilon

in the declared rate units. This is exactly -sum_a Q_a/T_a, including all three reservoirs. With u=T_01, v=T_02, j_u=f_0-f_1 and j_12=f_1-f_2, the two cycle current vectors are (j_u,j_12,-j_u-j_12) and (j_u+j_12,-j_u,-j_12). Dotting with (1,-3,-24) gives respectively 25j_u+21j_12 and 4j_u+25j_12. Both are positive. At the central cyclic scattering point the selected mean is positive; continuity gives a positive-width set. Therefore J>0 and sigma>0 also follow analytically. No partial or forward-backward entropy is substituted.

## Exact constant and rate-function reduction

The numerator of PRL SM (S5) is binary D(y||x). Applying Jensen to the square-root likelihood ratio gives D(y||x)>=-2 log C, where C=sqrt(xy)+sqrt((1-x)(1-y)). Write x=sin^2(alpha), y=sin^2(beta). For alpha>beta set r=sin(alpha-beta) and A=sin(alpha+beta). Then r<=A<=1, C=sqrt(1-r^2), x-y=Ar and x+y-x^2-y^2=[A^2(1-2r^2)+r^2]/2.

For fixed r, the denominator is F(A)=Ar asinh[2Ar/(A^2(1-2r^2)+r^2)]. Its derivative divided by r is at least asinh(u)-u/sqrt(1+u^2)>=0. The denominator is therefore at most F(1)=2r atanh(r). Also -log(1-r^2)>=r atanh(r), since the difference has derivative r/(1-r^2)-atanh(r)>=0. Combining gives D(y||x)>=half the denominator. The square-root bound holds in either KL direction, while the denominator is symmetric, so the proof covers x<y as well. Continuous limits give psi_0>=1/2. The diagonal limit of the ratio is one, so psi_0 is finite. No decimal minimizer is used.

Let c=J coth[sigma/(2 psi k_B J)]. Direct evaluation of the exact proposed shape gives

    B_psi(-J)=2J log[(c+J)/(c-J)]=2sigma/(psi k_B).

Positive finite sigma, J and psi imply c>J, so -J is interior. Fenchel at the fixed real field -24 gives I_0(-J)>=24J-chi_0(-24). Thus

    I_0(-J)-B_psi0(-J) >= 24J-chi_0(-24)-4sigma/k_B = Delta.

This establishes an actual rate-function violation whenever the stated Delta enclosure is positive. It needs neither a numerical saddle nor equality in the physical Legendre transform.

## Finite-model identities behind the range kernel

In q=(E-5000)/0.01, the closed-branch continuant has degree 128. Let F be its determinant, B the degree-127 endpoint-deleted determinant and G the degree-126 both-endpoints-deleted determinant. Exact branch reflection gives the same B at either endpoint. The contact-modified determinants are

    D=F+(i gamma-aq)B,
    C=qD-lambda^2[B+(i gamma-aq)G].

The core Schur complement is (C/D)I-i g_c(P-P^T). Its determinant is eta(eta^2-3g_c^2). Its (0,1) inverse numerator is -g_c^2-i g_c eta=-i g_c(eta-i g_c); the (0,2) numerator has the opposite sign. The endpoint-to-endpoint branch inverse has numerator product(h_l)/D. Consequently outer Green off-diagonal entries are proportional to (C minus or plus i g_c D)/[C(C-sqrt(3)g_c D)(C+sqrt(3)g_c D)], with the prefactor in the frozen kernel. This derives u and v as squared amplitudes over the whole band, without a filter limit.

Expanding C-i g_c D using lambda^2=gamma_f g_c and K=F+gamma_f^2 G yields exactly the small-numerator formulas in the packet. K is retained as an interval polynomial; no approximate coefficient is discarded. Current, entropy and marginal M then give the submitted direct residual u(-76j_u-84j_12)+v(8j_u-76j_12)-log M. The independent replay instead evaluates the original physical resolvent, original Fermi functions, all source currents and explicit Slater probabilities.

## Arithmetic issue investigated and closed for this fixed certificate

The generalized Horner jets of FE(x) and BE(x), x=q^2, evaluate the first 20 Taylor coefficients. At the dyadic midpoint, x_c is exactly representable at 336 bits. All basic point additions/multiplications are nearest-rounded. N=5544 is greater than the full operation count of each signed or positive jet recurrence. Standard absolute forward error is bounded by gamma_N times the exact positive recurrence, and its computed positive value is inflated by 1/(1-gamma_N). The independently bounded coefficient-relative uncertainty contributes the additional r term. This justifies the recorded jet envelope, including cancellation. A degree-19 Taylor expansion additionally needs the remainder upper bound

    radius^20 sum_(k>=20) |p_k| binom(k,20) X^(k-20).

The packet's prose incorrectly calls its intermediate ABS coefficient magnitudes outward upper bounds. The scalar mpf absolute value rounds to the point context. audit/referee-roundoff-replay.py independently reconstructs both the 250-digit coefficients and 500-digit intervals and proves 42 actual coefficient magnitudes exceed the initialized ABS values. This is a real implementation/argument issue; it is not suppressed or treated as evidence against the physical witness.

For the actual frozen certificate the issue is closed by a stronger exhaustive referee check. audit/referee-remainder-fullcheck.py computes each implemented remainder upper endpoint using an independently transcribed 85-digit evaluation, and compares it to a 500-digit directed reference bound. The reference takes magnitude upper endpoints by clearing the exact encoded sign bit, avoiding scalar nearest-rounded absolute values. It uses the same exact dyadic midpoint, interval radius and X, and new coefficients enclosing the exact model values. All 52,550 comparisons pass for both polynomials on all 26,275 final panels. Each actual remainder upper endpoint is at least the reference upper endpoint. Thus subsequent outward arithmetic supplies adequate margin for every remainder actually used. This is full fixed-certificate range verification, not a point sampling argument or a generic certification of the ABS helper.

With those actual remainder endpoints verified, the frozen FE/BE ranges enclose the exact continuants. All remaining real/complex-norm operations use directed interval arithmetic. A zero-inclusive denominator uses [0,1] for both transmissions, which is legal by unitarity. Clipping to physical transmission and moment bounds is an intersection with proved admissible ranges. exp(-24)<=M<=exp(24), so its logarithm is defined. No resonance or denominator-fallback panel is omitted.

## Full energy coverage and conclusion

Exact rational checks cover 26,275 consecutive dyadic panels in q=[-8192,16384], with total width 24576 and all 727 denominator-fallback panels included. Each stored integral interval bounds its entire panel. Parent-carried panels use the same kernel and endpoints; they are included in the exhaustive remainder check. Binary64 exports each move one representable number outward. Exact-rational sums of these exported bounds are independently recomputed in audit/referee-exact-sums.json.

For delta below -81.92, all three hole probabilities are bounded by exp(delta+24); above 163.84, all three particle probabilities are bounded by exp(1-delta). A nonzero extracted count requires at least one such hole/particle. Let H=3exp(-81.92+24), P=3exp(1-163.84), J_tail=2(H+P). Then sigma_tail/k_B<=28J_tail and |chi_tail|<=2exp(24)(H+P). The logarithm bound follows from |M-1|<=exp(24) times the event probability, which is below one half throughout the tails. The Delta tail is at most 24J_tail+4sigma_tail/k_B+|chi_tail|. Extending these bounds beyond the actual lead band is conservative. The independently computed Delta tail upper bound is 1.1139929091605643e-14 epsilon/h.

The exact exported sums with these tails give

    Delta in [0.019447591396978867, 0.024247460886202978] epsilon/h,
    J in [0.013576913534704596, 0.014624073530814305] epsilon/h,
    sigma/k_B in [0.073446431786451, 0.0791927501103559] epsilon/h.

The decimal display is outward from exact binary rational sums. In particular Delta>0.019 epsilon/h, proving the stated strict rate-function gap for this finite, positive-temperature sample and refuting the original universal formalization. The width is below 0.005. The two-terminal reciprocal theorem, published variance bound, alternative joint-current question and other possible full-statistics shapes retain their original scopes.

The trust base is Python exact integer/rational arithmetic, mpmath 1.3.0 interval elementary functions, nearest-rounded arbitrary-precision basic operations with the stated forward-error bound, and the finite-Hamiltonian algebra. High-precision point agreement and Gauss convergence are additional diagnostics, not replacements for the range proof. This is computer-assisted verification, not formal proof-assistant certification or external human peer review.
