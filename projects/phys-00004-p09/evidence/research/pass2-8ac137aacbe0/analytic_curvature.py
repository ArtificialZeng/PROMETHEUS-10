#!/usr/bin/env python3
"""Derived quadratic coefficients and direct tensor checks; no prior-code imports.

These are floating diagnostic evaluations of an analytic formula. They are not
interval certificates, global optimization, or an independent referee review.
"""
from pathlib import Path
import datetime as dt
import itertools
import json
import numpy as np
from scipy.linalg import expm, helmert

HERE=Path(__file__).resolve().parent
SQRT2=np.sqrt(2.0)
CONTRAST=helmert(4,full=False).T
PAIRS=list(itertools.combinations(range(4),2))

def logs(a):
    w,v=np.linalg.eigh(a)
    if np.min(w)<=0: raise ValueError('strict positive Gram required')
    loga=(v*np.log(w))@v.T
    fp=-(loga+np.eye(4))/np.log(2)
    div=np.zeros((4,4))
    for i in range(4):
        for j in range(4):
            x,y=w[i],w[j]
            if abs(x-y)<1e-10*max(x,y):
                div[i,j]=-1/((x+y)*.5*np.log(2))
            else:
                div[i,j]=-np.log(x/y)/((x-y)*np.log(2))
    return w,v,fp,div

class Curvature:
    def __init__(self,p):
        self.p=np.asarray(p,dtype=float)
        self.Q=np.kron(np.sqrt(self.p),np.sqrt(self.p))
        self.GL=self.Q@self.Q.T
        self.GR=self.Q.T@self.Q
        self.w,self.v,self.fp,self.div=logs(self.GL)
        self.wr,self.vr,self.fpr,_=logs(self.GR)
        self.W=self.Q*(self.Q@self.fpr)

    def phase(self,d):
        q=self.Q; F=q*d; E=-.5*q*d*d
        T=1j*(F@q.T-q@F.T)
        Z=self.v.T@T@self.v
        a=np.trace(self.fp@(E@q.T+q@E.T+F@F.T)).real
        b=.5*np.sum(self.div*abs(Z)**2)
        return float(a+b)

    def rotation_blocks(self):
        out=[]
        for trans in [False,True]:
            q=self.Q.T if trans else self.Q
            fp=self.fp if trans else self.fpr
            W=q*(q@fp)
            for i,u in PAIRS:
                L=(q[i,:,None]*fp*q[i,None,:]
                   +q[u,:,None]*fp*q[u,None,:]
                   -np.diag(W[i]+W[u]))
                out.append((trans,i,u,L))
        return out

    def full_coefficient(self,H):
        q=self.Q
        d=np.diag(H).real.reshape(4,4)
        F=q*d; D=1j*F
        hsq=np.sum(abs(H)**2,axis=1).reshape(4,4)
        E=-.5*q*hsq
        B=np.zeros((4,12),complex);C=np.zeros((12,4),complex)
        c=0
        for j in range(4):
            for s in range(4):
                if s==j:continue
                for i in range(4): B[i,c]=1j*q[i,j]*H[i*4+s,i*4+j]
                c+=1
        c=0
        for i in range(4):
            for r in range(4):
                if r==i:continue
                for j in range(4): C[c,j]=1j*q[i,j]*H[r*4+j,i*4+j]
                c+=1
        T=D@q.T+q@D.conj().T
        Z=self.v.T@T@self.v
        term1=np.trace(self.fp@(E@q.T+q@E.T+D@D.conj().T+B@B.conj().T)).real
        term2=np.trace(self.fpr@(C.conj().T@C)).real
        term3=.5*np.sum(self.div*abs(Z)**2)
        return float(term1+term2+term3)

    def separated_coefficient(self,H):
        out=self.phase(np.diag(H).real.reshape(4,4))
        for trans,i,u,L in self.rotation_blocks():
            z=np.asarray([H[j*4+u,j*4+i] if trans else H[u*4+j,i*4+j] for j in range(4)])
            out+=(z.conj()@L@z).real
        return float(out)

    def phase_matrix(self):
        b=[]
        for a in range(3):
            for c in range(3): b.append(np.outer(CONTRAST[:,a],CONTRAST[:,c]))
        vals=np.asarray([self.phase(d) for d in b])
        out=np.diag(vals)
        for a in range(9):
            for c in range(a):
                out[a,c]=out[c,a]=.5*(self.phase(b[a]+b[c])-vals[a]-vals[c])
        return out,b

