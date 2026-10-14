# Proposer computer-assisted counterexample to the frozen assertion

Job: phys-00030-p01-research-162196e61501. This is a scientific candidate for fresh referee review. It is not referee acceptance, a manuscript, or a claim that the alternative joint-current conjecture is resolved.

## Statement and exact model

For the exact stationary normal 387-site conductor defined in `evidence/research/r1-tightbinding-model.md`, and the fixed reservoirs in `evidence/research/r1-proposed-witness.json`, the curvature-matching universal assertion frozen in `source.md` and `problem.md` is false. With lead 0 extracted-particle counting and its positive mean J, the reversal current j=-J is strictly within the asserted domain and

    I_0(-J)-B_psi0(-J) > 0.019 epsilon/h.

Here psi_0 is the exact infimum in PRL supplemental Eq. (S5), not its numerical approximation. epsilon=k_B T_ref with any T_ref>0. The model has three one-channel semi-infinite normal tight-binding leads with hopping -10000 epsilon, onsite 20000 epsilon and propagating band [0,40000]epsilon. It has three 128-site filters with E0=5000 epsilon, w=0.02 epsilon and the exact PRL w/4 sine hoppings, coupled to the Hermitian flux ring i Gamma_c(P-P^T), Gamma_c=200000 epsilon. The precise outer onsite compensation and real contacts are in the model definition. Every reservoir has temperature T_ref and chemical potentials (5001,4997,4976)epsilon. All three reservoir heats enter sigma. The contacts have their exact energy-dependent retarded self-energy; there is no wide-band or small-width approximation in this witness.

## Analytic reduction

The stable proof in `evidence/research/r1-exact-psi-control.md` starts from D(y||x), the exact numerator of the defining infimum. Jensen's square-root likelihood bound and x=sin^2(alpha), y=sin^2(beta) give psi_0>=1/2 on the whole defining domain and its continuous limits. The diagonal limit of the same ratio is 1, so psi_0 is positive and finite. This argument does not need the rounded minimum or the authors' numerical minimization.

Let c=J coth[sigma/(2 psi k_B J)]. The stable derivation in `evidence/research/r1-legendre-cycle-derivation.md` gives

    B_psi(-J)=2 sigma/(psi k_B).

For J>0 and sigma>0, c>J, so -J is strictly interior to (-c,c). At the explicit real field s=-24, the definition of the physical Legendre rate function gives

    I_0(-J) >= 24J-chi_0(-24).

Consequently

    I_0(-J)-B_psi0(-J)
      >= 24J-chi_0(-24)-4 sigma/k_B = Delta.

This is a fixed-current Fenchel test. It neither approximates the exact psi_0 nor assumes a numerical optimizer or identifies the physical saddle with that of the proposed bound.

## Physical counting and entropy

Physical admissibility, unitarity, steady boundaries, exact contact scaling, Fermi reservoirs, source signs, units, and all-reservoir entropy are audited in `evidence/research/r3-physical-admissibility.md`. The finite dot Hamiltonian is Hermitian, stationary, number preserving, and noninteracting. It has only the three specified external reservoirs. Its retarded resolvent proves unitary scattering in the open lead band. Closed bound modes do not carry steady reservoir currents. The counted marginal is the source Levitov determinant, independently reconstructed using Slater-event probabilities.

With q=(E-5000)/0.01 and circulant transmission probabilities u=T_01 and v=T_02, put j_u=f_0-f_1 and j_12=f_1-f_2. Both are positive at every finite physical energy. Then the exact selected mean and actual total entropy densities are

    J_density = u j_u+v(j_u+j_12),
    (sigma/k_B)_density = u(25j_u+21j_12)+v(4j_u+25j_12).

The determinant marginal at s=-24 supplies M=1+u A_u+v A_v, with the exact Fermi A_b given in `evidence/research/r2-enclosure-derivation.md`. Thus the residual is integrated directly with density

    u(-76j_u-84j_12)+v(8j_u-76j_12)-log M.

