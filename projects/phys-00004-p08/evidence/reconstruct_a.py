#!/usr/bin/env python3
"""A: complete edge matching, transcribed input A only; no B artifacts read."""
import json
import math
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
A = json.loads((ROOT / 'evidence/input-a.json').read_text())

def matching(edges, cs, symbolic=True):
    """Continuity + inward-along-edge flux, all endpoint incidences retained."""
    width = 2*len(edges)
    ends = {}
    for j, (u, v, _) in enumerate(edges):
        c, s = cs[j]
        vo, vt, fo, ft = ([0]*width for _ in range(4))
        vo[2*j] = 1
        vt[2*j], vt[2*j+1] = c, s
        fo[2*j+1] = 1
        ft[2*j], ft[2*j+1] = s, -c
        ends.setdefault(u, []).append((vo, fo))
        ends.setdefault(v, []).append((vt, ft))
    rows, labels = [], []
    for vertex, incidences in ends.items():
        ref = incidences[0][0]
        for p, (value, _) in enumerate(incidences[1:], 1):
            rows.append([x-y for x, y in zip(value, ref)])
            labels.append(f'continuity:{vertex}:incidence{p}-incidence0')
        rows.append([sum(f[col] for _, f in incidences) for col in range(width)])
        labels.append(f'Kirchhoff:{vertex}')
    assert len(rows) == width
    return (sp.Matrix(rows) if symbolic else np.array(rows, float)), labels

def pumpkin_matrix(E, c, s):
    # A's explicitly transcribed row ordering, distinct from generic assembler.
    rows=[]
    for i in range(1,E):
        r=[0]*(2*E);r[2*i]=1;r[0]=-1;rows.append(r)
    for i in range(1,E):
        r=[0]*(2*E);r[2*i]=c;r[0]=-c;r[2*i+1]=s;r[1]=-s;rows.append(r)
    rows.append([int(i%2==1) for i in range(2*E)])
    rows.append([s if i%2==0 else -c for i in range(2*E)])
    return sp.Matrix(rows)

def encode(M):
    return [[str(z) for z in row] for row in M.tolist()]

def tree_edges(h,m,b):
    edges=[('v0','v1',.5),('v0','v3',.5),('v0','h_plus',h),('v0','h_minus',h)]
    for sign in ('plus','minus'):
        for j in range(m):
            edges.append((f'h_{sign}',f'{sign}_{j}',b))
    return edges

def duplicate(edges):
    return [edge for edge in edges for _ in range(2)]

def main():
    c,s=sp.symbols('c s')
    matrices={}
    tests=[]
    for E in (2,3,5,8):
        M=pumpkin_matrix(E,c,s)
        det=sp.factor(M.det())
        for n in (1,2,3):
            nullity=2*E-M.subs({c:(-1)**n,s:0}).rank()
            assert nullity==E
            tests.append({'graph':'unit pumpkin','E':E,'k':f'{n}*pi','nullity':nullity})
        assert sp.simplify(det/s**E) in (E**2,-E**2)
        matrices[f'pumpkin_E{E}']={'entries':encode(M),'determinant':str(det)}
    # Direct exact full matching for published four-arm half-length star.
    star=[('v0',f'leaf{j}',sp.Rational(1,2)) for j in range(4)]
    for doubled in (False,True):
        edges=duplicate(star) if doubled else star
        for n,(cv,sv) in enumerate(((0,1),(-1,0)),1):
            M,labels=matching(edges,[(cv,sv)]*len(edges))
            nullity=M.cols-M.rank()
            expected=(3 if n==1 else (5 if doubled else 1))
            assert nullity==expected, (doubled,n,nullity,expected)
            tests.append({'graph':'doubled star' if doubled else 'source star','k':'pi' if n==1 else '2*pi','nullity':nullity})
            matrices[f'star_doubled{doubled}_n{n}']={'entries':encode(M),'row_labels':labels}
    # Exact source split-tree instance at k=pi, h=1/6,m=5.
    m=A['split_tree']['reproduction_instance']['m']
    assert m==5 and A['split_tree']['reproduction_instance']['epsilon']=='1/6'
    radical=sp.sqrt(m*m+3)
    exact_edges=tree_edges(sp.Rational(1,6),m,sp.atan(sp.sqrt(3)/m)/sp.pi)
    cs=[(0,1),(0,1),(sp.sqrt(3)/2,sp.Rational(1,2)),(sp.sqrt(3)/2,sp.Rational(1,2))]
    cs += [(m/radical,sp.sqrt(3)/radical)]*(2*m)
    M,labels=matching(exact_edges,cs)
    rank=M.rank()
    assert M.cols-rank==3
    tests.append({'graph':'unperturbed source split tree','k':'pi','dimension':M.cols,'rank':rank,'nullity':3})
    matrices['split_tree_at_pi']={'edges':[[u,v,str(L)] for u,v,L in exact_edges],'entries':encode(M),'row_labels':labels}
    # A numerical root uses the COMPLETE matching determinant, not B's 2x2 reduction.
    h=1/6;delta=1/1000
    x0=.5+h
    source_F=-math.cos(math.pi*x0)
    source_A=math.sin(math.pi*x0)
    b=math.atan(source_A/(m*source_F))/math.pi
    edges=tree_edges(h,m,b+delta)
    def determinant(k):
        cs=[(math.cos(k*L),math.sin(k*L)) for _,_,L in edges]
        mat,_=matching(edges,cs,False)
        return float(np.linalg.det(mat))
    grid=np.linspace(math.pi*.95,math.pi*(1-1e-7),2001)
    lo=float(grid[0]);f_lo=determinant(lo)
    for point in grid[1:]:
        hi=float(point);f_hi=determinant(hi)
        if f_lo*f_hi<0:break
        lo,f_lo=hi,f_hi
    else:raise AssertionError('No complete-matching determinant root bracket found')
    k=brentq(determinant,lo,hi,xtol=5e-15,rtol=1e-14)
    numerical,_=matching(edges,[(math.cos(k*L),math.sin(k*L)) for _,_,L in edges],False)
    singular=np.linalg.svd(numerical,compute_uv=False)
    assert singular[-1]<1e-12 and singular[-2]>1e-5
    doubled_edges=duplicate(edges)
    doubled_matrix,_=matching(doubled_edges,[(math.cos(k*L),math.sin(k*L)) for _,_,L in doubled_edges],False)
    doubled_singular=np.linalg.svd(doubled_matrix,compute_uv=False)
    assert doubled_singular[-1]<1e-12 and doubled_singular[-2]>1e-5
    result={'method':'full endpoint matching A','versions':{'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
      'exact_checks':tests,'tree_lengths':{'h':h,'b_unperturbed':b,'b_perturbed':b+delta,'a':.5,'m':m,'delta':delta},
      'perturbed_tree_root':{'k':k,'mu2_numerical':k*k,'bracket':[lo,hi],'determinants_at_bracket':[f_lo,f_hi],
        'matching_smallest_singular_values':singular[-3:].tolist(),'doubled_smallest_singular_values':doubled_singular[-3:].tolist(),
        'tolerance':'Cross-representation root tolerance 1e-10; double-precision brentq, residual <1e-12. Not an interval-certified root.'},
      'analytic_obligation':'Firstness and multiplicity are proved for this source family in evidence/published-baseline.md; the determinant root alone does not establish ordering.',
      'status':'pass'}
    (ROOT/'evidence/matching-a.json').write_text(json.dumps(matrices,indent=2)+'\n')
    (ROOT/'evidence/results-a.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
