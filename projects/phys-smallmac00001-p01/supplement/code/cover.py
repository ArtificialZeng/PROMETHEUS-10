"""Packaged Arb replay using the independently derived Pauli functions.
Only rational witness centers, radii and preconditioners are taken from candidate.
No stored contraction, gluing, residual or sign verdict is trusted.
"""
import json,time,hashlib
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import sympy as s
from flint import arb,arb_mat,ctx
ROOT=Path(__file__).resolve().parents[1];AUD=ROOT/'results';AUD.mkdir(exist_ok=True);ctx.dps=100
START=time.monotonic()
def say(*x):print(*x,flush=True)
def E(n):return arb_mat([[int(i==j) for j in range(n)] for i in range(n)])
def fa(q):
 q=Fraction(q);return arb(q.numerator)/q.denominator
v=s.symbols('a h t lam',real=True);loc={str(q):q for q in v}
data=json.loads((AUD/'derived-functions.json').read_text())
mu=s.sympify(data['mu'],locals=loc);e2=s.sympify(data['e2'],locals=loc)
F=[s.diff(e2,q)-v[3]*s.diff(mu,q) for q in v[:3]]+[mu]
J=s.Matrix(F).jacobian(v)

def compiler(expr,derivatives=False):
 n,d=s.fraction(s.cancel(expr))
 assert all(q.q==1 for q in s.Poly(n,*v).coeffs()+s.Poly(d,*v).coeffs())
 exprs=[n,d]
 if derivatives:exprs += [s.diff(n,q) for q in v]+[s.diff(d,q) for q in v]
 fn=s.lambdify(v,exprs,modules='math',cse=True)
 def ev(box,flow=None):
  q=[arb(a) for a in fn(*box)];assert not q[1].contains(0)
  if flow is None:return q[0]/q[1]
  cent,velocity,width=flow
  cc=[arb(a) for a in fn(*cent)];assert not cc[1].contains(0)
  der=sum(((q[2+i]*q[1]-q[0]*q[6+i])/(q[1]*q[1]))*velocity[i] for i in range(4))
  return cc[0]/cc[1]+arb(0,width)*der
 return ev
ff=[compiler(q) for q in F];jj=[[compiler(J[i,j]) for j in range(4)] for i in range(4)]
scalar={name:compiler(s.sympify(data[name],locals=loc),True) for name in ['mu','e2','effect_multiplier','state_gap']}
gr=[compiler(s.sympify(q,locals=loc),True) for q in data['mean_gradient']]
mats={n:[[compiler(s.sympify(q,locals=loc),True) for q in row] for row in data[n]] for n in ['K','choi_slack','real_lagrangian_hessian','odd_lagrangian_hessian']}
def fun(b,m):
 out=[q(b) for q in ff];out[3]-=m;return arb_mat([[a] for a in out])
def jac(b):return arb_mat([[q(b) for q in row] for row in jj])
def unpack(rec):
 c=list(map(Fraction,rec['centers']));r=list(map(Fraction,rec['radii']))
 assert all(a>0 for a in r)
 B=[arb(fa(a),fa(b)) for a,b in zip(c,r)]
 C=arb_mat([[fa(q) for q in row] for row in rec['preconditioner']])
 return c,r,B,C

def norm(Q,r):
 return max((sum(abs(Q[i,j])*fa(r[j])/fa(r[i]) for j in range(4))).upper() for i in range(4))

def validate_root(rec,lo,hi):
 c,r,B,C=unpack(rec)
 Q=E(4)-C*jac(B);qn=norm(Q,r);assert qn<1
 mean=arb(fa((lo+hi)/2),fa((hi-lo)/2))
 center=[fa(q) for q in c]
 ds=-C*fun(center,mean)+Q*arb_mat([[arb(0,fa(q))] for q in r])
 ratios=[(abs(ds[i,0]).upper()/fa(r[i])).upper() for i in range(4)]
 assert all(q<1 for q in ratios)
 correction=C*fun(center,fa((lo+hi)/2))
 err=max((abs(correction[i,0]).upper()/fa(r[i])).upper() for i in range(4))/(1-qn)
 errors=[(err*fa(q)).upper() for q in r]
 assert all(q<arb('1e-30') for q in errors)
 return B,C,qn,max(ratios),max(errors)

def glue(left,right):
 lows=[min(Fraction(q['centers'][i])-Fraction(q['radii'][i]) for q in [left,right]) for i in range(4)]
 highs=[max(Fraction(q['centers'][i])+Fraction(q['radii'][i]) for q in [left,right]) for i in range(4)]
 r=[(u-l)/2 for l,u in zip(lows,highs)]
 box=[arb(fa((l+u)/2),fa(rr)) for l,u,rr in zip(lows,highs,r)]
 C=arb_mat([[fa(q) for q in row] for row in left['preconditioner']])
 n=norm(E(4)-C*jac(box),r);assert n<1;return n