This retains the correlation between mean current and total entropy. It is not event-reversal entropy, a partial dissipation, or an omitted probe heat. At E0 the exact scattering is cyclic, and positive-temperature occupations give positive probabilities for both signs of the selected count. The physical CGF is finite for finite real fields; it has the source count-variance normalization.

## Completed range certificate and independent checks

`evidence/research/r3-interval-enclosure.py/.json/.log` completed normally, independently of the old quadrature outputs. It generates the finite-model continuant coefficients with directed 250-digit intervals, encloses degree-19 Taylor ranges with an all-degree remainder and an explicit point-Horner forward-error bound, and uses directed 85-digit arithmetic for the remaining operations. It bounds whole energy panels, including unresolved filter-edge resonances. A denominator interval containing zero falls back to physical transmission bounds rather than dropping any energy set.

`evidence/research/r3-interval-refine.py/.json/.log` then refined that completed, audited outward certificate and completed normally in about 286 seconds, within its 300-second ceiling. Its final 26275 panels cover q=[-8192,16384] exactly. The independently constructed checker uses exact rational endpoint and width sums, verifies every consecutive panel and the exact total width, and adds analytic tails. Its actual output is `evidence/research/r3-refined-partition-check.json` and its log. All 727 remaining denominator-fallback panels retain full physical ranges; they are included in the reported uncertainty.

The resulting outward decimal enclosures are

    Delta                 in [0.019447, 0.024248] epsilon/h,
    J                     in [0.013576, 0.014625] epsilon/h,
    sigma/k_B             in [0.073446, 0.079193] epsilon/h,
    chi_0(-24)            in [0.010467, 0.012105] epsilon/h.

These are outward-rounded enclosures, not estimates or asserted significant digits. Delta is integrated directly; subtracting the displayed separate rate intervals would be much weaker. The actual exported Delta enclosure has width less than 0.004800 and hence below the requested 0.005. The analytic Delta tail is below 1.12e-14 epsilon/h. The remaining physical domain consists only of Fermi-suppressed tails within the actual band; the estimates conservatively extend beyond its endpoints.

The independent outgoing-Bloch, backward-sector, and explicit Slater-event reconstruction in `evidence/research/r3-independent-check.py/.json/.log` checks 23 declared points at 320 decimal digits, including filter edges. It does not consume the kernel's polynomial coefficients or cached scattering/quadrature outputs. Unitarity, probability normalization, event current, and determinant/Fock discrepancies are below 1e-130; independent transmissions and all four densities lie inside the point interval ranges. The first 180-digit comparison failed for 1e-155 amplitudes at |q|=4. That actual failed log and the precision diagnosis remain preserved. High-precision agreement is a diagnostic; the proof of integrated error is the interval range argument in `evidence/research/r3-arithmetic-audit.md` and the full partition certificate.

Since the completed enclosure establishes J>0, sigma>0 and Delta>=0.019447 epsilon/h, the analytic reduction proves the stated strict rate-function violation. One admissible example refutes the full universal quantifiers; no restriction of the original problem is silently introduced.

## Scope, value, and limits

The target is this project's exact curvature-matching interpretation of the first conjectural extension in final JPA Section 4. It is not a formula quoted verbatim as an established theorem. The established reciprocal full-statistics result and nonreciprocal variance inequality are unaffected. The alternative joint-current conjecture and other possible entropy-dependent rare-event bounds remain open here.

The physical mechanism is circulation: the intermediate reservoir reduces actual mean entropy per selected particle, while reversing the selected count depends on occupation of a reservoir with much lower chemical potential. A finite filter and flux ring realize this mechanism with actual Fermi reservoirs, rather than an arbitrary unitary array at one energy. Matching the variance inequality by replacing the reciprocal dissipation factor therefore does not suffice to control this rare reversal event.

Novelty comparison and fresh bounded searches are `evidence/research/r3-current-literature.md` with retained primary inputs. The search is not an exhaustive priority claim. Numerical trust rests on Python exact rationals and the specified installed mpmath interval/point arithmetic, as disclosed in the arithmetic audit. This is a computer-assisted proposer result requiring a fresh scientific referee to reconstruct the source, audit the finite-model identities and arithmetic, and assess novelty and significance before any writing.
