#!/usr/bin/env python3
"""Exclude the two-step antecedent for every b>=1.809."""
from interval_survival import I,F,PI,S,R,ONE
from pathlib import Path
import json,time

def q2upper(b):
 # P(S2<=b)=F(b/2). Remove paths which first crossed b then came back.
 ts=[R(i,64) for i in range(1025)]
 t=R(16)
 while t<1024:t=min(R(1024),t*R(9,8));ts.append(t)
 cdfs=[F((b+t).numerator,(b+t).denominator) for t in ts]
 lower=I(0)
 for j in range(1,len(ts)):
  mass=cdfs[j]-cdfs[j-1]
  assert mass.l>=0
  lower=lower+mass*F(-ts[j].numerator,ts[j].denominator)
 # Ignore the positive t>1024 contribution for lower A, hence upper Q2.
 return (F(b.numerator,2*b.denominator)-lower).u

def derivative_bound(l,u):
 # J = (f*f)(b) - integral_b^infty f(x)f(b-x)dx.
 # The removed part on x in [b,b+1] is >=f(b+1)/4.
 # Bound every factor outward uniformly on [l,u].
 two=I.rat(2)/(PI*I.rat((l*l+4).numerator,(l*l+4).denominator))
 tail=ONE/(PI*I.rat((4*(1+(u+1)**2)).numerator,(4*(1+(u+1)**2)).denominator))
 c=F(l.numerator,l.denominator)*I.rat(2)-I.rat(1,2)
 term=c/(PI*I.rat((1+u*u).numerator,(1+u*u).denominator))
 return (two-tail-term).u

def cover(l,u,depth=0):
 upper=q2upper(u)
 q=F(l.numerator,l.denominator)
 c=I(upper)-q*q
 if c.u<0:
  row=dict(left=str(l),right=str(u),Q2_at_right_upper=str(R(upper,S)),
   Q1_at_left_lower=str(R(q.l,S)),c2_uniform_upper=str(R(c.u,S)))
  print(json.dumps(row),flush=True);return [row]
 assert depth<15,('inconclusive',l,u,R(c.u,S))
 m=(l+u)/2
 return cover(l,m,depth+1)+cover(m,u,depth+1)

start=time.time();der=[]
points=[R(1809,1000)+R(j,1000) for j in range(192)]
assert points[-1]==2
for l,u in zip(points,points[1:]):
 v=derivative_bound(l,u);assert v<0
 der.append(dict(left=str(l),right=str(u),derivative_upper=str(R(v,S))))
rows=cover(R(2),R(7))
assert rows[0]['left']=='2' and rows[-1]['right']=='7'
assert all(a['right']==b['left'] for a,b in zip(rows,rows[1:]))
# For b>=7, x=1/b<=1/7, 2atan(x)-atan(2x)<=2x^3,
# atan(x)>=x/(1+x^2). 2pi*x*(1+x^2)^2<1 is sufficient.
v=PI*I.rat(2,7)*I.rat(2500,2401)
assert v.u<S
result=dict(status='PASS',scope='Q2(b)<Q1(b)^2 for every b>=1.809',
 derivative_cells=der,middle_cells=rows,
 initial_sign_input='evidence/interval-survival-result.json',
 large_barrier_sufficient_bound=str(R(v.u,S)),
 arithmetic='outward integer intervals scale 10^30; alternating rational atan',
 elapsed_seconds=time.time()-start)
Path('evidence/antecedent-exclusion-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',middle_cells=len(rows),elapsed_seconds=result['elapsed_seconds'])),flush=True)
