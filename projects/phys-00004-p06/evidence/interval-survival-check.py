#!/usr/bin/env python3
"""Additional same-worker consistency checks, not an independent referee."""
from interval_survival import *
from decimal import Decimal,localcontext
start=time.time()
# Published zero-barrier survival inputs Q2=3/8, Q3=5/16.
q2,err=q2_simpson(R(0),2048)
assert q2.l <= 3*S//8 <= q2.u
q3,n=q3_lower(R(0))
assert q3.l <= 5*S//16 <= q3.u
# Independently accumulated Decimal Machin atan checks fixed-point pi enclosure.
with localcontext() as ctx:
 ctx.prec=80
 def decatan(x):
  term=x;out=Decimal(0)
  for k in range(160):
   out += (term if k%2==0 else -term)/Decimal(2*k+1);term*=x*x
  return out
 dpi=16*decatan(Decimal(1)/5)-4*decatan(Decimal(1)/239)
 assert Decimal(PI.l)/Decimal(S)<dpi<Decimal(PI.u)/Decimal(S)
 # Several argument-reduction branches versus separately accumulated Decimal series.
 for p,q in [(1,5),(1,2),(3,4),(1,1),(5,2),(-5,2)]:
  x=Decimal(abs(p))/Decimal(q)
  if x>1:val=dpi/2-decatan(1/x)
  elif x>Decimal('.5'):val=dpi/4+decatan((x-1)/(x+1))
  else:val=decatan(x)
  if p<0:val=-val
  v=atan(p,q)
  assert Decimal(v.l)/Decimal(S)<=val<=Decimal(v.u)/Decimal(S)
# Outward arithmetic tested against exact fractions, including negative intervals.
for aa in [(-3,-1),(-1,2),(1,3)]:
 for bb in [(1,2),(2,4)]:
  a=I.rat(aa[0],7);a=I(a.l,I.rat(aa[1],7).u)
  b=I.rat(bb[0],11);b=I(b.l,I.rat(bb[1],11).u)
  for c,vals in [(a*b,[R(x,7)*R(y,11) for x in aa for y in bb]),(a/b,[R(x,7)/R(y,11) for x in aa for y in bb])]:
   assert R(c.l,S)<=min(vals) and R(c.u,S)>=max(vals)
print(json.dumps(dict(status='PASS',zero_barrier_Q2=q2.floats(),zero_barrier_Q3=q3.floats(),pi_interval=PI.out(),checks=['published Q2=3/8','published Q3=5/16','Decimal Machin pi','atan sign/inversion/addition branches','exact rational interval multiply/divide'],limitations='Same proposer; no referee acceptance or independent source reconstruction of new claim',elapsed_seconds=time.time()-start)),flush=True)
