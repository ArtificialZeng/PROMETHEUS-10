"""Portable exact manuscript check. Adapted from a separate symbolic replay.
This execution is not a new independent scientific audit.
"""
import json
from pathlib import Path
import sympy as s
import argparse
_parser = argparse.ArgumentParser()
_parser.add_argument("--output-dir", default="replay-output")
_output = Path(_parser.parse_args().output_dir).resolve()
_output.mkdir(parents=True, exist_ok=True)
R=s.Rational
checks=[]
def check(name,ok):
    checks.append({'name':name,'pass':bool(ok)})
    print(('PASS ' if ok else 'FAIL ')+name)
    assert ok,name
def norm2(A): return s.simplify(s.trace(A.conjugate().T*A))
def pt(A):
    return s.Matrix(4,4,lambda i,j:A[2*(i//2)+j%2,2*(j//2)+i%2])
bell=s.Matrix([0,1,1,0])/s.sqrt(2)
B=bell*bell.T
sep=B/3+s.eye(4)/6
check('general separable candidate PSD and trace one',sep.is_positive_semidefinite and s.trace(sep)==1)
check('general separable candidate PPT',pt(sep).eigenvals()=={s.Integer(0):1,R(1,3):3})
check('general separable distance squared 1/3',norm2(B-sep)==R(1,3))
singlet=s.Matrix([0,1,-1,0])/s.sqrt(2)
check('general optimum has antisymmetric population 1/6',(singlet.T*sep*singlet)[0]==R(1,6))
V=s.Matrix([[0,0,1],[0,1/s.sqrt(2),0],[0,1/s.sqrt(2),0],[1,0,0]])
classical=V*s.diag(R(1,4),R(1,2),R(1,4))*V.T
check('supported classical distance squared 3/8',norm2(B-classical)==R(3,8))
check('supported state has zero antisymmetric population',(singlet.T*classical*singlet)[0]==0)
# For every separable T, Tr(B*T)<=1/2. Hence
# Tr[(B-sep)*(T-sep)]=(2/3)(Tr(B*T)-1/2)<=0.
check('general optimizer normal witness',s.simplify(s.trace((B-sep)*sep))==R(1,6))

# A nonpositive Hermitian target with lambda still in the physical interval.
rho=s.Matrix([[R(1,10),0,-R(1,5)],[0,R(4,5),0],[-R(1,5),0,R(1,10)]])
Jz=s.diag(-1,0,1)
Jx=s.Matrix([[0,1,0],[1,0,1],[0,1,0]])/s.sqrt(2)
Jy=s.Matrix([[0,s.I,0],[-s.I,0,s.I],[0,-s.I,0]])/s.sqrt(2)
J=[Jx,Jy,Jz]
X=s.zeros(4); X[0,0]=s.trace(rho)
for a in range(3):
    X[0,a+1]=X[a+1,0]=s.trace(rho*J[a])
    for b in range(3):
        X[a+1,b+1]=s.trace(rho*(J[a]*J[b]+J[b]*J[a]-(s.eye(3) if a==b else s.zeros(3))))
W=s.diag(1,R(1,10),R(9,10),0)
Z=s.diag(0,0,0,R(9,10))
PZ=Z-s.diag(Z[0,0],*([s.trace(Z[1:4,1:4])/3]*3))
check('unphysical target eigenvalues',rho.eigenvals()=={R(-1,10):1,R(3,10):1,R(4,5):1})
check('unphysical target has lambda=-3/5',X==s.diag(1,R(2,5),R(6,5),R(-3,5)))
check('unphysical target exact K projection',X-W==-PZ and W*Z==s.zeros(4) and W.rank()==3)
check('unphysical target saturates linear ratio',norm2(X-W)/4==R(27,200))

# Generic rotated kernel: v=(a,0,0,b), b!=0. Wv=0 and W00=1
# give W03=-a/b and W33=a^2/b^2. trace(W_sp)=1 then gives
# W11+W22=(b^2-a^2)/b^2. Nonnegative diagonal entries force
# a^2<=b^2. Equality annihilates rows 1,2 by PSD and leaves
# the rank-one 0,3 block. rank(W)=3 therefore forces a^2<b^2.
a,b=s.symbols('a b',real=True,nonzero=True)
block=s.Matrix([[1,-a/b],[-a/b,a*a/(b*b)]])
check('kernel-block determinant identically zero',s.simplify(block.det())==0)
check('kernel-block equation',s.simplify(block*s.Matrix([a,b]))==s.zeros(2,1))
out={'provenance':'portable copy of separate symbolic replay','checks':checks,'all_pass':all(x['pass'] for x in checks),'bound_uses_target_positivity':False,'physical_positivity_remains_used_for_rank1_exclusion':True,'free_sets_equal':False,'new_scientific_counterexample_claim':False}
(_output / 'scope-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
