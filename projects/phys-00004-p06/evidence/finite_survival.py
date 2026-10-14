#!/usr/bin/env python3
"""Outward killed-kernel lower bounds; shares checked scalar interval library."""
from interval_survival import I,F,S,R,grid
import json,time
from pathlib import Path

def compute(b,h,L,N=9):
 start=time.time()
 xs=sorted(set(grid(b,h,L)+[R(0)]))
 # Endpoints v_j of cells (x_{j-1},x_j]; tail y<-L discarded.
 vs=xs[1:]
 cache={}
 def cdf(x):
  if x not in cache:cache[x]=F(x.numerator,x.denominator)
  return cache[x]
 rows=[]
 for x in vs:
  mass=[]
  for u,v in zip(xs[:-1],vs):
   a=cdf(v-x)-cdf(u-x)
   assert a.l>=0
   mass.append(a.l)
  assert sum(mass)<=S
  rows.append(mass)
 # Exact one-step survival at all nodes. At subsequent orders the entire
 # omitted left tail is bounded below by zero, never folded into a finite cell.
 f=[cdf(b-v).l for v in vs]
 at0=vs.index(R(0));out=[f[at0]]
 for n in range(2,N+1):
  f=[sum(a*u for a,u in zip(row,f))//S for row in rows]
  assert all(0<=u<=S for u in f)
  # Truncation can destroy monotonicity of the lower approximation. True
  # survival is decreasing in starting x by coupling. Its suffix maximum
  # therefore remains a valid lower bound and restores the needed cell bound.
  for j in range(len(f)-2,-1,-1):f[j]=max(f[j],f[j+1])
  assert all(f[j]>=f[j+1] for j in range(len(f)-1))
  out.append(f[at0])
 q=R(21,25)
 records=[dict(n=n,lower_exact=str(R(u,S)),lower_decimal=u/S,
               comparison_exact=str(q**n),margin_exact=str(R(u,S)-q**n))
          for n,u in enumerate(out,1)]
 return dict(b=str(b),spacing=str(h),left_cutoff=str(-L),nodes=len(vs),
             rows=records,elapsed_seconds=time.time()-start,
             tail_control='discarded nonnegative contribution y<-L at each step; no claim of small omitted mass for remote starting nodes',
             arithmetic='scale 10^30 outward integer CDF intervals; all kernel and recurrence lower endpoints rounded down')

def main():
 result=compute(R(226,125),R(1,16),R(64))
 for row in result['rows']:print(json.dumps(row),flush=True)
 assert all(R(row['margin_exact'])>0 for row in result['rows'][2:])
 # q_n(0)=binomial(2n,n)/4^n, independently generated rational recurrence.
 a=R(1)
 for n in range(1,11):a*=R(2*n-1,2*n)
 assert a>R(21,25)**10
 assert R(21,22)>R(21,25) # a_(n+1)/a_n >=21/22 for n>=10
 result['baseline_induction']=dict(n0=10,Q10_at_zero=str(a),q=str(R(21,25)),
  ratio_lower=str(R(21,22)),conclusion='Q_n(0)>q^n for every n>=10')
 result['checks']='PASS: Q_n(1.808)>(21/25)^n for 3<=n<=9; zero-barrier induction for n>=10'
 Path('evidence/finite-survival-result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(checks=result['checks'],elapsed_seconds=result['elapsed_seconds'])),flush=True)
if __name__=='__main__':main()
