#!/usr/bin/env python3
"""Exact graph, local Boltzmann enumeration, rational transfer and finite radicals.
No previous calculated answer or supervisor feasibility record is read.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from math import isqrt
import json, hashlib, sys, datetime

HERE=Path(__file__).resolve().parent
sys.set_int_max_str_digits(20000)

def dump(name,data):
    (HERE/name).write_text(json.dumps(data,indent=2)+'\n')

def canonical_edge(u,v,dx,dy):
    return min((u,v,dx,dy),(v,u,-dx,-dy))

def geometry(n):
    # Axial coordinates: Cartesian e1=(1,0), e2=(1/2,sqrt(3)/2).
    coordinates=[(Q(0),Q(0))]+[(Q(3*j-1,6*j),Q(1,3*j)) for j in range(1,n+1)]
    edges=[(0,0,1,0),(0,0,0,1),(0,0,-1,1)]
    edges += [(0,j,0,0) for j in range(1,n+1)]
    edges += [(j,0,1,0) for j in range(1,n+1)]
    edges += [(1,0,0,1)]
    edges += [(j-1,j,0,0) for j in range(2,n+1)]
    faces=[[(0,1,0),(0,1,1),(0,0,1)]] # Down face.
    A=(0,0,0); B=(0,1,0); C=(0,0,1)
    remaining=[A,B,C]
    barycentric=[]
    for j in range(1,n+1):
        X=(j,0,0)
        if j==1:
            coeff=(Q(1,3),)*3
        else:
            coeff=(Q(1,2*j),Q(1,2*j),Q(j-1,j))
        barycentric.append([str(c) for c in coeff])
        def point(v):
            idx,dx,dy=v
            return coordinates[idx][0]+dx,coordinates[idx][1]+dy
        weighted=tuple(sum(coeff[k]*point(remaining[k])[a] for k in range(3)) for a in range(2))
        assert weighted==point(X) and all(c>0 for c in coeff) and sum(coeff)==1
        prev=remaining[2]
        faces.extend([[B,prev,X],[prev,A,X]])
        remaining=[A,B,X]
    faces.append(remaining)
    keys=[canonical_edge(*e) for e in edges]
    assert len(set(keys))==len(keys)
    degrees=[0]*(n+1)
    for u,v,dx,dy in edges:
        assert u!=v or (dx,dy)!=(0,0)
        degrees[u]+=1; degrees[v]+=1
    incident={k:0 for k in keys}; twice_areas=[]
    for face in faces:
        pts=[(coordinates[i][0]+dx,coordinates[i][1]+dy) for i,dx,dy in face]
        area=sum(pts[k][0]*pts[(k+1)%3][1]-pts[(k+1)%3][0]*pts[k][1] for k in range(3))
        assert area>0
        twice_areas.append(area)
        for k in range(3):
            u,ux,uy=face[k]; v,vx,vy=face[(k+1)%3]
            incident[canonical_edge(u,v,vx-ux,vy-uy)]+=1
    assert all(v==2 for v in incident.values())
    assert sum(twice_areas)==2
    assert degrees[0]==2*n+7
    assert degrees[1:]==([3] if n==1 else [4]*(n-1)+[3])
    assert len(edges)==3*(n+1) and len(faces)==2*(n+1)
    return {'N':n,'basis':[[1,0],['1/2','sqrt(3)/2']],
            'axial_coordinates':[[str(x),str(y)] for x,y in coordinates],
            'translation_labelled_edges':edges,'oriented_faces':faces,
            'degrees':degrees,'q_max':max(degrees),'vertices':n+1,
            'edges':len(edges),'faces':len(faces),'euler_characteristic':n+1-len(edges)+len(faces),
            'positive_stellar_barycentric_coordinates':barycentric,
            'positive_face_areas':True,'each_edge_has_two_faces':True,
            'sum_axial_face_areas':'1','no_duplicate_lifted_edge':True}

def transfer(n,r):
    p,q=r.numerator,r.denominator
    # Integer numerator matrix; common denominator q(p+q).
    w1,w2=p,q
    for _ in range(n-1):
        w1,w2=p*p*w1+q*q*w2,q*q*(w1+w2)
    den=(p+q)*(q*(p+q))**(n-1)
    up=Q(p*p*w1+q*q*w2,p*q*den)
    um=Q(w1+w2,den)
    return up,um,{'p':p,'q':q,'N':n,'w1':str(w1),'w2':str(w2),'denominator':str(den)}

def enumerate_trace(n,r,A,B,C):
    # All 3N physical added bonds, each factor r when satisfied, 1 otherwise.
    total=Q(0)
    for xs in product((-1,1),repeat=n):
        satisfied=sum(int(x==A)+int(x==B) for x in xs)+int(xs[0]==C)
        satisfied+=sum(int(xs[j]==xs[j-1]) for j in range(1,n))
        total+=r**satisfied
    return total

def even_polynomial(graph,t):
    # Completely enumerate subsets of the original physical edge set.
    es=graph['translation_labelled_edges']; vs=graph['vertices']
    coeff=[0]*(len(es)+1)
    for mask in range(1<<len(es)):
        parity=[0]*vs; hx=hy=count=0
        for k,(u,v,dx,dy) in enumerate(es):
            if mask>>k&1:
                parity[u]^=1; parity[v]^=1
                hx^=(dx&1); hy^=(dy&1); count+=1
        if not any(parity): coeff[count]+=1 if (hx,hy)==(0,0) else -1
    return coeff,sum(Q(c)*t**k for k,c in enumerate(coeff))

def sqrt_bounds(x,D):
    lo=Q(isqrt((x.numerator*D*D)//x.denominator),D)
    hi=lo+Q(1,D)
    assert lo*lo<=x<hi*hi
    return lo,hi

def canonical_finite_radicals():
    D=10**60
    sl,su=sqrt_bounds(Q(3),D)
    low,high=2+sl,2+su
    rows=[]
    for k in range(10):
        rows.append({'n':k,'reciprocal_lower':str(low),'reciprocal_upper':str(high),
                     't_lower':str(1/high),'t_upper':str(1/low)})
        if k<9:
            a,_=sqrt_bounds(low*low+6*low-7,D)
            _,b=sqrt_bounds(high*high+6*high-7,D)
            low,high=(low+1+a)/2,(high+1+b)/2
    assert high<20 and 1/high>Q(1,20)
    return {'precision_scale':str(D),'method':'rational outward square-root bounds verified by exact square inequalities',
            'q':3072,'iterations':9,'rows':rows,'reciprocal_upper_less_than_20':True,
            't_lower_greater_than_1_over_20':True,
            'temperature_bound':'Tc_star(3072)/J < 1/t9 < 20; no logarithm approximation'}

def main():
    g=geometry(1024); dump('fan-graph.json',g)
    checks=[]
    for n in range(1,9):
        for r in (Q(11,10),Q(3,2),Q(2)):
            up,um,_=transfer(n,r)
            W0=r**n*(r+1)**n
            for A,B,C in product((-1,1),repeat=3):
                direct=enumerate_trace(n,r,A,B,C)/W0
                expected=Q(1) if A!=B else up if A==C else um
                assert direct==expected,(n,r,A,B,C,direct,expected)
            checks.append({'N':n,'r':str(r),'all_eight_boundary_traces_match':True})
    homology=[]
    for n in range(1,4):
        small=geometry(n); r=Q(3,2); t=(r-1)/(r+1)
        coeff,val=even_polynomial(small,t)
        up,um,_=transfer(n,r)
        # Transfer-based ordering sign, independently evaluated against original edge subsets.
        indicator=r*r*up-um-2
        assert (val>0)-(val<0)==-((indicator>0)-(indicator<0))
        homology.append({'N':n,'signed_original_coefficients_ascending':coeff,
                         'r':str(r),'signed_original_value':str(val),
                         'transfer_order_indicator':str(indicator),'ordered_sign_agreement':True})
    up,um,raw=transfer(1024,Q(11,10))
    delta=Q(121,100)*up-um-2
    assert delta>0 and up>um>=1
    dump('large-transfer-certificate.json',{'r':'11/10','N':1024,'integer_transfer':raw,
          'U_plus':str(up),'U_minus':str(um),'ordering_margin':str(delta),
          'ordering_margin_positive':True,'U_plus_greater_than_U_minus_at_least_one':True})
    dump('canonical-radical-certificate.json',canonical_finite_radicals())
    dump('input-a.json',{'representation':'exact axial periodic lift and independently enumerated local physical bond configurations',
          'source_model':'2605.10017v2 Eq17, pp4-5; local stellar insertion on p5',
          'triangle_primitive_edges':[[0,0,1,0],[0,0,0,1],[0,0,-1,1]],
          'homology_rule':'empty and all-three primitive loops have even total winding; the other six subsets have nonzero winding',
          'anisotropic_signed_polynomial':'1-a-b-c-a*b-a*c-b*c+a*b*c',
          'fan_graph':'evidence/research-pass4-20261013/fan-graph.json',
          'local_trace_definition':'sum_x exp(K*((A+B)*sum_j x_j+C*x_1+sum_j x_j*x_(j+1)))',
          'normalized_zero_field_trace':'(2*cosh(K))^N',
          'physical_couplings':'all original bonds J>0, no multiple physical edges'})
    summary={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'geometry':{k:g[k] for k in ['N','q_max','vertices','edges','faces','euler_characteristic']},
             'local_checks':checks,'original_homology_checks':homology,
             'large_N_ordering_margin_positive':True,'canonical_finite_radical_bound_less_than_20':True,
             'source_files_read_by_calculation':[],
             'limitations':'Exact proposer checks; no fresh-referee acceptance. Analytic criticality and canonical-function arguments are separately required.'}
    dump('fan-check-results.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
