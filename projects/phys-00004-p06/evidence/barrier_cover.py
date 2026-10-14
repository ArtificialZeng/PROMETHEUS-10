#!/usr/bin/env python3
"""Finite barrier cover proving all-order survival comparison on [0,1.809]."""
from finite_survival import compute
from interval_survival import F,R,S
import json,time
from pathlib import Path

def cover(l,u,depth=0):
 result=compute(l,R(1,32),R(128))
 q=F(u.numerator,u.denominator)
 margins=[R(row['lower_exact'])-R(q.u,S)**row['n'] for row in result['rows'][2:]]
 if min(margins)>0:
  row=dict(left=str(l),right=str(u),q_upper_exact=str(R(q.u,S)),
   Q_lower_exact=[v['lower_exact'] for v in result['rows']],
   margins_exact=[str(m) for m in margins],nodes=result['nodes'])
  print(json.dumps(row),flush=True)
  return [row]
 assert depth<12,('inconclusive',l,u,min(margins))
 m=(l+u)/2
 return cover(l,m,depth+1)+cover(m,u,depth+1)

start=time.time()
rows=cover(R(0),R(1809,1000))
assert R(rows[0]['left'])==0 and R(rows[-1]['right'])==R(1809,1000)
assert all(a['right']==b['left'] for a,b in zip(rows,rows[1:]))
assert F(1809,1000).u*25<21*S
result=dict(status='PASS',scope='For every b in [0,1.809], Q_n(b)>Q_1(b)^n for all n>=3',
 finite_orders='3..9 by monotone barrier cover and lower killed-kernel recurrence',
 infinite_orders='n>=10 by exact zero-barrier recurrence, q<=21/25, and ratio induction in finite-survival-result.json',
 spatial_spacing='1/32',left_cutoff='-128',cells=rows,elapsed_seconds=time.time()-start,
 limitations='Q2 comparison is a hypothesis; no restriction on all possible roots outside the barrier range is established')
Path('evidence/barrier-cover-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',cells=len(rows),elapsed_seconds=result['elapsed_seconds'])),flush=True)
