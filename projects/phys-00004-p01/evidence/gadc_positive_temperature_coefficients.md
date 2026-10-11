# Pure-output GADC coefficients and an exact phase/split reduction

This note continues the frozen two-use problem in `problem.md`.  It derives
only the two spectral coefficients needed by the sum-of-squares spread bound.
It does **not** prove the remaining positive-temperature inequality.

## 1. Variables and the exact output matrix

Write the upward and downward population-transfer probabilities as

\[
 u=\gamma\eta,\qquad d=\gamma(1-\eta),\qquad q=1-\gamma=1-u-d.
\]

Thus the physical domain is equivalently
`0 <= u <= d`, `u+d <= 1`.  For the reduced pure input use

\[
 |\psi\rangle=\sqrt A|00\rangle+\sqrt B|01\rangle
 +\sqrt C|10\rangle+e^{i\delta}\sqrt P|11\rangle,
\]

and define

\[
 S=B+C=2(e-P),\qquad v=BC,\qquad
 y=\sqrt{APv}\cos\delta .                                      \tag{1}
\]

Here `A+S+P=1`, `0<=v<=S^2/4`, and
`|y|<=sqrt(APv)`.  Direct tensoring of the printed one-cell map gives the
diagonal entries

\[
\begin{aligned}
 z_0&=(1-u)^2A+(1-u)dS+d^2P,\\
 z_1&=u(1-u)A+(1-u)(1-d)B+udC+d(1-d)P,\\
 z_2&=u(1-u)A+udB+(1-u)(1-d)C+d(1-d)P,\\
 z_3&=u^2A+u(1-d)S+(1-d)^2P,
\end{aligned}                                                    \tag{2}
\]

and upper-triangular off-diagonal entries

\[
\begin{aligned}
 \sigma_{01}&=\sqrt q\{(1-u)\sqrt{AB}+d\sqrt{CP}e^{-i\delta}\},\\
 \sigma_{02}&=\sqrt q\{(1-u)\sqrt{AC}+d\sqrt{BP}e^{-i\delta}\},\\
 \sigma_{03}&=q\sqrt{AP}e^{-i\delta},\qquad
 \sigma_{12}=q\sqrt{BC},\\
 \sigma_{13}&=\sqrt q\{u\sqrt{AC}+(1-d)\sqrt{BP}e^{-i\delta}\},\\
 \sigma_{23}&=\sqrt q\{u\sqrt{AB}+(1-d)\sqrt{CP}e^{-i\delta}\}.
\end{aligned}                                                    \tag{3}
\]

Equations (2)--(3) retain the invariant phase; no real-state assumption has
been made.

## 2. The second elementary coefficient

Put

\[
 \alpha=u(1-u),\quad \beta=d(1-d),\quad c=d-u,\quad
 \tau=u+d-2ud,\quad R_u=1-2u+2u^2.
\]

Using `E2=(1-Tr(sigma^2))/2`, exact collection of (2)--(3) yields

\[
\boxed{\begin{aligned}
 E_2={}&2\alpha(1-\alpha)-2c^2q^2P^2+4ucq^2PS
       +2cqR_uP\\
     &+(u+d)qR_uS^2-2uqR_uS-4q\tau y .
\end{aligned}}                                                   \tag{4}
\]

In particular, `E2` is independent of the population-split invariant `v`
once `S` and `y` are fixed.  At `u=0`, (4) reduces exactly to the ADC
coefficient `gamma(1-gamma) F` in
`adc_face_exact_proof.md`.

## 3. The determinant without a quartic expansion

It is useful first to define `D0`, the determinant at `v=y=0`.  This can be
evaluated by choosing `B=S,C=0`.  In addition to `z0,z3` from (2), put

\[
\begin{aligned}
 z_1^{(0)}&=u(1-u)A+(1-u)(1-d)S+d(1-d)P,\\
 z_2^{(0)}&=u(1-u)A+udS+d(1-d)P,
\end{aligned}
\]

and

\[
\begin{array}{lll}
 a_{01}=\sqrt{qAS}(1-u),&a_{02}=\sqrt{qSP}\,d,
 &a_{03}=q\sqrt{AP},\\
 a_{13}=\sqrt{qSP}(1-d),&a_{23}=\sqrt{qAS}\,u.&
\end{array}
\]

Fraction-free expansion of the structured determinant gives

