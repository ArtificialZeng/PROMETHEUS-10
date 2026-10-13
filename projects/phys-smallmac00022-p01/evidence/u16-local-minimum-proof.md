# Computer-assisted local-minimum theorem at `r=1/2`

## Statement and scope

Let

\[
 \rho_{1/2}=\frac{|00\rangle\!\langle00|+4|01\rangle\!\langle01|
 +4|10\rangle\!\langle10|+4|11\rangle\!\langle11|}{13}
\]

and use base-2 von Neumann entropy.  In the minimal ancillary split
`(d_A',d_B')=(4,4)`, write every orthonormal-flag purification of two
copies as

\[
 |\Psi_W\rangle=\sum_{I,J}\sqrt{P_{IJ}},|I\rangle_A|J\rangle_B
 W|IJ\rangle_{A'B'},\qquad W\in U(16),
\]

and set `F(W)=S(Tr_BB' |Psi_W><Psi_W|)`.  Let `W_0=I_16`, the product
canonical purification, and let

\[
 \mathcal G=\{U_{A'}\otimes V_{B'}:U,V\in U(4)\}
\]

act on flags from the left.

**Theorem.**  There is a neighborhood of the orbit `G W_0` in `U(16)`
on which

\[
 F(W)\geq F(W_0)
 =2h_2\!\left(\frac{13+3\sqrt{17}}{26}\right),
\]

with equality only on that orbit after the neighborhood is made smaller
if necessary.  Thus `W_0` is a strict local minimum modulo local ancillary
unitaries among **all complex minimal-split orthonormal flags**, including
directions that open new Schmidt support.

This is dimension-specific.  It proves neither global optimality in `U(16)`,
nor local or global optimality after ancillary enlargement, nor
`E_P(rho_{1/2}^{tensor 2})=2E_P(rho_{1/2})`.

## 1. Coefficient map, support, and tangent split

Across `AA':BB'`, define

\[
 M(W)_{(I,a),(J,b)}=C_{IJ}W_{(a,b),(I,J)},\qquad
 C=C_1\otimes C_1,quad
 C_1=\frac1{\sqrt{13}}\begin{pmatrix}1&2\\2&2\end{pmatrix}.
\]

Then `F(W)=S(M(W)M(W)^*)`.  At `W_0`, only the four rows `(I,I)`
and four columns `(J,J)` are active, and the active block is the invertible
matrix `C`.  Its four positive squared singular values are

\[
 b^2,\ ab,\ ab,\ a^2,\qquad
 a=\frac{13+3\sqrt{17}}{26},\quad
 b=\frac{13-3\sqrt{17}}{26}.
\]

For an anti-Hermitian unit tangent `K`, put `W(t)=exp(tK)`.  The
normal-normal block of `M'(0)` is

\[
 N(K)_{(I,a),(J,b)}=C_{IJ}K_{(a,b),(I,J)},
 \quad a\ne I,\ b\ne J.
\]

As derived in `evidence/u16-tangent-derivation.md`, its kernel consists of
16 imaginary diagonal generators and the real and imaginary generators on
the 48 unordered grid edges that share one coordinate.  Hence

\[
 \dim_{\mathbb R}\ker N=112,
 \qquad \dim_{\mathbb R}(\ker N)^\perp=144.
\]

The tangent to the local-ancilla orbit is
`X tensor I_4 + I_4 tensor Y`.  It has dimension 31 because the map from
`u(4) direct-sum u(4)` has the one-dimensional kernel
`(ic I_4,-ic I_4)`.  It lies in `ker N`.  An exact orthonormal complement
of this orbit inside `ker N` has dimension 81:

- 9 double-centered phase tables `h_p h_q^T`;
- 36 same-`I` rook-edge contrasts;
- 36 same-`J` rook-edge contrasts.

Here the three Helmert vectors

