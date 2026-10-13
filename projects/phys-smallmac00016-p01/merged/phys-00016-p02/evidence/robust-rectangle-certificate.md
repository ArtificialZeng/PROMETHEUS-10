# Exact uniform robustness certificate for the coarse `03|12` GAD instrument

Job: `phys-00016-p02-research-48719ecd8232`.

## Certified statement

Keep the ordered GAD Kraus representation, the two-use protocol, the `03|12`
coarse environment readout, and the fixed history witness in `problem.md`.  Put

\[
 R=\left[\frac{71}{100},\frac{723}{1000}\right]
   \times
   \left[\frac{29}{100},\frac{303}{1000}\right].
\]

The centre `(18/25,3/10)` lies strictly inside this closed rational rectangle.
For every `(p,gamma)` in `R`, including every boundary point, and every allowed
time-dependent current-bit policy whose recoveries are arbitrary qubit CPTP
maps,

\[
 F_e(\Phi^{\pi_M}_2(p,\gamma))
 \le H(p,\gamma)-\frac1{1000},
 \qquad H(p,\gamma)=1-\gamma+\frac{p\gamma^2}{2}.
\]

Since the same parameter-independent retained-history policy attains `H`, this
implies

\[
 \inf_{(p,\gamma)\in R}\bigl(F_2^B-F_2^M\bigr)\ge\frac1{1000}>0.
\]

This is an exact sufficient certificate, not an assertion that either optimum is
known.

## Arbitrary-CPTP bound

For one corrected use define
`C=R_0 o I_0 + R_1 o I_1`, with arbitrary CPTP recoveries.  Hermitian
trace-norm data processing and the triangle inequality give Bloch-column caps

\[
 \|Te_x\|_2,\|Te_y\|_2\le\sqrt{1-\gamma},\qquad
 \|Te_z\|_2\le
 z(p,\gamma)=\frac{1+|p-\gamma|+|1-p-\gamma|}{2}.
\]

The current-bit two-use record sum factorises exactly as `C_2 o C_1`.  The
identity `F_e=(1+tr(T_2T_1))/4` and Frobenius Cauchy--Schwarz therefore bound
every allowed policy by

\[
 U(p,\gamma)=\frac{1+2(1-\gamma)+z(p,\gamma)^2}{4}.
\]

This step assumes neither unitarity nor unitality of a recovery and introduces
no optimiser branch.

## Exact whole-rectangle minimisation

On `R`,

\[
 \gamma-(1-p)\ge 0,
 \qquad p-\gamma\ge\frac{407}{1000}>0.
\]

The first inequality is saturated only at the lower-left corner
`(71/100,29/100)`.  Thus the absolute-value chamber formula `z=p` is valid on
the entire closed rectangle, including that chamber boundary.  Consequently

\[
 G:=H-U=\frac{1-2\gamma+2p\gamma^2-p^2}{4}.
\]

The derivative signs are uniform and exact:

\[
 \partial_pG=\frac{\gamma^2-p}{2}<0,
 \quad p-\gamma^2\ge\frac{618191}{10^6},
\]

and

\[
 \partial_\gamma G=p\gamma-\frac12<0,
 \quad \frac12-p\gamma\ge\frac{280931}{10^6}.
\]

Hence the minimum is the upper-right corner, not a sampled grid point.  Exact
rational evaluation gives

\[
 \min_R G
 =G\!\left(\frac{723}{1000},\frac{303}{1000}\right)
 =\frac{2013407}{2000000000}
 =\frac1{1000}+\frac{13407}{2000000000}.
\]

All parameters stay in the open CPTP domain.  `K_1` and `K_3` occupy distinct
nonzero off-diagonal matrix units.  Within the diagonal subspace, the squared
determinant of the two coordinate vectors from `K_0,K_2` is
`p(1-p)gamma^2`; on `R` it is bounded below by the strictly positive rational
`168427911/10000000000`.  Thus the four Kraus operators remain linearly
independent and full Choi rank is uniform as well.

## Boundary and larger-region attacks

- The lower-left point lies on the chamber boundary `gamma=1-p`; the general
  absolute-value expression and `z=p` agree there, and the certified remainder
  is `17661/2000000`, well above `1/1000`.  The proof therefore genuinely
  includes a chamber boundary rather than relying on an open-neighbourhood
  continuity argument.
- At `(709/1000,29/100)`, just beyond that chamber, `z=1-gamma=71/100`.
  The general bound still has positive remainder `175769/20000000`, but using
  the old `z=p` branch would overstate it by `1419/4000000`.  Chamber crossing
  changes the certificate formula; it is not disappearance of history
  advantage.
- The strict superset
  `[71/100,29/40] x [29/100,61/200]` remains in the same chamber, but its
  upper-right remainder is `-591/3200000`.  Along the simultaneous upper
  displacement `(p,gamma)=(18/25+r,3/10+r)`, the certificate zero lies between
  exact radii `1/225` (positive remainder `13297/91125000`) and `1/200`
  (negative remainder above).  This is failure of this sufficient all-CPTP
  bound, not evidence that the true optimal advantage is nonpositive there.

## Error control and reproducibility

`scripts/verify_robust_rectangle.py` independently reconstructs Kraus
completeness, all six instrument Pauli images, and all sixteen hidden history
paths before evaluating the inequalities above.  Every asserted comparison is
symbolic or rational in SymPy; decimals, heat maps, optimisers, fits, and
continuity are absent from the logical certificate.  Its complete successful
output is `evidence/robust-rectangle-check.log`, and the runtime preflight is
`evidence/research-runtime-versions.txt`.
