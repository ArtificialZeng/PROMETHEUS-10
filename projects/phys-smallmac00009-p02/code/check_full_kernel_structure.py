#!/usr/bin/env python3
"""Input-A replay of the full-kernel proof's finite algebraic steps.

Does not read input B, the membership solver answer, or the previous six-support
certificate. The 26-dimensional input-A kernel is intersected with annihilator
conditions, unlike the original compressed input-B construction. Same agent,
same SymPy library: this is a certificate replay, not a fresh referee.
"""
from pathlib import Path
from itertools import combinations_with_replacement, permutations
from datetime import datetime, timezone
import json,time,hashlib
import sympy as s

ROOT=Path(__file__).resolve().parents[1]; START=time.monotonic()
A=json.loads((ROOT/'evidence/input-a.json').read_text())
ks=[s.Matrix(m) for m in A['kernel_matrices']]
ops=[s.Matrix(o['matrix']) for o in A['operators']]
e=s.eye(8)
U=s.Matrix.hstack(e[:,0],e[:,1]+e[:,2]+e[:,4],e[:,3]+e[:,5]+e[:,6],e[:,7])
V=s.Matrix.hstack(e[:,1]-e[:,2],e[:,1]+e[:,2]-2*e[:,4],
                 e[:,3]-e[:,5],e[:,3]+e[:,5]-2*e[:,6])
assert U.T*V==s.zeros(4) and s.Matrix.hstack(U,V).det()!=0
for K in ks:
    assert K==K.H and K.trace()==0
    assert all(s.trace(K*O)==0 for O in ops)
    assert U.T*K*U==s.zeros(4)
    C=U.T*K*V
    eq=[C[3,0]-(-s.conjugate(C[0,2])+s.conjugate(C[0,3]))/2,
        C[3,1]-(3*s.conjugate(C[0,2])+s.conjugate(C[0,3]))/2,
        s.re(C[2,2])-(-s.re(C[1,0])+s.re(C[1,1]))/2,
        s.re(C[2,3])-(3*s.re(C[1,0])+s.re(C[1,1]))/2,
        C[3,2]-s.conjugate(C[1,2])-(s.conjugate(C[0,0])-s.conjugate(C[0,1])-C[2,0]+C[2,1])/2,
        C[3,3]-s.conjugate(C[1,3])-(-3*s.conjugate(C[0,0])-s.conjugate(C[0,1])+3*C[2,0]+C[2,1])/2]
    assert all(s.expand(v)==0 for v in eq)
print('PASS: all 26 input-A kernel generators, 37 measurement constraints, zero symmetric block and six displayed complex/real cross relations',flush=True)

def annihilator_matrix(bases, vectors):
    return s.Matrix.hstack(*[s.Matrix([part(v) for w in vectors for v in K*w for part in (s.re,s.im)]) for K in bases])

