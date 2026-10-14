"""Exact complex-rational adversarial checks of proposed noisy-unitary witnesses.
No numerical packages, imported reconstruction scripts, SDP solver or tolerance.
Run: python3 evidence/research-check.py
"""
from fractions import Fraction as F
from itertools import product
import json, hashlib
from pathlib import Path

class C:
    def __init__(self,r=0,i=0):
        if isinstance(r,C): self.r,self.i=r.r,r.i
        else: self.r,self.i=F(r),F(i)
    def __add__(self,z):
        z=C(z); return C(self.r+z.r,self.i+z.i)
    __radd__=__add__
    def __neg__(self): return C(-self.r,-self.i)
    def __sub__(self,z): return self+-C(z)
    def __rsub__(self,z): return C(z)+-self
    def __mul__(self,z):
        z=C(z); return C(self.r*z.r-self.i*z.i,self.r*z.i+self.i*z.r)
    __rmul__=__mul__
    def __truediv__(self,z):
        z=C(z); den=z.r*z.r+z.i*z.i
        return self*C(z.r/den,-z.i/den)
    def conj(self): return C(self.r,-self.i)
    def __eq__(self,z):
        z=C(z); return self.r==z.r and self.i==z.i
    def __repr__(self): return f'({self.r},{self.i})'

