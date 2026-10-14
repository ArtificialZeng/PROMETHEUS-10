# Cauchy every-jump sufficiency: computer-assisted proposer proof

Job phys-00004-p06-research-3b82157ed896, 2026-10-12. This is a stable
scientific argument. It does not depend on checkpoint.md or state.json.
No independent referee acceptance is asserted.

## Model and statement

Use precisely the update, units, absorption event and unbounded spatial domain
in problem.md and physics.json: unit-scale iid Cauchy jumps, reset to zero
immediately before the jump in the same step, absorbing on landing above b.
Q_n(b) is reset-free PATH survival through n jumps. There is no reflected
left wall and no finite-variance premise. Time is in jumps, length in Cauchy
scale units. At finite b>=0 and 0<r<=1 all reset passage means are finite.

**Submitted statement.** For every finite b>=0, if Q_2(b)>=Q_1(b)^2, then
T_b(r)>T_b(1)=1/[1-F(b)] for every 0<r<1. Equality occurs at r=1.
In particular the original non-strict global sufficiency statement is proved
by the argument below, subject to fresh scientific audit of this packet.
No monotonicity in r, uniqueness of a barrier threshold, general stable-index
result, continuum resetting result or experimental observation is claimed.

The primary renewal/backward convention map and baseline are in
evidence/reproduction-derivation.md, evidence/input-a.json and
evidence/input-b.json, with the primary PDF in source-ledger.json.

## 1. A finite-to-infinite survival comparison

Write q=F(b), z=1-r. The reproduced formula gives
T_b(r)=zG_b(z)/[1-rG_b(z)]. Its denominator is positive for 0<r<1:
the reset-before-jump killed transition has row mass <=1-r(1-q)<1;
the reproduced scalar resolvent is the finite positive passage-time solution.
Direct subtraction shows the sign of T_b(r)-1/(1-q) is the sign of
H_b(z)=(1-zq)G_b(z)-1.

It therefore suffices to prove Q_n(b)>=q^n for all n, with strict inequality
for at least one n. The coefficient comparison yields
G_b(z)>sum_{n>=0}(zq)^n=1/(1-zq) for every 0<z<1.
All series converge absolutely since 0<=Q_n<=1. This step covers reset
rates arbitrarily near both endpoints without a finite z grid or an
uncontrolled generating-function tail.

For 0<=b<=1809/1000, exact scalar CDF intervals give q<21/25.
Q_0=1 and Q_1=q are identities, while Q_2>=q^2 is the hypothesis.
For n>=10, barrier inclusion and the symmetric continuous zero-barrier
baseline give Q_n(b)>=a_n=binomial(2n,n)/4^n.
Exactly a_10=46189/262144>(21/25)^10, and
a_(n+1)/a_n=(2n+1)/(2n+2)>=21/22>21/25 for n>=10.
Induction proves Q_n(b)>(21/25)^n>q^n at every n>=10.
The only remaining finite orders are 3<=n<=9.

## 2. Killed-kernel lower enclosure at finite orders

For fixed b define u_n(x)=P_x(S_j<=b, 1<=j<=n), x<=b, with u_0=1.
First-step conditioning gives u_(n+1)(x)=integral_{-infinity}^b
f(y-x)u_n(y)dy. Coupling identical increments proves u_n(x) decreases
as x increases. It also proves Q_n(b)=u_n(0) increases with b.

Choose exact rational endpoints -L=x_0<...<x_m=b including zero.
At endpoint x_j, the cell (x_(k-1),x_k] has exact mass
M_jk=F(x_k-x_j)-F(x_(k-1)-x_j). If L_nk<=u_n(x_k), then
sum_k M_jk L_nk<=u_(n+1)(x_j). The omitted y<-L integral is
nonnegative; discarding it is a valid lower enclosure, not a reflecting
boundary and not an assumption that its mass is uniformly small.

Start with the exact one-step values u_1(x_j)=F(b-x_j). Enclose every
CDF with outward intervals, take nonnegative lower kernel masses, and
round the positive recurrence sums downward. A truncated approximation
need not itself be monotone. Replace its node values by their suffix
maximum: max_{k>=j} L_nk still bounds u_n(x_j), since the true u_n is
decreasing. The next cell enclosure is consequently valid by induction.

evidence/finite_survival.py implements this in exact integer arithmetic,
using the scalar library evidence/interval_survival.py at scale 10^30.
The scalar library encloses pi by Machin's identity, reduces rational atan
arguments to absolute value <=1/2, and encloses its 60-term alternating
series by the next-term remainder. Multiplication/division round outward;
no transcendental libm calls enter the certificate. Its original consistency
checks are evidence/interval-survival-check.py and its actual log.

The exploratory first replay at b=1.808, grid spacing 1/16 and L=64, proves
Q_n(1.808)>(21/25)^n for 3<=n<=9. Its exact values are in
evidence/finite-survival-result.json and actual log evidence/finite-survival.log.
A failed initial monotonicity assertion was corrected by the justified suffix
maximum above; no failed assertion is being interpreted as physical evidence.

The final evidence/barrier_cover.py uses spacing 1/32 centrally, geometric
negative-tail cells and L=128, and recursively subdivides the barrier range.
For each closed barrier cell [l,u] it proves
Q_n(b)>=Q_n(l)>=lower_n(l)>F(u)^n>=F(b)^n, 3<=n<=9.
The ten closed cells join exactly and cover [0,1809/1000]; the smallest
strict rational margin exceeds 0.0004785884. The exact endpoints, bounds
and margins, rather than the displayed decimal, are authoritative in
evidence/barrier-cover-result.json and evidence/barrier-cover.log.

