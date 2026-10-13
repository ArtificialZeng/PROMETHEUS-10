"""Packaged Pauli-transfer reconstruction and complete certificate replay.
No project discovery code is imported. Frozen boxes are witnesses only.
"""
import json, time, hashlib, sys
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import sympy as s
import flint
from flint import arb, arb_mat, ctx
START=time.monotonic()
ROOT=Path(__file__).resolve().parents[1]
AUD=ROOT/'results';AUD.mkdir(exist_ok=True)
ctx.dps=100

def say(*v): print(*v, flush=True)
def cancel(M): return M.applyfunc(s.cancel)
def matrix_list(M): return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
a,h,t,x,z,lam=s.symbols('a h t x z lam', real=True)
pvars=(a,h,t,lam)
I=s.eye(2)
sigma=[I,s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
W=s.Matrix([[h*h,-h],[-h,1]])/(1+h*h)
D=I+(a-1)*W
# Cayley map written as scalar plus Pauli generator.
q=x*x+t*t+z*z
U=((1-q)*I+2*s.I*(x*sigma[1]+t*sigma[2]+z*sigma[3]))/(1+q)
fullK=U*D
K=cancel(fullK.subs({x:0,z:0}))
def transfer(L,R):
 return cancel(s.Matrix(4,4,lambda i,j:s.trace(sigma[i]*L*sigma[j]*R.conjugate().T)/2))
T=transfer(K,K)
inds=[0,1,3]
R3=cancel((s.eye(3)-T.extract(inds,inds)).inv())
R=s.zeros(4)
for i in range(3):
 for j in range(3): R[inds[i],inds[j]]=R3[i,j]
R[2,2]=1/(1-a)
assert cancel((s.eye(4)-T)*R)==s.eye(4)
rho=s.Matrix([1,0,0,1]); e0=s.Matrix([1,0,0,0])
X=cancel(R*rho); Z=cancel(R*X)
mu=s.cancel(X[0]); e2=s.cancel(2*Z[0]-X[0])
Av=cancel(R.T*e0); Bv=cancel(R.T*(2*Av-e0))
cv=cancel(Bv-lam*Av)
def primal(v):return cancel(sum((v[i]*sigma[i]/2 for i in range(4)),s.zeros(2)))
def dual(v):return cancel(sum((v[i]*sigma[i] for i in range(4)),s.zeros(2)))
Xm,Zm,A,C=primal(X),primal(Z),dual(Av),dual(cv)
G=cancel(s.kronecker_product(Xm.T,C)+2*s.kronecker_product(Zm.T,A))
k=s.Matrix([K[0,0],K[1,0],K[0,1],K[1,1]])
E=s.kronecker_product((I-W).T,I)
y=s.cancel(-((E*k).T*G*k)[0])
assert s.cancel(((E*k).T*(E*k))[0]-1)==0
Hchoi=cancel(G+y*E)
gap=s.cancel(C[1,1]-C[0,0])
grad=[s.cancel(s.diff(mu,v)) for v in (a,h,t)]
Hreal=cancel(s.hessian(e2-lam*mu,(a,h,t)))
say('PAULI_MOMENTS_AND_SLACKS',round(time.monotonic()-START,2))
oddvars=(x,z); Td=[];Xd=[];Zd=[]; kds=[]
for v in oddvars:
 kd=cancel(fullK.diff(v).subs({x:0,z:0}));kds.append(kd)
 d=cancel(transfer(kd,K)+transfer(K,kd));Td.append(d)
 xi=cancel(R*d*X);Xd.append(xi)
 Zd.append(cancel(R*(xi+d*Z)))
Hodd=s.zeros(2)
for i in range(2):
 for j in range(i,2):
  kdd=cancel(fullK.diff(oddvars[i]).diff(oddvars[j]).subs({x:0,z:0}))
  Tij=cancel(transfer(kdd,K)+transfer(K,kdd)+transfer(kds[i],kds[j])+transfer(kds[j],kds[i]))
  b=cancel(Tij*X+Td[i]*Xd[j]+Td[j]*Xd[i])
  c=cancel(Tij*Z+Td[i]*Zd[j]+Td[j]*Zd[i])
  # Direct second derivative of the primal Pauli resolvent.
  xx=cancel(R*b); zz=cancel(R*(xx+c))
  Hodd[i,j]=Hodd[j,i]=s.cancel(2*zz[0]-(1+lam)*xx[0])
  say('ODD_HESSIAN',i,j,round(time.monotonic()-START,2))
# No submitted scalar/Hessian cache is used until our expressions exist.
new={'mu':mu,'e2':e2,'effect_multiplier':y,'state_gap':gap,
     'mean_gradient':grad,'K':K,'choi_slack':Hchoi,
     'real_lagrangian_hessian':Hreal,'odd_lagrangian_hessian':Hodd}
saved=json.loads((ROOT/'data/choi-continuation-functions.json').read_text())
loc={str(v):v for v in pvars}
checks=0
for name,obj in new.items():
 old=saved[name]
 if isinstance(obj,s.MatrixBase):
  for i in range(obj.rows):
   for j in range(obj.cols):
    assert s.cancel(obj[i,j]-s.sympify(old[i][j],locals=loc))==0,(name,i,j)
    checks+=1
 elif isinstance(obj,list):
  for i,v in enumerate(obj):
   assert s.cancel(v-s.sympify(old[i],locals=loc))==0,(name,i)
   checks+=1
 else:
  assert s.cancel(obj-s.sympify(old,locals=loc))==0,name
  checks+=1
say('EXACT_SYMBOLIC_IDENTITIES',checks,round(time.monotonic()-START,2))
# Baseline independently reconstructed from the published K of Budroni Eq C1.
base=[]
for m in (3,4,6):
 atten=1-s.Rational(2,m); uu=2*atten/(1+atten**2)
 KK=s.Matrix([[s.sqrt(uu),s.sqrt(1-uu)],[-s.sqrt(1-uu),s.sqrt(uu)]])*s.diag(1,atten)
 RR=(s.eye(4)-transfer(KK,KK)).inv()
 xx=RR*rho; zz=RR*xx
 mm=s.simplify(xx[0]);ee=s.simplify(2*zz[0]-xx[0]);cost=s.simplify(2*ee-3*mm**2+2*mm)
 assert mm==m and cost==-s.Rational(m*m*(m-2)**2,2*(m-1)**2)
 base.append({'m':m,'mean':str(mm),'variance':str(s.simplify(ee-mm**2)),'CF2':str(cost)})
say('EXACT_PUBLISHED_BASELINE',base)
serialized={n:matrix_list(v) if isinstance(v,s.MatrixBase) else [str(q) for q in v] if isinstance(v,list) else str(v) for n,v in new.items()}
(AUD/'derived-functions.json').write_text(json.dumps(serialized,indent=2)+'\n')
(AUD/'symbolic-check.json').write_text(json.dumps({'run_kind':'packaged_replay','basis':'Pauli coefficients x_i=tr(sigma_i X), X=sum(x_i sigma_i)/2; direct primal second derivatives','exact_identities_checked':checks,'published_baselines':base,'elapsed_seconds':time.monotonic()-START},indent=2)+'\n')
if '--symbolic-only' in sys.argv:sys.exit(0)
