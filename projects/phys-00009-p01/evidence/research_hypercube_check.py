"""Exact proposer checks for the homogeneous hypercube two-particle reduction.

Direct occupation jumps and independent (k-1)-sector incidence construction
are compared exactly. Character embeddings, radial lump and thresholds are
checked without eigensolver tolerances. The proof is in hypercube-result.md.
"""
import itertools
import json
from math import factorial,comb
from pathlib import Path
import sympy as s
from reconstruct_a import reconstruct

HERE=Path(__file__).resolve().parent
a=s.Symbol('a',positive=True)
t=s.Symbol('lambda')


def independent_incidence(spec):
    n=spec['n'];alpha=[s.Rational(x) for x in spec['alpha']]
    occ=[]
    for labels in itertools.combinations_with_replacement(range(n),2):
        eta=[0]*n
        for x in labels:eta[x]+=1
        occ.append(tuple(eta))
    index={eta:i for i,eta in enumerate(occ)}
    weights=[]
    for eta in occ:
        w=s.Integer(1)
        for x,m in enumerate(eta):
            local=s.Integer(1)
            for j in range(1,m+1):local*= (alpha[x]+j-1)/j
            w*=local
        weights.append(w)
    Z=sum(weights);mu=[w/Z for w in weights]
    total=sum(alpha);K=s.zeros(len(occ))
    for z in range(n):
        residual=alpha[z]/total
        for x,y,c in spec['edges']:
            ex=[0]*n;ey=[0]*n
            ex[z]+=1;ex[x]+=1;ey[z]+=1;ey[y]+=1
            i=index[tuple(ex)];j=index[tuple(ey)]
            q=2/(total+1)*residual*s.Rational(c)*(alpha[x]+int(z==x))*(alpha[y]+int(z==y))
            K[i,i]+=q;K[j,j]+=q;K[i,j]-=q;K[j,i]-=q
    L=s.zeros(len(occ))
    for i in range(len(occ)):
        for j in range(len(occ)):L[i,j]=-K[i,j]/mu[i]
    return occ,mu,L


def block(D,m,parameter):
    q=(1<<m)-1
    zlist=[z for z in range(1<<D) if (q&z).bit_count()%2==0]
    idx={z:i for i,z in enumerate(zlist)}
    B=s.zeros(len(zlist))
    for z in zlist:
        i=idx[z];B[i,i]=2*D*parameter+ (2 if z.bit_count()==1 else 0)
        if z==0:B[i,i]=2*D*parameter
        for bit in range(D):
            target=z^(1<<bit)
            if target not in idx:continue
            rate=2*parameter
            if z==(1<<bit):rate+=2
            B[i,idx[target]]-=rate
    return zlist,B


def radial(D,parameter):
    T=s.zeros(D+1)
    for d in range(D+1):
        if d>0:T[d,d-1]=-2*d*parameter-(2 if d==1 else 0)
        if d<D:T[d,d+1]=-2*(D-d)*parameter
        T[d,d]=-sum(T[d,j] for j in range(D+1) if j!=d)
    return T


def embedding(occ,D,m,zlist):
    q=(1<<m)-1;index={z:i for i,z in enumerate(zlist)}
    E=s.zeros(len(occ),len(zlist))
    for i,eta in enumerate(occ):
        sites=[x for x,number in enumerate(eta) for _ in range(number)]
        x,y=sites;z=x^y
        if z in index:E[i,index[z]]=(-1)**((q&x).bit_count())
    return E


def intervals(poly):
    return [{'bounds':[str(lo),str(hi)],'multiplicity':int(mult)}
            for (lo,hi),mult in s.polys.polytools.intervals(poly,eps=s.Rational(1,10**12))]


def first_positive(data):
    for item in data:
        lo,hi=map(s.Rational,item['bounds'])
        if hi>0:
            assert lo>0
            return lo,hi
    raise AssertionError('missing positive root')


