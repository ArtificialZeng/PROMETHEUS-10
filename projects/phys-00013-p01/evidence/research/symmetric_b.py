"""Independent exact symmetric-tensor partial-swap construction.

This script does not import A or read its answers. Mode order is reversed.
Sparse matrices are dictionaries of rows; polynomial algebra uses Fractions.
"""
from datetime import datetime, timezone
import argparse
from fractions import Fraction as F
import json, math, resource, time
from pathlib import Path

def partitions8(k):
    def extend(prefix, left):
        if len(prefix)==7:
            yield tuple(prefix+[left])
        else:
            for value in range(left,-1,-1):
                yield from extend(prefix+[value],left-value)
    return list(extend([],k))

def row_product(A,B):
    rows=[]
    for a in A:
        row={}
        for j,x in a.items():
            for l,y in B[j].items(): row[l]=row.get(l,0)+x*y
        rows.append({j:x for j,x in row.items() if x})
    return rows

def polynomial_mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--degree',type=int,default=7)
    k=parser.parse_args().degree
    started=time.monotonic(); basis=partitions8(k); ids={n:i for i,n in enumerate(basis)}
    d=len(basis); I=[{i:1} for i in range(d)]
    metric=[math.prod(math.factorial(v) for v in n) for n in basis]
    # Standard Cauchy branching; independent closed Weyl-dimension formula.
    sectors=[]
    for r in range(k//2+1):
        a,b=k-r,r
        dim4=F((a-b+1)*(a+2)*(a+3)*(b+1)*(b+2),12)
        assert dim4.denominator==1
        sectors.append({'partition':[a,b], 'dim_SU4':int(dim4),
                        'dim_SU2':a-b+1,'rank':int(dim4)*(a-b+1),
                        'casimir':(a-b)*(a-b+2)})
    assert sum(s['rank'] for s in sectors)==d==math.comb(k+7,7)
    eigenvalues=[s['casimir'] for s in sectors]
    coefficients=[]
    for value in eigenvalues:
        p=[F(1)]
        for other in eigenvalues:
            if other!=value: p=polynomial_mul(p,[F(-other,value-other),F(1,value-other)])
        coefficients.append(p)
    def endpoint(mask):
        # On Sym^k, K=(4k-k^2)I+4 sum_{p<q} T_pq^(endpoint).
        rows=[{} for _ in basis]
        for column,n in enumerate(basis):
            rows[column][column]=4*k-k*k
            for i in range(8):
                for j in range(i,8):
                    pairs=n[i]*(n[i]-1)//2 if i==j else n[i]*n[j]
                    if not pairs: continue
                    u=(i & ~mask)|(j & mask); v=(j & ~mask)|(i & mask)
                    changed=list(n); changed[i]-=1; changed[j]-=1; changed[u]+=1; changed[v]+=1
                    row=ids[tuple(changed)]
                    rows[row][column]=rows[row].get(column,0)+4*pairs
        rows=[{j:v for j,v in row.items() if v} for row in rows]
        assert all(metric[i]*v==metric[j]*rows[j].get(i,0) for i,row in enumerate(rows) for j,v in row.items())
        powers=[I,rows]
        while len(powers)<len(eigenvalues): powers.append(row_product(powers[-1],rows))
        projectors=[]
        for coef in coefficients:
            P=[]
            for row_id in range(d):
                entries={}
                for a,power in zip(coef,powers):
                    for j,value in power[row_id].items(): entries[j]=entries.get(j,F(0))+a*value
                P.append({j:v for j,v in entries.items() if v})
            projectors.append(P)
        ranks=[sum(P[i].get(i,0) for i in range(d)) for P in projectors]
        assert ranks==[s['rank'] for s in sectors]
        for s,P in enumerate(projectors):
            assert row_product(P,P)==P
            for t in range(s): assert all(not row for row in row_product(P,projectors[t]))
        for i in range(d):
            row={}
            for P in projectors:
                for j,v in P[i].items(): row[j]=row.get(j,F(0))+v
            assert {j:v for j,v in row.items() if v}==I[i]
        return rows,powers,projectors
    # B mode is 4c+2b+a: physical endpoints use the opposite masks.
    K1,powers1,P1=endpoint(1); print('B site1 exact swap/projector/branching checks passed',flush=True)
    K3,powers3,P3=endpoint(4); print('B site3 exact swap/projector/branching checks passed',flush=True)
    def trace_product(A,B):
        return sum(v*B[j].get(i,0) for i,row in enumerate(A) for j,v in row.items())
    cross=[[trace_product(A,B) for B in P3] for A in P1]
    moments=[[trace_product(A,B) for B in powers3] for A in powers1]
    assert all(sum(row)==sectors[r]['rank'] for r,row in enumerate(cross))
    result={'job_id':'phys-00013-p01-research-701e3768750c','created_at':datetime.now(timezone.utc).isoformat(),
            'method':'B: permutation-invariant partial tensor swaps on symmetrized slot words; closed two-row Weyl dimensions; rational row algebra',
            'degree':k,'dimension':d,'mode_index':'4c+2b+a','basis':basis,
            'metric':'product n_i!, overall degree-dependent constant omitted',
            'branching':sectors,'projector_coefficients_ascending':[[str(v) for v in c] for c in coefficients],
            'ranks':[s['rank'] for s in sectors],
            'endpoint_casimirs':{'site1':[[i,j,v] for i,row in enumerate(K1) for j,v in sorted(row.items())],
                                 'site3':[[i,j,v] for i,row in enumerate(K3) for j,v in sorted(row.items())]},
            'trace_moments':[[str(v) for v in row] for row in moments],
            'cross_gram':[[str(v) for v in row] for row in cross],
            'all_projector_and_metric_checks':True,
            'independence':'Same agent/shared model, but no A imports, files, Gram or differential generators. Different algorithm, mode order, basis order and rational representation. Not a fresh referee.',
            'elapsed_seconds':time.monotonic()-started,'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(f'evidence/research/sym{k}-input-b.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['degree','dimension','ranks','cross_gram','elapsed_seconds','max_rss_bytes_macos']},indent=2),flush=True)

if __name__=='__main__': main()
