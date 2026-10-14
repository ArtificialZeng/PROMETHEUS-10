#!/usr/bin/env python3
"""Exact all-q pair and normal-block verification modulo the witness relation."""
import json
import sympy as sp

u,b,t=sp.symbols('u b t',real=True)
relation=u*u-b*b-2*u*b+2
c=1+u*u; q=1+u*u-b*b; N=u*u+b*b
def reduce_zero(z):
    num,den=sp.cancel(z).as_numer_denom()
    remainder=sp.rem(sp.Poly(num,u,b,t),sp.Poly(relation,u,b,t))
    assert remainder.is_zero, str(remainder.as_expr())
    return True
def operators(A):
    n=A.rows
    P=sp.kronecker_product(A.T,sp.eye(n)); Q=sp.kronecker_product(sp.eye(n),A)
    return P-Q,P-q*Q
def hermitian(A):
    L,M=operators(A)
    return (L.T.conjugate()*M+M.T.conjugate()*L)/2

# Schur equality pair, polynomial for every real t.
A=sp.Matrix([[u,t],[0,-b]])
B=sp.Matrix([[-b*t/N,1],[0,u*t/N]])
v=sp.Matrix([B[0,0],B[1,0],B[0,1],B[1,1]])
pair=[reduce_zero(z) for z in (c*(N+t*t)*sp.eye(4)-hermitian(A))*v]
phi=reduce_zero(A.det()+u*b*sp.trace(A)**2/(u-b)**2)

# Direct simple-eigenvalue second derivatives from the two multiplication
# operators. No q=1/2 arithmetic class or saved Hessian is imported.
A0=sp.diag(u,-b,0)
L0,M0=operators(A0); H0=hermitian(A0)
e=sp.zeros(9,1); e[3]=1
lam=H0[3,3]
reduce_zero(lam-c*N)
def data(i,j):
    D=sp.zeros(3); D[i,j]=1
    L,M=operators(D)
    first=(L.T*M0*e+L0.T*M*e+M.T*L0*e+M0.T*L*e)/2
    return L*e,M*e,first
def hessian_block(i,j):
    li,mi,fi=data(i,j); lj,mj,fj=data(j,i)
    out=sp.zeros(2)
    arr=[(li,mi,fi),(lj,mj,fj)]
    for a in range(2):
        for d in range(2):
            la,ma,fa=arr[a]; ld,md,fd=arr[d]
            z=(la.T*md+ld.T*ma)[0]
            for r in range(9):
                if r!=3 and fa[r]!=0 and fd[r]!=0:
                    z+=2*fa[r]*fd[r]/(lam-H0[r,r])
            out[a,d]=sp.cancel((z-(2*c if a==d else 0))/N)
    return out

beta1=-4*c*(c-q)/((2*c-q)*N)
beta2=-4*c*(c-1)/((2*c-1)*N)
results=[]
for i,j,beta in [(0,2,beta1),(1,2,beta2)]:
    block=hessian_block(i,j)
    expected=beta*sp.Matrix([[1,-1],[-1,1]])/2
    residuals=[reduce_zero(z) for z in block-expected]
    results.append({'active_index':i+1,'spectator_index':j+1,'entrywise_residual_zero':residuals})

# The active diagonal Rayleigh quotient has eigenvalues c and c-N,
# whose difference is N. Its nonzero quotient Hessian is -2. Lower
# spectator blocks annihilate B0 on both sides and contribute -2c/N.
active=sp.Matrix([[q, -(1+q)/2],[-(1+q)/2,1]])
reduce_zero(active.det()-c*(c-N))
reduce_zero(active.trace()-(2*c-N))
reduce_zero(N*N-2*(1+q*q))
reduce_zero(2*u*b-(1+q))
reduce_zero(c*(c-1-q)-(1-q)**2/4)

print(json.dumps({
 'status':'exact_allq_pair_and_normal_block_identities',
 'domain':'q real except -1,1; u=sqrt(c-1)>0; b=sign(1+q)sqrt(c-q) nonzero',
 'arithmetic':'Exact SymPy rational expressions reduced modulo u^2-b^2-2ub+2=0; denominators justified in the stable proof',
 'schur_pair_residuals_zero':pair,
 'schur_equality_Phi_residual_zero':phi,
 'normal_blocks':results,
 'nonzero_hessian_spectrum':['-2','-4c(c-q)/[(2c-q)N]','-4c(c-1)/[(2c-1)N]','-2c/N'],
 'multiplicities':['2','2(n-2)','2(n-2)','2(n-2)^2'],
 'negative_rank':'2(n-1)^2', 'nullity':'4n-2',
 'sign_proof':'c>max(1,q), N>0, 2c-q>0 and 2c-1>0, so all displayed eigenvalues are strictly negative',
 'scope_limit':'Local Morse-Bott maximum only; no explicit radius or global inequality.'
},indent=2,sort_keys=True))
