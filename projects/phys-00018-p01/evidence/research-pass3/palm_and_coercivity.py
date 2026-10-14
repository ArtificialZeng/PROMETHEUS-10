"""Exact one-dimensional Palm response and finite weighted coercivity checks.

No whole-space injection coercivity, no coupled stationary solve, no referee.
The infinite parent marginal and return coefficients use positive compound
Poisson recurrences, alternating Taylor brackets and fixed-point intervals.
Only the injection U matrices are inputs from the earlier n=16 enclosure.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib.util, json, math, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence/research-pass3'
BITS=384; Q=1<<BITS; ORDER=160; S=64
sys.set_int_max_str_digits(0)

def fixed(a,b):
    return (a.numerator*Q//a.denominator,
            -((-b.numerator*Q)//b.denominator))

def bracket(term):
    z=F(0)
    for k in range(ORDER+2):
        z+=(-1 if k%2 else 1)*term(k)
        if k==ORDER:hi=z
    assert 0<=z<=hi
    return z,hi

def conv(a,b,n):
    return [(sum(a[j][0]*b[k-j][0] for j in range(k+1))//Q,
             -((-sum(a[j][1]*b[k-j][1] for j in range(k+1)))//Q))
            for k in range(n+1)]

def sub(a,b):return a[0]-b[1],a[1]-b[0]
def rat(a):return F(a[0],Q),F(a[1],Q)
def mid(a):return F(a[0]+a[1],2*Q)
def frac_interval(a):return {'lower':str(a[0]),'upper':str(a[1])}
def riadd(a,b):return a[0]+b[0],a[1]+b[1]
def rimul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)
def rineg(a):return -a[1],-a[0]

def upper(z):
    y=float(z)
    while F.from_float(y)<z:y=float(np.nextafter(y,math.inf))
    return y

def lower(z):
    y=float(z)
    while F.from_float(y)>z:y=float(np.nextafter(y,-math.inf))
    return y

def factorial(d,degree=8):
    out={(0,0):F(1)}
    for k in range(1,degree+1):
        for s in range(k+1):
            r=k-s;v=F(0)
            if r:v+=r*d*out[r-1,s]
            if s:v+=s*(out[r+1,s-1]+r*out.get((r,s-1),F(0)))
            out[r,s]=v/(r*d+s)
    return out

def parent(d):
    qa=[];levy=[(0,0)]
    for j in range(S+1):
        qa.append(fixed(*bracket(lambda l:F(math.factorial(d)*math.factorial(j+l),
            math.factorial(j)*math.factorial(l)*math.factorial(j+l+d)))))
        if j:levy.append(fixed(*bracket(lambda l:F(d*math.factorial(d)*math.factorial(j+l-1),
            math.factorial(j)*math.factorial(l)*math.factorial(j+l+d)))))
    lm=bracket(lambda l:F(d*math.factorial(d),(l+1)*math.factorial(d+l+1)))
    ar=(1-rat(qa[0])[1]+lm[0],1-rat(qa[0])[0]+lm[1])
    assert 0<=ar[0]<=ar[1]<=1
    p0lo=bracket(lambda l:ar[1]**l/math.factorial(l))[0]
    p0hi=bracket(lambda l:ar[0]**l/math.factorial(l))[1]
    p=[fixed(p0lo,p0hi)]
    for k in range(1,S+1):
        ll=sum(j*(qa[j][0]+levy[j][0])*p[k-j][0] for j in range(1,k+1))
        hh=sum(j*(qa[j][1]+levy[j][1])*p[k-j][1] for j in range(1,k+1))
        p.append((ll//(k*Q),-((-hh)//(k*Q))))
    mq=conv(p,qa,S)
    A=[sub(mq[k],p[k]) for k in range(S+1)]
    H=[((k-1)*p[k][0],(k-1)*p[k][1]) if k>=1
       else (-p[k][1],-p[k][0]) for k in range(S+1)]
    nus={};Ds={}
    for s in [1,2]:
        for tw in [False,True] if s==1 else [False]:
            tag=f'{s}'+('t' if tw else '')
            def term(k,l):
                n=k+l
                v=F(math.comb(n,k),s+n)
                for j in range(n):v/=s+d+j
                if tw:
                    v*=F(1,s+n)+sum((F(1,s+d+j) for j in range(n)),F(0))
                return v
            nu=[fixed(*bracket(lambda l:term(k,l))) for k in range(S+1)]
            cc=conv(p,nu,S)
            ds=[sub(cc[k],(p[k][0]//(s*s if tw else s),
                     -((-p[k][1])//(s*s if tw else s)))) for k in range(S+1)]
            nus[tag]=nu;Ds[tag]=ds
    f=factorial(d)
    m4=f[0,4]+10*f[0,3]+25*f[0,2]+15*f[0,1]+1
    tails={}
    for n in [16,32,48,64]:
        lo=max(F(0),m4-sum(F((k+1)**4)*rat(p[k])[1] for k in range(n)))
        hi=m4-sum(F((k+1)**4)*rat(p[k])[0] for k in range(n))
        assert hi>=lo
        tails[str(n)]={'E_1plusP4_indicator_lower':lower(lo),
            'E_1plusP4_indicator_upper':upper(hi),'exact_upper':str(hi)}
    ptail=min(F(1)-sum(rat(z)[0] for z in p),f[0,8]/math.prod(range(S-6,S+2)))
    assert ptail>=0
    record={'d':d,'parameters':{'c':d,'delta':d,'beta':1,'gamma':1},
      'fixed_point_bits':BITS,'Taylor_order':ORDER,'maximum_coefficient':S,
      'denominator':str(Q),'protein_probability_numerators':[[str(x),str(y)] for x,y in p],
      'alive_RNA_mark_numerators':[[str(x),str(y)] for x,y in qa],
      'return_coefficient_numerators':{k:[[str(x),str(y)] for x,y in z]
           for k,z in {'A':A,'H':H,'D1':Ds['1'],'D2':Ds['2'],'Dt1':Ds['1t']}.items()},
      'extra_RNA_probability_Laplace_numerators':{k:[[str(x),str(y)] for x,y in z] for k,z in nus.items()},
      'protein_tail_probability_upper':str(ptail),'weighted_fourth_moment_tails':tails,
      'scope':'Infinite parent marginal and all displayed return coefficients; coefficient truncation does not alter lower coefficients. No whole-space U bound.'}
    (OUT/f'palm-delta{d}-S{S}.json').write_text(json.dumps(record,indent=2)+'\n')
    return {'p':p,'A':A,'H':H,'Ds':Ds,'record':record,'ptail':ptail}

def weighted_matrix(g,n=16):
    p=[rat(z) for z in g['p']];w=[F(1,(k+1)**2) for k in range(len(p))]
    zi=(sum(w[k]*p[k][0] for k in range(len(p))),
        sum(w[k]*p[k][1] for k in range(len(p)))+g['ptail']/F((len(p)+1)**2))
    M=[];errors=[]
    for i in range(n):
        row=[];er=[]
        for j in range(n):
            v=rimul(p[i],p[j]);fac=(zi[0]-w[i]-w[j],zi[1]-w[i]-w[j])
            a=rimul(v,fac)
            if i==j:a=riadd(a,(p[i][0]*w[i],p[i][1]*w[i]))
            row.append((a[0]+a[1])/2);er.append((a[1]-a[0])/2)
        M.append(row);errors.append(er)
    return M,max(max(row) for row in errors),zi

def ldlt(A):
    n=len(A);L=[[F(0) for j in range(n)] for i in range(n)];D=[]
    for i in range(n):
        L[i][i]=F(1);v=A[i][i]-sum(L[i][k]**2*D[k] for k in range(i));D.append(v)
        if v<=0:return {'positive_definite':False,'first_nonpositive_pivot':i,'pivot':str(v)}
        for j in range(i+1,n):L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/v
    return {'positive_definite':True,'pivots_lower':[lower(z) for z in D],
        'exact_pivot_digest':hashlib.sha256(json.dumps([str(z) for z in D]).encode()).hexdigest()}

def finite_coercivity(gs):
    src='evidence/research-pass2/cluster-gram-n16-R24-S80-exact.json'
    a=json.loads((ROOT/src).read_text());n=16;cases=[];exact={}
    for d,key,alphas in [(1,'U2',[F(1,100),F(2,5)]),(2,'U1',[F(1,100),F(4,5)])]:
        U=[[F(z) for z in r] for r in a[key]];eU=F(a['entry_errors'][key])
        W,eW,zw=weighted_matrix(gs[d],n);checks=[]
        for alpha in alphas:
            shift=n*(eU+alpha*eW)
            K=[[U[i][j]-alpha*W[i][j]-(shift if i==j else 0) for j in range(n)] for i in range(n)]
            checks.append({'alpha':str(alpha),'spectral_error_shift_upper':upper(shift),'ldlt':ldlt(K)})
        cases.append({'parent_delta':d,'injection_key':key,'basis_size':n,
            'weighted_entry_error_upper':upper(eW),'checks':checks})
        exact[key]={'W':[[str(z) for z in r] for r in W],'weighted_entry_error':str(eW),
                    'z_weighted_expectation_interval':frac_interval(zw)}
    (OUT/'weighted-coercivity-n16-exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    return {'input':src,'scope':'All real responses constant above protein count 15; constants may be subtracted globally.',
            'whole_space_coercivity_established':False,'cases':cases}

def return_replay(gs):
    old=json.loads((ROOT/'evidence/research-pass2/cluster-gram-n16-R24-S80-exact.json').read_text())
    intervals={};report={}
    for key in ['B1','B2_transpose']:
        mat=[];dif=[]
        for i in range(16):
            row=[]
            for j in range(16):
                if key=='B1':
                    dr=riadd(rat(gs[2]['Ds']['1'][j]),rat(gs[2]['Ds']['1t'][j]))
                    r=riadd(rimul(rat(gs[1]['A'][i]),dr),
                            rimul(rat(gs[1]['H'][i]),rat(gs[2]['Ds']['1'][j])))
                else:
                    dr=riadd(rat(gs[1]['Ds']['1'][i]),
                             rimul((F(-1,2),F(-1,2)),rat(gs[1]['Ds']['2'][i])))
                    r=riadd(rimul(rat(gs[2]['A'][j]),dr),
                            rimul(rat(gs[2]['H'][j]),rat(gs[1]['Ds']['1'][i])))
                center=F(old[key][i][j]);err=F(old['entry_errors'][key])
                assert r[0]>=center-err and r[1]<=center+err
                row.append([str(r[0]),str(r[1])]);dif.append(max(abs(r[0]-center),abs(r[1]-center)))
            mat.append(row)
        intervals[key]=mat;report[key]={'entries_checked':256,
           'all_new_intervals_contained_in_previous_entry_enclosures':True,
           'maximum_central_difference_upper':upper(max(dif))}
    (OUT/'return-replay-exact.json').write_text(json.dumps(intervals,indent=2)+'\n')
    return report

def functional_bounds(gs):
    out={}
    constants={'A':F(1),'H':F(1),'D1':F(5,2),'D2':F(5,2),'Dt1':F(5,2)}
    for d,g in gs.items():
        vals={'A':g['A'],'H':g['H'],'D1':g['Ds']['1'],'D2':g['Ds']['2'],'Dt1':g['Ds']['1t']}
        dual={}
        for key,v in vals.items():
            q=F(0)
            for k in range(S):
                a=rat(v[k]);pm=rat(g['p'][k])[0]
                assert pm>0
                q+=max(abs(a[0]),abs(a[1]))**2*F((k+1)**2)/pm
            tail=F(g['record']['weighted_fourth_moment_tails'][str(S)]['exact_upper'])
            dual[key]={'whole_space_weighted_dual_norm_squared_upper':upper(q+constants[key]**2*tail),
                'tail_squared_upper_by_n':{str(n):upper(constants[key]**2*F(t['exact_upper']))
                    for n,t in [(int(nn),tt) for nn,tt in g['record']['weighted_fourth_moment_tails'].items()]}}
        out[str(d)]=dual
    return out

def run():
    gs={d:parent(d) for d in [1,2]}
    result={'job_id':'phys-00018-p01-research-3ff79a4c94a6','finite_coercivity':finite_coercivity(gs),
        'independent_return_replay':return_replay(gs),'weighted_dual_functional_bounds':functional_bounds(gs),
        'limitations':'Weighted-dual bounds are exact for the stated weighted variance. Continuity in the full injection norm still requires the unproved whole-space coercivity inequality. No original resolution, scientific referee acceptance, or publication candidate.'}
    (OUT/'palm-and-coercivity-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':run()
