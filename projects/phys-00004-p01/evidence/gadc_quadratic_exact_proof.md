# Exact completion of the two-use GADC coefficient inequality

This note closes the quadratic sign obstruction left in
`gadc_positive_temperature_coefficients.md`.  Together with the prior pure
input reduction, the universal four-level spread inequality, and the
energy-ball argument, it proves the frozen two-use claim.  It does not address
arbitrary numbers of channel uses.

## 1. Notation

Retain

\[
 0\le u\le d,\qquad g=u+d\le1,\qquad q=1-g,
\]

and the pure-state variables

\[
 A,S,P\ge0,\quad A+S+P=1,\quad
 -{S\sqrt{AP}\over2}\le y\le {S\sqrt{AP}\over2}.
\]

Put

\[
 \alpha=u(1-u),\quad \beta=d(1-d),\quad
 \tau=g-2ud,\quad R=A\alpha+P\beta,
\]

\[
 X_0=R+Sud,\quad X_1=R+S(1-u)(1-d),\quad X=X_0X_1,
\]

\[
 K=SR+4APud,
 \qquad J=X_0^2+udq(S^2-4AP).
\]

The identities

\[
 (1-u)(1-d)=q+ud,qquad X=qK+J                         \tag{1}
\]

will be useful.  Although the last expression defining `J` is not manifestly
positive when `S^2<4AP`, it is nonnegative.  Indeed,
`alpha*beta=ud(q+ud)`, so

\[
 R\ge2\sqrt{APud(q+ud)}
\]

and this bound in `X_0=R+Sud` gives `J>=0` directly.

Let `D0` be Eq. (5) of `gadc_positive_temperature_coefficients.md`.  Exact
fraction-free collection gives the additional compression

\[
 \boxed{K D_0-4APudX^2=SRJ^2.}                               \tag{2}
\]

Thus, away from removable zero denominators, the worst-split determinant is
an ellipse written as a sum of two squares,

\[
 E_{4,\min}(y)={SRJ^2\over K}
 +{4udq^2K\over AP}\left(y-{APX\over qK}\right)^2.          \tag{3}
\]

Equation (2), rather than division in (3), is the polynomial identity used at
the boundary.

## 2. A multiplier identity for the whole interval

Let

\[
 T=d_e-{E_2\over2},\qquad Q=E_{4,\min}-T^2,
\]

and define the nonnegative interval quantities

\[
 G={S^2\over4}+AP-2y,qquad
 H={APS^2\over4}-y^2.                                       \tag{4}
\]

Writing `r=sqrt(AP)` and `s=S/2` shows
`G=s^2+r^2-2y>=0` and `H=s^2r^2-y^2>=0`.  Moreover,

\[
 APG-H=(AP-y)^2,                                             \tag{5}
\]

so `H<=AP G` everywhere in the physical interval.

Define

\[
 \kappa=g(g-4ud),\qquad F=g(2-g)-4udq,                       \tag{6}
\]

and the homogeneous quadratic

\[
\begin{aligned}
 \mathcal R={}&g^2\alpha^2A^2+2ud\alpha F,AS
 +2u^2d^2g^2AP+{udg^2(q+2ud)\over2}S^2\\
 &+2ud\beta F,SP+g^2\beta^2P^2.                            \tag{7}
\end{aligned}
\]

Direct exact expansion, using only `A+S+P=1`, yields

\[
\boxed{
 AP\tau Q
 =APqG\{\kappa T+\mathcal R\}
 -4Sudq^2\tau R H.}                                         \tag{8}
\]

This identity treats both signs of the invariant phase at once and does not
assume the sign of the quadratic leading coefficient.

## 3. Sign certificate

Every channel factor needed below is nonnegative.  First,
`4ud<=g^2<=g`, hence `kappa>=0`.  Also

\[
 F-2q\tau=g^2.                                                \tag{9}
\]

Consequently

\[
\begin{aligned}
 \mathcal R_0&:=\mathcal R-4Sudq\tau R\\
 &=g^2\alpha^2A^2+2ud\alpha g^2AS+2u^2d^2g^2AP\\
 &\quad+{udg^2(q+2ud)\over2}S^2
 +2ud\beta g^2SP+g^2\beta^2P^2\ge0.                        \tag{10}
\end{aligned}
\]

Using (5) in the negative term of (8) gives, whenever `T>0`,

\[
\begin{aligned}
 AP\tau Q
 &\ge APqG\{\kappa T+\mathcal R-4Sudq\tau R\}\\
 &=APqG\{\kappa T+\mathcal R_0\}\ge0.                      \tag{11}
\end{aligned}
\]

If `g>0`, then `tau=g-2ud>0`; therefore (11) proves `Q>=0` for
`AP>0`.  When `AP=0`, necessarily `y=0`, and the result follows by continuity
from the same polynomial identity (strict `T>0` persists in a sufficiently
small interior neighbourhood).  At `g=0`, `T=0`; at `q=0`, the channel is the
input-independent thermal replacement map and the coefficient inequality is
an equality.  These observations cover every closed-domain endpoint.

Where `T<=0`, the desired inequality is automatic.  Where `T>0`, (11) gives

\[
 E_{4,\min}\ge T^2,
 \qquad E_2+2\sqrt{E_{4,\min}}\ge2d_e.                       \tag{12}
\]

The determinant is nondecreasing in the discarded split variable `v`, while
`E2` is independent of it, so (12) holds for every complex pure input.

## 4. Completion of the frozen claim

For any four-level output spectrum, the exact sum-of-squares identity in
`adc_face_exact_proof.md` gives

\[
 D^2\le1-2E_2-4\sqrt{E_4}.
\]

Equation (12) and `1-r(e)^2=4d_e` therefore imply the full shell bound

\[
 D\le r(e).                                                   \tag{13}
\]

In the unsaturated one-use branch, (13) is exactly the required bound.  In
the saturated branch, concavity gives

\[
 r(e)\le r(x_*)-2q(e-x_*),
\]

which is the required tangent bound.  The prior extreme-point argument covers
all mixed inputs, monotonicity covers an input whose actual energy is below
the available budget, and equal product codes give the reverse inequality.
Hence

\[
\boxed{
 W_2^{\gamma,\eta}(e)=2W_1^{\gamma,\eta}(e)
 \quad\text{for every }\gamma\in[0,1],\ \eta\in[0,1/2],\ e\in[0,1].}
                                                                    \tag{14}
\]

This is exactly the frozen two-use, global-extraction statement.  It does not
prove the primary paper's conjecture for arbitrary `n`.  The algebra in
(1)--(12) is independently regenerated by
`verify_gadc_quadratic_proof.py`; its captured output is
`gadc-quadratic-proof-verification.log`.  A fresh scientific referee and a
bounded novelty check are still required before manuscript preparation.
