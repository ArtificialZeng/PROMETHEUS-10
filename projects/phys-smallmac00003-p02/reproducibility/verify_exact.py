"""Portable exact manuscript check. Adapted from a separate symbolic replay.
This execution is not a new independent scientific audit.
"""
import json, sys, time, platform
from pathlib import Path
import sympy as s
import argparse
_parser = argparse.ArgumentParser()
_parser.add_argument("--output-dir", default="replay-output")
_output = Path(_parser.parse_args().output_dir).resolve()
_output.mkdir(parents=True, exist_ok=True)

start = time.monotonic()
I = s.I
R = s.Rational
eye = s.eye
zero = s.zeros
checks = []
def simp(A):
    return A.applyfunc(s.simplify) if isinstance(A, s.MatrixBase) else s.simplify(A)
def check(name, expr):
    ok = expr is True or expr == True
    checks.append({'name': name, 'pass': bool(ok)})
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)
    if not ok:
        raise AssertionError(name)
def meq(A, B):
    return simp(A-B) == zero(*A.shape)
def f2(A):
    return s.expand(s.trace(A.conjugate().T*A))

pauli = [eye(2), s.Matrix([[0,1],[1,0]]), s.Matrix([[0,-I],[I,0]]), s.diag(1,-1)]
# Columns are |11>, (|01>+|10>)/sqrt(2), |00>: fixed m=-1,0,+1.
V = s.Matrix([[0,0,1],[0,1/s.sqrt(2),0],[0,1/s.sqrt(2),0],[1,0,0]])
S = [[simp(V.T*s.kronecker_product(a,b)*V) for b in pauli] for a in pauli]
J = S[0][1:]
check('symmetric isometry', meq(V.T*V,eye(3)))
check('Jz and positive ladder convention', meq(J[2],s.diag(-1,0,1)) and meq(J[0]+I*J[1],s.Matrix([[0,0,0],[s.sqrt(2),0,0],[0,s.sqrt(2),0]])))
for a in range(3):
    for b in range(3):
        check('Pauli compression equals spin moment S%d%d'%(a+1,b+1), meq(S[a+1][b+1],J[a]*J[b]+J[b]*J[a]-(eye(3) if a==b else zero(3))))
def moments(rho):
    return simp(s.Matrix(4,4,lambda a,b:s.trace(rho*S[a][b])))
def inverse(X):
    return simp(sum((X[a,b]*S[a][b]/4 for a in range(4) for b in range(4)),zero(3)))
def tangent(A):
    return A-s.diag(A[0,0],*([sum(A[k,k] for k in range(1,4))/3]*3))
u=s.symbols('u0:8',real=True)
D=s.Matrix([[u[0],u[2]+I*u[3],u[4]+I*u[5]],
            [u[2]-I*u[3],u[1],u[6]+I*u[7]],
            [u[4]-I*u[5],u[6]-I*u[7],-u[0]-u[1]]])
Xd=moments(D)
check('generic complex traceless inverse identity',meq(inverse(Xd),D))
check('generic Hilbert-Schmidt metric factor 1/4',s.expand(f2(Xd)-4*f2(D))==0)
check('generic affine trace and 00 identities',Xd[0,0]==0 and s.trace(Xd)==0)
a,b=s.symbols('a b', real=True)
v=s.Matrix([a,0,0,b]); B=v*v.T
Gamma=simp(sum((v[i]*v[j]*S[i][j] for i in range(4) for j in range(4)),zero(3)))
check('Gamma spectrum after a spatial rotation',meq(Gamma,s.diag((a-b)**2,a*a-b*b,(a+b)**2)))
k=s.factor(f2(tangent(B)))
check('normal norm before normalization',s.factor(k-(2*a*a*b*b+R(2,3)*b**4))==0)
r=s.symbols('r',real=True)
kappa=R(2,3)*(1-r)*(1+2*r)
check('kappa minus 2/3 factorization',s.expand(kappa-R(2,3)-R(2,3)*r*(1-2*r))==0)
check('Frobenius orthogonal projection',s.simplify(s.trace(B*tangent(B))-k)==0)

