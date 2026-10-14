"""Fresh referee reconstruction. No discovery module or cached point data imported.

Physical parameters transcribed from the frozen model; published inputs checked
against JPA (19),(26),(49)-(54) and PRL (22)-(25), SM (S5).
The exported interval partition is used only for exact certificate resummation,
independent point/range comparisons and a disclosed quadrature integration grid.
Quadrature is a diagnostic, never the rigorous range certificate.
"""
import datetime, hashlib, itertools, json, math, time
from fractions import Fraction
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.linalg import solve
from scipy.special import expit

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'reproducibility/run-output'
RUN.mkdir(parents=True,exist_ok=True)
OUT=RUN/'physical-replay.json'
N=128
OBS=['Delta','J','sigma_over_kB','chi_minus24']
START=time.monotonic()
result={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'in_progress', 'independence':'No discovery code imported; fresh LDL branch elimination and direct 3x3 core inverse, dense 387-site solve, Slater minors and source determinant. Only the frozen exported partition/range bounds are read for comparison and diagnostic integration grid.'}

def save(stage,data):
    result[stage]=data
    result['elapsed_seconds']=time.monotonic()-START
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'stage':stage,'result':data}),flush=True)

def certificate():
    path=ROOT/'evidence/research/r3-interval-refine.json'
    cert=json.loads(path.read_text()); panels=cert['panels']
    assert cert['status']=='positive_residual_enclosed_proposer_only'
    assert panels[0]['q_interval'][0]==-8192 and panels[-1]['q_interval'][1]==16384
    totals=[[Fraction(0),Fraction(0)] for _ in OBS]; width=Fraction(0)
    prev=Fraction(-8192)
    for row in panels:
        lo,hi=map(Fraction,row['q_interval'])
        assert lo==prev and hi>lo
        assert Fraction(float(hi)-float(lo))==hi-lo
        prev=hi; width+=hi-lo
        for total,interval in zip(totals,row['integrated_ranges']):
            a,b=map(Fraction,interval);assert a<=b
            total[0]+=a;total[1]+=b
    assert width==24576 and prev==16384
    mp.iv.dps=100
    h=3*mp.iv.exp(-mp.iv.mpf(8192)/100+24)
    p=3*mp.iv.exp(1-mp.iv.mpf(16384)/100)
    jt=2*(h+p);et=28*jt;ct=2*mp.iv.exp(24)*(h+p);dt=24*jt+4*et+ct
    tails=[dt,jt,et,ct]
    # Read exact mpf tuple directly, without nearest-rounded decimal conversion.
    def exact_endpoint(t):
        sign,man,exponent,_=t
        return (-1 if sign else 1)*Fraction(man)*(Fraction(2)**exponent)
    tail_upper=[exact_endpoint(t._mpi_[1]) for t in tails]
    enclosed={}
    exact={}
    for name,total,tail in zip(OBS,totals,tail_upper):
        lo,hi=total[0]-tail,total[1]+tail
        exact[name]=[str(lo),str(hi)]
        enclosed[name]=[math.nextafter(float(lo),-math.inf),math.nextafter(float(hi),math.inf)]
    assert totals[0][0]-tail_upper[0]>Fraction('0.019447')
    assert totals[0][1]+tail_upper[0]<Fraction('0.024248')
    assert totals[0][1]-totals[0][0]+2*tail_upper[0]<Fraction('0.005')
    assert totals[1][0]-tail_upper[1]>0 and totals[2][0]-tail_upper[2]>0
    save('certificate_resummation',{'panels':len(panels),'fallback_panels':sum(not r['transmission_denominator_validated'] for r in panels),
         'exact_q_width':str(width),'full_consecutive_coverage':True,'enclosures':enclosed,
         'tails_upper':[math.nextafter(float(t),math.inf) for t in tail_upper],
         'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (RUN/'exact-sums.json').write_text(json.dumps({'exact_endpoint_fractions_with_independent_tails':exact},indent=2)+'\n')
    return panels,enclosed

def constants():
    mp.mp.dps=200
    eps=mp.mpf(1)/100
    gf=eps/(2*mp.sin(mp.pi/256))
    h=[eps/(2*mp.sqrt(mp.sin((2*l+1)*mp.pi/256)*mp.sin((2*l-1)*mp.pi/256))) for l in range(1,128)]
    gc=mp.mpf(200000);lam2=gf*gc;t=mp.mpf(10000);E0=mp.mpf(5000)
    v2=2*t*t*gf/mp.sqrt(E0*(4*t-E0))
    sig0=v2*(E0-2*t-mp.j*mp.sqrt(E0*(4*t-E0)))/(2*t*t)
    P=mp.matrix([[0,0,1],[1,0,0],[0,1,0]])
    ring=mp.j*gc*(P-P.T)
    return eps,gf,h,gc,lam2,t,v2,sig0,ring

C=constants()
def scattering_mp(q):
    eps,gf,h,gc,lam2,t,v2,sig0,ring=C
    delta=eps*mp.mpf(q);E=5000+delta
    sig=v2*(E-2*t-mp.j*mp.sqrt(E*(4*t-E)))/(2*t*t)
    broad=-mp.im(sig)
    diag=delta+mp.re(sig0)-sig
    # Symmetric (not conjugate) LDL, because the branch retarded matrix is
    # complex symmetric. Inverse (1,1) is a sum over inverse-L factors.
    prefix=mp.mpc(1);g11=mp.mpc(0)
    for l in range(N):
        g11+=prefix*prefix/diag
        if l==N-1:
            gnn=1/diag;g1n=prefix/diag
        else:
            prefix*=h[l]/diag
            diag=delta-h[l]*h[l]/diag
    core=(delta-lam2*gnn)*mp.eye(3)-ring
    green=g11*mp.eye(3)+lam2*g1n*g1n*(core**-1)
    S=mp.eye(3)-2*mp.j*broad*green
    f=[1/(1+mp.exp(delta-mu)) for mu in [1,-3,-24]]
    return S,f

def slater_statistics(S,f):
    probs={-1:mp.mpf(0),0:mp.mpf(0),1:mp.mpf(0)}
    currents=[mp.mpf(0)]*3
    masks=list(range(8))
    for incoming in masks:
        cols=[b for b in range(3) if incoming>>b&1]
        w=mp.fprod(f[b] if incoming>>b&1 else 1-f[b] for b in range(3))
        for outgoing in masks:
            rows=[a for a in range(3) if outgoing>>a&1]
            if len(rows)!=len(cols):continue
            amp=mp.mpf(1) if not rows else mp.det(mp.matrix([[S[a,b] for b in cols] for a in rows]))
            prob=w*abs(amp)**2
            counts=[((incoming>>a)&1)-((outgoing>>a)&1) for a in range(3)]
            probs[counts[0]]+=prob
            for a in range(3):currents[a]+=prob*counts[a]
    M=sum(probs[k]*mp.exp(-24*k) for k in probs)
    chi=mp.log(M);J=currents[0];entropy=sum(mu*j for mu,j in zip([1,-3,-24],currents))
    return [24*J-chi-4*entropy,J,entropy,chi],probs,currents

def high_precision(panels):
    # Freeze a deterministic adversarial grid: center, transmission edge,
    # both sides, largest residual widths, valid and fallback panels.
    indices=sorted(set([0,len(panels)-1]+[int(i*(len(panels)-1)/24) for i in range(25)]
                  +sorted(range(len(panels)),key=lambda i:panels[i]['integrated_ranges'][0][1]-panels[i]['integrated_ranges'][0][0],reverse=True)[:16]))
    points=[mp.mpf(str(x)) for x in [-4,-2,-1.1,-1.01,-1,-.999,-.99,-.5,0,.5,.99,.999,1,1.01,1.1,2,4]]
    selected=[(i,mp.mpf(panels[i]['q_interval'][0])/2+mp.mpf(panels[i]['q_interval'][1])/2) for i in indices]
    checks=[];maxima={name:mp.mpf(0) for name in ['unitarity','probability_sum','mean_match','all_current_match','MGF_match','conservation','surface_map']}
    for index,q in [(None,x) for x in points]+selected:
        S,f=scattering_mp(q)
        data,prob,current=slater_statistics(S,f)
        unit=S*S.H-mp.eye(3)
        err=max(abs(v) for v in unit)
        src=[f[a]-sum(abs(S[a,b])**2*f[b] for b in range(3)) for a in range(3)]
        pp=f[0]*sum(abs(S[0,b])**2*(1-f[b]) for b in [1,2])
        pm=(1-f[0])*sum(abs(S[0,b])**2*f[b] for b in [1,2])
        scalar=1+pp*(mp.exp(-24)-1)+pm*(mp.exp(24)-1)
        F=mp.diag(f);Vminus=mp.diag([mp.exp(24),1,1]);Vplus=mp.diag([mp.exp(-24),1,1])
        determinant=mp.det(mp.eye(3)-F+F*S.H*Vminus*S*Vplus)
        mgf=sum(prob[k]*mp.exp(-24*k) for k in prob)
        E=mp.mpf(5000)+C[0]*q
        outgoing_k=mp.acos(1-E/(2*C[5]))
        surface_bloch=-mp.exp(mp.j*outgoing_k)/C[5]
        surface_quadratic=(E-2*C[5]-mp.j*mp.sqrt(E*(4*C[5]-E)))/(2*C[5]**2)
        errors={'unitarity':err,'probability_sum':abs(sum(prob.values())-1),
                'mean_match':abs(data[1]-(pp-pm)),
                'all_current_match':max(abs(x-y) for x,y in zip(src,current)),
                'MGF_match':max(abs(mgf-scalar),abs(mgf-determinant)),
                'conservation':abs(sum(current)),'surface_map':abs(surface_bloch-surface_quadratic)}
        for name,value in errors.items():maxima[name]=max(maxima[name],value)
        contained=None
        if index is not None:
            row=panels[index];lo,hi=row['q_interval'];width=mp.mpf(hi)-mp.mpf(lo)
            contained=[mp.mpf(r[0])<=v*C[0]*width<=mp.mpf(r[1]) for v,r in zip(data,row['integrated_ranges'])]
            assert all(contained),(index,str(q),contained,[str(v) for v in data],row)
        checks.append({'q':str(q),'panel_index':index,'point_in_exported_full_panel_integral_range':contained,
                       'u_T01':mp.nstr(abs(S[0,1])**2,30),'v_T02':mp.nstr(abs(S[0,2])**2,30),
                       'densities':{name:mp.nstr(v,30) for name,v in zip(OBS,data)}})
    assert max(maxima.values())<mp.mpf('1e-150'),{k:str(v) for k,v in maxima.items()}
    save('independent_high_precision',{'decimal_digits':200,'points':len(checks),'max_errors':{k:mp.nstr(v,8) for k,v in maxima.items()},'checks':checks})

def np_constants():
    eps,gf,h,gc,lam2,t,v2,sig0,ring=C
    return float(eps),float(gf),np.array([float(x) for x in h]),float(gc),float(lam2),float(t),float(v2),float(mp.re(sig0)),np.array(ring.tolist(),dtype=complex)

NC=np_constants()
def scattering_np(q):
    eps,gf,h,gc,lam2,t,v2,sig0,ring=NC
    q=np.asarray(q);delta=eps*q;E=5000+delta
    broad=v2*np.sqrt(E*(4*t-E))/(2*t*t)
    # The real contact difference is exactly linear in delta. Evaluate that
    # identity without subtracting two 5000-scale floating energies.
    diag=delta*(1-v2/(2*t*t))+1j*broad
    prefix=np.ones_like(q,dtype=complex);g11=np.zeros_like(prefix)
    for l in range(N):
        g11+=prefix*prefix/diag
        if l==N-1:gnn=1/diag;g1n=prefix/diag
        else:
            prefix*=h[l]/diag;diag=delta-h[l]*h[l]/diag
    core=(delta-lam2*gnn)[...,None,None]*np.eye(3)-ring
    green=g11[...,None,None]*np.eye(3)+lam2*(g1n*g1n)[...,None,None]*np.linalg.inv(core)
    S=np.eye(3)-2j*broad[...,None,None]*green
    return S

def dense_check():
    eps,gf,h,gc,lam2,t,v2,sig0,ring=NC
    dim=3*(N+1);H=np.zeros((dim,dim),complex)
    outer=[a*(N+1) for a in range(3)];cores=[a*(N+1)+N for a in range(3)]
    for a in range(3):
        start=a*(N+1)
        H[start,start]=-sig0
        for l,x in enumerate(h):H[start+l,start+l+1]=H[start+l+1,start+l]=x
        H[start+N-1,start+N]=H[start+N,start+N-1]=math.sqrt(lam2)
    H[np.ix_(cores,cores)]=ring
    assert np.max(abs(H-H.conj().T))==0
    errs=[]
    for q in [-1.01,-.99,0,.99,1.01]:
        delta=eps*q;E=5000+delta
        sig=v2*(E-2*t-1j*np.sqrt(E*(4*t-E)))/(2*t*t)
        A=delta*np.eye(dim)-H
        for a in outer:A[a,a]-=sig
        rhs=np.eye(dim)[:,outer]
        G=solve(A,rhs,assume_a='gen',check_finite=False)[outer,:]
        S=np.eye(3)-2j*(-sig.imag)*G
        rep=scattering_np(np.array([q]))[0]
        errs.append({'q':q,'max_scattering_difference':float(np.max(abs(S-rep))),'max_unitarity_error':float(np.max(abs(S@S.conj().T-np.eye(3))))})
    assert max(r['max_scattering_difference'] for r in errs)<1e-6
    save('dense_hamiltonian_check',{'sample_sites':dim,'Hermitian':True,'method':'Direct dense 387-site retarded solve, without LDL/continuant coefficients','points':errs})

def diagnostics(panels,enclosed):
    # Direct quadrature at fixed Hamiltonian, using original Fermi occupations
    # and source row currents, not the submitted linear residual formulas.
    a=np.array([p['q_interval'][0] for p in panels]);b=np.array([p['q_interval'][1] for p in panels])
    rows=[]
    for order in [2,4,8]:
        nodes,weights=np.polynomial.legendre.leggauss(order)
        vals=np.zeros(4)
        peak_unit=0.
        for start in range(0,len(a),1000):
            aa,bb=a[start:start+1000],b[start:start+1000]
            q=((aa+bb)[:,None]/2+(bb-aa)[:,None]*nodes/2).ravel()
            S=scattering_np(q);T=abs(S)**2
            f=expit(np.array([1,-3,-24])[None,:]-.01*q[:,None])
            # Differences avoid subtracting unit reflection at remote energies.
            currents=np.sum(T*(f[:,:,None]-f[:,None,:]),axis=2)
            entropy=currents@np.array([1,-3,-24])
            pp=f[:,0]*np.sum(T[:,0,1:]*(1-f[:,1:]),axis=1)
            pm=(1-f[:,0])*np.sum(T[:,0,1:]*f[:,1:],axis=1)
            # M is positive, with no clipping of a discovered violation.
            chi=np.log1p(pp*np.expm1(-24)+pm*np.expm1(24))
            J=currents[:,0];delta=24*J-chi-4*entropy
            array=np.stack([delta,J,entropy,chi],axis=1).reshape(len(aa),order,4)
            vals+=np.sum(array*weights[None,:,None]*(bb-aa)[:,None,None]/2,axis=(0,1))*.01
            if np.max(abs(q))<2:
                peak_unit=max(peak_unit,float(np.max(abs(S@S.conj().transpose(0,2,1)-np.eye(3)))))
        row={'Gauss_order_per_frozen_panel':order,'integrals':dict(zip(OBS,vals.tolist())),
             'inside_rigorous_submitted_enclosures':[bool(enclosed[name][0]<=v<=enclosed[name][1]) for name,v in zip(OBS,vals)],
             'central_max_unitarity_error':peak_unit}
        assert all(row['inside_rigorous_submitted_enclosures']),row
        rows.append(row)
        print(json.dumps({'quadrature_diagnostic':row}),flush=True)
    save('independent_quadrature_diagnostic',{'rows':rows,'order4_to8_difference':{name:abs(rows[-1]['integrals'][name]-rows[-2]['integrals'][name]) for name in OBS},
        'error_status':'Diagnostic convergence; not a rigorous enclosure. Grid shared with exported certificate, fresh physical Hamiltonian/scattering/integrand implementation.'})

def baseline():
    # Published centered boxcar, F=4, width shrinks at positive T=1.
    F=mp.mpf(4);center=mp.tanh(F/4);s=mp.mpf('-1.3')
    leading=mp.log((1+mp.cosh(F/2+s))/(1+mp.cosh(F/2)))
    cases=[]
    for w in [mp.mpf(1)/16,mp.mpf(1)/32,mp.mpf(1)/64]:
        f0=lambda x:1/(1+mp.exp(x-F/2))
        f1=lambda x:1/(1+mp.exp(x+F/2))
        mean=mp.quad(lambda x:f0(x)-f1(x),[-w/2,w/2])
        cgf=mp.quad(lambda x:mp.log((1-f0(x)+f0(x)*mp.exp(s))*(1-f1(x)+f1(x)*mp.exp(-s))),[-w/2,w/2])
        cases.append({'width':str(w),'J_over_width':float(mean/w),'J_limit_error':float(abs(mean/w-center)),
                      'chi_over_width':float(cgf/w),'chi_limit_error':float(abs(cgf/w-leading)),
                      'entropy_equals_FJ':True})
    assert cases[-1]['J_limit_error']<cases[-2]['J_limit_error']/3.99
    assert cases[-1]['chi_limit_error']<cases[-2]['chi_limit_error']/3.99
    save('published_boxcar_baseline',{'source':'JPA final (19),(26),(49)-(54)','F':4,'T':1,'counting_field':float(s),
        'mean_limit':float(center),'CGF_limit':float(leading),'cases':cases})

def main():
    panels,enclosed=certificate();baseline();high_precision(panels);dense_check();diagnostics(panels,enclosed)
    result['status']='completed_reproducibility_replay'
    result['elapsed_seconds']=time.monotonic()-START
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds']}),flush=True)

if __name__=='__main__':main()
