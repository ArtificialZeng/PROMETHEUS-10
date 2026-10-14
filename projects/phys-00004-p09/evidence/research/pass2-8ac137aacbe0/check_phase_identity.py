#!/usr/bin/env python3
"""Exact polynomial identity check for the generic phase Gram decomposition.

Four algebraically independent raw amplitudes x,y,z,w are normalized by
N=x^2+y^2+z^2+w^2. No finite samples, eigenvalue fits or logarithms are used.
"""
from pathlib import Path
import datetime as dt
import json
import time
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

HERE=Path(__file__).resolve().parent
R,x,y,z,w=ring('x,y,z,w',QQ)
ZERO=R.zero;ONE=R.one
def mat(rows):return [[R(v) for v in row] for row in rows]
def eye(n):return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def trans(A):return list(map(list,zip(*A)))
def add(A,B):return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(A,c):return [[c*v for v in row] for row in A]
def mul(A,B):
    Bt=trans(B)
    return [[sum((a*b for a,b in zip(ar,bc)),ZERO) for bc in Bt] for ar in A]
def dot(A,B):return sum((a*b for ar,br in zip(A,B) for a,b in zip(ar,br)),ZERO)
def kron(A,B):
    return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]
def ew(A,B):return [[a*b for a,b in zip(ar,br)] for ar,br in zip(A,B)]

def main():
    start=time.monotonic()
    M=[[x,y],[z,w]];Mt=trans(M);g=mul(M,Mt)
    N=x*x+y*y+z*z+w*w;D0=(x*w-y*z)**2;E=N*N-4*D0;den=2*E
    I=eye(4);Q=kron(M,M);K=add(kron(g,eye(2)),kron(eye(2),g))
    n=add(scale(g,2),scale(eye(2),-N))
    Pm=add(scale(I,E),scale(kron(n,n),-1))
    Ps=add(scale(I,den),scale(Pm,-1))
    Sn=add(scale(add(scale(I,2*den),scale(Pm,-1)),N),scale(K,-den))
    rows=[[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
    bas=[mat([[QQ(a*b,4) for b in rb] for a in ra]) for ra in rows for rb in rows]
    F=[ew(Q,d) for d in bas]
    T=[add(mul(f,trans(Q)),scale(mul(Q,trans(f)),-1)) for f in F]
    Smid=[mul(mul(Sn,t),Pm) for t in T]
    Ssum=[mul(mul(Ps,t),Ps) for t in T]
    Sdeg=[mul(mul(Pm,t),Pm) for t in T]
    u=x*y+z*w;v=x*z+y*w;du=x*y-z*w;dv=x*z-y*w;J=x*y*z*w
    vv=[ZERO,u*v,u*dv,u*v,ZERO,u*dv,v*du,v*du,2*du*dv]
    base=[[ZERO for _ in range(9)] for _ in range(9)]
    entries=[[x*x,y*y],[z*z,w*w]]
    for i in range(2):
        for j in range(2):
            za=1-2*i;zb=1-2*j
            for inds in [[0,2,6,8],[4,5,7,8]]:
                coeff=[1,zb,za,za*zb]
                for ia,a in enumerate(inds):
                    for ib,b in enumerate(inds):base[a][b]+=J*entries[i][j]*coeff[ia]*coeff[ib]
    checks=[]
    for a in range(9):
        for b in range(a+1):
            mixed=ew(Q,ew(bas[a],bas[b]))
            R2=add(scale(add(mul(F[a],trans(F[b])),mul(F[b],trans(F[a]))),QQ(1,2)),
                   scale(add(mul(mixed,trans(Q)),mul(Q,trans(mixed))),QQ(-1,2)))
            lhs=(-4*D0*den*den*N*dot(K,R2)
                 -2*N*dot(Smid[a],T[b])
                 -4*D0*dot(Ssum[a],T[b])
                 -N*N*dot(Sdeg[a],T[b]))
            rhs=4*D0*den*den*N*base[a][b]+2*D0*den*den*vv[a]*vv[b]
            residual=lhs-rhs
            ok=(residual==ZERO)
            rec={'a':a,'b':b,'zero_polynomial':ok,
                 'residual_terms':len(residual),'cleared_total_degree':20}
            checks.append(rec)
            print(json.dumps(rec),flush=True)
            if not ok:
                (HERE/'symbolic-nonzero.txt').write_text(str(residual)+'\n')
                break
        if not checks[-1]['zero_polynomial']:break
    result={'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),
            'method':'Exact rational polynomial ring QQ[x,y,z,w], all 45 symmetric coefficients after clearing the explicit denominator.',
            'common_denominator':'4 (xw-yz)^2 [2(N^2-4(xw-yz)^2)]^2 N^4',
            'coefficient_checks':checks,'completed':len(checks)==45,
            'all_zero_polynomials':all(c['zero_polynomial'] for c in checks),
            'wall_seconds':time.monotonic()-start,
            'limitation':'Identity verification supports the displayed analytic proof. It is same-worker code, not independent referee acceptance.'}
    (HERE/'symbolic-phase-identity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='coefficient_checks'}),flush=True)

if __name__=='__main__':main()
