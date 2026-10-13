#!/usr/bin/env python3
"""Fresh referee's exact check. Standard library only; no discovery code/data imports.

Witness transcribed from claim.json; conventions independently read from PRA
111, 052449 (2025), Eqs. (3), (10), (11), Definition 8. Figure 15 inputs were
transcribed directly from the frozen page-16 image, without reading cached inputs.
Gaussian integer amplitude numerators carry an explicit sqrt(2) denominator.
All partial traces below are rational, directly from computational-basis signs.
"""
from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
import datetime
import json
import platform
import time

T0 = time.perf_counter()

def edges(pairs):
    return frozenset(tuple(sorted(p)) for p in pairs)

def neighbors(E, v):
    return sorted(y if x == v else x for x,y in E if v in (x,y))

def lc(E, v):
    return E ^ edges(combinations(neighbors(E,v),2))

def connected(V,E):
    reached={V[0]}
    while True:
        new=reached|{u for v in reached for u in neighbors(E,v)}
        if new==reached: return len(new)==len(V)
        reached=new

def condense(E,C):
    Q=set()
    for x,y in E:
        x=7 if x in C else x
        y=7 if y in C else y
        if x!=y: Q.add(tuple(sorted((x,y))))
    return frozenset(Q)

def cut(E,A,B):
    return [[int(tuple(sorted((a,b))) in E) for b in B] for a in A]

def binary_rank(M):
    # Explicit GF(2) row operations; not cached spans.
    A=[r[:] for r in M]; r=0
    for j in range(len(A[0]) if A else 0):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None: continue
        A[r],A[k]=A[k],A[r]
        for k in range(len(A)):
            if k!=r and A[k][j]: A[k]=[a^b for a,b in zip(A[k],A[r])]
        r+=1
    return r

def sign_vector(V,E):
    pos={v:i for i,v in enumerate(V)}
    return [(-1)**sum(((z>>pos[x])&1)*((z>>pos[y])&1) for x,y in E)
            for z in range(1<<len(V))]

def gi_add(x,y): return (x[0]+y[0],x[1]+y[1])
def gi_i(x,sgn=1): return (-sgn*x[1],sgn*x[0])

def rx_num(vec,q):
    return [gi_add(a,gi_i(vec[z^(1<<q)],-1)) for z,a in enumerate(vec)]

def rz_num(vec,q,sgn=1):
    return [gi_add(a,gi_i(a,sgn*(-1 if (z>>q)&1 else 1))) for z,a in enumerate(vec)]

def circuit_replay(V,E,word,wrong_neighbor_sign=False):
    vec=[(s,0) for s in sign_vector(V,E)]; g=E; ngates=0; steps=[]
    for v in word:
        N=neighbors(g,v)
        vec=rx_num(vec,V.index(v)); ngates+=1
        for u in N:
            vec=rz_num(vec,V.index(u),-1 if wrong_neighbor_sign else 1); ngates+=1
        g=lc(g,v)
        target=sign_vector(V,g); phase=vec[0]
        residual=sum(a!=(s*phase[0],s*phase[1]) for a,s in zip(vec,target))
        norm_num=sum(a*a+b*b for a,b in vec)
        assert norm_num == 2**(len(V)+ngates)
        steps.append({'vertex':v,'neighbors':N,'edges':sorted(g),
            'phase_numerator':phase,'phase_denominator':'sqrt(2)^'+str(ngates),
            'unequal_amplitudes_up_to_global_phase':residual,
            'external_degrees_C123':[len(set(neighbors(g,u))-{1,2,3}) for u in (1,2,3)] if len(V)==6 else None})
        if not wrong_neighbor_sign:
            assert residual==0
            assert phase[0]**2+phase[1]**2==2**ngates
    return {'steps':steps,'gates':ngates,'final_edges':sorted(g),'all_amplitudes_checked':len(vec)}

def reduced(V,E,A):
    # Direct amplitude sum, independent of cut rank or stabilizer subgroup formulas.
    B=[v for v in V if v not in A]
    signs=sign_vector(V,E); pos={v:i for i,v in enumerate(V)}
    def full_index(a,b):
        return sum(((a>>i)&1)<<pos[v] for i,v in enumerate(A)) + sum(((b>>i)&1)<<pos[v] for i,v in enumerate(B))
    dim=1<<len(A)
    M=[[F(sum(signs[full_index(a,b)]*signs[full_index(c,b)] for b in range(1<<len(B))),1<<len(V))
        for c in range(dim)] for a in range(dim)]
    assert sum(M[a][a] for a in range(dim))==1
    assert all(M[a][b]==M[b][a] for a in range(dim) for b in range(dim))
    return M

def projector_spectrum(M):
    # Determine the exact flat nonzero spectrum from rho^2=lambda*rho and trace 1.
    n=len(M)
    MM=[[sum(M[a][k]*M[k][b] for k in range(n)) for b in range(n)] for a in range(n)]
    lam=next(MM[a][b]/M[a][b] for a in range(n) for b in range(n) if M[a][b])
    assert lam>0 and all(MM[a][b]==lam*M[a][b] for a in range(n) for b in range(n))
    rank=1/lam; assert rank.denominator==1 and 0<rank<=n
    return {'eigenvalue':str(lam),'multiplicity':int(rank),'zero_multiplicity':n-int(rank),
            'purity':str(sum(MM[a][a] for a in range(n))),
            'proof':'Hermitian, trace one, and exactly rho^2=lambda*rho; hence spectrum {0,lambda}.'}

def lc_orbit(V,E):
    found={E}; queue=deque([E])
    while queue:
        g=queue.popleft()
        for v in V:
            h=lc(g,v)
            if h not in found: found.add(h);queue.append(h)
    return found

