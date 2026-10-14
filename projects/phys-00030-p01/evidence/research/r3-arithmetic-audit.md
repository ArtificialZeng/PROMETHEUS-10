# Proposer audit of the finite-model enclosure kernel

This stable argument audits `evidence/research/r3-interval-enclosure.py`, derived from the preserved `evidence/research/r2-interval-enclosure-v2.py`. It is not independent referee acceptance. The exact model is `evidence/research/r1-tightbinding-model.md`; determinant and integrand identities are `evidence/research/r2-enclosure-derivation.md`. No physical parameter is changed.

## Polynomial ranges and floating-point envelope

Each exact trigonometric hopping-squared lies in its 250-digit directed interval. Addition and multiplication in the real continuant recurrence therefore enclose every exact coefficient of F, B, G, and K=F+gamma_f^2 G. Reflection of the finite chain follows from the exact sine identity h_l=h_(128-l), not from rounding. The small residual coefficients of K are retained; none is set to zero. Even F and odd B allow polynomials in x=q^2. All panels have binary dyadic endpoints.

The actual point coefficient c_k is the value rounded by mpmath at 100 decimal digits. For each coefficient interval p_k, the program obtains an outward relative error r_k with |p_k-c_k| <= r_k |c_k|; the maximum r is used. A zero center is permitted only for an exact zero interval. The generalized Horner jet algorithm at the binary midpoint m evaluates the first 20 Taylor coefficients at x_c=m^2. This square is exact at its 336-bit point precision for every binary64 m: its integer significand has at most 106 bits. Powers have unbounded exponents, with no hardware underflow/overflow assumption.

For nearest-rounded basic addition/multiplication use u=2^(1-p), conservatively exceeding their relative unit-roundoff error. With N=4(65+1)(20+1)=5544, gamma_N=N u/(1-N u) is an outward bound. N exceeds all additions/multiplications in the signed or absolute jet recurrence and hence every dependency path. Taking absolute values of the polynomial coefficients and using x_c>=0 gives a nonnegative recurrence A_hat for the absolute Taylor coefficient sum. The signed floating-point jet error is at most gamma_N A_exact, and A_exact <= A_hat/(1-gamma_N). Input-coefficient uncertainty contributes at most r A_exact. Hence each stored jet is enclosed by

    jet_hat +/- (gamma_N+r) A_hat/(1-gamma_N).

All operations forming this envelope and evaluating the degree-19 Taylor polynomial are directed interval operations at 85 decimal digits. Cancellation cannot invalidate this absolute forward-error bound. The remainder is bounded independently over the whole panel by

    radius^20 sum_(k>=20) abs(p_k) binom(k,20) X^(k-20),

where radius bounds |x-x_c| and X bounds |x| on the panel and along the Taylor segment. This includes every degree, with no fitted degree truncation. For the dyadic panels split at zero, x_c lies within the squared panel range. The absolute coefficient upper bounds themselves are converted with outward interval rounding.

## Non-polynomial operations and physical clipping

All divisions, square roots, exponentials, logarithms, complex squared norms, and integration widths use directed intervals. On a denominator interval containing zero, both transmissions are replaced by [0,1]. Otherwise the resulting intervals are intersected with [0,1], which is legal by the exact unitary scattering construction. No narrow resonance is dropped: an interval range over an entire panel, multiplied by its positive width, encloses that panel's integral even if the denominator bound falls back. The marginal moment-generating function is intersected with [exp(-24),exp(24)], an exact consequence of the possible single-channel extracted counts -1,0,1. Its logarithm then exists on the whole interval.

The point kernel is a finite-Hamiltonian determinant identity. The self-energy gamma(q) is the exact tight-binding retarded self-energy, not a wide-band approximation. Current, entropy, and CGF use the same transmissions, fixed Fermi reservoirs, and all three reservoir heats. The residual is integrated directly rather than formed by subtracting independently loose integrated observables.

## Integral coverage, export, and tails

The refinement heap chooses panels only; it does not estimate an error. A completed panel replacement preserves an exact dyadic partition. The new driver checks consecutive ordered endpoints, nonzero widths, endpoints -8192 and 16384, and the exact rational width sum 24576. It then recomputes all four total intervals from the active panel list with directed arithmetic, independently of the incremental endpoint accumulator. Its time ceiling is checked only between complete replacements. A partial run remains incomplete.

Each exported binary64 endpoint is moved by one representable value outwards with nextafter. This encloses the arbitrary-precision endpoint regardless of the direction of nearest conversion. A separate checker uses exact rational sums of these exported panel endpoints and verifies coverage and tails. This exported certificate may be slightly wider than the internal total and is the conservative bound to quote.

The analytic tails derived in `evidence/research/r2-enclosure-derivation.md` use only Fermi probabilities, unitarity, and single-channel counting. They enclose the remaining physical energies from 0 to 40000; extending the estimates beyond that band enlarges them. They include all reservoir entropy. The Delta tail is below 1.12e-14 in epsilon/h.

Trust base: Python integers and binary64 endpoint arithmetic, installed mpmath 1.3.0 directed interval elementary functions, and its nearest-rounded arbitrary-precision addition/multiplication. This is computer-assisted arithmetic, not a formally verified proof assistant result. An independently reconstructed high-precision sector/Fock calculation is a diagnostic cross-check, not a replacement for these range arguments or a fresh scientific referee.

## Refinement from the completed certificate

The first new run completed normally with 17603 active panels, a strictly positive residual enclosure, and exact independent partition/export checks in `evidence/research/r3-partition-check.json` and its log. To meet the earlier width objective, `evidence/research/r3-interval-refine.py` uses that completed certificate as an explicit stable input. Its exported outward panel intervals are valid starting integral bounds, rather than point or quadrature estimates. Reading their binary64 endpoints into intervals can only preserve/enlarge those bounds. Selected parent panels are then replaced by freshly computed child interval ranges of the same kernel. Analytic tails are added once after summing finite panels.

The refinement completed normally in about 286 seconds, within its 300-second ceiling, with 26275 active panels. It explicitly verifies every new binary width subtraction as an exact rational difference, checks the full consecutive partition, and recomputes all final sums directly. `evidence/research/r3-refined-partition-check.json` and its actual log independently sum all exported endpoints using Python exact fractions and add the outward tail bounds. The final Delta interval has width below 0.005 and positive lower endpoint. The stable parent certificate, both drivers, both complete output logs/JSON records, and both independent partition checks are necessary scientific dependencies. No incomplete prior run is used as a certified input.
