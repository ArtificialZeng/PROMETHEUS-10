#!/usr/bin/env python3
"""Packaged exact rational replay for the missing-arc manuscript.

The calculation is copied from the accepted independent referee implementation.
Only the CLI, output location, metadata and explanatory header were adapted.
No scientific calculation statement is changed. Reads no input data or caches.
See ../source-map.md for the preserved original and its SHA-256 binding.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import argparse
parser = argparse.ArgumentParser(description="Replay exact rational identities; reads no input files.")
parser.add_argument("--output-dir", type=Path, default=Path("replay-output"), help="Directory for generated JSON results; relative to the invocation directory")
args = parser.parse_args()
OUTPUT = args.output_dir.resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)



class G:
    def __init__(self, a=0, b=0):
        if isinstance(a,G):
            self.a,self.b=a.a,a.b
        else:
            self.a,self.b=F(a),F(b)
    def __add__(self,x):
        x=G(x); return G(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):
        return G(-self.a,-self.b)
    def __sub__(self,x):
        return self+-G(x)
    def __rsub__(self,x):
        return G(x)+-self
    def __mul__(self,x):
        x=G(x); return G(self.a*x.a-self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=G(x); n=x.a*x.a+x.b*x.b
        if not n: raise ZeroDivisionError
        return G((self.a*x.a+self.b*x.b)/n,(self.b*x.a-self.a*x.b)/n)
    def __eq__(self,x):
        x=G(x); return self.a==x.a and self.b==x.b
    def __repr__(self):
        return f"({self.a})+i({self.b})"


def solve(A,b):
    n=len(b)
    a=[[G(x) for x in row]+[G(rhs)] for row,rhs in zip(A,b)]
    for k in range(n):
        pivot=next(j for j in range(k,n) if a[j][k]!=0)
        a[k],a[pivot]=a[pivot],a[k]
        v=a[k][k]
        a[k]=[x/v for x in a[k]]
        for j in range(n):
            if j!=k:
                v=a[j][k]
                a[j]=[x-v*y for x,y in zip(a[j],a[k])]
    x=[row[-1] for row in a]
    assert all(sum(A[i][j]*x[j] for j in range(n))==b[i] for i in range(n))
    return x


def mv(A,x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]


r0=[G(1),G(0,1),G(-1),G(0,-1)]
l0=[G(1)/4,G(0,-1)/4,G(-1)/4,G(0,1)/4]
lam0=G(-1,F(1,2))
Q0=[[G(0) for _ in range(4)] for _ in range(4)]
for j in range(4):
    Q0[j][j]=G(-1)
    Q0[j][(j+1)%4]=G(F(3,4))
    Q0[j][(j-1)%4]=G(F(1,4))
assert mv(Q0,r0)==[lam0*x for x in r0]
assert sum(a*b for a,b in zip(l0,r0))==1


def compute(c,u,s=None,m=F(0)):
    s=s or [F(0)]*4
    E=[[G(0) for _ in range(4)] for _ in range(4)]
    T=[[G(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        E[j][j]=G(s[j])
        E[j][(j+1)%4]=G(-F(3,4)*(c[j]+s[j])+u[j]-F(3,8)*m)
        E[j][(j-1)%4]=G(-F(1,4)*(c[j]+s[j])-u[j]+F(3,8)*m)
        E[j][(j+2)%4]=G(c[j])
        # Second derivative coefficient needed only for s=m=0 quadratic.
        T[j][(j+1)%4]=G(-c[j]*u[j]-F(4,3)*u[j]*u[j])
        T[j][(j-1)%4]=-T[j][(j+1)%4]
    A=[[Q0[i][j]-(lam0 if i==j else 0) for j in range(4)]+[-r0[i]] for i in range(4)]
    A.append(l0+[G(0)])
    b=[-x for x in mv(E,r0)]+[G(0)]
    sol=solve(A,b)
    r1,lam1=sol[:4],sol[4]
    Er1,Tr0=mv(E,r1),mv(T,r0)
    lam2=sum(l0[j]*(Er1[j]+Tr0[j]) for j in range(4))
    assert sum(l0[j]*r1[j] for j in range(4))==0
    return lam1,lam2


H=[[F(-14,3),F(-4,3),F(-10,3)],[F(-4,3),F(-8,3),F(-4,3)],[F(-10,3),F(-4,3),F(-14,3)]]
def expected(c,u):
    a,b=c[0]+c[2],c[1]+c[3]
    d,e=(c[0]-c[2])/2,(c[1]-c[3])/2
    umax=[(-3*c[0]+6*c[1]+3*c[2]-6*c[3])/40,(-6*c[0]-3*c[1]+6*c[2]+3*c[3])/40,(3*c[0]-6*c[1]-3*c[2]+6*c[3])/40]
    v=[u[j]-umax[j] for j in range(3)]
    return F(2,5)*(d*d+e*e)-F(5,64)*(a-b)**2+sum(v[i]*H[i][j]*v[j] for i in range(3) for j in range(3))/2


records=[]
directions=[]
for i in range(7):
    v=[F(0)]*7; v[i]=F(1)
    directions.append((f"basis_{i}",v))
for i in range(7):
    for j in range(i+1,7):
        v=[F(0)]*7; v[i]=v[j]=F(1)
        directions.append((f"basis_{i}_plus_{j}",v))
for name,v in directions:
    c=v[:4]; u=v[4:]+[-sum(v[4:])]
    l1,l2=compute(c,u)
    cb=sum(c)/4
    assert l1==G(-cb,-cb/2)
    got=l2.b-l2.a/2
    want=expected(c,u)
    assert got==want,(name,got,want)
    records.append({'name':name,'K':str(got),'expected':str(want),'pass':True})
    print(f"PASS {name}: K={got}",flush=True)
for i in range(5):
    s=[F(0)]*4;m=F(0)
    if i<4: s[i]=F(1)
    else: m=F(1)
    l1,_=compute([F(0)]*4,[F(0)]*4,s,m)
    h1=l1.b-l1.a/2
    expected_h1=-sum(s)/4-F(3,4)*m
    assert h1==expected_h1
    records.append({'name':f'slack_{i}','h_first':str(h1),'pass':True})
    print(f"PASS slack_{i}: first tangent excess={h1}",flush=True)

obj={'arithmetic':'Python standard-library fractions.Fraction only; Gaussian rationals implemented here; no symbolic/numeric library and no input files.','complete_identity_justification':'E is linear and the intrinsic second-order rate term is quadratic. The bordered derivative solve is linear in E; lambda2 is homogeneous quadratic in the seven variables. Seven basis evaluations and 21 pair-sum evaluations uniquely determine all 28 coefficients.','checks':records,'all_pass':all(x['pass'] for x in records),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUTPUT/'rational-results.json').write_text(json.dumps(obj,indent=2)+'\n')
print('ALL 28 QUADRATIC COEFFICIENTS AND 5 SLACK DIRECTIONS PASS',flush=True)
