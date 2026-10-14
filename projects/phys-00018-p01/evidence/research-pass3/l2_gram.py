"""Stationary L2 residual bounds with a constant-gauge rare-count basis.

Foreground bounded computation. All numerical solves are approximants; exact
integer residuals, infinite-state moments and rational congruence bounds decide
the finite-basis statements. No arbitrary-tail coercivity is inferred.
"""
import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.sparse import coo_matrix,eye
from scipy.sparse.linalg import splu

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/research-pass3'
sys.path.insert(0,str(OUT))
import palm_and_coercivity as palm
sys.set_int_max_str_digits(0)
QV=1<<192;QT=1<<96;QK=1<<192

def sqrt_upper(z):
    if not z:return F(0)
    a=(z.numerator*(1<<256)+z.denominator-1)//z.denominator
    b=math.isqrt(a)
    if b*b<a:b+=1
    out=F(b,1<<128);assert out*out>=z
    return out

def moments(d,order=104):
    return palm.factorial(d,order)

def tails(f,R,S):
    ret=[]
    for j in range(3):
        am=[];ap=[]
        for k in range(1,min(R+1,100)+1):
            z=f[k,0] if j==0 else (f[k+1,0]+k*f[k,0] if j==1 else
                f[k+2,0]+(2*k+1)*f[k+1,0]+k*k*f[k,0])
            am.append(z/math.prod(range(R+2-k,R+2)))
        for k in range(1,min(S+1,100)+1):
            z=f[0,k] if j==0 else (f[1,k] if j==1 else f[2,k]+f[1,k])
            ap.append(z/math.prod(range(S+2-k,S+2)))
        ret.append(min(am)+min(ap))
    return ret

