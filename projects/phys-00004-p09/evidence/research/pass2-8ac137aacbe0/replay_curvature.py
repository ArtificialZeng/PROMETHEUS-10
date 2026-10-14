#!/usr/bin/env python3
"""Separate 70-digit tensor/partial-trace replay of the Gram formula.

No imports of the discovery or symbolic-check programs. This is same-worker
method separation, not a fresh referee. Finite differences are diagnostics.
"""
from pathlib import Path
import datetime as dt
import argparse
import itertools
import json
import random
import time
import mpmath as mp

HERE=Path(__file__).resolve().parent
mp.mp.dps=70
def kron(A,B):
    return mp.matrix([[A[i,j]*B[k,l] for j in range(A.cols) for l in range(B.cols)]
                      for i in range(A.rows) for k in range(B.rows)])
def trace(A):return sum(A[k,k] for k in range(A.rows))
def norm(A):return mp.sqrt(sum(abs(v)**2 for v in A))
def sqentropy(w):return -sum(x*mp.log(x,2) for x in w if x>0)

def prediction(p,H):
    M=mp.matrix([[mp.sqrt(p[i,j]) for j in range(2)] for i in range(2)])
    x,y,z,w=M[0,0],M[0,1],M[1,0],M[1,1]
    J=x*y*z*w;u=x*y+z*w;v=x*z+y*w;du=x*y-z*w;dv=x*z-y*w
    delta=mp.sqrt(1-4*(x*w-y*z)**2);a=(1+delta)/2;b=(1-delta)/2
    kappa=mp.log(a/b)/delta
    chars=[[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
    alpha=mp.matrix([[sum(H[i*4+j,i*4+j].real*chars[r][i]*chars[s][j]/4
                          for i in range(4) for j in range(4)) for s in range(3)] for r in range(3)])
    D=mp.mpf(0)
    for i,j in itertools.product(range(2),repeat=2):
        za=1-2*i;zb=1-2*j
        r1=alpha[0,0]+alpha[0,2]*zb+alpha[2,0]*za+alpha[2,2]*za*zb
        r2=alpha[1,1]+alpha[1,2]*zb+alpha[2,1]*za+alpha[2,2]*za*zb
        D+=J*p[i,j]*(r1*r1+r2*r2)
    plus=u*v*(alpha[0,1]+alpha[1,0])+u*dv*(alpha[0,2]+alpha[1,2])+v*du*(alpha[2,0]+alpha[2,1])+2*du*dv*alpha[2,2]
    D+=plus*plus/2
    Q=kron(M,M);F=mp.matrix([[Q[i,j]*H[i*4+j,i*4+j].real for j in range(4)] for i in range(4)])
    R=F*Q.T-Q*F.T
    g=M*M.T;theta=mp.atan2(2*g[0,1],g[0,0]-g[1,1])/2
    O=mp.matrix([[mp.cos(theta),-mp.sin(theta)],[mp.sin(theta),mp.cos(theta)]])
    OO=kron(O,O);zeta=(OO.T*R*OO)[1,2]
    out=(kappa*D+(kappa/2-1)*zeta*zeta/(a*b))/mp.log(2)
    # Independently enter the logarithm using the two-eigenvalue projector.
    for transpose in [False,True]:
        G=M*M.T if transpose else M.T*M
        logG=mp.eye(2)*mp.log(b)+(G-mp.eye(2)*b)*kappa
        fp=-(kron(logG,mp.eye(2))+kron(mp.eye(2),logG)+mp.eye(4))/mp.log(2)
        q=Q.T if transpose else Q
        for i,r in itertools.combinations(range(4),2):
            Z=[H[j*4+r,j*4+i] if transpose else H[r*4+j,i*4+j] for j in range(4)]
            for j,k in itertools.combinations(range(4),2):
                out+=-fp[j,k]*(q[i,j]*q[i,k]+q[r,j]*q[r,k])*abs(Z[j]-Z[k])**2
    return out,2*sqentropy([a,b])

def direct(p,H,t):
    U=mp.expm(mp.j*t*H)
    # Tensor indices A,B,R,S; complete partial traces entered by explicit sums.
    Q=[[mp.sqrt(p[i//2,j//2]*p[i%2,j%2]) for j in range(4)] for i in range(4)]
    psi={}
    for i,j,r,s in itertools.product(range(4),repeat=4):psi[i,j,r,s]=Q[i][j]*U[r*4+s,i*4+j]
    AR=mp.matrix(16);AB=mp.matrix(16)
    for i,r,k,u in itertools.product(range(4),repeat=4):
        AR[i*4+r,k*4+u]=sum(psi[i,j,r,s]*mp.conj(psi[k,j,u,s]) for j,s in itertools.product(range(4),repeat=2))
    for i,j,k,l in itertools.product(range(4),repeat=4):
        AB[i*4+j,k*4+l]=sum(psi[i,j,r,s]*mp.conj(psi[k,l,r,s]) for r,s in itertools.product(range(4),repeat=2))
    vals=mp.eighe(AR,eigvals_only=True)
    physical=mp.diag([Q[i][j]**2 for i,j in itertools.product(range(4),repeat=2)])
    return sqentropy(vals),norm(AB-physical),norm(U.H*U-mp.eye(16)),sum(max(mp.mpf(0),vals[k]) for k in range(12))

def generator(rng,kind):
    H=mp.matrix(16)
    for k in range(16):H[k,k]=mp.mpf(rng.randint(-6,6))/32
    if kind=='phase':return H
    for i,r in itertools.combinations(range(4),2):
        for j in range(4):
            value=(mp.mpf(rng.randint(-6,6))+mp.j*rng.randint(-6,6))/32
            H[r*4+j,i*4+j]=value;H[i*4+j,r*4+j]=mp.conj(value)
    for j,s in itertools.combinations(range(4),2):
        for i in range(4):
            value=(mp.mpf(rng.randint(-6,6))+mp.j*rng.randint(-6,6))/32
            H[i*4+s,i*4+j]=value;H[i*4+j,i*4+s]=mp.conj(value)
    return H

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--refine-near-product',action='store_true')
    args=parser.parse_args()
    if args.refine_near_product:
        records=[]
        for line in (HERE/'replay-records.jsonl').read_text().splitlines():
            old=json.loads(line)
            if old['name']!='near-product':continue
            values=old['P'];p=mp.matrix([[mp.mpf(values[0]),mp.mpf(values[1])],[mp.mpf(values[2]),mp.mpf(values[3])]])
            H=mp.matrix([[mp.mpf(old['H_real'][i][j])+mp.j*mp.mpf(old['H_imag'][i][j]) for j in range(16)] for i in range(16)])
            c,ref=prediction(p,H);probes=[]
            for st in ['.000001','.0000001','.00000001']:
                t=mp.mpf(st);ep,marp,unp,tailp=direct(p,H,t);em,marm,unm,tailm=direct(p,H,-t)
                ratio=((ep+em)/2-ref)/(t*t)
                probes.append({'t':st,'central_gap_over_t2':str(ratio),'formula_c':str(c),
                               'absolute_discrepancy':str(abs(ratio-c)),
                               'physical_residual_max':str(max(marp,marm)),
                               'unitarity_residual_max':str(max(unp,unm)),
                               'tail_weight_max':str(max(tailp,tailm))})
            records.append({'name':old['name'],'kind':old['kind'],'input_record':'replay-records.jsonl','probes':probes})
        summary={'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),'precision_decimal_digits':70,
                 'completed':True,'reason':'The near-product table had a nonuniform small-step regime; refine the same saved directions without changing inputs or overwriting the original replay.',
                 'records':records,'limitations':'Same-worker finite-difference diagnostic, not an interval or fresh referee certificate.'}
        (HERE/'replay-near-product-refinement.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary),flush=True);return
    start=time.monotonic();rng=random.Random(271405)
    inputs=[('generic',['.4','.1','.2','.3']),('symmetric',['.4','.1','.1','.4']),
            ('biased',['.7','.1','.05','.15']),('near-product',['.251','.249','.249','.251'])]
    records=[]
    for name,values in inputs:
        p=mp.matrix([[mp.mpf(values[0]),mp.mpf(values[1])],[mp.mpf(values[2]),mp.mpf(values[3])]])
        for kind in ['phase','mixed']:
            H=generator(rng,kind);c,ref=prediction(p,H);probes=[]
            for st in ['.001','.0001','.00001']:
                if time.monotonic()-start>150:raise RuntimeError('explicit replay ceiling reached; no pass inferred')
                t=mp.mpf(st);ep,mp1,up,tailp=direct(p,H,t);em,mm1,um,tailm=direct(p,H,-t)
                ratio=((ep+em)/2-ref)/(t*t)
                probes.append({'t':st,'central_gap_over_t2':str(ratio),'formula_c':str(c),
                               'absolute_discrepancy':str(abs(ratio-c)),
                               'physical_residual_max':str(max(mp1,mm1)),
                               'unitarity_residual_max':str(max(up,um)),
                               'tail_weight_max':str(max(tailp,tailm))})
            rec={'name':name,'P':values,'kind':kind,'H_real':[[str(H[i,j].real) for j in range(16)] for i in range(16)],
                 'H_imag':[[str(H[i,j].imag) for j in range(16)] for i in range(16)],'probes':probes}
            records.append(rec);print(json.dumps({'name':name,'kind':kind,'last_probe':probes[-1]}),flush=True)
            (HERE/'replay-records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
    summary={'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),'precision_decimal_digits':70,
             'completed':True,'tables':len(inputs),'directions':len(records),'signed_entropy_evaluations':len(records)*6,
             'max_last_step_discrepancy':str(max(mp.mpf(r['probes'][-1]['absolute_discrepancy']) for r in records)),
             'maximum_marginal_residual':str(max(mp.mpf(q['physical_residual_max']) for r in records for q in r['probes'])),
             'maximum_unitarity_residual':str(max(mp.mpf(q['unitarity_residual_max']) for r in records for q in r['probes'])),
             'wall_seconds':time.monotonic()-start,
             'independence':'Separate code and full tensor/partial-trace eigensolver; shared model, same proposer. No fresh referee independence.',
             'error_control':'70-digit arithmetic and three central step sizes check the formula; not interval entropy certification. Exact proof rests on the analytic derivation and complete polynomial identity, not these finite differences.'}
    (HERE/'replay-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
