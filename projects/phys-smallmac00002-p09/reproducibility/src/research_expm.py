"""A: symmetric eigendecomposition of piecewise killed propagators.

Event phase quadrature is split at both start and end protocol switches.
No channel is renormalized. Deterministic Gaussian convergence is diagnostic;
the exact sign and infinite-domain existence have a separate proof.
"""
import json, sys, time
from pathlib import Path
import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.linalg import expm

OUT=Path('evidence/research')
RATES=np.array([[10.,1.,1.],[1.,10.,1.],[1.,1.,10.]])
S=np.array([[[-a-c,0,c],[0,-a-b,b],[c,b,-b-c]] for a,b,c in RATES])
EIG=[np.linalg.eigh(z) for z in S]
FULL=[expm(z) for z in S]
MID={}
for st in range(3):
    p=np.eye(3)
    MID[st,0]=p.copy()
    for num in range(1,85):
        p=FULL[(st+num-1)%3]@p
        MID[st,num]=p.copy()

def mat_batch(seg, durations):
    val,vec=EIG[seg%3]
    return np.einsum('ij,nj,kj->nik',vec,np.exp(np.asarray(durations)[:,None]*val),vec)

def phase_breaks(x):
    pts=[0.,1.,2.,3.]+[float((i-x)%3) for i in range(3)]
    return sorted(set(round(p,13) for p in pts))

def density(x, order=24):
    nodes,weights=leggauss(order)
    answer=np.zeros((2,2))
    breaks=phase_breaks(x)
    for left,right in zip(breaks[:-1],breaks[1:]):
        if right-left<1e-13: continue
        t=(right+left)/2+(right-left)/2*nodes
        si=int(np.floor((left+right)/2))
        sj=int(np.floor((left+right)/2+x))
        if si==sj:
            U=np.broadcast_to(expm(S[si%3]*x),(order,3,3))
        else:
            first=mat_batch(si,si+1-t)
            last=mat_batch(sj,t+x-sj)
            U=last@MID[(si+1)%3,sj-si-1]@first
        # Initial +,- arrive in states 2,1. Final +,- depart 1,2.
        D=U[:,[0,1],:][:,:,[1,0]].transpose(0,2,1)
        # p=1/3 and integral_0^3 k12=12, so conditional phase weight=a/12.
        weight=RATES[si%3,0]*RATES[sj%3,0]/12
        answer += weight*(right-left)/2*np.einsum('n,nij->ij',weights,D)
    return answer

def integrate(delay_order, phase_order, H):
    nodes,weights=leggauss(delay_order)
    norms=np.zeros((2,2)); entropy=0.
    for k in range(H):
        for z,w in zip(nodes,weights):
            x=k+(z+1)/2
            D=density(x,phase_order)
            if np.min(D)<=0: raise ArithmeticError((x,D))
            a,b=D[0,0],D[1,1]
            entropy += w/2*(4/3)*(a-b)*np.log(a/b)
            norms += w/2*D
    return {'delay_gauss_order':delay_order,'phase_gauss_order':phase_order,
            'H':H,'entropy_times_t_star':entropy,'joint_channel_integrals':norms.tolist(),
            'row_sums':norms.sum(axis=1).tolist()}

if __name__=='__main__':
    began=time.time()
    samples=[{'x':x,'D':density(x,32).tolist()} for x in [.001,.01,.05,.1,.3,.7,1.,1.2,2.5,3.,5.,10.]]
    rows=[]
    for d,p,H in [(12,12,40),(20,20,80),(32,32,80),(48,48,80),(64,64,80)]:
        row=integrate(d,p,H); rows.append(row)
        print(json.dumps(row),flush=True)
    result={'method':'A: three-state chronological matrix exponentials using symmetric eigendecomposition; split Gaussian phase/delay quadrature',
            'rates':RATES.tolist(),'samples':samples,'convergence':rows,'elapsed_seconds':time.time()-began,
            'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
            'error_scope':'Convergence and roundoff diagnostic, not certified quadrature. The scientific sign follows from exact-result.json and proof.md without relying on these integrals.'}
    (OUT/'expm-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'elapsed_seconds':result['elapsed_seconds'],'output':'evidence/research/expm-result.json'}))