\[
 (1,-1,0,0)/\sqrt2,\quad
 (1,1,-2,0)/\sqrt6,\quad
 (1,1,1,-3)/\sqrt{12}
\]

form an orthonormal basis of the subspace perpendicular to `(1,1,1,1)`.
The certificate constructs these 81 generators directly and encloses their
Gram matrix around the identity.

The 144 normalized opening generators have mutually orthogonal images under
`N`.  For the unordered both-coordinate edge with endpoints `x=(I,J)` and
`y=(a,b)`, either real generator has squared image norm

\[
 \frac{C_{IJ}^2+C_{ab}^2}{2}.
\]

The least value is exactly `5/338`.  Therefore `N` is injective on the
144-dimensional opening complement, with a quantitative gap.  This fact is
certified from exact radicals in `evidence/certify_u16_hessian.py`.

## 2. Analytic entropy Hessian

Let `L` denote the linear map `W -> M(W)`.  Along `exp(tK)`,

\[
 M_1=L(K),\quad M_2=L(K^2),
\]

and, for `rho(t)=M(t)M(t)^*`,

\[
 \rho_1=M_1M_0^*+M_0M_1^*,\qquad
 \rho_2=M_2M_0^*+M_0M_2^*+2M_1M_1^*.
\]

Let `P` project onto the four-dimensional positive support of `rho_0`,
`Q=I-P`, and let the columns of `U` be the exact tensor-product eigenbasis
with eigenvalues `lambda_a` listed above.  Define

\[
 X=U^*P\rho_1PU,\qquad Z=U^*P\rho_2PU,\qquad
 Y=Q\rho_1PU.
\]

For `f(x)=-x log_2 x`, let

\[
 f'^{[1]}(x,y)=
 \begin{cases}
 (f'(x)-f'(y))/(x-y),&x\ne y,\\
 f''(x),&x=y.
 \end{cases}
\]

Second-order Hermitian eigenvalue perturbation, with the degenerate `ab`
eigenspace handled by the divided difference, gives the analytic quadratic
form

