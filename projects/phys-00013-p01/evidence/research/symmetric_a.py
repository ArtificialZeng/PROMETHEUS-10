"""Exact bosonic differential-operator reconstruction; no source Gram input.

Run from the project root with the installed research interpreter.
All large sparse entries and contractions are Python integers, not int64.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json, math, resource, time
from pathlib import Path
import sympy as sp

def compositions(k, d):
    if d == 1:
        yield (k,)
    else:
        for a in range(k + 1):
            for n in compositions(k-a, d-1):
                yield (a,) + n

def multiply(a, b):
    out = []
    for col in b:
        c = {}
        for j, x in col.items():
            for i, y in a[j].items():
                c[i] = c.get(i, 0) + x*y
        out.append({i:x for i,x in c.items() if x})
    return out

def add_terms(powers, coeffs):
    result = []
    for j in range(len(powers[0])):
        col = {}
        for power, coeff in zip(powers, coeffs):
            for i, value in power[j].items():
                col[i] = col.get(i,0) + coeff*value
        result.append({i:x for i,x in col.items() if x})
    return result

def trace_product(a,b):
    return sum(v*b[i].get(j,0) for j,col in enumerate(a) for i,v in col.items())

def scaled(a,factor):
    return [{i:factor*x for i,x in col.items() if factor*x} for col in a]

def serialize(a):
    return [[i,j,v] for j,col in enumerate(a) for i,v in sorted(col.items())]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--degree',type=int,default=7)
    args=parser.parse_args(); k=args.degree
    t=time.monotonic(); basis=list(compositions(k,8)); index={n:i for i,n in enumerate(basis)}
    size=len(basis); identity=[{i:1} for i in range(size)]
    metric=[math.prod(math.factorial(x) for x in n) for n in basis]
    def ladder(n, mask, up):
        for low in range(8):
            if low & mask: continue
            high=low|mask; src,dst=(high,low) if up else (low,high)
            if n[src]:
                out=list(n); out[src]-=1; out[dst]+=1
                yield tuple(out),n[src]
    def casimir(mask):
        columns=[]
        for n in basis:
            z=sum(v*(1 if not (i & mask) else -1) for i,v in enumerate(n))
            col={index[n]:z*z}
            for up in [True,False]:
                for m,coeff in ladder(n,mask,up):
                    for o,coeff2 in ladder(m,mask,not up):
                        i=index[o]; col[i]=col.get(i,0)+2*coeff*coeff2
            columns.append({i:v for i,v in col.items() if v})
        assert all(metric[i]*v==metric[j]*columns[i].get(j,0)
                   for j,col in enumerate(columns) for i,v in col.items())
        return columns
    x=sp.Symbol('x'); kappas=[(k-2*r)*(k-2*r+2) for r in range(k//2+1)]
    polys=[sp.Poly(sp.prod((x-b)/(a-b) for b in kappas if b!=a),x) for a in kappas]
    denominators=[int(c.q) for p in polys for c in p.all_coeffs()]
    common=math.lcm(*denominators)
    coeffs=[[int(p.nth(i)*common) for i in range(len(kappas))] for p in polys]
    endpoints=[]
    for name,mask in [('site1',4),('site3',1)]:
        K=casimir(mask); powers=[identity,K]
        while len(powers)<len(kappas): powers.append(multiply(K,powers[-1]))
        next_power=multiply(K,powers[-1])
        minimal=sp.Poly(sp.prod(x-a for a in kappas),x)
        assert all(not col for col in add_terms(powers+[next_power],[int(minimal.nth(i)) for i in range(len(kappas)+1)]))
        projections=[add_terms(powers,c) for c in coeffs]
        assert add_terms(projections,[1]*len(projections))==scaled(identity,common)
        for r,P in enumerate(projections):
            assert multiply(P,P)==scaled(P,common)
            assert multiply(K,P)==scaled(P,kappas[r])
            assert all(metric[i]*v==metric[j]*P[i].get(j,0) for j,col in enumerate(P) for i,v in col.items())
            for s in range(r): assert all(not col for col in multiply(P,projections[s]))
        ranks=[sum(P[i].get(i,0) for i in range(size))//common for P in projections]
        assert sum(ranks)==size
        endpoints.append({'name':name,'K':K,'powers':powers,'projectors':projections,'ranks':ranks})
        print(json.dumps({'endpoint':name,'degree':k,'dimension':size,'ranks':ranks,'all_exact_projector_checks':True}),flush=True)
    assert endpoints[0]['ranks']==endpoints[1]['ranks']
    G=sp.diag(*endpoints[0]['ranks'])
    T=sp.Matrix([[trace_product(a,b) for b in endpoints[1]['powers']] for a in endpoints[0]['powers']])
    C=sp.Matrix([[sp.Rational(trace_product(a,b),common**2) for b in endpoints[1]['projectors']] for a in endpoints[0]['projectors']])
    assert C==C.T
    assert C*sp.ones(len(kappas),1)==G*sp.ones(len(kappas),1)
    B=G.inv()*C
    eigs=B.eigenvals(); squared=(B*B).charpoly(x).as_expr()
    assert eigs.get(sp.Integer(1))==1
    nonfixed=[abs(v) for v in eigs if v!=1]
    assert all(v.is_Rational for v in eigs)
    result={'job_id':'phys-00013-p01-research-701e3768750c','created_at':datetime.now(timezone.utc).isoformat(),
            'method':'A: x_i partial_j bosonic Lie generators in monomial basis; exact integer sparse algebra',
            'degree':k,'dimension':size,'mode_index':'4a+2b+c','basis':basis,
            'metric':'product n_i!, overall degree-dependent constant omitted',
            'casimir_eigenvalues':kappas,'projector_common_denominator':common,
            'projector_coefficients_ascending':coeffs,'all_projector_and_metric_checks':True,
            'endpoint_casimirs':{p['name']:serialize(p['K']) for p in endpoints},
            'ranks':endpoints[0]['ranks'],'trace_moments':[[str(v) for v in row] for row in T.tolist()],
            'cross_gram':[[str(v) for v in row] for row in C.tolist()],
            'signed_eigenvalues':{str(v):int(m) for v,m in eigs.items()},
            'squared_angle_polynomial':str(sp.factor(squared)),
            'largest_nonfixed_cosine':str(max(nonfixed,default=sp.Integer(0))),
            'global_fixed_dimension_by_SU8_irreducibility':1,
            'counterexample_found':bool(max(nonfixed,default=sp.Integer(0))>sp.Rational(1,2)),
            'elapsed_seconds':time.monotonic()-t,'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'limitations':'Finite representation calculation; completeness/global irreducibility require the accompanying derivation. Not an all-representation result or fresh referee audit.'}
    path=Path(f'evidence/research/sym{k}-input-a.json'); path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({a:result[a] for a in ['degree','dimension','ranks','cross_gram','signed_eigenvalues','squared_angle_polynomial','largest_nonfixed_cosine','counterexample_found','elapsed_seconds','max_rss_bytes_macos']},indent=2),flush=True)

if __name__=='__main__': main()
