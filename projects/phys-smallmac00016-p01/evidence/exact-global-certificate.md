# Exact global certificate for the two-step current-bit optimum

## Theorem

For the fixed GAD instrument with
\(p=18/25\), \(q=7/25\), \(\gamma=3/10\), and disclosed
pairing `03|12`, allowing four arbitrary clock-dependent qubit CPTP recovery
maps conditioned only on the current bit,

\[
\boxed{F_2^M=\frac{289}{400}}.
\]

It is attained by
\(\mathcal R_{k,b}=\operatorname{id}\) for both clocks and both bits.

## One-clock branch matrices

Put

\[
r=1-\gamma=\frac7{10},\quad c=\frac\gamma2=\frac3{20},
\quad d_0=p\sqrt r,\quad d_1=q\sqrt r,
\]
\[
z_0=p-c=\frac{57}{100},\qquad z_1=q-c=\frac{13}{100},
\quad D_b=\operatorname{diag}(d_b,d_b,z_b).
\]

For a traceless Hermitian input \(x\cdot\sigma\), the two instrument
branches have scalar/Bloch pairs

\[
\mathcal I_0(x\cdot\sigma): (c x_z,D_0x),\qquad
\mathcal I_1(x\cdot\sigma): (-c x_z,D_1x).
\]

After arbitrary CPTP recoveries, write the corresponding output Bloch vectors
as \(B_0x\) and \(B_1x\). The attainable one-clock block is
\(T=B_0+B_1\).

For a Hermitian qubit operator \(aI+v\cdot\sigma\),
\(\lVert aI+v\cdot\sigma\rVert_1=2\max(|a|,\lVert v\rVert)\).
Trace-norm contractivity and trace preservation therefore imply

\[
\lVert B_0x\rVert\leq\lVert D_0x\rVert,
\tag{1}
\]

because both diagonal entries of \(D_0\) exceed \(c\), and

\[
\lVert B_1x\rVert^2\leq
\max\{d_1^2(x_x^2+x_y^2)+z_1^2x_z^2,\ c^2x_z^2\}.
\tag{2}
\]

Equation (1) is the Loewner inequality
\(B_0^TB_0\preceq D_0^2\). Hence \(B_0=C D_0\) for a real contraction
\(C\).

## Sharp bit-1 Gram bounds

Let \(G=B_1^TB_1\). Average \(G\) over rotations about the input \(z\)-axis.
The right side of (2) is invariant under these rotations, so the averaged
matrix \(\bar G=\operatorname{diag}(a,a,b)\) remains feasible and preserves
\(\operatorname{Tr}G\). The two linear pieces in (2) cross at

\[
t_0=\frac{d_1^2}{d_1^2+c^2-z_1^2}=\frac{49}{54}.
\]

Testing the endpoints and this crossing (each piece is linear in
\(t=x_z^2\)) gives

\[
0\leq a\leq d_1^2,\quad 0\leq b\leq c^2,
\quad 5a+49b\leq49c^2.\tag{3}
\]

The exact identity

\[
5d_1^2+49z_1^2=49c^2\tag{4}
\]

then shows, because \(2-5/49>0\),

\[
\lVert B_1\rVert_F^2=\operatorname{Tr}G=2a+b
\leq2d_1^2+z_1^2.\tag{5}
\]

For the cross term, use

\[
\lVert B_1D_0\rVert_*
=\operatorname{Tr}\sqrt{D_0GD_0}.
\]

The trace of the matrix square root is concave. Since \(D_0\) commutes with
the axial rotations, Jensen's inequality bounds this expression by its value
on \(\bar G\):

\[
\lVert B_1D_0\rVert_*
\leq2d_0\sqrt a+z_0\sqrt b.
\]

The right side is increasing in \(b\), so (3) reduces its maximization to

\[
f(a)=2d_0\sqrt a+z_0\sqrt{c^2-5a/49},
\qquad0\leq a\leq d_1^2.
\]

Its derivative is decreasing on this interval and at the right endpoint is

\[
f'(d_1^2)=\frac{d_0}{d_1}-\frac{5z_0}{98z_1}
=\frac{18}{7}-\frac{285}{1274}>0.
\]

Thus the maximum is the endpoint fixed by (4), and

\[
\lVert B_1D_0\rVert_*\leq2d_0d_1+z_0z_1.\tag{6}
\]

## Global one-clock and two-clock bounds

The contraction/nuclear-norm duality, (5), and (6) give

\[
\begin{aligned}
\lVert T\rVert_F^2
&=\lVert CD_0+B_1\rVert_F^2\\
&\leq\lVert D_0\rVert_F^2+\lVert B_1\rVert_F^2
  +2\lVert B_1D_0\rVert_*\\
&\leq2(d_0+d_1)^2+(z_0+z_1)^2\\
&=2r+r^2=\frac{189}{100}.
\end{aligned}
\]

For the two independent clocks,

\[
\operatorname{Tr}(T_2T_1)
\leq\lVert T_2\rVert_F\lVert T_1\rVert_F
\leq\frac{189}{100}.
\]

Identity recovery at all four positions gives
\(T_1=T_2=\operatorname{diag}(\sqrt r,\sqrt r,r)\), attaining this value.
Therefore

\[
F_2^M=\frac{1+189/100}{4}=\frac{289}{400}.
\]

The fixed history witness consequently exceeds the exact current-bit optimum by

\[
\frac{1831}{2500}-\frac{289}{400}=\frac{99}{10000}.
\]

This is the advantage of that fixed history witness, not a proof of the full
Bayesian optimum.