def record_parent(d,n,R,S):
    spec=importlib.util.spec_from_file_location('cluster3',ROOT/'evidence/research-pass2/joint_stationary.py')
    cl=importlib.util.module_from_spec(spec);spec.loader.exec_module(cl)
    cl.BITS=384;cl.Q=1<<384;cl.ORDER=160
    prob,perr,pr=cl.generate(d,R,S,OUT/f'l2-cluster-delta{d}-R{R}-S{S}.json')
    pnum=[int(lo)+int(hi) for lo,hi in pr['interval_probability_numerators']]
    phigh=[int(hi) for lo,hi in pr['interval_probability_numerators']]
    N=(R+1)*(S+1);idx=lambda m,p:m*(S+1)+p
    rows=[];cols=[];data=[];edges=[];categories=[]
    for m in range(R+1):
        for p in range(S+1):
            i=idx(m,p);e=[]
            if m<R:e.append((idx(m+1,p),d))
            if m:e.append((idx(m-1,p),d*m))
            if m and p<S:e.append((idx(m,p+1),m))
            if p:e.append((idx(m,p-1),p))
            for j,a in e:rows.append(i);cols.append(j);data.append(a)
            rows.append(i);cols.append(i);data.append(-sum(a for j,a in e));edges.append(e)
            categories.append(p-1 if 1<=p<n else (n-1 if p>=n else -1))
    q=coo_matrix((data,(rows,cols)),shape=(N,N)).tocsc()
    rhs=np.zeros((N,n))
    for i,c in enumerate(categories):
        if c>=0:rhs[i,c]=1
    lu1=splu(eye(N,format='csc')-q);v1=lu1.solve(rhs)
    lu2=splu(2*eye(N,format='csc')-q);v2=lu2.solve(rhs);w1=lu1.solve(v1)
    raw=OUT/f'l2-delta{d}-n{n}-R{R}-S{S}-raw.npz'
    np.savez_compressed(raw,v1=v1,v2=v2,w1=w1)
    f=moments(d);tt=tails(f,R,S);aa=d*R+S;bb=d+1
    aq=aa*aa*tt[0]+2*aa*bb*tt[1]+bb*bb*tt[2]
    palmrec=json.loads((OUT/f'palm-delta{d}-S64.json').read_text());qp=int(palmrec['denominator'])
    pi=[(F(int(a),qp),F(int(b),qp)) for a,b in palmrec['protein_probability_numerators']]
    eta=pi[1:n]+[(1-sum(x[1] for x in pi[:n]),1-sum(x[0] for x in pi[:n]))]
    scale=[]
    for lo,hi in eta:
        assert 0<lo<=hi<=1
        e=math.floor(-math.log2(float(hi))/2);s=F(2)**e
        while s*s*hi>1:s/=2
        while 4*s*s*hi<=1:s*=2
        scale.append(s)
    tables={};bounds={};norms={};vmaxs={};resq={}
    for tag,v,s in [('v1',v1,1),('v2',v2,2),('w1',w1,1)]:
        vv=[[int(round(float(v[i,k])*QV)) for i in range(N)] for k in range(n)]
        tables[tag]=vv
        norm=[];vm=[];eqs=[]
        for k in range(n):
            residual=[]
            for i,e in enumerate(edges):
                target=tables['v1'][k][i] if tag=='w1' else (QV if categories[i]==k else 0)
                residual.append(s*vv[k][i]-sum(a*(vv[k][j]-vv[k][i]) for j,a in e)-target)
            em=F(max(map(abs,residual)),QV);vvmax=F(max(map(abs,vv[k])),QV)
            inside=F(sum(phigh[i]*residual[i]**2 for i in range(N)),cl.Q*QV*QV)
            outside=2*em*em*tt[0]+8*vvmax*vvmax*aq
            eq=inside+outside;norm.append(sqrt_upper(eq));vm.append(vvmax);eqs.append(eq)
        norms[tag]=norm;vmaxs[tag]=vm;resq[tag]=eqs
        print(json.dumps({'stage':'residuals','d':d,'tag':tag,
            'maximum_scaled_L2_residual_upper':palm.upper(max(scale[k]*norm[k] for k in range(n)))}),flush=True)
    # Integrate only the category selected by the first basis index.
    pair=[[0 for k in range(n)] for l in range(n)]
    for k in range(n):
        v=tables['v1'][k];w=tables['w1'][k];v2i=tables['v2'][k]
        for i,c in enumerate(categories):
            if c>=0:
                value=2*(v[i]+w[i]) if d==2 else 2*v[i]-v2i[i]
                pair[c][k]+=pnum[i]*value
    # pair denominator includes a factor two for both probability midpoints
    # and the half coefficient in the unequal receiver's impulse kernel.
    den=4*cl.Q*QV
    coef=F(2) if d==2 else F(3,4)
    center=[[F(pair[i][j],den)-coef*((eta[i][0]+eta[i][1])/2)*((eta[j][0]+eta[j][1])/2)
             for j in range(n)] for i in range(n)]
    es=[]
    for i in range(n):
        row=[]
        for k in range(n):
            vms=vmaxs['v1'][k]+(vmaxs['w1'][k] if d==2 else vmaxs['v2'][k]/2)
            rn=(2*norms['v1'][k]+norms['w1'][k]) if d==2 else norms['v1'][k]+norms['v2'][k]/4
            eta_product=palm.rimul(eta[i],eta[k]);cm=((eta[i][0]+eta[i][1])/2)*((eta[k][0]+eta[k][1])/2)
            ep=max(abs(eta_product[0]-cm),abs(eta_product[1]-cm))
            err=sqrt_upper(eta[i][1])*rn+vms*(tt[0]+perr)+coef*ep
            row.append(scale[i]*scale[k]*err)
        es.append(row)
    U=[[scale[i]*scale[j]*(center[i][j]+center[j][i])/2 for j in range(n)] for i in range(n)]
    eU=[[(es[i][j]+es[j][i])/2 for j in range(n)] for i in range(n)]
    # Weighted centered Gram with disjoint categories, including the rare tail.
    wp=[F(1,(k+1)**2) for k in range(len(pi))]
    ptail=F(palmrec['protein_tail_probability_upper'])
    z=(sum(wp[k]*pi[k][0] for k in range(len(pi))),sum(wp[k]*pi[k][1] for k in range(len(pi)))+ptail/F(66**2))
    weighted=[(pi[k][0]*wp[k],pi[k][1]*wp[k]) for k in range(1,n)]
    weighted.append((z[0]-sum(wp[k]*pi[k][1] for k in range(n)),
                     z[1]-sum(wp[k]*pi[k][0] for k in range(n))))
    W=[];eW=[]
    for i in range(n):
        row=[];er=[]
        for j in range(n):
            r=palm.riadd(palm.rineg(palm.rimul(weighted[i],eta[j])),palm.rineg(palm.rimul(eta[i],weighted[j])))
            r=palm.riadd(r,palm.rimul(z,palm.rimul(eta[i],eta[j])))
            if i==j:r=palm.riadd(r,weighted[i])
            row.append(scale[i]*scale[j]*(r[0]+r[1])/2);er.append(scale[i]*scale[j]*(r[1]-r[0])/2)
        W.append(row);eW.append(er)
    # Exact zero-sum sequences supply the threshold coefficient by complement.
    fun={}
    for tag,arr in palmrec['return_coefficient_numerators'].items():
        ar=[(F(int(a),qp),F(int(b),qp)) for a,b in arr]
        v=ar[1:n]+[(-sum(x[1] for x in ar[:n]),-sum(x[0] for x in ar[:n]))]
        fun[tag]=[(scale[i]*v[i][0],scale[i]*v[i][1]) for i in range(n)]
    info={'d':d,'basis_size':n,'RNA_cap':R,'protein_cap':S,
        'basis':'I(P=k), k=1,...,n-1, and I(P>=n); global constants excluded',
        'exact_scales':[str(x) for x in scale],'eta_intervals':[list(map(str,x)) for x in eta],
        'outside_probability_upper':str(tt[0]),'outside_M_upper':str(tt[1]),'outside_M2_upper':str(tt[2]),
        'residual_L2_squared_upper':{k:[str(x) for x in v] for k,v in resq.items()},
        'maximum_scaled_Gram_entry_error_upper':palm.upper(max(max(x) for x in eU)),
        'raw_vectors':str(raw.relative_to(ROOT)),'probability_intervals':str((OUT/f'l2-cluster-delta{d}-R{R}-S{S}.json').relative_to(ROOT))}
    return {'U':U,'eU':eU,'W':W,'eW':eW,'fun':fun,'info':info}