# First remove endpoint rows in the full 26-dimensional input-A basis.
E=annihilator_matrix(ks,[e[:,0],e[:,7]])
ES=E.nullspace(); assert len(ES)==14
end_bases=[sum((v*B for v,B in zip(c,ks)),s.zeros(8)) for c in ES]
assert all(K*e[:,0]==s.zeros(8,1) and K*e[:,7]==s.zeros(8,1) for K in end_bases)
r=s.symbols('r',real=True)
S1=U[:,1]; S2=U[:,2]
records=[]
for tag,ww in [('finite_nonzero',[r*S1-S2]),('zero',[S2]),('infinite',[S1]),('zero_cross',[S1,S2])]:
    Z=annihilator_matrix(end_bases,ww)
    ns=Z.nullspace()
    B=[sum((v*K for v,K in zip(c,end_bases)),s.zeros(8)).applyfunc(s.cancel) for c in ns]
    N=s.Matrix.hstack(*ns)
    piv=Z.rref()[1]; rows=Z[:,list(piv)].T.rref()[1]
    det=s.factor(Z.extract(rows,piv).det())
    free=[j for j in range(14) if j not in piv]
    assert N.extract(free,range(len(ns)))==s.eye(len(ns))
    assert (Z*N).applyfunc(s.cancel)==s.zeros(Z.rows,N.cols)
    denoms=sorted(set(str(s.factor(s.denom(s.cancel(v)))) for v in N))
    if tag=='finite_nonzero':
        assert len(B)==6
        # Prove det has no nonzero real roots; report the actual factorization.
        constant,factors=s.factor_list(det,r)
        assert constant!=0
        for f,power in factors:
            assert f==r or (s.degree(f,r)==2 and s.discriminant(f,r)<0)
        for c in N:
            dd=s.denom(s.cancel(c))
            assert s.Poly(dd,r).is_monomial
        domain='all real r !=0; determinant factors only r and real quadratics with negative discriminant; denominators are monomials in r'
    else:
        assert det!=0 and not det.has(r) and denoms==['1']
        assert len(B)==(4 if tag=='zero_cross' else 6)
        domain='fixed degenerate branch; nonzero constant maximal minor'
    # Polarize: check each homogeneous cubic coefficient separately.
    counts=0
    for inds in combinations_with_replacement(range(len(B)),3):
        coefficient=sum((s.trace(B[i]*B[j]*B[k]) for i,j,k in set(permutations(inds))),s.S(0))
        assert s.cancel(coefficient)==0,(tag,inds,coefficient)
        counts+=1
    records.append({'branch':tag,'annihilators':[[str(v) for v in w] for w in ww],
      'dimension':len(B),'maximal_minor_rows':list(rows),'maximal_minor_cols':list(piv),
      'maximal_minor':str(det),'nullspace_denominators':denoms,'parameter_domain':domain,
      'independence':'free-coordinate submatrix equals identity; Z*N=0; maximal minor lower-bounds rank at every admitted parameter',
      'basis':[[[str(v) for v in row] for row in K.tolist()] for K in B],
      'polarized_cubic_coefficients_checked':counts,'all_exactly_zero':True})
    print('PASS',tag,'dimension',len(B),'minor',det,'polarized coefficients',counts,flush=True)

# Known two-qubit collision embedded with a third |0>, to replay the explicit
# second-pure endpoint formula on a nontrivial PSD segment.
p=s.kronecker_product(s.Matrix([1,-1,1,1])/2,s.Matrix([1,0]))
q=s.kronecker_product(s.Matrix([1,1,-1,1])/2,s.Matrix([1,0]))
P=p*p.H;Q=q*q.H;K=(Q-P)/2;rho=P+K
assert all(s.trace(O*K)==0 for O in ops)
t=-2*s.trace(P*K)/s.trace(K*K)
assert t==2 and P+t*K==Q and rho*rho==rho/2
print('PASS known two-qubit pair embedded in three qubits: mixed segment and exact second-pure formula t=2',flush=True)
record={'job_id':'phys-smallmac00009-p02-research-10b8522d8222','completed_at':datetime.now(timezone.utc).isoformat(),
 'input':'evidence/input-a.json','input_sha256':hashlib.sha256((ROOT/'evidence/input-a.json').read_bytes()).hexdigest(),
 'full_kernel_generators':26,'cross_relations_per_generator':6,'zero_endpoint_kernel_dimension':14,
 'chart_records':records,'known_collision_endpoint_parameter':str(t),
 'arithmetic':'Exact rational functions and coefficient polarization, SymPy '+s.__version__,
 'elapsed_seconds':time.monotonic()-START,
 'coverage':'Finite algebra in the structural proof; SU(2) covariance, projective-root/antipodal argument and PSD spectral argument require mathematical reading of the proof.',
 'independence':'Full input-A 26-coordinate intersection, not old input-B supported-unit generator or cached six-support bases; same agent and CAS; no fresh referee or human review.'}
(ROOT/'evidence/check-full-kernel-structure-v1.json').write_text(json.dumps(record,indent=2)+'\n')
print('COMPLETED seconds',time.monotonic()-START,flush=True)