def main():
    records=[]
    for D,alpha_string in [(3,'1/100'),(4,'1/100'),(4,'1/35'),(4,'1/10'),(4,'1')]:
        parameter=s.Rational(alpha_string);n=1<<D
        spec={'id':f'cube{D}-a{alpha_string}','n':n,'alpha':[alpha_string]*n,
              'edges':[[x,y,'1'] for x in range(n) for y in range(x+1,n) if (x^y).bit_count()==1]}
        direct=reconstruct(spec,2)
        occA=[tuple(v) for v in direct['state_order']]
        LA=s.Matrix([[s.Rational(v) for v in row] for row in direct['L_backward']])
        occB,muB,LB=independent_incidence(spec)
        perm=[occB.index(v) for v in occA]
        LBordered=LB.extract(perm,perm)
        assert LA==LBordered
        assert [s.Rational(v) for v in direct['mu']]==[muB[j] for j in perm]
        assert sum(muB)==1 and all(v>0 for v in muB)
        print('Exact A/B occupation inputs agree:',spec['id'],'dimension',len(occA),flush=True)
        polys={};roots={}
        for m in range(D+1):
            zs,B=block(D,m,parameter)
            E=embedding(occA,D,m,zs)
            assert (-LA)*E==E*B
            assert E.rank()==len(zs)
            p=s.Poly(B.charpoly(t).as_expr(),t)
            polys[str(m)]=str(s.factor(p.as_expr()))
            roots[str(m)]=intervals(p)
            if m:
                lo,hi=first_positive(roots[str(m)])
                assert lo>=2*m*parameter
            else:
                W=s.zeros(1<<D,D+1)
                for z in range(1<<D):W[z,z.bit_count()]=1
                assert B*W==W*radial(D,parameter)
        p_rad=s.Poly(radial(D,parameter).charpoly(t).as_expr(),t)
        roots_rad=intervals(p_rad)
        radial_gap=first_positive(roots_rad)
        all_candidates=[first_positive(r) for r in roots.values()]
        full_gap=min(all_candidates,key=lambda bounds:bounds[0])
        predicted=min([(2*parameter,2*parameter),radial_gap],key=lambda bounds:bounds[0])
        assert full_gap==predicted
        if D==4 and parameter<s.Rational(1,35):assert full_gap[1]<2*parameter
        else:assert full_gap==(2*parameter,2*parameter)
        record={'spec':spec,'status':'exact_proposer_check_completed','occupation_dimension':len(occA),
                'A_B_entries_and_measures_equal':True,'character_blocks_intertwine_exactly':True,
                'character_block_dimensions':[len(block(D,m,parameter)[0]) for m in range(D+1)],
                'character_block_polynomials_by_weight':polys,
                'character_block_root_intervals_by_weight':roots,
                'radial_polynomial':str(s.factor(p_rad.as_expr())),
                'radial_root_intervals':roots_rad,'lambda2_interval':list(map(str,full_gap)),
                'lambda1':str(2*parameter)}
        records.append(record)
        (HERE/'research-hypercube-checks.json').write_text(json.dumps({'mode':'exact','role':'proposer','not_referee_acceptance':True,'cases':records},indent=2)+'\n')
        print('  Full block spectral ordering agrees with min(2a,radial gap).',flush=True)
    threshold=[]
    b=s.Symbol('b')
    for D in range(1,17):
        C=s.zeros(D+1)
        for d in range(D+1):
            C[d,d]=D-1
            if d>0:C[d,d-1]=-d
            if d<D:C[d,d+1]=-(D-d)
        base=C.det()
        C[1,1]+=b;C[1,0]-=b
        det=s.factor(C.det())
        coefficient=s.diff(det,b)
        determinant_threshold=s.factor(-coefficient/base)
        green=s.Rational(1,1<<D)*sum(s.Rational(comb(D,j),2*j-1) for j in range(D+1))
        integral=sum(s.Rational(comb(D-1,j),2*j+1) for j in range(D)) / (1<<(D-1))
        formula=(D-1)*integral-1
        assert formula==((D-1)*green-1)/D==determinant_threshold
        if D>=4:assert formula>0
        if D>=3:
            prev=s.Rational(threshold[-1]['critical_a'])
            assert formula==((D-1)**2*prev+1)/((D-2)*(2*D-1))
        threshold.append({'D':D,'critical_a':str(formula),'determinant_at_2a_scaled':str(det)})
    T4=radial(4,a)
    cp=s.factor(T4.charpoly(t).as_expr())
    expected=t*(t-8*a)*(t**3-(32*a+2)*t**2+(304*a*a+32*a)*t-768*a**3-48*a*a)
    assert s.expand(cp-expected)==0
    at_single=s.factor(cp.subs(t,2*a))
    assert at_single==96*a**4*(35*a-1)
    symbolic={'status':'exact_symbolic_checks_completed','D4_radial_matrix':s.sstr(T4),
              'D4_radial_characteristic_polynomial':str(cp),
              'D4_at_single_particle_gap':str(at_single),
              'threshold_formula':'a_D=(D-1)*2**(-(D-1))*integral_0^1 (1+u**2)**(D-1) du - 1',
              'threshold_recurrence':'a_(D+1)=(D**2*a_D+1)/((D-1)*(2*D+1)), D>=2',
              'checked_thresholds':threshold,
              'limitations':'Finite exact checks supplement the all-D proof; they are not the source of its quantifiers. Same worker wrote checks and proof; no fresh referee acceptance.'}
    (HERE/'research-hypercube-symbolic-checks.json').write_text(json.dumps(symbolic,indent=2)+'\n')
    print('Symbolic cubic, 1/35 crossover and all threshold identities D=1..16 checked exactly.',flush=True)


if __name__=='__main__':main()