def eye(n): return [[C(i==j) for j in range(n)] for i in range(n)]
def dag(a): return [[x.conj() for x in r] for r in zip(*a)]
def mul(a,b): return [[sum((x*y for x,y in zip(row,col)),C()) for col in zip(*b)] for row in a]
def sc(a,c): return [[c*x for x in r] for r in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def kron(a,b): return [[x*y for x in r for y in s] for r in a for s in b]
def outer(v): return [[x*y.conj() for y in v] for x in v]
def tr(a): return sum((a[i][i] for i in range(len(a))),C())
def norm(v): return sum((x*x.conj() for x in v),C())
def vec(m): return [m[o][r] for r in range(2) for o in range(2)]
def ptrx(a): return [[sum((a[4*x+i][4*x+j] for x in range(4)),C()) for j in range(4)] for i in range(4)]
def ptrb(a): return [[sum((a[2*i+b][2*j+b] for b in range(2)),C()) for j in range(2)] for i in range(2)]
def ptrrb(a): return [[sum((a[2*r+i][2*r+j] for r in range(2)),C()) for j in range(2)] for i in range(2)]
def psd(a):
    assert a==dag(a)
    a=[r[:] for r in a]; n=len(a)
    for k in range(n):
        q=a[k][k]; assert q.i==0
        if q.r<0: return False
        if q.r==0:
            if any(a[k][j]!=0 for j in range(k+1,n)): return False
        else:
            for i in range(k+1,n):
                for j in range(k+1,n): a[i][j]=a[i][j]-a[i][k]*a[k][j]/q
    return True

i=C(0,1); I=eye(2)
pauli=[I,[[C(),C(1)],[C(1),C()]],[[C(),-i],[i,C()]],[[C(1),C()],[C(),C(-1)]]]
localI=(I,I,I,I)
rot=[[C(F(3,5)),C(F(-4,5))],[C(F(4,5)),C(F(3,5))]]
phase=[[C(F(3,5),F(4,5)),C()],[C(),C(F(3,5),F(-4,5))]]
loc=(rot,phase,phase,rot) # LA,LB,RA,RB
cases=[
 ('rank1', [C(1),C(),C(),C()], [F(1),F(0),F(0),F(0)]),
 ('rank2-unequal',[C(F(3,5)),i*F(4,5),C(),C()], [F(3,5),F(4,5),F(0),F(0)]),
 ('rank4-unequal',[C(F(15,65)),i*F(20,65),i*F(36,65),C(F(48,65))], [F(15,65),F(20,65),F(36,65),F(48,65)]),
 ('rank4-degenerate-SWAP',[C(F(1,2))]*4,[F(1,2)]*4),
]
records=[]
for name,coeff,abscoeff in cases:
 for localname,local in [('canonical',localI),('complex-local',loc)]:
    LA,LB,RA,RB=local
    amat=[mul(mul(LA,s),RA) for s in pauli]
    bmat=[mul(mul(LB,s),RB) for s in pauli]
    av,bv=list(map(vec,amat)),list(map(vec,bmat))
    # All Pauli vectorizations are norm sqrt(2); projectors divide by 2.
    assert all(norm(v)==2 for v in av+bv)
    AP=[sc(outer(v),F(1,2)) for v in av]
    BP=[sc(outer(v),F(1,2)) for v in bv]
    assert sum((1 for j in range(4) if norm(bv[j])==2))==4
    for j in range(4):
        assert ptrb(BP[j])==sc(I,F(1,2))
        assert ptrrb(BP[j])==sc(I,F(1,2))
        for k in range(4):
            assert mul(AP[j],AP[k])==(AP[j] if j==k else sc(eye(4),0))
            assert mul(BP[j],BP[k])==(BP[j] if j==k else sc(eye(4),0))
    U=sc(eye(4),0)
    for c,A,B in zip(coeff,amat,bmat): U=add(U,sc(kron(A,B),c))
    assert mul(dag(U),U)==eye(4)
    # Direct matrix-element Choi vector; independent of the Schmidt witness.
    u=[U[2*a+b][2*ra+rb]/2 for ra in range(2) for a in range(2) for rb in range(2) for b in range(2)]
    assert norm(u)==1
    P=outer(u); red=ptrx(P)
    root=sc(eye(4),0); Pi=sc(eye(4),0); w=[C()]*16
    for c,a,x,y,BPj in zip(coeff,abscoeff,av,bv,BP):
        assert c*c.conj()==a*a
        root=add(root,sc(BPj,a))
        if a:
            Pi=add(Pi,BPj)
            for xx in range(4):
                for yy in range(4): w[4*xx+yy]+=c/a*x[xx]*y[yy]/2
    assert mul(root,root)==red
    L=sum(abscoeff); assert tr(root)==L
    assert ptrb(root)==sc(I,L/2)
    W=add(outer(w),kron(sc(eye(4),F(1,4)),add(eye(4),sc(Pi,-1))))
    assert psd(W) and ptrx(W)==eye(4) and tr(W)==4
    # Dense rational PSD feasible Q which does NOT initially obey TP.
    z=[C(1),C(2,1),C(-1,2),C(3,-1)]
    Qtest=add(eye(4),outer(z))
    assert ptrb(Qtest)!=sc(I,tr(Qtest)/2)
    assert psd(add(kron(eye(4),Qtest),sc(P,-1)))
    Qbar=sc(eye(4),0)
    for signs in product([-1,1],repeat=4):
        VX=sc(eye(4),0); VY=sc(eye(4),0)
        for e,A,B in zip(signs,AP,BP):
            VX=add(VX,sc(A,e)); VY=add(VY,sc(B,e))
        assert mul(VX,dag(VX))==eye(4) and mul(VY,dag(VY))==eye(4)
        # Testing the ket avoids multiplying every 16x16 invariant matrix.
        V=kron(VX,VY)
        assert [sum((V[j][k]*u[k] for k in range(16)),C()) for j in range(16)]==u
        Qbar=add(Qbar,sc(mul(mul(VY,Qtest),dag(VY)),F(1,16)))
    assert tr(Qbar)==tr(Qtest) and psd(Qbar)
    assert ptrb(Qbar)==sc(I,tr(Qbar)/2)
    assert psd(add(kron(eye(4),Qbar),sc(P,-1)))
    # Four endpoint/interior values; bI invariance follows from unitarity above.
    for p in [F(0),F(1,7),F(1,2),F(1)]:
        rho=add(sc(P,1-p),sc(eye(16),p/16))
        Q=add(sc(root,(1-p)*L),sc(eye(4),p/16))
        assert psd(Q) and psd(add(kron(eye(4),Q),sc(rho,-1)))
        assert ptrb(Q)==sc(I,tr(Q)/2)
        objective=(1-p)*L*L+p/4
        assert tr(Q)==tr(mul(rho,W))==objective
        records.append({'gate':name,'basis':localname,'p':str(p),'kappa':str(L*L),
                        's=t':str(objective),'checks':'exact PSD, primal=dual, TP marginal; 16 signs invariant'})
print(json.dumps({'arithmetic':'Gaussian rational Fraction, zero tolerance; analytic proof supplies all-U quantifiers',
                  'cases':records,'counts':{'unitaries':8,'noisy_certificates':len(records),'sign_invariance_tests':128},
                  'limitations':'finite selected complex rational gates; no fresh referee; no general mixed-channel extension'},indent=2))
assert hashlib.sha256(Path('source.md').read_bytes()).hexdigest()=='64520010b568dafe82d8d5e1aecc669475eb5d5b5fef3ff5f01b2e180c2469af'
