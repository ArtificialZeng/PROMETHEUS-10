#!/usr/bin/env python3
"""Alternative scalar arithmetic replay of all antecedent-exclusion pieces."""
from independent_survival_check import R,D,pi,cdf,add,sub,mul,floor,ceil
from pathlib import Path
import json,time,math

def div(a,b):
 assert b[0]>0
 v=[R(x*D,y) for x in a for y in b]
 return floor(min(v)),ceil(max(v))
def rational(x):return floor(x*D),ceil(x*D)
one=(D,D)

def initial_sign(b):
 N=16384;total=(0,0)
 for k in range(N+1):
  t=R(k,N);den=t*t+((b+1)*t-1)**2
  A=one if k==0 else cdf(R(N-k,k))
  g=div(div(A,pi),rational(den))
  total=add(total,mul(g,1 if k in (0,N) else 4 if k%2 else 2))
 value=mul(total,R(1,3*N))
 # Independently write the inverse quadratic differentiated-product bound.
 a=1+(b+1)**2;d1=max(2*(b+1),2*a-2*(b+1));d2=2*a
 V=[a]
 for j in range(1,5):
  V.append(a*(j*d1*V[-1]+(R(j*(j-1),2)*d2*V[-2] if j>1 else 0)))
 W=[R(2)]
 for j in range(1,4):W.append(2*(2*j*W[-1]+(2*j*(j-1)*W[-2] if j>1 else 0)))
 AA=[R(1)]+[w/3 for w in W]
 M=sum(math.comb(4,j)*AA[j]*V[4-j] for j in range(5))/3
 error=M/(180*N**4)
 q=rational(R(cdf(b)[0],D)**2)
 upper=R(value[1],D)+error-R(q[0],D)
 assert upper<0
 return dict(b=str(b),N=N,Q2_quadrature_upper=str(R(value[1],D)),
             M4=str(M),error=str(error),c2_upper=str(upper))

def upper_q2(b):
 ts=[R(k,96) for k in range(1537)]
 t=R(16)
 while t<2048:t=min(R(2048),t*R(10,9));ts.append(t)
 acc=0
 last=cdf(b)
 for t in ts[1:]:
  v=cdf(b+t);mass=sub(v,last);assert mass[0]>=0
  acc+=(mass[0]*cdf(-t)[0])//D;last=v
 return cdf(b/2)[1]-acc

start=time.time();data=json.loads(Path('evidence/antecedent-exclusion-result.json').read_text())
initial=initial_sign(R(1809,1000));print(json.dumps(initial),flush=True)
der=[]
for c in data['derivative_cells']:
 l,u=R(c['left']),R(c['right'])
 first=div(rational(R(2)/(l*l+4)),pi)
 tail=div(rational(1/(4*(1+(u+1)**2))),pi)
 coeff=sub(mul(cdf(l),2),rational(R(1,2)))
 last=div(div(coeff,pi),rational(1+u*u))
 bound=sub(sub(first,tail),last)[1]
 assert bound<0;der.append(str(R(bound,D)))
rows=[]
for c in data['middle_cells']:
 l,u=R(c['left']),R(c['right'])
 bound=R(upper_q2(u),D)-R(cdf(l)[0],D)**2
 assert bound<0,(l,u,bound)
 row=dict(left=str(l),right=str(u),c2_upper=str(bound));rows.append(row)
 print(json.dumps(row),flush=True)
large=mul(pi,R(2,7)*R(2500,2401));assert large[1]<D
result=dict(status='PASS',initial=initial,derivative_upper_bounds=der,middle_cells=rows,
 large_barrier_condition_upper=str(R(large[1],D)),elapsed_seconds=time.time()-start,
 independence='Different scalar arithmetic; direct compact Q2 quadrature at initial barrier with doubled N; different tail grid for middle bounds; original cell boundaries only. Same proposer and shared analytic model/baseline, not a fresh referee.')
Path('evidence/independent-exclusion-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',elapsed_seconds=result['elapsed_seconds'])),flush=True)