\[
\begin{aligned}
 D_0={}&z_0z_1^{(0)}z_2^{(0)}z_3
 -a_{01}^2z_2^{(0)}z_3-a_{02}^2z_1^{(0)}z_3
 -a_{03}^2z_1^{(0)}z_2^{(0)}\\
 &-a_{13}^2z_0z_2^{(0)}-a_{23}^2z_0z_1^{(0)}
 +a_{01}^2a_{23}^2+a_{02}^2a_{13}^2-2a_{01}a_{02}a_{13}a_{23}\\
 &+2a_{01}a_{03}a_{13}z_2^{(0)}
 +2a_{02}a_{03}a_{23}z_1^{(0)} .
\end{aligned}                                                    \tag{5}
\]

Although (5) contains square roots, every displayed product is polynomial in
`A,S,P,u,d,q`.  Define the nonnegative quantities

\[
\begin{aligned}
 K&=AS\alpha+SP\beta+4APud,\\
 X_0&=A\alpha+Sud+P\beta,\\
 X_1&=A\alpha+S(1-u)(1-d)+P\beta .
\end{aligned}                                                    \tag{6}
\]

The fourth elementary coefficient is the compact affine expression

\[
\boxed{E_4=\det\sigma
 =D_0+4udq^2K\,v-8udqX_0X_1\,y,\qquad
 \sqrt{E_4}=\sqrt{D_0+4udq^2K v-8udqX_0X_1y}.}                  \tag{7}
\]

The executable check derives (7) from the full phase-dependent matrix by
fraction-free symbolic elimination; it is not a fit to numerical data.

## 4. One coefficient inequality covers both optimizer branches

For a pure one-qubit input of excitation `e`, its GADC output determinant is

\[
 d_e=\alpha-2uqe+(u+d)qe^2.                                    \tag{8}
\]

The one-use gap in `problem.md` obeys the exact identity

\[
 1-r(e)^2=4d_e.                                                  \tag{9}
\]

Consequently the four-level spread inequality from the ADC pass would prove
the shell bound `D<=r(e)` if

\[
 \boxed{E_2+2\sqrt{E_4}\ge 2d_e.}                              \tag{10}
\]

In the unsaturated one-use branch, (10) is exactly half of the requested
coefficient inequality.  In the saturated branch, concavity of `r` and the
stationarity relation `r'(x_*)=-2q` give

\[
 r(e)\le r(x_*)-2q(e-x_*),
\]

so (10) is stronger than the requested tangent-branch inequality.  Thus no
separate positive-temperature algebra is needed for the two optimizer
branches once (10) is proved.

## 5. Exact reduction of the remaining state variables

The coefficient of `v` in (7) is `4udq^2K>=0`, while (4) is independent of
`v`.  At fixed `A,S,P,y`, physical admissibility gives

\[
 {y^2\over AP}\le v\le {S^2\over4}                             \tag{11}
\]

when `AP>0` (with the continuous endpoint convention otherwise).  Therefore
the left side of (10) is minimized exactly at

\[
 v={y^2\over AP}.                                                \tag{12}
\]

This boundary is realized by `delta=0` or `pi` and an appropriate split of
`B,C`; it is an optimization consequence, not an assumption that all spectra
are phase independent.  The full phase/split sector is hence reduced to

\[
 -{S\sqrt{AP}\over2}\le y\le {S\sqrt{AP}\over2},               \tag{13}
\]

with

\[
 E_{4,\min}(y)=D_0+{4udq^2K\over AP}y^2-8udqX_0X_1y.            \tag{14}
\]

Finally set `T(y)=d_e-E2(y)/2`.  Where `T<=0`, (10) is automatic.  Where
`T>0`, (10) is exactly equivalent to the polynomial inequality

\[
 E_{4,\min}(y)-T(y)^2\ge0.                                     \tag{15}
\]

Both terms in (15) are quadratic in `y`.  This is the remaining analytic
obstruction after the coefficient pass.

## 6. Verification and scope

`verify_gadc_coefficients.py` checks (4) and (7) symbolically, including the
full Laurent phase dependence, then compares 2,048 deterministic random
states against both the Kraus and Liouville implementations.  A 262,144-point
Sobol attack found no negative shell or branch margin.  The scan also tested
the worst `v` in (12) and found no negative value of (15) when `T>0`.
These finite tests are diagnostics only and do not prove (10).

The exact new result of this pass is the coefficient formula plus the
monotonicity reduction (11)--(15).  The full frozen claim remains unresolved.