\[
 q(K)=\sum_a f'(\lambda_a)Z_{aa}
 +\sum_{a,b} f'^{[1]}(\lambda_a,\lambda_b)|X_{ab}|^2
 +2\sum_a\frac{f'(\lambda_a)}{\lambda_a}\|Y_{:a}\|_2^2. \tag{1}
\]

The last term is essential: it accounts for motion of a positive
eigenvector into the zero eigenspace.  For `K in ker N`, the small singular
values of `M(exp(tK))` are `O(t^2)`, so their squared weights are `O(t^4)`
and their entropy is `O(-t^4 log |t|)`.  It has zero second derivative.
Consequently (1) is also the Hessian of the full entropy on `ker N`.

Directional stationarity in all 256 real tangent directions was proved in
`evidence/u16-tangent-derivation.md`: diagonal phase variations pair a purely
imaginary antisymmetric `rho_1` with a real symmetric `log rho_0`, while all
other elementary directions have no active-active first variation.  Hence at
this point the Hessian obtained from exponential curves is the intrinsic
Hessian, independent of the chosen connection or local chart.

## 3. Outward-rounded positivity certificate

`evidence/certify_u16_hessian.py` evaluates (1), and its polarization, on the
exact 81-vector quotient basis using 320-bit Arb ball arithmetic.  No finite
difference or floating-point error estimate enters the certificate.  The
largest radius of any Hessian entry is below `1.64e-93`.

The script applies a no-pivot interval `LDL^T` factorization to

\[
 H-\frac{159}{1000}I_{81}.
\]

All 81 interval pivots are strictly positive; the smallest recorded lower
pivot endpoint is greater than `0.0290093`.  Sylvester's criterion therefore
gives the rigorous bound

\[
 \boxed{\lambda_{\min}(H)>0.159\ \text{bits per squared unit tangent}.} \tag{2}
\]

The binary64 midpoint eigenvalue `0.159148973002032` is reported only as a
diagnostic.  The proof is (2), not agreement with that midpoint or with the
earlier Richardson calculation.  The full command output is preserved in
`evidence/u16-hessian-certificate.log`.

## 4. Uniform treatment of mixed support-opening directions

It remains to explain why (2) is enough even when a direction approaches
`ker N` while opening Schmidt support.  This step is analytic and does not
replace a logarithmic boundary term by an ordinary Hessian.

Use the active row and column decompositions to write, near `W_0`,

\[
 M(W)=\begin{pmatrix}A&B\\E&D\end{pmatrix},\qquad A(W_0)=C,
\]

and define the Schur complement

\[
 Z(W)=D-EA^{-1}B.
\]

It is analytic near `W_0` and `dZ_{W_0}=N`.  Moreover

\[
 M=
 \begin{pmatrix}I&0\\EA^{-1}&I\end{pmatrix}
 \begin{pmatrix}A&0\\0&Z\end{pmatrix}
 \begin{pmatrix}I&A^{-1}B\\0&I\end{pmatrix}. \tag{3}
\]

The outer matrices and their inverses are uniformly bounded in a sufficiently
small neighborhood.  By the Eckart--Young characterization of the distance
to rank at most four, (3) implies that the total small-eigenvalue weight

\[
 \tau(W)=\sum_{j=5}^{16}s_j(M(W))^2
\]

satisfies `tau(W) >= c ||Z(W)||_F^2` there for some `c>0`.

Take the orthogonal projection `Pi` onto the 144-real-dimensional image of
`N`, and put `z=Pi Z(W)`.  On a local slice perpendicular to the 31 gauge
directions, the derivative of the map from the 144 opening coordinates to
`z` is invertible (its least squared scale at the origin is `5/338`).  The
inverse-function theorem therefore supplies local analytic coordinates
`(k,z)`, where `k` is the 81-dimensional quotient-kernel coordinate.  Since
`||Z||_F >= ||z||`, after reducing the neighborhood,

\[
 \tau(k,z)\ge c\|z\|^2. \tag{4}
\]

Let `G(k,z)` be the entropy contribution of the four eigenvalues separated
from zero.  The positive spectral gap at `W_0` makes `G` analytic, including
through the double eigenvalue `ab`.  Stationarity and (2), followed by an
ordinary Taylor bound on the remaining Hessian blocks, give constants
`A,B>0` such that

\[
 G(k,z)-G(0,0)\ge A\|k\|^2-B\|k\|\|z\|-B\|z\|^2. \tag{5}
\]

For sufficiently small `tau`, the entropy `T` of the other twelve weights
obeys

\[
 T\ge-\tau\log_2\tau
 \ge-c\|z\|^2\log_2(c\|z\|^2), \tag{6}
\]

because `-x log x` is increasing near zero and (4) holds (decrease `c` if
needed).  Young's inequality absorbs the mixed term in (5) into half of the
positive `A ||k||^2` term plus a constant times `||z||^2`.  The logarithm in
(6) then dominates every remaining bounded multiple of `||z||^2`, uniformly
as `(k,z)->(0,0)`.  Thus

\[
 F(k,z)-F(0,0)>0
\]

for every sufficiently small nonzero slice coordinate.  Compact-group slice
coordinates for the local-ancilla action transfer this conclusion to a
neighborhood of the full orbit and prove the theorem.

## 5. Independent consistency checks and limitations

- The earlier finite-difference quotient minimum was
  `0.159148970--0.159148977`; it was not used as an error bound.
- The independent 100-decimal direct partial trace along the weakest phase
  mode converged to the same curvature and found positive finite entropy
  differences; it was not used to certify all 81 directions.
- The exact opening-map scale and the `-t^2 log_2(t^2)` behavior agree with
  the separate Givens-path calculation.
- The proof establishes an existential neighborhood, not a practical radius.
  It says nothing about distant purifications, larger ancillary splits, or
  the global additivity conjecture.
