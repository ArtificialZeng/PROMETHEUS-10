# Fixed-interval correction and gap bound

Use the same finite open all-cycle-`+1` matrix and `A_k=2h_k`.  Let
`F_k(x,J)=A_(k-1)^sc(z=-ix,J)` be the boundary-symmetric factor.  The proved
flat-locus identity is `F_k(J,J)=1-3^(k-3)J^2`, and the complete remainder
proves this is its only nonzero meeting with the positive flat branch.

Write `F_k=sum c_(p,q)J^p x^q` and set
`M_k=sum_(q>=1) q|c_(p,q)|2^p 4^(q-1)`.  Row sums give every eigenvalue
`|x|<=4` for `|J|<=2`, hence `|partial_x F_k|<=M_k`.  The mean-value theorem
therefore gives the source-lambda gap bound
`Delta_k^+/- >= d_k/(2M_k)` on `I_+=[1/4,1/2]`, `I_-=-I_+`, where
`d_3=3/4`, `d_4=1/4`, and `d_k=3^(k-3)/16-1` for every `k>=6`.  These are
strictly positive.  At `k=5`, `J_5=1/3` lies in the interval and
`Delta_5^+/-=0`.  Thus the fixed-window minimum is zero iff `k=5`.

For the separate moving windows `W_k^+=[J_k/2,3J_k/2]` and its negative
mirror, the unique crossing lies inside and the minimum is zero for all
`k>=3`.  This corrects the old unqualified sentence without changing the
all-depth crossing theorem.