This is a uniform barrier proof by event monotonicity. Finite samples alone
are not being used as a continuous-parameter theorem. Together with section 1
it proves the full all-rate implication whenever b<=1809/1000.

## 3. Excluding the antecedent at every larger barrier

Let c_2(b)=Q_2(b)-F(b)^2. The existing Simpson enclosure in
evidence/interval-survival-result.json proves c_2(1809/1000)<-0.0000069474.
Its transformed integral, fourth-derivative bound and explicit error control
are fully derived in evidence/research-derivation.md; original code and logs
are retained. We now prove c_2(b)<0 for all b>=1809/1000 without assuming
uniqueness of its zero elsewhere.

For b in [1809/1000,2], differentiating the exact integral gives
Q_2'(b)=f(b)/2+J(b), J(b)=integral_{-infinity}^b f(x)f(b-x)dx.
Differentiation is valid by integrable Cauchy bounds on this compact b range.
The full convolution is 2/[pi(b^2+4)], because the sum of two unit Cauchy
variables is Cauchy of scale two (characteristic functions exp(-|k|) multiply).
On the removed tail x in [b,b+1], f(x)>=f(b+1) and
integral_b^(b+1) f(b-x)dx=1/4. Therefore

c_2'(b)<=2/[pi(b^2+4)]-1/[4pi(1+(b+1)^2)]
             -(2F(b)-1/2)/[pi(1+b^2)].

For each rational cell [l,u] of width 1/1000, the first positive term is
bounded at l, both subtracted inverse quadratics at u, and 2F(b)-1/2
from below at l. Outward intervals prove all 191 such upper derivative
bounds strictly negative. Thus c_2 stays negative through b=2.

For 2<=b<=7 use the distinct representation
Q_2(b)=F(b/2)-A(b), A(b)=integral_0^infinity f(b+t)F(-t)dt.
It subtracts paths with S_1>b but S_2<=b from the marginal event S_2<=b.
For each exact t-cell [v,w], its contribution to A is at least
[F(b+w)-F(b+v)]F(-w), since F(-t) decreases. Sum lower interval
contributions with grid spacing 1/64 to t=16 and geometric cells to1024;
discard the nonnegative t>1024 tail. This gives an upper bound on Q_2.
On a barrier cell [l,u], monotonicity yields
c_2(b)<=Q_2(u)-F(l)^2. Recursive subdivision certifies 42 closed cells
joining exactly to cover [2,7]. Every upper bound is strictly negative,
with the largest upper bound less than -0.0001724763.

For b>=7, put x=1/b<=1/7, t=atan(x), v=atan(2x). Path inclusion gives
Q_2(b)<=F(b/2), so c_2(b)<0 follows if F(b/2)-F(b)^2<0.
For this range, 2t-v=atan[2x^3/(1+3x^2)]<=2x^3 and
t>=x/(1+x^2). Hence
F(b/2)-F(b)^2=(2t-v)/pi-t^2/pi^2
 <=2x^3/pi-x^2/[pi^2(1+x^2)^2]<0
provided 2pi*x*(1+x^2)^2<1. The left side increases with x>=0;
its interval upper bound at x=1/7 is strictly below one, saved exactly
in evidence/antecedent-exclusion-result.json. This is an analytic
infinite-barrier tail proof, not a finite large-b scan.

All three pieces are executable in evidence/antecedent_exclusion.py.
Actual results, derivative and barrier cells, and log are
evidence/antecedent-exclusion-result.json and evidence/antecedent-exclusion.log.

## 4. Conclusion and physical consequence

Any barrier satisfying the antecedent must lie below 1.809 by section 3.
Sections 1 and 2 then give coefficientwise survival dominance, a strictly
positive H_b(z), and strict T_b(r)>T_b(1) at every interior reset rate.
This proves the exact frozen original implication across its complete b,r
domain, including the equality antecedent. No equality-root isolation or
barrier uniqueness theorem is needed. The check treats the Cauchy flight's
long tail and arbitrarily small reset rates without finite-moment assumptions.

Physically, in this model the two-jump endpoint test suffices to select
reset-before-every-jump as the unique optimum among constant Bernoulli reset
protocols when Q2>=Q1^2; an interior-rate search cannot outperform it.
This is the alpha=1 restriction of the source's conjectured stable-family
region-II behavior, not a proof for every Levy index or other timing rules.

The alternative same-proposer replay in evidence/independent_survival_check.py
uses distance to barrier, a separately implemented exact-rational atan series,
scale 10^24, spacing 1/40 to16, geometric cells to256 and prefix maxima.
It reconstructs finite survival bounds using only the first cover's barrier
endpoints, never its cached numerical answers. Its outputs and limitations
are in evidence/independent-survival-check-result.json and its actual log.
This supplies a distinct computational representation but does not replace
the required fresh referee reconstruction, correctness, novelty and physics
audit. Priority and journal-version comparison limitations are explicit in
evidence/pass2-literature-check.md. No manuscript or acceptance is generated.

An additional alternative replay, evidence/independent_exclusion_check.py,
uses that separate scalar library to reconstruct the initial Q2 sign with
N=16384 and an independently written derivative recurrence, then rechecks
all derivative cells, all 42 middle-barrier cells using spacing 1/96 and a
different geometric tail grid to2048, and the large-barrier sufficient bound.
Its actual PASS results and log are evidence/independent-exclusion-check-result.json
and evidence/independent-exclusion-check.log. It uses only the first
exclusion's cell boundaries, not cached Q2 answers; the analytic enclosure
arguments remain shared and must still be audited by the fresh referee.
