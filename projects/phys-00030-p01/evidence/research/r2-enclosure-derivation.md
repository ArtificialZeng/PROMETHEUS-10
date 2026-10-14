# Interval integration of the fixed finite conductor

This is the derivation behind r2-interval-enclosure.py and its explicitly improved version r2-interval-enclosure-v2.py. It is a proposer calculation, with no referee acceptance. The Hamiltonian and physical boundary conditions remain exactly those in r1-tightbinding-model.md and r1-proposed-witness.json. All previous sources and calculations remain preserved.

## Dimensionless determinant representation

Use q=(E-5000)/0.01. In this section gamma_f, gamma(q), g_c, lambda and each filter hopping are divided by the appropriate power of 0.01. Thus g_c=20000000, gamma_f=1/[2 sin(pi/256)], lambda^2=gamma_f g_c, and h_l^2=1/[4 sin((2l+1)pi/256) sin((2l-1)pi/256)]. The small real-contact coefficient a is dimensionless and equals the PHYSICAL Gamma_f/sqrt(5000*35000).

Let F(q) be the real closed-filter determinant (128 sites), B(q) the determinant after removing its first site (127 sites), and G(q) the determinant after removing both endpoints (126 sites). Reflection symmetry of the specified hoppings makes B also the determinant with the last site removed. The real continuant recurrence is P_(j+1)=q P_j-h_j^2 P_(j-1), with P_0=1 and P_1=q. Define K=F+gamma_f^2 G. The code computes its coefficients with outward intervals; it DOES NOT assume an exact simplification of K, or infer a zero from a small residual coefficient.

The contact-modified filter and zero-core-sector determinants are

    D=F+(i gamma-a q) B,
    C=q D-lambda^2 [B+(i gamma-a q)G],
    gamma(q)=gamma_f sqrt[(1+0.01q/5000)(1-0.01q/35000)].

The three Fourier core energies are 0 and +/-sqrt(3)g_c. The three retarded sector determinants are C and C+/-sqrt(3)g_c D. Their endpoint cofactors give the flux-normalized resolvent scattering matrix specified in the fixed model. They are nonsingular inside the lead band: a Jacobi chain with all connecting hoppings nonzero cannot have an eigenvector vanishing at the sole absorbing endpoint. A zero-inclusive interval denominator therefore signals loss of an interval bound, not a physical singularity.

Put H=product_(l=1)^127 h_l^2 and

    A=4 gamma^2 (lambda^2)^2 H^2 g_c^2 /
      [|C|^2 |C-sqrt(3)g_c D|^2 |C+sqrt(3)g_c D|^2].

The off-diagonal circulant probabilities are

    u=T_01=A |C-i g_c D|^2,
    v=T_02=A |C+i g_c D|^2.

This follows either from the core adjugate, whose off-diagonal entries are -g_c^2 +/- i g_c eta for eta=C/D, or from its three Fourier sectors. Eliminating the chains supplies the factor (lambda^2)H/D^2; all D factors cancel in the displayed expression. It avoids subtracting nearly equal scattering phases. The orientation agrees with the independent old resolvent and Bloch/sector programs at the saved point checks: at q=0, v=1 and u=0 in exact arithmetic.

For the small reverse numerator the cancellation is performed algebraically before interval evaluation. With B_k=q B-lambda^2 G, its real and imaginary parts are

    Re(C-i g_c D)=qF+g_c(gamma-gamma_f)B-a q B_k,
    Im(C-i g_c D)=q(gamma+g_c a)B
                  -g_c(gamma/gamma_f)K
                  +g_c(gamma/gamma_f-1)F.

Every identity here is finite dimensional and at finite filter width; no wide-band replacement, perturbative expansion, infinite-chain limit or freely chosen energy occupations is made.

## Currents, actual entropy and counting

The reservoirs stay at T=1 and mu-5000=(1,-3,-24), with the original rate units epsilon/h and entropy units k_B epsilon/h. Let z=exp(0.01q), e_0=exp(-1), e_1=exp(3), e_2=exp(24), and d_a=1+z e_a. Set

    j_u=f_0-f_1=z(e_1-e_0)/(d_0 d_1),
    j_12=f_1-f_2=z(e_2-e_1)/(d_1 d_2),
    j_v=f_0-f_2=j_u+j_12.

The complete current vectors for u and v are respectively (j_u,j_12,-j_v) and (j_v,-j_u,-j_12). All three reservoirs are included in heat-derived entropy. Energy conservation at the common temperature gives the exact dimensionless entropy density

    e=u(25 j_u+21 j_12)+v(4 j_u+25 j_12).

