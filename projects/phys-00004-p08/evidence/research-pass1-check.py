#!/usr/bin/env python3
"""Complete matching, rational pole ranks, and all-edge-pair metric diagnostics.

The matrix is constructed directly from cosine/sine solutions and all endpoint
conditions, without division by a secular sine. It reads no old solver output.
All floating-point results are diagnostics subordinate to the exact proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, math, sys, itertools
import numpy as np
import scipy
from scipy.optimize import brentq, linprog
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / 'research-pass1-input.json').read_text())

def edges(m, doubled=False):
    h = math.atan(1 / math.sqrt(m)) / math.pi
    result = [(0, 1, .5, 'long', 1), (0, 2, .5, 'long', 1),
              (0, 3, h, 'stem', 1), (0, 4, h, 'stem', -1)]
    for j in range(m):
        result.append((3, 5+j, 2*h, 'leaf', 1))
        result.append((4, 5+m+j, 2*h, 'leaf', -1))
    if doubled:
        result = [e for e in result for _ in range(2)]
    return result

def matrix(edge_list, k=None, exact_trig=None):
    E = len(edge_list)
    symbolic = exact_trig is not None
    incident = {}
    for i, (u, v, L, kind, sign) in enumerate(edge_list):
        incident.setdefault(u, []).append((i, False))
        incident.setdefault(v, []).append((i, True))
    def row():
        return [sp.S.Zero if symbolic else 0.0 for _ in range(2*E)]
    def trig(i):
        if symbolic:
            return exact_trig[edge_list[i][3]]
        return math.cos(k*edge_list[i][2]), math.sin(k*edge_list[i][2])
    def value(i, terminal):
        r = row()
        if terminal:
            r[2*i], r[2*i+1] = trig(i)
        else:
            r[2*i] = 1
        return r
    rows = []
    for vertex, incidences in sorted(incident.items()):
        base = value(*incidences[0])
        for incidence in incidences[1:]:
            val = value(*incidence)
            rows.append([x-y for x,y in zip(val,base)])
        flux = row()
        for i, terminal in incidences:
            if terminal:
                c,s = trig(i)
                flux[2*i] += s
                flux[2*i+1] -= c
            else:
                flux[2*i+1] += 1
        rows.append(flux)
    assert len(rows) == 2*E
    return sp.Matrix(rows) if symbolic else np.array(rows)

def witness(edge_list, m):
    theta = math.atan(1/math.sqrt(2*m+1))
    C = math.sqrt(m+1)/(math.sqrt(2)*m)
    result = []
    for u,v,L,kind,sgn in edge_list:
        if kind == 'long': result += [0.,0.]
        elif kind == 'stem': result += [0.,float(sgn)]
        else: result += [sgn*C*math.cos(2*theta), sgn*C*math.sin(2*theta)]
    return np.array(result)

def full_matching_checks():
    results = []
    for m in CONFIG['full_matching_m']:
        h = math.atan(1/math.sqrt(m))/math.pi
        prediction = math.atan(1/math.sqrt(2*m+1))/h
        pair = {}
        for doubled in [False, True]:
            es = edges(m, doubled)
            # The root search sees only full matching and a fixed discovery bracket.
            def det(k): return float(np.linalg.det(matrix(es,k)))
            signs = [np.linalg.slogdet(matrix(es,k))[0] for k in [2.,2.5]]
            assert signs[0] * signs[1] == -1
            found = brentq(det,2.,2.5,xtol=2e-14,rtol=1e-14)
            mat = matrix(es,prediction)
            sv = np.linalg.svd(mat,compute_uv=False)
            residual = float(np.max(np.abs(mat@witness(es,m))))
            assert abs(found-prediction) < CONFIG['diagnostic_tolerances']['wave_number_comparison']
            assert residual < CONFIG['diagnostic_tolerances']['double_matrix_residual']
            assert int(np.sum(sv<CONFIG['diagnostic_tolerances']['sample_nullity_threshold'])) == 1
            pair['doubled' if doubled else 'tree'] = {
                'matrix_dimension': len(mat), 'discovery_bracket':[2,2.5],
                'full_determinant_root': found, 'closed_form_k': prediction,
                'absolute_difference':abs(found-prediction),
                'maximum_matching_residual':residual,
                'smallest_two_singular_values':sv[-2:].tolist(),
                'diagnostic_nullity':1}
        results.append({'m':m,'checks':pair})
    return results

def exact_checks():
    m=sp.symbols('m',positive=True)
    st=1/sp.sqrt(2*m+2)
    ct=sp.sqrt((2*m+1)/(2*m+2))
    c2=m/(m+1)
    s2=sp.sqrt(2*m+1)/(m+1)
    C=sp.sqrt(m+1)/(sp.sqrt(2)*m)
    identities={
        'hub_continuity':sp.simplify(C*c2-st),
        'hub_flux':sp.simplify(m*C*s2-ct),
        'leaf_neumann_cosine_expansion':sp.simplify(C**2-st**2-(ct/m)**2),
        'tan_characteristic':sp.simplify(2*m/(2*m+1)/(1-1/(2*m+1))-1)}
    assert all(value==0 for value in identities.values())
    # Exact secular pole k=2*pi for m=4: no floating-point trigonometry.
    pole=matrix(edges(4,True),exact_trig={
        'long':(-sp.S.One,sp.S.Zero),
        'stem':(sp.Rational(3,5),sp.Rational(4,5)),
        'leaf':(sp.Rational(-7,25),sp.Rational(24,25))})
    rank=pole.rank()
    assert pole.rows-rank == 2
    # Two independent DD witnesses, one on each long-edge pair.
    for pair in [0,1]:
        v=sp.zeros(pole.cols,1)
        v[2*(2*pair)+1]=1
        v[2*(2*pair+1)+1]=-1
        assert pole*v == sp.zeros(pole.rows,1)
    return {'symbolic_identity_remainders':{k:str(v) for k,v in identities.items()},
            'doubled_m4_pole_2pi':{'matrix_dimension':pole.rows,'exact_rank':rank,
                'exact_nullity':pole.rows-rank,'independent_DD_pair_witnesses':2,
                'field':'rational','note':'All added long-edge DD modes retained.'}}

def metric_checks():
    m=CONFIG['diameter_lp_m']
    es=edges(m,True)
    nv=max(max(e[:2]) for e in es)+1
    dv=np.full((nv,nv),np.inf)
    np.fill_diagonal(dv,0.)
    for u,v,L,kind,sgn in es:
        dv[u,v]=min(dv[u,v],L); dv[v,u]=min(dv[v,u],L)
    for k in range(nv): dv=np.minimum(dv,dv[:,k,None]+dv[None,k,:])
    rows=[]
    for i,j in itertools.combinations_with_replacement(range(len(es)),2):
        u,v,L,_,_=es[i]; p,q,R,_,_=es[j]
        inequalities=[]; rhs=[]
        for xvertex,sx,ix in [(u,1.,0.),(v,-1.,L)]:
            for yvertex,sy,iy in [(p,1.,0.),(q,-1.,R)]:
                inequalities.append([-sx,-sy,1.])
                rhs.append(ix+iy+dv[xvertex,yvertex])
        values=[]
        for order in ([0,1] if i==j else [None]):
            mat=list(inequalities); bound=list(rhs)
            if order == 0:  # x <= y, direct route length y-x
                mat += [[1.,-1.,0.],[1.,-1.,1.]]; bound += [0.,0.]
            elif order == 1:
                mat += [[-1.,1.,0.],[-1.,1.,1.]]; bound += [0.,0.]
            sol=linprog([0.,0.,-1.],A_ub=mat,b_ub=bound,
                bounds=[(0.,L),(0.,R),(0.,None)],method='highs')
            assert sol.success, sol.message
            values.append({'maximum_distance':-float(sol.fun),'coordinates':sol.x.tolist()})
        winner=max(values,key=lambda r:r['maximum_distance'])
        assert winner['maximum_distance'] <= 1+CONFIG['diagnostic_tolerances']['metric_lp_tolerance']
        rows.append({'edges':[i,j],**winner})
    maximum=max(r['maximum_distance'] for r in rows)
    assert abs(maximum-1)<CONFIG['diagnostic_tolerances']['metric_lp_tolerance']
    h=math.atan(1/math.sqrt(m))/math.pi
    M=list(range(5,5+2*m))
    Mdiam=float(np.max(dv[np.ix_(M,M)]))
    assert abs(Mdiam-6*h)<1e-12
    (HERE/'research-pass1-metric-pairs.json').write_text(json.dumps(rows,indent=2)+'\n')
    return {'m':m,'doubled_edges':len(es),'edge_pairs_optimized':len(rows),
            'all_interior_coordinate_domains_included':True,
            'maximum_distance':maximum,'extrema_vertex_diameter':Mdiam,
            'predicted_extrema_diameter':6*h,
            'opposite_long_pair_maximum':next(r['maximum_distance'] for r in rows if r['edges']==[0,1]),
            'method':'max-min affine path-length LP, with direct same-copy path on both x/y order domains',
            'error_control':'Binary64/HiGHS diagnostics only; no directed enclosure. Exact case proof is separate.'}

def scalar_checks():
    mp.mp.dps=70
    rows=[]
    for m in CONFIG['scalar_m']:
        h=mp.atan(1/mp.sqrt(m))/mp.pi
        k=mp.atan(1/mp.sqrt(2*m+1))/h
        C=mp.sqrt(m+1)/(mp.sqrt(2)*m)
        assert 3*h<mp.mpf('.5') and k<mp.pi
        residual=mp.cos(k*h)*mp.cos(2*k*h)-m*mp.sin(k*h)*mp.sin(2*k*h)
        assert abs(residual)<mp.mpf('1e-60')
        rows.append({'m':m,'h':mp.nstr(h,15),'mu2':mp.nstr(k*k,15),
            'extrema_diameter':mp.nstr(6*h,15),
            'leaf_amplitude':mp.nstr(C,15),'characteristic_residual':mp.nstr(residual,5),
            'added_DD_threshold':'4*pi^2'})
    epsrows=[]
    for e in CONFIG['epsilon_checks']:
        eps=mp.mpf(str(e))
        m=max(4,int(mp.ceil(36/(mp.pi**2*eps**2))))
        h=mp.atan(1/mp.sqrt(m))/mp.pi
        assert 6*h<eps
        epsrows.append({'epsilon':str(eps),'m':m,'extrema_diameter':mp.nstr(6*h,15),
            'number_of_doubled_edges':4*m+8,
            'diagnostic':'scalar formula only; enormous graphs are not numerically instantiated'})
    return {'m_checks':rows,'epsilon_checks':epsrows}

def main():
    start=datetime.now(timezone.utc).isoformat()
    result={'job_id':CONFIG['job_id'],'started_at':start,'python':sys.version,
        'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
        'mpmath':mp.__version__,'mode':'exact identities plus numerical diagnostics',
        'independence':'Same proposer worker; different full matching / metric representation, no fresh referee.'}
    print('Exact radical identities and complete rational DD pole rank',flush=True)
    result['exact']=exact_checks()
    print('Direct complete endpoint matching and fixed-bracket determinant roots',flush=True)
    result['matching']=full_matching_checks()
    print('All doubled-edge-pair interior metric domains',flush=True)
    result['metric']=metric_checks()
    print('70-digit scalar parameter and epsilon diagnostics',flush=True)
    result['scalar']=scalar_checks()
    result['finished_at']=datetime.now(timezone.utc).isoformat()
    result['diagnostic_status']='passed actual checks'
    result['limitations']='No floating root/SVD/LP output is an exact enclosure; no independent referee or exhaustive novelty verdict. Exact universal proof is separate.'
    (HERE/'research-pass1-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__': main()
