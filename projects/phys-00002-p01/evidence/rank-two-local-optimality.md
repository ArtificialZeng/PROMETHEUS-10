# Certified rank-two local optimality at `a=1/2`

## Statement and conventions

Use the canonical traceless Pauli representation

\[
 {\cal L}_{h,z,w}(\rho)=-i[h\cdot\sigma,\rho]
   +D[z\cdot\sigma](\rho)+D[w\cdot\sigma](\rho),
 \qquad h\in\mathbb R^3,quad z,w\in\mathbb C^3.
\]

Let `a` and `b` be the fixed-basis survival probabilities defined in
`problem.md`.  The interval-Newton record encloses one exact KKT point
`x_*` with `a(x_*)=1/2`, support slope `lambda_*`, and

\[
 b_*\in
 [0.02261621659234744314244509548210769726387405395479335700973522899,
  0.02261621659234744314244509548210769726387405395479335700973924048].
\]

The following is the certified finite-amplitude statement.  Take the native
real coordinates

\[
 x=(h_x,h_y,h_z,\Re z_y,\Re z_z,\Im z_x,\Im z_y,
       \Re\eta_1,\Re\eta_2,\Im\eta_1,\Im\eta_2),
\]

put `x=x_*+B y`, where the fixed numerical matrix `B` is recorded in
`evidence/interval-rank-two-neighborhood.json`, and define

\[
 z=(i\Im z_x,\Re z_y+i\Im z_y,\Re z_z),\qquad
 w=\left(\eta_1,\eta_2,
 -\frac{\bar z_x\eta_1+\bar z_y\eta_2}{\bar z_z}\right).
\]

For every real `y` with `|y_i|<=10^-4` for all eleven coordinates, if the
resulting channel has `a=1/2`, then

\[
 b(y)-b_*\ge 0.0165\,\|y\|_2^2.
\]

In particular, the same conclusion holds on the Euclidean ball
`||y||_2<=10^-4`.  Equality is possible only at `y=0` within this chart.
The generator is finite and GKSL throughout the chart.  The result is local,
rank-at-most-two, and at the single section `a=1/2`.

## Why this is a rank-two local parameterization

The displayed definition gives `z^dagger w=0` identically and the canonical
Kossakowski matrix is

\[
 C=zz^\dagger+ww^\dagger\succeq0,\qquad \operatorname{rank}C\le2.
\]

The certified box keeps `z_z` away from zero, so the rational coordinate is
regular.  Conversely, a rank-at-most-two positive semidefinite `C` close to
the rank-one base point has a simple leading eigenvalue.  Orthogonal spectral
amplitudes give `C=zz^dagger+ww^dagger`.  The leading-jump phase and the
diagonal system-basis rephasing put `z` on
`Re(z_x)=Im(z_z)=0`; the earlier Arb certificate bounds the corresponding
slice-transversality determinant away from zero.  The condition `z_z!=0`
then expresses every orthogonal `w` by the two complex coordinates
`eta_1,eta_2`.  Thus the parameterization covers the nearby rank-at-most-two
cone modulo representation freedoms that preserve the observed `a,b`.
The phase of `w` need not be fixed because it leaves `ww^dagger` unchanged.

## Constrained local-minimum argument

Set

\[
 F=b-\lambda_*a,\qquad
 G=F+(a-1/2)^2.
\]

The seven gauge-slice derivatives of `F` vanish at the exact interval-Newton
root.  The four `eta` derivatives vanish because `D[w]` starts quadratically
at `w=0`.  Since `a(x_*)=1/2`, the penalty has zero gradient there.  Hence
`grad G(x_*)=0` without treating a ball that merely contains zero as an exact
stationarity equation.

The calculation differentiates the affine-Bloch generator through second
order by automatic differentiation.  For every derivative of the finite-time
channel it evaluates the full Frechet derivative of the matrix exponential
with Arb block exponentials.  At 256-bit precision, on the complete cube
`|y_i|<=10^-4`, direct interval Gershgorin lower bounds for the eleven rows of
`Hess G` are respectively greater than

\[
 (0.0333886,0.848479,0.833121,0.910825,0.910825,0.811641,
   0.912136,0.841653,0.857748,0.954848,0.954848).
\]

The smallest rigorous directed lower endpoint is
`0.033388632850592175...`; therefore `Hess G >= 0.033 I` on the cube.  Along
the segment from zero to any `y` in the cube,

\[
 G(y)-G(0)=\int_0^1(1-s)y^T\operatorname{Hess}G(sy)y\,ds
 \ge 0.0165\|y\|_2^2.
\]

On the fixed section `a(y)=a(0)=1/2`, the penalty vanishes and the support
terms cancel, so `G(y)-G(0)=b(y)-b_*`.  This proves the stated result.

## Independent Taylor-remainder control

As a separate conservative check, third-order automatic differentiation of
the chart generator was combined with the submultiplicative-norm bounds

\[
 \|D^k\exp(A)[E_1,\ldots,E_k]\|
 \le e^{\|A\|}\prod_j\|E_j\|,
\]

including all chain-rule terms containing first, second, and third generator
derivatives.  On the same containing cube the resulting Frobenius bound for
the third-derivative tensor of `G` is below `3.291e14`.  The whitened point
Hessian has a rigorous lower bound above `0.9999999999999958`.  Taylor's
formula therefore independently proves nonnegativity for
`||y||_2<=9.11e-15`.  This bound is intentionally coarse; the direct uniform
Hessian enclosure proves the much larger `10^-4` result above.

## Replays and limits

The primary computation uses python-flint 0.9.0/Arb at 256 bits.  A 320-bit
replay retains the same largest tested successful radius.  An independent
complex matrix-unit implementation finite-differences the whitened point
Hessian (maximum entrywise difference from the identity
`6.60e-6`), verifies `z^dagger w` below `8.56e-22` on holdouts, and finds all
sixteen independently corrected fixed-`a` trials above `b_*`; these numerical
checks are diagnostics rather than the interval proof.

No statement is made about rank-three Kossakowski matrices, another distant
rank-two chart, global minimization of the four-parameter family, unbounded
time/rate tails, or whether this point lies on the true boundary of `Q2`.
Consequently the original boundary-coverage question remains unresolved.