def ldlt(M):
 # Independent symmetric Schur elimination, no inertia code import.
 A=[[M[i,j] for j in range(M.ncols())] for i in range(M.nrows())]
 out=[]
 for k in range(len(A)):
  d=A[k][k];assert d>0;out.append(d.lower())
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[i][j]=A[j][i]=A[i][j]-A[i][k]*A[j][k]/d
 return out

def signs(B,rec,lo,hi):
 assert B[0]>0 and B[0]<1 and B[1]>0 and B[2]<0
 velocity=jac(B).solve(arb_mat([[0],[0],[0],[1]]))
 flow=([arb(fa(q),arb('1e-30')) for q in rec['centers']], [velocity[i,0] for i in range(4)],fa((hi-lo)/2))
 def ev(name):return arb_mat([[f(B,flow) for f in row] for row in mats[name]])
 yy=scalar['effect_multiplier'](B,flow);gap=scalar['state_gap'](B,flow)
 assert yy>arb('0.01') and gap>arb('0.01')
 g=[f(B,flow) for f in gr]+[arb(0),arb(0)];assert g[2]>0
 hh=arb_mat(5,5);hr=ev('real_lagrangian_hessian');ho=ev('odd_lagrangian_hessian')
 for i in range(3):
  for j in range(3):hh[i,j]=hr[i,j]
 for i in range(2):
  for j in range(2):hh[i+3,j+3]=ho[i,j]
 free=[0,1,3,4]
 tangent=arb_mat([[-g[j]/g[2] if i==2 else int(i==j) for j in free] for i in range(5)])
 red=tangent.transpose()*hh*tangent;hp=ldlt(red-arb('0.01')*E(4))
 K=ev('K');k=[K[0,0],K[1,0],K[0,1],K[1,1]];assert not k[0].contains(0)
 V=arb_mat([[-k[j]/k[0] for j in range(1,4)]]+[[int(i==j) for j in range(1,4)] for i in range(1,4)])
 H=ev('choi_slack');cp=ldlt(V.transpose()*(H-arb('0.01')*E(4))*V)
 K2=K*K;contract=arb(999)/1000*E(2)-K2.transpose()*K2
 tp=ldlt(contract)
 return yy.lower(),gap.lower(),g[2].lower(),min(hp),min(cp),min(tp)

say('COMPILED',round(time.monotonic()-START,2))
anchor_raw=json.loads((ROOT/'data/choi-kkt-certificate.json').read_text())
anchor={'centers':anchor_raw['root_box_centers'],'radii':anchor_raw['root_box_radii'],'preconditioner':anchor_raw['rational_preconditioner']}
validate_root(anchor,Fraction(4),Fraction(4));say('MEAN4_ANCHOR_RECERTIFIED')
end=Fraction(3);prev=None;count=0;anchor_count=0
maxq=arb(0);maxinc=arb(0);maxglue=arb(0);maxerr=arb(0);minimum=[arb(10**100) for _ in range(6)]
for line in (ROOT/'data/choi-continuation-cells.jsonl').open():
 rec=json.loads(line);lo,hi=map(Fraction,rec['mean_interval'])
 assert rec['index']==count and lo==end and lo<hi<=6
 B,C,qn,inc,err=validate_root(rec,lo,hi)
 maxq=max(maxq,qn);maxinc=max(maxinc,inc);maxerr=max(maxerr,err)
 if prev is not None:maxglue=max(maxglue,glue(prev,rec))
 if lo<=4<=hi:
  gg=glue(rec,anchor);anchor_count+=1
  say('ANCHOR_GLUE',count,str(gg))
 bounds=signs(B,rec,lo,hi);minimum=[min(a,b) for a,b in zip(minimum,bounds)]
 prev=rec;end=hi;count+=1
 if count%1000==0:
  say('CHECKED',count,'end',str(end),'elapsed',round(time.monotonic()-START,2))
  (AUD/'cover-progress.json').write_text(json.dumps({'cells_checked':count,'covered_until':str(end),'elapsed_seconds':time.monotonic()-START})+'\n')
assert count==8433 and end==6 and anchor_count>=1
out={'run_kind':'packaged_replay','checked_at':datetime.now(timezone.utc).isoformat(),'cells':count,'mean_interval':['3','6'],'all_roots_recomputed':True,'all_adjacent_gluing_recomputed':True,'mean4_anchor_recomputed':True,'all_signs_recomputed':True,'source_of_functions':'results/derived-functions.json','arb_digits':ctx.dps,'maximum_contraction':str(maxq),'maximum_inclusion_ratio':str(maxinc),'maximum_gluing_contraction':str(maxglue),'maximum_midpoint_error':str(maxerr),'minimum_lower_bounds':dict(zip(['effect','state_gap','mean_t','Hessian_shifted_LDL_pivot','Choi_shifted_LDL_pivot','transience_LDL_pivot'],map(str,minimum))),'elapsed_seconds':time.monotonic()-START,'all_checks_pass':True,'limitations':'Floating Arb enclosures over exact rational witnesses; no global bound and no numerical basin radius; LDL pivots are coordinate dependent.'}
(AUD/'cover-results.json').write_text(json.dumps(out,indent=2)+'\n');say('PASS',json.dumps(out))