E3=s.diag(0,0,0,1)
examples=[
 ('published_lambda_minus_one',s.diag(0,1,0),s.diag(1,R(1,2),R(1,2),0),R(3,2)*E3,R(3,8)),
 ('submitted_zero_dipole',s.Matrix([[R(1,10),0,R(1,20)],[0,R(4,5),0],[R(1,20),0,R(1,10)]]),s.diag(1,R(3,5),R(2,5),0),R(9,10)*E3,R(27,200)),
 ('submitted_nonzero_dipole',s.diag(R(4,9),R(23,45),R(2,45)),s.Matrix([[1,0,0,-R(1,3)],[0,R(4,9),0,0],[0,0,R(4,9),0],[-R(1,3),0,0,R(1,9)]]),s.Matrix([R(1,3),0,0,1])*s.Matrix([[R(1,3),0,0,1]])/5,R(2,225)),
 # Deliberately outside the physical state space: tests the claimed necessity
 # of target positivity. This is NOT a counterexample to the source conjecture.
 ('nonphysical_target_control',s.diag(-R(1,4),R(3,2),-R(1,4)),s.diag(1,R(1,2),R(1,2),0),3*E3,R(3,2))]
records=[]
for name,rho,W,Z,q2 in examples:
    X=moments(rho); sigma=inverse(W)
    check(name+' exact normal-cone stationarity',meq(X-W,-tangent(Z)))
    check(name+' complementarity',meq(W*Z,zero(4)))
    check(name+' rank3 feasible classical matrix',W.rank()==3 and W.is_positive_semidefinite is True and W[0,0]==1 and s.trace(W)==2)
    check(name+' exact density and Bloch distances',s.simplify(f2(rho-sigma)-q2)==0 and s.simplify(f2(X-W)/4-q2)==0)
    check(name+' density positivity',rho.is_positive_semidefinite is (name!='nonphysical_target_control'))
    vv=W.nullspace()[0]; rr=s.simplify(vv[0]**2/(vv.dot(vv)))
    eig=X.eigenvals(); lam=min(eig,key=lambda x:float(x.evalf()))
    difference=s.simplify(R(3,8)*lam**2-q2)
    check(name+' bound and equality condition',bool(difference>=0) and ((difference==0)==(rr==0)))
    records.append({'name':name,'rho_eigenvalues':{str(x):n for x,n in rho.eigenvals().items()},'lambda':str(lam),'Q_squared':str(q2),'kernel_time_square':str(rr),'bound_squared_margin':str(difference)})

# A rational complex SU(2) rotation on the nonzero-dipole example; no real-only test.
U=s.Matrix([[1+2*I,3+4*I],[-3+4*I,1-2*I]])/s.sqrt(30)
check('complex SU2 unitary',meq(U*U.conjugate().T,eye(2)) and s.simplify(U.det()-1)==0)
Uspin=simp(V.T*s.kronecker_product(U,U)*V)
Rot=simp(s.Matrix(3,3,lambda a,b:s.trace(pauli[a+1]*U*pauli[b+1]*U.conjugate().T)/2))
Rot4=s.diag(1,Rot)
rho,W,Z,q2=examples[2][1:]
rho_rot=simp(Uspin*rho*Uspin.conjugate().T)
W_rot=simp(Rot4*W*Rot4.T); Z_rot=simp(Rot4*Z*Rot4.T)
check('complex rotation moment covariance',meq(moments(rho_rot),Rot4*moments(rho)*Rot4.T))
check('complex rotation retains exact projection',meq(moments(rho_rot)-W_rot,-tangent(Z_rot)) and meq(W_rot*Z_rot,zero(4)))
check('complex rotation retains norm',s.simplify(f2(rho_rot-inverse(W_rot))-q2)==0)

out={'provenance':'portable copy of separate symbolic replay','method':'fresh Pauli compression and exact symbolic normal-cone certificates','source_files_read_by_code':[], 'python':sys.version,'sympy':s.__version__,'platform':platform.platform(),'checks':checks,'examples':records,'wall_seconds':time.monotonic()-start,'numeric_sdp_is_proof':False}
(_output / 'exact-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_pass':all(c['pass'] for c in checks),'check_count':len(checks),'wall_seconds':out['wall_seconds'],'examples':records},indent=2),flush=True)
