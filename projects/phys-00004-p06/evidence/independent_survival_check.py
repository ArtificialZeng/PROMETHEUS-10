#!/usr/bin/env python3
"""Same-proposer alternative replay, not independent referee acceptance.
Different coordinate, grid, scalar rational-series implementation and kernel loop.
Does not read numerical survival outputs from the discovery implementation.
"""
from fractions import Fraction as R
from functools import lru_cache
from pathlib import Path
import json,time,math
D=10**24

def floor(x):return x.numerator//x.denominator
def ceil(x):return -floor(-x)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[1],a[1]-b[0])
def mul(a,k):
 v=[R(a[0])*k,R(a[1])*k]
 return floor(min(v)),ceil(max(v))
def small(x):
 assert abs(x)<=R(1,2)
 # Exact rational terms, then round just once; no fixed-point term recurrence.
 term=x;total=R(0)
 for k in range(48):
  total+=(-1 if k%2 else 1)*term/(2*k+1);term*=x*x
 rem=abs(term)/97
 return floor((total-rem)*D),ceil((total+rem)*D)
pi=sub(mul(small(R(1,5)),16),mul(small(R(1,239)),4))
@lru_cache(None)
def angle(x):
 if x<0:
  a=angle(-x);return -a[1],-a[0]
 if x>1:return sub(mul(pi,R(1,2)),angle(1/x))
 if x>R(1,2):return add(mul(pi,R(1,4)),small((x-1)/(x+1)))
 return small(x)
@lru_cache(None)
def cdf(x):
 a=angle(x)
 vals=[R(v,p) for v in a for p in pi]
 return floor((R(1,2)+min(vals))*D),ceil((R(1,2)+max(vals))*D)

def survival(b):
 # a=b-x is distance to absorption. True survival increases with a.
 grid=[R(k,40) for k in range(641)] # [0,16], step 1/40
 v=R(16)
 while v<256:v=min(R(256),v*R(9,8));grid.append(v)
 grid=sorted(set(grid+[b]));nodes=grid[:-1]
 weights=[]
 for a in nodes:
  row=[]
  for l,u in zip(grid[:-1],grid[1:]):
   m=sub(cdf(u-a),cdf(l-a));assert m[0]>=0;row.append(m[0])
  assert sum(row)<=D
  weights.append(row)
 values=[cdf(a)[0] for a in nodes]
 out=[values[nodes.index(b)]]
 for n in range(2,10):
  values=[sum(w*v for w,v in zip(row,values))//D for row in weights]
  # Prefix maximum: each earlier-node lower bound also bounds the true
  # survival at all later nodes. Omitted positive a'>256 tail stays omitted.
  for j in range(1,len(values)):values[j]=max(values[j],values[j-1])
  out.append(values[nodes.index(b)])
 return out,len(nodes)

def main():
 start=time.time()
 cover=json.loads(Path('evidence/barrier-cover-result.json').read_text())
 rows=[]
 for cell in cover['cells']:
  l,u=R(cell['left']),R(cell['right'])
  values,nodes=survival(l);q=R(cdf(u)[1],D)
  margins=[R(v,D)-q**n for n,v in enumerate(values,1) if n>=3]
  assert min(margins)>0,(l,u,min(margins))
  row=dict(left=str(l),right=str(u),nodes=nodes,Q_lower_exact=[str(R(v,D)) for v in values],
           minimum_margin_exact=str(min(margins)))
  rows.append(row);print(json.dumps(row),flush=True)
 # Independently use factorial closed form at n=10, not recurrence.
 a=R(math.factorial(20),math.factorial(10)**2*4**10)
 assert a>R(21,25)**10 and R(21,22)>R(21,25)
 # Scalar checks against exact zero-barrier published values.
 values,nodes=survival(R(0))
 assert all(R(v,D)<=R(math.comb(2*n,n),4**n) for n,v in enumerate(values,1))
 assert abs(R(values[1],D)-R(3,8))<R(1,200)
 result=dict(status='PASS',representation='distance to barrier, independent rational atan terms, 1/40 grid to16, geometric to256, prefix bounds',
  rows=rows,baseline_Q10=str(a),zero_barrier_lower=[str(R(v,D)) for v in values],
  limitations='Same proposer and same Cauchy/Sparre-Andersen assumptions; replays finite survival comparison, not a fresh scientific referee. Uses only barrier cell boundaries from first output, never its computed survival answers.',
  elapsed_seconds=time.time()-start)
 Path('evidence/independent-survival-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(status='PASS',elapsed_seconds=result['elapsed_seconds'])),flush=True)

if __name__=='__main__':main()
