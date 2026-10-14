"""Foreground exact-arithmetic finite Riesz residual and whole-space enclosure.

Uses preserved n=64 U intervals and exact Palm coefficients. Floating linear
solves only propose rational approximants; all accepted bounds use Fractions.
No stored scientific input is modified. No coupled stationary truncation.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, json, math, sys, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'evidence/research-pass3'; OUT=ROOT/'evidence/research-pass4'
sys.set_int_max_str_digits(0)
QV=1<<128

def sqrt_up(v):
    assert v>=0
    if not v:return F(0)
    q=(v.numerator*(1<<256)+v.denominator-1)//v.denominator
    k=math.isqrt(q)
    if k*k<q:k+=1
    z=F(k,1<<128); assert z*z>=v
    return z

def up(v):
    z=float(v)
    while F.from_float(z)<v:z=float(np.nextafter(z,math.inf))
    return z

def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    vals=[x*y for x in a for y in b];return min(vals),max(vals)

def factorial(d,order=6):
    f={(0,0):F(1)}
    for k in range(1,order+1):
        for s in range(k+1):
            r=k-s;z=F(0)
            if r:z+=r*d*f[r-1,s]
            if s:z+=s*(f[r+1,s-1]+r*f.get((r,s-1),F(0)))
            f[r,s]=z/(r*d+s)
    return f

def stirling(n,k):
    if n==k==0:return 1
    if k<=0 or k>n:return 0
    row=[1]
    for j in range(1,n+1):
        row=[0]+[(row[i-1] if i-1<len(row) else 0)+i*(row[i] if i<len(row) else 0) for i in range(1,j+1)]
    return row[k]

def parent(d,n,allmat,oldinfo):
    rec=json.loads((OLD/f'palm-delta{d}-S64.json').read_text()); den=int(rec['denominator'])
    pi=[(F(int(a),den),F(int(b),den)) for a,b in rec['protein_probability_numerators']]
    oldscale=[F(v) for v in oldinfo['exact_scales']]
    eta=pi[1:n]+[(1-sum(x[1] for x in pi[:n]),1-sum(x[0] for x in pi[:n]))]
    s=oldscale[:n-1]
    t=F(2)**math.floor(-math.log2(float(eta[-1][1]))/2)
    while t*t*eta[-1][1]>1:t/=2
    while 4*t*t*eta[-1][1]<=1:t*=2
    s.append(t)
    # Exact change of basis. The new tail is the sum of all old tail categories.
    trans=[[(i,F(1))] for i in range(n-1)]
    trans.append([(i,t/oldscale[i]) for i in range(n-1,64)])
    Uold=[[F(v) for v in row] for row in allmat['U']]
    Eold=[[F(v) for v in row] for row in allmat['eU']]
    def transform(M):
        return [[sum(a*b*M[i][j] for i,a in ri for j,b in rj) for rj in trans] for ri in trans]
    U=transform(Uold);E=transform(Eold)
    cf={tag:[(F(int(a),den),F(int(b),den)) for a,b in rows]
        for tag,rows in rec['return_coefficient_numerators'].items()}
    cf['Dg']=cf['D1']
    cf['Dr']=[add(cf['D1'][p],cf['Dt1'][p]) if d==2 else
        add(cf['D1'][p],mul((F(-1,2),F(-1,2)),cf['D2'][p])) for p in range(65)]
    alpha=F(3,102400) if d==1 else F(1,187272)
    kernel_mass=F(3,4) if d==1 else F(2)
    ff=factorial(d)
    tail={}
    for k in [4,5,6]:
        full=sum(stirling(k+1,j+1)*ff[0,j] for j in range(k+1))
        tail[k]=full-sum((p+1)**k*pi[p][0] for p in range(n))
        assert tail[k]>=0
    result={}; exact={'U':[[str(v) for v in row] for row in U],
        'entry_error_bounds':[[str(v) for v in row] for row in E],
        'scales':list(map(str,s)),'alpha':str(alpha),
        'tail_moments':{str(k):str(v) for k,v in tail.items()},'functions':{}}
    for tag,C in [('A',F(1)),('H',F(1)),('Dr',F(15,4) if d==1 else F(5)),('Dg',F(5,2))]:
        arr=cf[tag]
        coeff=arr[1:n]+[(-sum(v[1] for v in arr[:n]),-sum(v[0] for v in arr[:n]))]
        coeff=[(s[i]*z[0],s[i]*z[1]) for i,z in enumerate(coeff)]
        aa=[(a+b)/2 for a,b in coeff]
        xfloat=np.linalg.solve(np.array([[float(v) for v in r] for r in U]),np.array([float(v) for v in aa]))
        x=[F(int(round(float(v)*QV)),QV) for v in xfloat]
        q=[]
        for i in range(n):
            center=aa[i]-sum(U[i][j]*x[j] for j in range(n))
            allowance=(coeff[i][1]-coeff[i][0])/2+sum(E[i][j]*abs(x[j]) for j in range(n))
            q.append(abs(center)+allowance)
        rzero=sum(q[i]/s[i] for i in range(n))
        head=rzero*rzero/pi[0][0]
        for i in range(n-1):head+=(i+2)**4*(q[i]/s[i])**2/pi[i+1][0]
        raw=[F(0)]+[s[i]*x[i] for i in range(n)]
        mean=(F(0),F(0))
        for i in range(n):mean=add(mean,mul(eta[i],(s[i]*x[i],s[i]*x[i])))
        vmax=max(abs(z-v) for z in raw for v in mean)
        K=kernel_mass*vmax
        tailbound=C*C*tail[6]+2*C*K*tail[5]+K*K*tail[4]
        residual_sq=(head+tailbound)/alpha
        delta=sqrt_up(residual_sq)
        vnormsq=sum(x[i]*x[j]*U[i][j]+abs(x[i]*x[j])*E[i][j] for i in range(n) for j in range(n))
        assert vnormsq>=0
        vnorm=sqrt_up(vnormsq)
        projection_norm=vnorm+delta
        result[tag]={'projection_norm_upper':up(projection_norm),'projection_error_dual_norm_upper':up(delta),
            'approximant_U_norm_upper':up(vnorm),'centered_approximant_sup_upper':up(vmax),
            'head_residual_W4dual_squared_upper':up(head),'tail_residual_W4dual_squared_upper':up(tailbound)}
        exact['functions'][tag]={'source_intervals':[list(map(str,z)) for z in coeff],
            'approximant_coefficients':list(map(str,x)),'scaled_head_residual_bounds':list(map(str,q)),
            'count_zero_residual_upper':str(rzero),'centered_approximant_sup_upper':str(vmax),
            'head_residual_W4dual_squared_upper':str(head),'tail_residual_W4dual_squared_upper':str(tailbound),
            'projection_error_dual_norm_upper':str(delta),'approximant_U_norm_squared_upper':str(vnormsq),
            'approximant_U_norm_upper':str(vnorm),'projection_norm_upper':str(projection_norm)}
    path=OUT/f'riesz-d{d}-n{n}-exact.json';path.write_text(json.dumps(exact,indent=2)+'\n')
    return result,exact,path

def run(n):
    matrices=json.loads((OLD/'l2-gram-n64-exact.json').read_text())
    infos=json.loads((OLD/'l2-gram-n64-results.json').read_text())['parents']
    prs={};exs={};files=[]
    for d in [1,2]:
        r,e,p=parent(d,n,matrices[str(d)],next(x for x in infos if x['d']==d));prs[d]=r;exs[d]=e;files.append(str(p.relative_to(ROOT)))
        print(json.dumps({'stage':'parent','d':d,'basis':n,'functions':r}),flush=True)
    checks=[]
    for key,pairs in [('B1',[('A','Dr'),('H','Dg')]),('B2_transpose',[('Dr','A'),('Dg','H')])]:
        error=F(0)
        for a,b in pairs:
            aa=exs[1]['functions'][a];bb=exs[2]['functions'][b]
            da=F(aa['projection_error_dual_norm_upper']);db=F(bb['projection_error_dual_norm_upper'])
            ma=F(aa['projection_norm_upper']);mb=F(bb['projection_norm_upper'])
            error+=da*mb+ma*db+da*db
        norm=F(3,4)+error
        checks.append({'form':key,'finite_projected_norm_upper':'3/4',
            'whole_space_omitted_form_norm_upper':str(error),'whole_space_norm_upper':str(norm),
            'whole_space_norm_numeric_upper':up(norm),'norm_at_most_four_fifths':norm<=F(4,5)})
    out={'job_id':'phys-00018-p01-research-d34512ad717d','basis_size':n,
        'scope':'All real bounded whole-lattice protein response functions, fixed unequal constitutive parents only.',
        'W4_coercivity':{'U2_parent_d1':'3/102400','U1_parent_d2':'1/187272'},
        'parents':{str(d):prs[d] for d in prs},'checks':checks,'exact_files':files,
        'full_response_contraction_check_passed':all(c['norm_at_most_four_fifths'] for c in checks),
        'original_status':'unresolved','referee_acceptance':False,
        'limitations':'Proposer enclosure depends on the analytic whole-space generator proof and preserved pass-3 certificates; no arbitrary kinetics, strong-feedback or larger-N resolution.'}
    p=OUT/f'riesz-n{n}-results.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--basis',type=int,default=48);a=p.parse_args()
    assert 16<=a.basis<=64
    run(a.basis)
