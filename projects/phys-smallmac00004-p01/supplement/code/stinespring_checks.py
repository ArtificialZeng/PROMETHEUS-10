#!/usr/bin/env python3
"""Independent source reconstruction and finite diagnostics; no proposer imports."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import json,time,sys,resource
import numpy as np
import sympy as sy
import mpmath as mp
from flint import arb,ctx

JOB='phys-smallmac00004-p01-referee-64603a9bf05d'
mp.mp.dps=80
ctx.prec=256

def symbolic():
    # Real nonnegative amplitudes; impose their physical squared magnitudes later.
    u,v,w=sy.symbols('u v w',real=True,nonnegative=True)
    p,q=sy.symbols('p q',real=True)
    x,y,z=sy.symbols('x y z',real=True)
    rho=sy.Matrix([[1+z,x-sy.I*y],[x+sy.I*y,1-z]])/2
    iso=sy.zeros(12,2)
    iso[0,0]=u; iso[1,0]=v; iso[10,0]=w
    iso[4,1]=u; iso[5,1]=-v; iso[11,1]=w
    J=iso*rho*iso.conjugate().T
    rec=sy.Matrix(3,3,lambda i,j:sum(J[4*i+k,4*j+k] for k in range(4)))
    env=sy.Matrix(4,4,lambda i,j:sum(J[4*k+i,4*k+j] for k in range(3)))
    substitution={u*u:(1-q)*(1-p),v*v:(1-q)*p,w*w:q}
    def physical(M):
        # Replace the cross amplitude before squared amplitudes; otherwise SymPy
        # rewrites u via u^2 and creates sqrt products with unassumed p,q signs.
        return M.applyfunc(lambda t:sy.simplify(sy.expand(t).subs(u*v,(1-q)*sy.sqrt(p*(1-p))).subs(substitution,simultaneous=True)))
    expectedB=sy.diag(0,0,q)
    expectedB[:2,:2]=(1-q)*sy.Matrix([[1+z,(1-2*p)*(x-sy.I*y)],[(1-2*p)*(x+sy.I*y),1-z]])/2
    expectedE=sy.diag(0,0,0,0)
    expectedE[:2,:2]=(1-q)*sy.Matrix([[1-p,sy.sqrt(p*(1-p))*z],[sy.sqrt(p*(1-p))*z,p]])
    expectedE[2:4,2:4]=q*rho
    checks={
        'isometry_completeness':physical(iso.T*iso)==sy.eye(2),
        'receiver_partial_trace':(physical(rec)-expectedB).applyfunc(sy.simplify)==sy.zeros(3),
        'full_environment_partial_trace':(physical(env)-expectedE).applyfunc(sy.simplify)==sy.zeros(4),
        'rho_determinant':sy.simplify(rho.det()-(1-x*x-y*y-z*z)/4)==0,
        'dephased_determinant':sy.simplify((expectedB[:2,:2]/(1-q)).det()-(1-(1-2*p)**2*(x*x+y*y)-z*z)/4)==0,
        'dephasing_env_determinant':sy.simplify((expectedE[:2,:2]/(1-q)).det()-p*(1-p)*(1-z*z))==0,
    }
    assert all(checks.values()),checks
    return {'checks':checks,'receiver':str(expectedB),'environment':str(expectedE),
            'squared_spectral_radii':{'rho':'x^2+y^2+z^2','receiver_qubit':'(1-2p)^2(x^2+y^2)+z^2','environment_dephase':'(1-2p)^2+4p(1-p)z^2'},
            'source_map':'S1 PDF p.7 (C1), p.9 (D1), p.5 (16). E uses [d0,d1,er0,er1]; C1 uses [er0,er1,d0,d1].'}

def H(r):
    r=mp.mpf(r)
    if abs(r-1)<mp.mpf('1e-14'): r=mp.mpf(1)
    assert 0<=r<=1,r
    a=(1+r)/2;b=(1-r)/2
    return -sum(t*mp.log(t,2) for t in [a,b] if t)

def scalar_ic(p,q,v):
    p,q=mp.mpf(str(p)),mp.mpf(str(q))
    x,y,z=map(lambda t:mp.mpf(str(t)),v)
    R=mp.sqrt(x*x+y*y+z*z)
    a=1-2*p
    s=mp.sqrt(a*a*(x*x+y*y)+z*z)
    t=mp.sqrt(a*a+4*p*(1-p)*z*z)
    return (1-q)*(H(s)-H(t))-q*H(R)

def outputs(p,q,v):
    x,y,z=v
    rho=np.array([[1+z,x-1j*y],[x+1j*y,1-z]])/2
    W=np.zeros((12,2),complex)
    W[0,0]=np.sqrt((1-q)*(1-p));W[1,0]=np.sqrt((1-q)*p);W[10,0]=np.sqrt(q)
    W[4,1]=np.sqrt((1-q)*(1-p));W[5,1]=-np.sqrt((1-q)*p);W[11,1]=np.sqrt(q)
    joint=(W@rho@W.conj().T).reshape(3,4,3,4)
    return np.trace(joint,axis1=1,axis2=3),np.trace(joint,axis1=0,axis2=2)

eigen_min=1.0
trace_max=0.0
def entropy(M):
    global eigen_min,trace_max
    e=np.linalg.eigvalsh(M)
    eigen_min=min(eigen_min,float(e.min()))
    trace_max=max(trace_max,abs(float(e.sum())-1))
    assert e.min()>-5e-14
    e=e[e>0]
    return -float(np.sum(e*np.log2(e)))

def coherent(p,q,v):
    B,E=outputs(p,q,v)
    return entropy(B)-entropy(E)

def optimal_radius(p):
    p=mp.mpf(str(p));q=3*p;a=1-2*p
    # Unique root: atanh(a r)/atanh(r) strictly decreases, by coefficient ratios.
    lo=mp.mpf(0);hi=mp.mpf(1)
    for _ in range(230):
        r=(lo+hi)/2
        if (1-q)*a*mp.atanh(a*r)-q*mp.atanh(r)>0:lo=r
        else:hi=r
    r=(lo+hi)/2
    B=(1-q)*(1-H(a*r))-q*(1-H(r))
    return r,B

def root_ball(p,approx):
    pp=arb(str(p));q=3*pp;a=1-2*pp
    # Exact decimal rational bracket around the independently bisected root.
    n=int(mp.floor(approx*10**60));lo=arb(n)/10**60;hi=arb(n+1)/10**60
    def derivative(r):return ((1-q)*a*(a*r).atanh()-q*r.atanh())/arb(2).log()
    dl,dh=derivative(lo),derivative(hi)
    assert dl>0 and dh<0
    def hh(r):
        s=(1+r)/2;t=(1-r)/2
        return -(s*s.log()+t*t.log())/arb(2).log()
    rb=lo.union(hi)
    val=(1-q)*(1-hh(a*rb))-q*(1-hh(rb))
    return {'root_decimal_numerator':str(n),'root_denominator':'10^60','lower_derivative':str(dl),'upper_derivative':str(dh),'B_enclosure':str(val),'globality':'Strictly decreasing positive power-series coefficient ratio atanh(a r)/atanh(r), plus derivative signs at 0+ and 1-.'}

def main():
    start=time.monotonic();sym=symbolic()
    rng=np.random.default_rng(2026091264603)
    states=[np.array(v,float) for v in [(0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,0,1),(0,0,-1),(.3,-.4,.5),(0,0,.8)]]
    for radius in [.05,.5,.87,.93,.98,.999999,1.0]:
        for _ in range(6):
            v=rng.normal(size=3);states.append(radius*v/np.linalg.norm(v))
    cases=[(0,0),(0,1),(.5,0),(.5,1),(.5,.5),(.1,.3),(.108,.324),(.10925,.32775),(.11,.33),(.1105,.3315)]
    differences=[]
    for p,q in cases:
        for v in states:differences.append(abs(coherent(p,q,v)-float(scalar_ic(p,q,v))))
    tol=2e-12
    assert max(differences)<tol
    baselines={};min_claim=1e9;max_holevo_ic_difference=0.;ensemble_count=0
    lower_margins=[];upper_margins=[];signal_count=0
    for p in [.1,.108,.10925,.11,.1105]:
        r,B=optimal_radius(p)
        baselines[str(p)]={'r':mp.nstr(r,75),'B_bits':mp.nstr(B,75),'arb_global_enclosure':root_ball(p,r)}
        pair=[np.array([float(r),0,0]),np.array([-float(r),0,0])]
        pi_pair=coherent(p,3*p,[0,0,0])-sum(coherent(p,3*p,v) for v in pair)/2
        baselines[str(p)]['stinespring_pair_rate']=pi_pair
        baselines[str(p)]['pair_scalar_error']=abs(pi_pair-float(B))
        assert abs(pi_pair-float(B))<tol
        if p==.1:continue
        C=float(scalar_ic(p,3*p,[0,0,0]));m=C-float(B)
        for v in states:
            f=coherent(p,3*p,v);z=v[2]
            lower_margins.append(f-m-.012*z*z)
            upper_margins.append(C+.011*z*z-f)
        for M in [1,2,3,4,8,19]:
            for mode in range(10):
                vs=[]
                for _ in range(M):
                    v=rng.normal(size=3);v*=rng.uniform(0,1)/np.linalg.norm(v)
                    if mode==0:v[2]=0
                    if mode==1:v[:2]=0
                    vs.append(v)
                weights=rng.integers(1,100,size=M).astype(float)
                if mode==2 and M>1:weights[0]=0
                weights/=weights.sum()
                outputs_a=[outputs(p,3*p,v) for v in vs]
                meanB=sum(w*o[0] for w,o in zip(weights,outputs_a))
                meanE=sum(w*o[1] for w,o in zip(weights,outputs_a))
                pi=entropy(meanB)-sum(w*entropy(o[0]) for w,o in zip(weights,outputs_a))-entropy(meanE)+sum(w*entropy(o[1]) for w,o in zip(weights,outputs_a))
                mean=sum(w*v for w,v in zip(weights,vs))
                pi_ic=float(scalar_ic(p,3*p,mean)-sum(mp.mpf(str(w))*scalar_ic(p,3*p,v) for w,v in zip(weights,vs)))
                max_holevo_ic_difference=max(max_holevo_ic_difference,abs(pi-pi_ic))
                zbar=mean[2];var=sum(w*(v[2]-zbar)**2 for w,v in zip(weights,vs))
                min_claim=min(min_claim,float(B)-.012*var-.001*zbar*zbar-pi)
                ensemble_count+=1;signal_count+=M
    assert min_claim>-tol and min(lower_margins)>-tol and min(upper_margins)>-tol
    assert max_holevo_ic_difference<tol
    pp=arb(11)/100;q=3*pp;a=1-2*pp;z=arb(4)/5
    def h(r):
        u=(1+r)/2;v=(1-r)/2
        return -(u*u.log()+v*v.log())/arb(2).log()
    C=(1-q)*(1-h(a))-q
    G=(1-2*q)*h(z)-(1-q)*h((a*a+4*pp*(1-pp)*z*z).sqrt())
    slack=G-C
    assert slack>0
    result={'job_id':JOB,'created_at':datetime.now(timezone.utc).isoformat(),'symbolic':sym,
            'state_channel_cases':len(differences),'matrix_scalar_max_abs_bits':max(differences),
            'minimum_output_eigenvalue_float':eigen_min,'maximum_trace_error_float':trace_max,
            'diagnostic_tolerance_bits':tol,'baselines':baselines,'ensemble_count':ensemble_count,'signal_count':signal_count,
            'ensemble_full_holevo_vs_scalar_error':max_holevo_ic_difference,'minimum_penalized_bound_margin':min_claim,
            'minimum_lower_envelope_margin':min(lower_margins),'minimum_upper_envelope_margin':min(upper_margins),
            'existing_bound_slack_at_p011_arb':str(slack),'slack_argument':'max F - min F - B >= G(16/25)-C, since min F <= m and B=C-m. Legal z=4/5; no numerical global maximizer is assumed.',
            'all_pass':True,'elapsed_seconds':time.monotonic()-start,'max_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'limitations':'Finite matrix/ensemble tests are floating diagnostic checks, not proof. Universal scope comes from reviewed analytic reductions and the separate continuum interval replay. Pure-state roundoff is tolerated explicitly.'}
    Path('audit/referee-source-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