Both cycle contributions are strictly positive for these unequal occupations, and the selected mean density is J_0=u j_u+v j_v. There are no probes or controllers. For extracted-particle count X in {-1,0,1}, the independently established Fock marginal gives M=1+u A_u+v A_v at s=-24, with

    A_b=z[e_b(exp(-24)-1)+e_0(exp(24)-1)]/(d_0 d_b).

Thus the linear residual density is exactly

    u(-76 j_u-84 j_12)+v(8 j_u-76 j_12)-log M.

Integration carries the Jacobian dE=0.01 dq. This direct density retains correlations between J and the actual entropy. On interval failure, the code uses the physical bounds 0<=u,v<=1 and exp(-24)<=M<=exp(24). Allowing u and v to vary independently enlarges the interval and is safe even though they satisfy the stronger u+v<=1.

## Polynomial ranges and roundoff

The defining trigonometric coefficients and real continuants are formed using mpmath.iv at 250 decimal digits. F is even, while B is odd. Their even polynomials in x=q^2 are enclosed by a Taylor polynomial of degree 19 about the panel's binary midpoint squared. The order-20 Lagrange remainder is bounded by

    radius^20 sum_(k>=20) |p_k| binom(k,20) X^(k-20),

where X bounds |x| throughout the panel. This is an a priori derivative bound, including all polynomial degrees. It is unrelated to adaptive Gauss/Kronrod error estimates.

The first program evaluates all point Taylor coefficients with outward interval operations at 85 digits. Version 2 evaluates point generalized-Horner jets with nearest-rounded mpf arithmetic at 100 digits and then supplies an explicit forward-error envelope. A separate positive generalized-Horner recurrence computes the absolute coefficient sum for each jet. For N=ROUND_OPS, u=2^(1-precision_bits), gamma_N=N u/(1-N u), each point jet error is bounded by

    (gamma_N+coefficient_relative_radius) S_computed/(1-gamma_N).

Here coefficient_relative_radius is itself an outward bound on the difference between the exact interval coefficient and the actual rounded point coefficient. N=4(maximum_even_polynomial_length+1)(20+1) exceeds the total elementary operations of each jet recurrence, hence each arithmetic dependency path. The positive recurrence's own rounding is covered by 1/(1-gamma_N). The point midpoint square is exact at this precision, since the binary64 midpoint has at most 53 significand bits. All remainder, complex norm, transmission, exponential, logarithm and integral operations still use directed iv endpoints. The computational trust base is Python integer/binary arithmetic and the installed mpmath implementations of basic rounded mpf and interval elementary functions. This is disclosed computer-assisted arithmetic, not a formalized proof assistant certificate.

## Coverage, sharp resonances and tails

Every panel returns an interval RANGE over its whole energy interval. Multiplying by its positive width therefore encloses the integral, including arbitrarily narrow resonances within it. A zero-inclusive denominator invokes a broad physical interval; subdivision must reduce its integrated uncertainty before a positive conclusion is allowed. The adaptive heap chooses which interval to refine but contributes no correctness assumption. Endpoint sums use outward operations, and old intervals are replaced through their separate lower and upper endpoints. Final panel coverage must span [-8192,16384] without gaps or overlaps.

These cuts correspond to delta=E-5000 in [-81.92,163.84]. For the lower tail, each reservoir hole probability is at most exp(delta+24); for the upper tail, each particle probability is at most exp(1-delta). A nonzero single-terminal count requires at least one hole or particle among the three incoming channels. Consequently the integrated nonzero-event bounds are H_t=3 exp(-81.92+24) and P_t=3 exp(1-163.84). Their exp(24)-amplified values are below 1/2 throughout the respective tails, so |log M|<=2 exp(24) times the nonzero-event probability. Conservative integrated bounds are

    J_tail<=2(H_t+P_t),
    (sigma/k_B)_tail<=28 J_tail,
    chi_tail<=2 exp(24)(H_t+P_t),
    Delta_tail<=24 J_tail+4(sigma/k_B)_tail+chi_tail.

The code encloses these exponentials as well. Integrating the estimates beyond the actual propagating band [0,40000] only enlarges them. Finite sample bound states carry no steady reservoir current. The new interval tail for Delta is less than 1.12e-14 in epsilon/h.

## What a successful enclosure would establish

The stable exact arguments in r1-legendre-cycle-derivation.md and r1-exact-psi-control.md prove psi_0>=1/2 and B_psi0(-J)<=4sigma/k_B. Finiteness of psi_0 also follows from the diagonal limit of its defining ratio, which is 1. For J>0 and sigma>0, -J is strictly inside the asserted current domain. Fenchel's inequality at s=-24 gives I_0(-J)>=24J-chi_0(-24). Therefore a strictly positive enclosed Delta establishes an actual rate-function violation at this specified current, with no rounded infimum, numerical saddle or unknown optimizer. Until such an enclosure is completed, the witness remains unverified. A completed proposer calculation still requires a fresh scientific referee.
