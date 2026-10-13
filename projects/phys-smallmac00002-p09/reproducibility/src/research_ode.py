"""B: separately built conservative row generator, integrated by DOP853.

Reads no A script or output. States are ordered (3,1,2,absorber+,absorber-).
The protocol and observable definitions are shared problem inputs.
"""
import json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss

OUT=Path('evidence/research')
TRIPLES=[(10,1,1),(1,10,1),(1,1,10)]
BASIS=[3,1,2,'plus','minus']
INDEX={v:i for i,v in enumerate(BASIS)}
GENERATORS=[]
for a,b,c in TRIPLES:
    row=np.zeros((5,5))
    for u,v,k in [(1,2,a),(2,1,a),(2,3,b),(3,2,b),(3,1,c),(1,3,c)]:
        dest='plus' if (u,v)==(1,2) else 'minus' if (u,v)==(2,1) else v
        row[INDEX[u],INDEX[dest]]+=k
        row[INDEX[u],INDEX[u]]-=k
    assert np.array_equal(row.sum(axis=1),np.zeros(5))
    GENERATORS.append(row)

def at(t,x,rtol=2e-11,atol=2e-13):
    stop=t+x; now=t
    y=np.zeros((2,5));y[0,INDEX[2]]=1;y[1,INDEX[1]]=1
    while now<stop-1e-14:
        seg=int(np.floor(now+1e-12));end=min(stop,seg+1.)
        G=GENERATORS[seg%3]
        sol=solve_ivp(lambda z,w:(w.reshape(2,5)@G).reshape(-1),
                      (now,end),y.reshape(-1),method='DOP853',rtol=rtol,atol=atol)
        assert sol.success
        y=sol.y[:,-1].reshape(2,5);now=end
    final=int(np.floor(stop+1e-12))%3
    a=TRIPLES[final][0]
    flux=np.array([[a*y[0,INDEX[1]],a*y[0,INDEX[2]]],
                   [a*y[1,INDEX[1]],a*y[1,INDEX[2]]]])
    return flux,float(np.max(np.abs(y.sum(axis=1)-1)))

def averaged(x,order):
    nodes,weights=leggauss(order);D=np.zeros((2,2));masserr=0
    cuts=sorted(set([0.,1.,2.,3.]+[round(float((j-x)%3),13) for j in range(3)]))
    for lo,hi in zip(cuts[:-1],cuts[1:]):
        if hi-lo<1e-13:continue
        for q,w in zip(nodes,weights):
            t=(hi+lo)/2+(hi-lo)*q/2
            flux,err=at(t,x)
            a0=TRIPLES[int(np.floor(t))%3][0]
            D+=((hi-lo)*w/2)*(a0/12)*flux
            masserr=max(masserr,err)
    return D,masserr

began=time.time();samples=[]
for x in [.001,.01,.05,.1,.3,.7,1.,1.2,2.5,3.,5.,10.]:
    D,m=averaged(x,24)
    samples.append({'x':x,'D':D.tolist(),'max_conservation_error':m})
    print(json.dumps(samples[-1]),flush=True)
refine=[]
for x in [.1,1.2,3.]:
    D,m=averaged(x,40);refine.append({'x':x,'D':D.tolist(),'max_conservation_error':m})
result={'method':'B: elementary-jump conservative 5-state row generator plus piecewise DOP853 ODE and absorption flux',
        'basis':BASIS,'generators':[G.tolist() for G in GENERATORS],
        'samples':samples,'phase_order':24,'phase_refinement':refine,'phase_refinement_order':40,
        'ode_rtol':2e-11,'ode_atol':2e-13,'elapsed_seconds':time.time()-began,
        'independence':'Same agent and prescribed rates/laws; independently constructed row generator, different basis and ODE algorithm. No A source or output read. This is not a fresh referee.'}
(OUT/'ode-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'elapsed_seconds':result['elapsed_seconds'],'output':'evidence/research/ode-result.json'}))