def matrix_strings(M): return [[str(x) for x in row] for row in M]

V=list(range(1,7)); C={1,2,3}; O=[4,5,6]
E=edges([(1,3),(1,6),(2,4),(3,5),(4,6)])
Ep=edges([(1,3),(1,5),(2,4),(3,6),(4,6),(5,6)])
assert connected(V,E) and connected(V,Ep)
assert 2<=len(C)<=len(V)-2
replay=circuit_replay(V,E,[3,1,5])
assert replay['final_edges']==sorted(Ep)
assert replay['steps'][-1]['phase_numerator']==(-32,0)
ends=[]
for g in (E,Ep):
    M=cut(g,sorted(C),O); assert all(sum(row)==1 for row in M)
    rho=reduced(V,g,sorted(C)); spec=projector_spectrum(rho)
    assert binary_rank(M)==3 and spec['multiplicity']==8
    ends.append({'edges':sorted(g),'cut_matrix':M,'cut_rank':binary_rank(M),
                 'C_external_degrees':[sum(row) for row in M], 'rho_C_spectrum':spec})
Q,Qp=condense(E,C),condense(Ep,C); W=[4,5,6,7]; B=[4,5]
outputs=[]
for q in (Q,Qp):
    rho=reduced(W,q,B);spec=projector_spectrum(rho)
    outputs.append({'edges':sorted(q),'cut_matrix_B':cut(q,B,[6,7]),
                    'cut_rank_B':binary_rank(cut(q,B,[6,7])),
                    'rho_B':matrix_strings(rho),'spectrum':spec})
assert [o['cut_rank_B'] for o in outputs]==[2,1]
assert [o['spectrum']['multiplicity'] for o in outputs]==[4,2]
orbit=lc_orbit(W,Q)
assert Qp not in orbit
swap={4:4,5:6,6:5,7:7}
assert edges((swap[x],swap[y]) for x,y in Qp)==lc(Q,7)

# Check every nontrivial labeled marginal on the witness, using two representations.
cut_checks=0
for vs,g in ((V,E),(V,Ep),(W,Q),(W,Qp)):
    for k in range(1,len(vs)):
        for A in combinations(vs,k):
            spec=projector_spectrum(reduced(vs,g,list(A)))
            assert spec['multiplicity']==2**binary_rank(cut(g,list(A),[v for v in vs if v not in A]))
            cut_checks+=1

# Actual Fig. 3 seven-qubit control; n=4 is the paper's general-n special case.
baselines=[]
for n in (4,7):
    vs=list(range(1,n+1)); star=edges((1,v) for v in vs[1:]); complete=edges(combinations(vs,2))
    out=circuit_replay(vs,star,[1]); assert out['final_edges']==sorted(complete)
    # For n=7, representative 7 collides with an external label, so use a fresh map.
    def quotient_to_8(g):
        return edges((8 if x in (2,3) else x,8 if y in (2,3) else y) for x,y in g
                     if not (x in (2,3) and y in (2,3)))
    sq,kq=quotient_to_8(star),quotient_to_8(complete)
    assert lc(sq,1)==kq
    assert binary_rank(cut(star,[2,3],[v for v in vs if v not in (2,3)]))==1
    assert binary_rank(cut(complete,[2,3],[v for v in vs if v not in (2,3)]))==1
    baselines.append({'n':n,'lc_circuit':out,'rank_one_condensation_control':True,
                      'target_both_end_degree_domain':False,
                      'complete_endpoint_degrees':[n-2,n-2]})

# Fresh manual visual reconstruction of Fig.15(a,b), preserving top-row labels.
figures=[]
for name,vs,g,c,v in [
    ('Fig15a',list(range(1,7)),edges([(1,2),(2,3),(1,6),(3,5),(4,5),(5,6)]),{1,2,3},5),
    ('Fig15b',list(range(1,8)),edges([(1,3),(2,3),(3,4),(4,5),(5,6),(5,7)]),{3,4,5},3)]:
    h=lc(g,v)
    profiles=[[len(set(neighbors(k,u))-c) for u in sorted(c)] for k in (g,h)]
    ranks=[binary_rank(cut(k,sorted(c),[u for u in vs if u not in c])) for k in (g,h)]
    assert ranks==[2,2] and not all(d<=1 for profile in profiles for d in profile)
    figures.append({'figure':name,'original_edges':sorted(g),'lc_vertex':v,'final_edges':sorted(h),
                    'C':sorted(c),'external_degree_profiles':profiles,'cut_ranks':ranks})

# Discriminating convention challenge: invert every neighbor Z rotation sign.
negative=circuit_replay(V,E,[3,1,5],True)
assert negative['steps'][-1]['unequal_amplitudes_up_to_global_phase']>0

report={'job_id':'phys-smallmac00008-p01-referee-0f50c3c6c5f1',
        'run_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'arithmetic':'exact integers/Gaussian integers/Fraction; no numerical tolerances',
        'label_map':'7=c in the six-qubit witness quotient only; bit index follows the explicit V list',
        'input_endpoints':ends,'candidate_circuit':replay,'outputs':outputs,
        'all_nontrivial_marginal_checks':cut_checks,
        'output_labeled_orbit':{'members':len(orbit),'queue_exhausted':True,'target_in_orbit':False},
        'unlabeled_limitation':'swapping external labels 5 and 6 maps Qp to LC_c(Q)',
        'published_baselines':baselines,'primary_figure_checks':figures,'wrong_sign_control':negative,
        'result':'All exact assertions passed; novelty and significance assessed separately in science.md.',
        'elapsed_seconds':time.perf_counter()-T0}
print(json.dumps(report,indent=2))
