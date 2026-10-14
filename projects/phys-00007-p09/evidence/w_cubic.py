"""Exact cubic reduced missing moment; no checkpoint or cached results as inputs."""
from radical_algebra import *
def mv(M,v): return [sum(a*b for a,b in zip(row,v)) for row in M]
def dot(v,w): return sum(a.conj()*b for a,b in zip(v,w))
def vs(*vectors): return [sum(x) for x in zip(*vectors)]
def sv(a,v): return [a*x for x in v]
controls=[tensor([p if k==j else I for k in range(3)]) for j in range(3) for p in [X,Y,Z]]
K=[tensor([X if k==j else Z for k in range(3)]) for j in range(3)]
S=[K[0],K[1],K[2],mul(K[0],K[1]),mul(K[0],K[2]),mul(K[1],K[2])]
O=add(mul(S[3],K[2]),scale(-2,add(add(K[0],K[1]),K[2])))
z=mv(tensor([q,q,q]),[one if k in [1,2,4] else zero for k in range(8)])
sqrt2=2*r*a*b
def generator(theta):
 M=[[zero for _ in range(8)] for _ in range(8)]
 for x,C in zip(theta,controls): M=add(M,scale(x*Q(1,2),C))
 return M
def moment_coeff(S,vectors,n):
 return sum(dot(vectors[k],mv(S,vectors[n-k])) for k in range(n+1))*Q(1,3)
def calculate(u):
 theta=sum([[zero,sqrt2*u[j],F(2*sum(u)-5*u[j])] for j in range(3)],[])
 H=generator(theta); hz=mv(H,z)
 v1=sv(-i,hz); v2raw=sv(Q(-1,2),mv(H,hz))
 assert all(moment_coeff(T,[z,v1],1)==0 for T in S+[O])
 f2=[moment_coeff(T,[z,v1,v2raw],2) for T in S]
 assert moment_coeff(O,[z,v1,v2raw],2)==0
 # Complement = Z1,Z2,Z3,X1,X2,X3, all Y corrections fixed to zero.
 zz=[-9*a*b*x for x in f2[:3]]
 targets=[-Q(3,2)*sqrt2*x for x in f2[3:]]
 xx=[(targets[0]+targets[1]-targets[2])*Q(1,2),
     (targets[0]+targets[2]-targets[1])*Q(1,2),
     (targets[1]+targets[2]-targets[0])*Q(1,2)]
 correction=sum([[xx[j],zero,zz[j]] for j in range(3)],[])
 L=generator(correction)
 v2=vs(v2raw,sv(-i,mv(L,z)))
 assert all(moment_coeff(T,[z,v1,v2],2)==0 for T in S+[O])
 v3=vs(sv(Q(-1,2),vs(mv(H,mv(L,z)),mv(L,hz))),sv(i*Q(1,6),mv(H,mv(H,hz))))
 c=moment_coeff(O,[z,v1,v2,v3],3)
 assert c==c.conj()
 return c,correction,f2
exponents=[e for e in product(range(4),repeat=3) if sum(e)==3]
samples=[calculate(e) for e in exponents]
# Unisolvent homogeneous degree-three interpolation, rational elimination.
M=[[Q(math.prod(u[j]**e[j] for j in range(3))) for e in exponents] for u in exponents]
rhs=[x[0] for x in samples]
for col in range(10):
 pivot=next(k for k in range(col,10) if M[k][col])
 M[col],M[pivot]=M[pivot],M[col];rhs[col],rhs[pivot]=rhs[pivot],rhs[col]
 factor=M[col][col];M[col]=[x/factor for x in M[col]];rhs[col]=rhs[col]* (1/factor)
 for row in range(10):
  if row==col:continue
  factor=M[row][col]
  M[row]=[x-factor*y for x,y in zip(M[row],M[col])];rhs[row]=rhs[row]-factor*rhs[col]
def evaluate(u):return sum(c*math.prod(u[j]**e[j] for j in range(3)) for c,e in zip(rhs,exponents))
holdout=[]
for u in [(1,-1,2),(2,3,-1),(-2,1,0),(1,1,1),(1,0,0)]:
 actual,correction,f2=calculate(u);assert actual==evaluate(u)
 holdout.append({'u':u,'cubic_exact':actual.record(),'cubic_numeric':actual.val().real,'correction_exact':[x.record() for x in correction]})
out={'definition':'theta=s v(u)+s^2 c(u)+O(s^3); c in span Xj,Zj; six moments vanish through s^2',
 'missing_moment':'K1K2K3-2(K1+K2+K3)',
 'coefficient_convention':'coefficient of s^3 (not third derivative)',
 'cubic_coefficients':[{'exponents':e,'exact':c.record(),'numeric':c.val().real} for e,c in zip(exponents,rhs)],
 'holdout':holdout,'checks':'Exact first and second order constraints; missing quadratic zero; five exact cubic holdouts',
 'scope':'One local chart through published triangle W encoder; no global exclusion or universal encoding proof'}
Path('evidence/w-cubic.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
