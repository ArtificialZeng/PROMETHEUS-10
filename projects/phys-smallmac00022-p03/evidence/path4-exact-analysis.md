# Exact continuum result for the smallest non-star tree

Let (P_4) be the four-vertex path and put (t=s^2).  This note uses
(K_s=-H_s), so the lowest two energies of (H_s) are obtained from the
two largest eigenvalues of (K_s).  The direct parity-block construction in
`certify_small_trees.py` gives

\[
 \chi_e(x)=x^3(x-1-t)Q_t(x),
\]

where

\[
\begin{aligned}
Q_t(x)={}&x^4-5(1+t)x^3+(7+18t+7t^2)x^2\\
&-3(1+t)(1+4t+t^2)x+2t(1+4t+t^2),
\end{aligned}
\]

and

\[
 \chi_o(x)=x^2(x-1-t)^2
 [x^2-2(1+t)x+2t]^2.
\]

These are identities in (mathbb{Q}[t,x]), not fitted formulas.  The odd
sector's largest eigenvalue is therefore

\[
 b(t)=1+t+r,qquad r=\sqrt{1+t^2}.
\]

All roots of (Q_t) are real because (Q_t) is a factor of the
characteristic polynomial of a real symmetric invariant block.  At (t=0),
(Q_0=x(x-1)^2(x-3)), so exactly one root of (Q_0) is above (b(0)=2).
Exact reduction modulo (r^2=1+t^2) gives

\[
 Q_t(b(t))=-(1-t)^2(1+t)b(t)<0
 quad (0<t<1).
\]

No root can cross the continuous threshold (b(t)) on this interval.
Continuity of the eigenvalues thus shows that exactly one root of (Q_t) is
above (b(t)).  The remaining even-sector roots (0) and (1+t) are also
below (b(t)).  Hence the second-largest even eigenvalue is strictly below
the largest odd eigenvalue: for (P_4), the first excitation is odd throughout
(0<t<1).

Now evaluate (Q_t) at the target-shifted odd root:

\[
\begin{aligned}
Q_t(b(t)+1-t)
 &=Q_t(2+r)\\
 &=-8t(1-t)\big[(1-t)r+t^2-t+1\big]<0.
\end{aligned}
\]

Since (Q_t) is monic, it has a root larger than (b(t)+1-t).  Its largest
root is the largest even eigenvalue (mu_1^e), and consequently

\[
 \Delta(P_4,s)=\mu_1^e-b(t)>1-t=1-s^2
 \qquad (0<s<1).
\]

At (s=0), the separately reproduced endpoint value is
(Delta(P_4,0)=1).  Thus the smallest non-star tree is a strict case away
from the endpoint and an equality case only at the excluded equality-
classification endpoint.  This result does not prove the corresponding
statement for larger trees.

The symbolic identities and radical reductions are machine-checked in
`evidence/small-tree-certificates.json`; the exact rational specializations
are separately root-isolated there.