def entropy(p,H,t):
    Q=np.kron(np.sqrt(p),np.sqrt(p));U=expm(1j*t*H)
    K=np.zeros((16,16),complex)
    for i,j,r,s in itertools.product(range(4),repeat=4):
        K[i*4+r,j*4+s]=Q[i,j]*U[r*4+s,i*4+j]
    w=np.linalg.svd(K,compute_uv=False)**2
    pos=w[w>0];value=-np.sum(pos*np.log2(pos))
    # Independent complete physical density from auxiliary column overlaps.
    phys=(Q.reshape(16,1)*Q.reshape(1,16))*(U.conj().T@U).T
    marginal=np.linalg.norm(phys-np.diag(Q.ravel()**2))
    return float(value),w,float(marginal),float(np.linalg.norm(U.conj().T@U-np.eye(16)))

def random_H(rng):
    H=np.diag(rng.normal(size=16)).astype(complex)
    for i,u in PAIRS:
        for j in range(4):
            z=(rng.normal()+1j*rng.normal())/SQRT2
            H[u*4+j,i*4+j]=z;H[i*4+j,u*4+j]=z.conjugate()
    for j,s in PAIRS:
        for i in range(4):
            z=(rng.normal()+1j*rng.normal())/SQRT2
            H[i*4+s,i*4+j]=z;H[i*4+j,i*4+s]=z.conjugate()
    return H/np.linalg.norm(H)

def main():
    rng=np.random.default_rng(832011)
    tables=[('rational-generic',np.asarray([[.4,.1],[.2,.3]])),
            ('symmetric',np.asarray([[.4,.1],[.1,.4]])),
            ('biased',np.asarray([[.7,.1],[.05,.15]]))]
    for k in range(64):
        p=rng.dirichlet(np.ones(4)*(.3 if k<32 else 2)).reshape(2,2)
        if min(p.ravel())<1e-7 or abs(np.linalg.det(np.sqrt(p)))<1e-3: continue
        tables.append((f'heldout-{k}',p))
    records=[]
    for idx,(name,p) in enumerate(tables):
        c=Curvature(p);A,b=c.phase_matrix();w,v=np.linalg.eigh(A)
        blocks=c.rotation_blocks()
        mins=[float(np.linalg.eigvalsh(CONTRAST.T@L@CONTRAST)[0]) for _,_,_,L in blocks]
        null_d=sum(v[a,0]*b[a] for a in range(9))
        np.savez(HERE/f'analytic-{idx:03d}.npz',P=p,phase_coefficient_matrix=A,
                 phase_eigenvalues=w,phase_min_direction=null_d,
                 rotation_blocks=np.asarray([x[3] for x in blocks]))
        rec={'name':name,'P':p.tolist(),'file':f'analytic-{idx:03d}.npz',
             'phase_min_eigenvalue':float(w[0]),'phase_second_eigenvalue':float(w[1]),
             'phase_nearzero_count_abs_below_1e-9':int(np.sum(abs(w)<1e-9)),
             'rotation_reduced_min_eigenvalue':min(mins),
             'rotation_gauge_residual_max':max(float(np.linalg.norm(L@np.ones(4))) for _,_,_,L in blocks)}
        if idx<3:
            tests=[]
            for k in range(4):
                H=random_H(rng);a=c.full_coefficient(H);s=c.separated_coefficient(H)
                ent0=entropy(p,H,0)[0];probes=[]
                for t in [0.003,0.001,0.0003]:
                    ent,sw,mar,uni=entropy(p,H,t)
                    probes.append({'t':t,'gap_over_t2':(ent-ent0)/(t*t),'predicted_c':a,
                                   'tail_weight':float(np.sum(sw[4:])),
                                   'marginal_residual':mar,'unitary_residual':uni})
                tests.append({'full':a,'separated':s,'difference':abs(a-s),'probes':probes})
            rec['direct_checks']=tests
            print(json.dumps(rec),flush=True)
        records.append(rec)
    (HERE/'analytic-records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
    summary={'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),
             'tables':len(records),'strict_domain':'All sampled tables strictly positive, det(sqrt(P)) nonzero.',
             'phase_min_eigenvalue':min(r['phase_min_eigenvalue'] for r in records),
             'phase_second_min_eigenvalue':min(r['phase_second_eigenvalue'] for r in records),
             'rotation_reduced_min_eigenvalue':min(r['rotation_reduced_min_eigenvalue'] for r in records),
             'phase_kernel_counts':sorted(set(r['phase_nearzero_count_abs_below_1e-9'] for r in records)),
             'limitation':'Formula evaluations in binary64. Sign near zero is not certified. No global or arbitrary-auxiliary result.'}
    (HERE/'analytic-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
