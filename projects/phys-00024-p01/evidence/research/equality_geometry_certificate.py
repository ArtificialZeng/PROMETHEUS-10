#!/usr/bin/env python3
"""Exact pair, curvature, and independent full-Hessian checks; no cached Hessian."""
import json
import sympy as sp

s=sp.sqrt(10); c=(3+s)/4; rho=(s+1)/3; u2=(s-1)/4
kappa=sp.Rational(3,2)*(3+s)
def clean(z):
    return sp.expand(sp.radsimp(sp.cancel(sp.expand(z))))
def hc(A):
    n=A.rows
    P=sp.kronecker_product(A.T,sp.eye(n))
    Q=sp.kronecker_product(sp.eye(n),A)
    return P.T.conjugate()*P+Q.T.conjugate()*Q/2-3*(P.T.conjugate()*Q+Q.T.conjugate()*P)/4

t=sp.symbols('t', real=True)
A=sp.Matrix([[1,t],[0,-rho]])
B=sp.Matrix([[-rho*t/(1+rho*rho),1],[0,t/(1+rho*rho)]])
N=clean(1+rho*rho+t*t)
vec=sp.Matrix([B[0,0],B[1,0],B[0,1],B[1,1]])
res=[clean(z) for z in (c*N*sp.eye(4)-hc(A))*vec]
assert res==[0]*4
phi=clean(A.det()+kappa*sp.trace(A)**2)
assert phi==0
nil=sp.Matrix([[0,1],[0,0]])
nil_char=sp.factor(hc(nil).charpoly().as_expr(),extension=s)
assert clean(hc(nil).trace()-sp.Rational(3,2)-c-(3-s)/4)==0

# Curvature equation after division by u: e/u=1/[u*v-2*kappa*u*(u-v)].
e_over_u=clean(1/(u2*(rho-2*kappa*(1-rho))))
assert clean(e_over_u-(-4+4*s/3))==0
phi_a=clean(-rho+2*kappa*(1-rho))
phi_d=clean(1+2*kappa*(1-rho))
assert clean(phi_a-rho*phi_d)==0 and phi_d!=0

def hessian(n):
    a=sp.diag(1,-rho,*([0]*(n-2)))
    P=sp.kronecker_product(a.T,sp.eye(n)); Q=sp.kronecker_product(sp.eye(n),a)
    L=P-Q; M=P-Q/2
    top=n
    e=sp.zeros(n*n,1); e[top]=1
    H0=(L.T.conjugate()*M+M.T.conjugate()*L)/2
    lam=clean(H0[top,top]); N=clean(1+rho*rho)
    assert clean(lam-c*N)==0
    gaps=[clean(lam-H0[j,j]) for j in range(n*n)]
    directions=[]; labels=[]; lv=[]; mv=[]; fv=[]
    for i in range(n):
        for j in range(n):
            for z,label in [(1,'Re'),(sp.I,'Im')]:
                d=sp.zeros(n); d[i,j]=z
                p=sp.kronecker_product(d.T,sp.eye(n)); q=sp.kronecker_product(sp.eye(n),d)
                l=p-q; m=p-q/2
                v=(l.T.conjugate()*M*e+L.T.conjugate()*m*e+m.T.conjugate()*L*e+M.T.conjugate()*l*e)/2
                directions.append(d); labels.append(f'{label}A{i+1}{j+1}'); lv.append(l*e); mv.append(m*e)
                fv.append(v.applyfunc(clean))
                ni=2*sp.re(sp.trace(a.T.conjugate()*d))
                assert clean(v[top]-c*ni)==0
    size=2*n*n; gh=sp.zeros(size)
    for i in range(size):
        for j in range(i,size):
            direct=sp.re((lv[i].T.conjugate()*mv[j]+lv[j].T.conjugate()*mv[i])[0])
            mix=0
            for r in range(n*n):
                if r!=top and fv[i][r]!=0 and fv[j][r]!=0:
                    mix+=2*sp.re(sp.conjugate(fv[i][r])*fv[j][r])/gaps[r]
            gh[i,j]=gh[j,i]=clean((direct+mix-(2*c if i==j else 0))/(N*u2))
    expected=sp.zeros(size)
    def ind(i,j,k=0):return 2*(i*n+j)+k
    nonzero=[-2,-sp.Rational(5,6)-7*s/30,-sp.Rational(5,9)-13*s/90,-1-3*s/10]
    # Active diagonal block: kernel vector (1,-rho).
    for k in (0,1):
        i,j=ind(0,0,k),ind(1,1,k)
        block=-2/(1+rho*rho)*sp.Matrix([[rho*rho,rho],[rho,1]])
        for r in range(2):
            for z in range(2):expected[[i,j][r],[i,j][z]]=clean(block[r,z])
    for aindex,eig in [(0,nonzero[1]),(1,nonzero[2])]:
        for spectator in range(2,n):
            for k in (0,1):
                i,j=ind(aindex,spectator,k),ind(spectator,aindex,k)
                sign=1 if k==0 else -1
                expected[i,i]=expected[j,j]=eig/2
                expected[i,j]=expected[j,i]=-sign*eig/2
    for i in range(2,n):
        for j in range(2,n):
            for k in (0,1):expected[ind(i,j,k),ind(i,j,k)]=nonzero[3]
    assert all(clean(z)==0 for z in gh-expected)
    # The two active off-diagonal entries are arbitrary complex tangents.
    assert all(gh[ind(0,1,k),j]==0 and gh[ind(1,0,k),j]==0 for k in (0,1) for j in range(size))
    mult=[2,2*(n-2),2*(n-2),2*(n-2)**2]
    return {'n':n,'real_dimension':size,'negative_rank':sum(mult),'nullity':size-sum(mult),
            'expected_normal_eigenvalues':[str(x) for x in nonzero],
            'multiplicities':mult,'full_hessian_entrywise_exact_match':True,
            'stationary_gradient_exact_match':True}

out={'scope':'q=1/2 only; equality pairs and independent exact Hessians at embedded published witness',
     'schur_pair_kernel_residuals':[str(z) for z in res],
     'schur_Phi_residual':str(phi),'nilpotent_H_characteristic_polynomial':str(nil_char),
     'second_order_correction_e_over_u':str(e_over_u),
     'active_tangent_relation':'delta A22=-rho delta A11; both offdiagonal entries arbitrary complex',
     'hessian_checks':[]}
for n in [3,4]:
    print('checking_n =',n,flush=True)
    out['hessian_checks'].append(hessian(n))
print(json.dumps(out,indent=2,sort_keys=True))
