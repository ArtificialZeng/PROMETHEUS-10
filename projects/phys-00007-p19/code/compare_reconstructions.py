#!/usr/bin/env python3
"""Compare independent output files with the explicit k <-> N-q basis map."""
from pathlib import Path
import json
import sys
from math import comb,sqrt
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
z=s.Symbol('z',nonzero=True)

def parse(value): return s.sympify(value,locals={'z':z})
def matrix(rows): return s.Matrix([[parse(v) for v in row] for row in rows])

def full_trace_numeric(c,t):
    # Computational representation, |1> up, retaining first t bits.
    N=len(c)-1
    psi=np.array([c[x.bit_count()]/sqrt(comb(N,x.bit_count())) for x in range(1<<N)])
    wave=psi.reshape(1<<t,1<<(N-t))
    rho=wave@wave.conj().T
    D=np.zeros((1<<t,t+1))
    for x in range(1<<t): D[x,x.bit_count()]=1/sqrt(comb(t,x.bit_count()))
    return D.T@rho@D

def down_trace_numeric(b,t):
    # Separate descending-basis sum over environmental down counts.
    N=len(b)-1
    result=np.zeros((t+1,t+1),dtype=complex)
    for a in range(t+1):
        for ap in range(t+1):
            for e in range(N-t+1):
                factor=comb(N-t,e)*sqrt(comb(t,a)*comb(t,ap)/(comb(N,a+e)*comb(N,ap+e)))
                result[a,ap]+=factor*b[a+e]*b[ap+e].conjugate()
    return result[::-1,::-1]

def main():
    a=json.loads((ROOT/'evidence/reproduce-20261012-output-a.json').read_text())
    b=json.loads((ROOT/'evidence/reproduce-20261012-output-b.json').read_text())
    assert a['N']==b['N']==9
    c=[parse(v) for v in a['coefficients_k']]
    down=[parse(v) for v in b['coefficients_q']]
    for k in range(10): assert s.simplify(c[k]-down[9-k])==0
    print('Coefficient map: q=9-k, b_q=c_(9-q); all 10 exact coefficient residuals zero.')
    print('Retained basis: R_t[a,r]=delta_(a,t-r); rho_A=R_t.T*rho_B*R_t.')
    checked=0
    for t in range(1,5):
        A=matrix(a['marginals'][str(t)]['rho_sym'])
        B=matrix(b['marginals'][str(t)]['rho_down'])
        R=s.Matrix(t+1,t+1,lambda aa,rr: s.S.One if aa==t-rr else s.S.Zero)
        mapped=R.T*B*R
        for r in range(t+1):
            for col in range(t+1):
                residual=s.simplify(A[r,col]-mapped[r,col])
                assert residual==0,(t,r,col,residual)
                checked+=1
            print(f't={t} row {r}: {list(A.row(r))}; exact B-mapped row residuals all zero.')
        for key in ('purity','A'):
            residual=s.simplify(parse(a['marginals'][str(t)][key])-parse(b['marginals'][str(t)][key]))
            assert residual==0
        if t==3:
            assert s.simplify(s.trace(A*A)-s.Rational(789,3136))==0
            assert s.simplify(s.trace(A*A)-s.Rational(1,4))==s.Rational(5,3136)
    # Two-qubit full-space identity is the symmetric projector, not I_4/4.
    full2=matrix(a['marginals']['2']['rho_full'])
    swap=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    assert full2==(s.eye(4)+swap)/6
    assert full2!=s.eye(4)/4
    # Exact rho_1 compatibility, tracing the last qubit of full rho_2.
    rho1=s.Matrix(2,2,lambda r,col: sum(full2[2*r+e,2*col+e] for e in range(2)))
    assert rho1==matrix(a['marginals']['1']['rho_full'])
    print(f'Exact comparison PASS: {checked} marginal entries, 10 coefficients, all A1--A4/purities; rho2=P_sym/3; Tr_one(rho2)=rho1.')
    # Dense probes prevent a sparse-state coincidence from masking indexing errors.
    rng=np.random.default_rng(190908355)
    probes=[]
    coherent=np.zeros(10,dtype=complex); coherent[9]=1
    cat=np.zeros(10,dtype=complex); cat[0]=cat[9]=1/sqrt(2)
    probes += [('coherent',coherent),('GHZ',cat)]
    for i in range(5):
        v=rng.normal(size=10)+1j*rng.normal(size=10)
        probes.append((f'dense-{i}',v/np.linalg.norm(v)))
    maxres=0.0
    tolerance=2e-14
    minimum_eigenvalue=1.0
    for name,v in probes:
        for t in range(1,5):
            A=full_trace_numeric(v,t)
            B=down_trace_numeric(v[::-1],t)
            error=float(np.max(np.abs(A-B)))
            maxres=max(maxres,error)
            mineig=float(np.linalg.eigvalsh(A).min())
            minimum_eigenvalue=min(minimum_eigenvalue,mineig)
            assert error<tolerance,(name,t,error)
            assert abs(np.trace(A)-1)<tolerance
            assert mineig>-tolerance
    print(f'Numerical algorithm stress checks: {len(probes)} probes x 4 marginals; seed=190908355; complex128; tolerance={tolerance:.2e}; max entry difference={maxres:.17g}; min eigenvalue={minimum_eigenvalue:.17g}.')
    print('These finite stress checks are not an optimization, a strict interval certificate or a global-bound proof.')
    summary={'exact_comparison':'pass','entries_compared':checked,'coefficient_entries':10,
             'basis_map':'q=9-k; rho_A=R_t.T*rho_B*R_t, R_t[a,r]=delta_(a,t-r)',
             'baseline':{'A1':'1','A2':'1','A3':'2347/2352','purity3':'789/3136','purity_gap_to_1_over_4':'5/3136',
                         'A4':'5*(355609+175*sqrt(273)*cos(2*chi))/1806336'},
             'numerical_stress':{'probes':len(probes),'marginals_per_probe':4,'dtype':'complex128','seed':190908355,
                                 'tolerance':tolerance,'max_entry_residual':maxres,'minimum_eigenvalue':minimum_eigenvalue},
             'limitations':'Same agent and symbolic library; no fresh referee, no global optimization or proof of the universal conditioned bound.'}
    (ROOT/'evidence/reproduce-20261012-comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
    (ROOT/'evidence/reproduce-20261012-environment.json').write_text(json.dumps({
        'python':sys.version,'executable':sys.executable,'sympy':s.__version__,'numpy':np.__version__,
        'commands':['python code/reproduce_full_qubit_a.py','python code/reproduce_schmidt_b.py','python code/compare_reconstructions.py'],
        'dependency_requirement':'Python 3.10 or later with SymPy and NumPy; no package installed during this job.'},indent=2)+'\n')

if __name__=='__main__': main()