def certificate(A,E,tag):
    n=len(A);a=np.array([[float(x) for x in r] for r in A])
    try:T=np.linalg.inv(np.linalg.cholesky(a))
    except np.linalg.LinAlgError:
        return {'tag':tag,'positive_definite':False,'status':'central_Cholesky_failed_inconclusive'}
    Ki=[[round(x*QK) for x in r] for r in A]
    Ti=[[int(round(float(x)*QT)) for x in r] for r in T]
    err=max(E[i][j]+abs(A[i][j]-F(Ki[i][j],QK)) for i in range(n) for j in range(n))
    prod=[[sum(Ti[i][k]*Ki[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    M=[[sum(prod[i][k]*Ti[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    ls=[F(sum(map(abs,r)),QT) for r in Ti];total=sum(ls);den=QK*QT*QT
    margin=[F(M[i][i]-sum(abs(M[i][j]) for j in range(n) if j!=i),den)-err*ls[i]*total for i in range(n)]
    record={'tag':tag,'dimension':n,'positive_definite':all(z>0 for z in margin),
      'proof':'Exact rational congruence; every transformed true diagonal exceeds sum of off-diagonal absolute values after perturbation allowance.',
      'central_entry_error_upper':str(err),'minimum_Gershgorin_margin_lower':palm.lower(min(margin)),
      'K_denominator':str(QK),'T_denominator':str(QT),'K_numerators':[[str(z) for z in r] for r in Ki],
      'T_numerators':[[str(z) for z in r] for r in Ti],
      'exact_Gershgorin_margins':[str(z) for z in margin]}
    path=OUT/f'l2-certificate-{tag}.json';path.write_text(json.dumps(record,indent=2)+'\n')
    return {k:v for k,v in record.items() if k not in ['K_numerators','T_numerators','exact_Gershgorin_margins','K_denominator','T_denominator']}|{'certificate_file':str(path.relative_to(ROOT))}

def returns(g1,g2,key):
    n=len(g1['U']);B=[];E=[]
    for i in range(n):
        row=[];er=[]
        for j in range(n):
            if key=='B1':
                dr=palm.riadd(g2['fun']['D1'][j],g2['fun']['Dt1'][j])
                v=palm.riadd(palm.rimul(g1['fun']['A'][i],dr),palm.rimul(g1['fun']['H'][i],g2['fun']['D1'][j]))
            else:
                dr=palm.riadd(g1['fun']['D1'][i],palm.rimul((F(-1,2),F(-1,2)),g1['fun']['D2'][i]))
                v=palm.riadd(palm.rimul(dr,g2['fun']['A'][j]),palm.rimul(g1['fun']['D1'][i],g2['fun']['H'][j]))
            row.append((v[0]+v[1])/2);er.append((v[1]-v[0])/2)
        B.append(row);E.append(er)
    return B,E

def run(n,R,S):
    assert 16<=n<=64 and S>n
    gs={d:record_parent(d,n,R,S) for d in [1,2]};checks=[]
    exact={}
    for d,g in gs.items():
        for alpha in [F(1,100),F(2,5) if d==1 else F(4,5)]:
            K=[[g['U'][i][j]-alpha*g['W'][i][j] for j in range(n)] for i in range(n)]
            E=[[g['eU'][i][j]+alpha*g['eW'][i][j] for j in range(n)] for i in range(n)]
            checks.append(certificate(K,E,f'n{n}-d{d}-coercivity-{alpha.numerator}over{alpha.denominator}'))
        exact[str(d)]={k:[[str(z) for z in r] for r in g[k]] for k in ['U','eU','W','eW']}
    for key in ['B1','B2_transpose']:
        B,eb=returns(gs[1],gs[2],key);k=F(3,4);K=[];E=[]
        for i in range(2*n):
            row=[];er=[]
            for j in range(2*n):
                if i<n and j<n:z=k*gs[1]['U'][i][j];e=k*gs[1]['eU'][i][j]
                elif i>=n and j>=n:z=k*gs[2]['U'][i-n][j-n];e=k*gs[2]['eU'][i-n][j-n]
                elif i<n:z=B[i][j-n];e=eb[i][j-n]
                else:z=B[j][i-n];e=eb[j][i-n]
                row.append(z);er.append(e)
            K.append(row);E.append(er)
        checks.append(certificate(K,E,f'n{n}-{key}-contraction'))
        exact[key]={'matrix':[[str(z) for z in r] for r in B],'entry_errors':[[str(z) for z in r] for r in eb]}
    (OUT/f'l2-gram-n{n}-exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    result={'job_id':'phys-00018-p01-research-3ff79a4c94a6','basis_size':n,
      'scope':f'All real responses constant above protein count {n-1}, for the fixed unequal parent pair, on the infinite-state unregulated process. Perturbative local route only.',
      'parents':[gs[d]['info'] for d in [1,2]],'checks':checks,
      'whole_space_coercivity_established':False,'original_status':'unresolved',
      'limitations':'No arbitrary bounded tail, arbitrary kinetic tuple, strong-feedback or larger-N theorem. Proposer verification is not referee acceptance.'}
    path=OUT/f'l2-gram-n{n}-results.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--basis',type=int,default=32);a.add_argument('--RNA-cap',type=int,default=48);a.add_argument('--protein-cap',type=int,default=128)
    p=a.parse_args();run(p.basis,p.RNA_cap,p.protein_cap)
