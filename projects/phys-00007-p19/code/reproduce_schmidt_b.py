#!/usr/bin/env python3
"""Input B only: separately transcribed weights and down-spin Schmidt trace."""
from pathlib import Path
import json
from math import comb
import sympy as sym

BASE=Path(__file__).resolve().parents[1]
z=sym.Symbol('z', nonzero=True)

def adjoint_entry(v):
    return sym.conjugate(v).subs(sym.conjugate(z),1/z)

def simplify(v):
    return sym.cancel(sym.expand(v))

def matrix_strings(M):
    return [[str(v) for v in row] for row in M.tolist()]

def main():
    path=BASE/'evidence/reproduce-20261012-input-b.json'
    data=json.loads(path.read_text())
    n=data['N']
    b=[sym.S.Zero for _ in range(n+1)]
    for item in data['occupied_down_counts']:
        weight=sym.Rational(item['probability'])
        phase=sym.sympify(item['phase'],locals={'z':z})
        b[item['q']]=sym.sqrt(weight)*phase
    norm=simplify(sum(v*adjoint_entry(v) for v in b))
    assert norm==1
    marginals={}
    for retained in range(1,5):
        discarded=n-retained
        # Independent grouping by down-spin counts; no computational-space array.
        M=sym.zeros(retained+1,discarded+1)
        for a in range(retained+1):
            for e in range(discarded+1):
                q=a+e
                count=sym.Rational(comb(retained,a)*comb(discarded,e),comb(n,q))
                M[a,e]=b[q]*sym.sqrt(count)
        rho=(M*M.applyfunc(adjoint_entry).T).applyfunc(simplify)
        assert simplify(sym.trace(rho))==1
        assert (rho-rho.applyfunc(adjoint_entry).T).applyfunc(simplify)==sym.zeros(retained+1)
        purity=simplify(sum(rho[a,bx]*rho[bx,a] for a in range(retained+1) for bx in range(retained+1)))
        A=simplify(sym.Rational(retained+1,retained)*(1-purity))
        if retained<=3:
            expected=sym.Rational(data['purities_derived_from_published_A'][f't{retained}'])
            assert purity==expected
        if retained<=2:
            assert rho==sym.eye(retained+1)/sym.Integer(retained+1)
        if retained==4:
            expected=sym.sympify(data['published_A4'],locals={'z':z})
            assert simplify(A-expected)==0,(A,expected)
        marginals[str(retained)]={'schmidt_matrix':matrix_strings(M),'rho_down':matrix_strings(rho),
                                 'purity':str(purity),'A':str(A),'trace':'1','source_residual':'0'}
        print(f'B: t={retained}; purity={purity}; A_t={A}; exact published residual=0',flush=True)
    # Vandermonde's identity checks the normalized decomposition for every q.
    for t in range(1,n+1):
        for q in range(n+1):
            count=sum(comb(t,a)*comb(n-t,q-a) for a in range(t+1) if 0<=q-a<=n-t)
            assert count==comb(n,q)
    result={'implementation':'independent descending-basis Schmidt/binomial trace; no input A or A-output read',
            'input_file':str(path.relative_to(BASE)),'N':n,'norm':str(norm),
            'coefficients_q':[str(v) for v in b],'marginals':marginals,
            'vandermonde':'exact for t=1,...,9 and q=0,...,9'}
    (BASE/'evidence/reproduce-20261012-output-b.json').write_text(json.dumps(result,indent=2)+'\n')
    print('B: normalization, trace, Hermiticity and all finite Vandermonde checks PASS')

if __name__=='__main__': main()
