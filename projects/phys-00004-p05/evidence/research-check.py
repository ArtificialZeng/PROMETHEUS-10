"""Supplementary adversarial replay. No finite scan establishes the theorem."""
import json, hashlib, platform
from pathlib import Path
import numpy as np
import sympy as sy
import reconstruct_a as a
import reconstruct_b as b

ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(20261012051)
K=np.array([np.kron(s,a.I) for s in a.S])
def entropy(r):
    w=np.linalg.eigvalsh(r)
    assert w.min()>-2e-12
    w=w[w>0]
    return float(-np.dot(w,np.log2(w)))
def pin(r, ref=None):
    w,v=np.linalg.eigh(a.marginal(r if ref is None else ref))
    out=np.zeros((4,4),complex)
    for j in range(2):
        q=np.kron(np.outer(v[:,j],v[:,j].conj()),a.I)
        out+=q@r@q
    return out,float(w[1]-w[0])
def rel(r,s):
    w,v=np.linalg.eigh(s)
    assert w.min()>0
    logs=(v*np.log2(w))@v.conj().T
    return -entropy(r)-float(np.trace(r@logs).real)
def channel(r,p):
    return sum(p[j]*K[j]@r@K[j].conj().T for j in range(4))
def encode(r):
    return np.stack([r.real,r.imag],axis=-1).tolist()

# Independent exact check: all output blocks commute with marginal b I+(a-b) A.
aa,bb,u,v,x,y=sy.symbols('a b u v x y',real=True)
A=sy.Matrix([[u,x-sy.I*y],[x+sy.I*y,v]])
R=bb*sy.eye(2)+(aa-bb)*A
assert (A*R-R*A).applyfunc(sy.simplify)==sy.zeros(2)
assert ((sy.eye(2)-A)*R-R*(sy.eye(2)-A)).applyfunc(sy.simplify)==sy.zeros(2)
print('Exact arbitrary-entry image-block/marginal commutators: zero')

records=[]; worst=None; raw_rho=[]; raw_p=[]
for i in range(6000):
    g=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    rho=g@g.conj().T; rho/=np.trace(rho)
    regime='generic_complex'
    if i>=3000:
        # Whiten A marginal, retain complex correlations, then add a controlled gap.
        w,vv=np.linalg.eigh(a.marginal(rho))
        f=(vv*(1/np.sqrt(2*w)))@vv.conj().T
        f=np.kron(f,a.I); rho=f@rho@f
        rho=.8*rho+.2*np.eye(4)/4
        n=rng.normal(size=3); n/=np.linalg.norm(n)
        eps=10.**(-rng.uniform(2,7))
        rho+=eps*np.kron(sum(n[j]*a.S[j+1] for j in range(3)),a.I)/4
        regime='small_nonzero_gap'
    p=rng.dirichlet(np.full(4,[1.,.15,3.][i%3]))
    if i%25==0: p=np.array([.5,.5,0,0]) # rank-deficient transfer, admissible output checked
    out=channel(rho,p)
    tau,gi=pin(rho); pout,go=pin(out)
    assert gi>1e-10 and go>1e-12
    sigma=channel(tau,p); fixed,_=pin(sigma,out)
    din=entropy(tau)-entropy(rho); dout=entropy(pout)-entropy(out)
    dt=rel(out,sigma); corr=rel(pout,sigma)
    transfer=np.diag([1,p[0]-p[1]-p[2]+p[3],p[0]+p[1]-p[2]-p[3],p[0]-p[1]+p[2]-p[3]])
    out_b=b.channel(rho,transfer)
    pb,_=pin(out_b)
    row=dict(index=i,regime=regime,gap_in=gi,gap_out=go,gain=dout-din,
        compatibility_residual=float(np.linalg.norm(sigma-fixed)),
        pythagorean_residual=abs(dt-dout-corr),dpi_loss=din-dt,correction=corr,
        matrix_ab_difference=float(np.linalg.norm(out-out_b)),
        discord_ab_difference=abs(dout-(entropy(pb)-entropy(out_b))),
        noncommutation=float(np.linalg.norm(pout-sigma)),min_state_eigenvalue=float(np.linalg.eigvalsh(rho).min()))
    records.append(row)
    raw_rho.append(rho); raw_p.append(p)
    if worst is None or row['gain']>worst['record']['gain']:
        worst=dict(record=row,rho=encode(rho),p=p.tolist())
summary=dict(seed=20261012051,cases=len(records),near_gap_cases=3000,
    max_gain=max(r['gain'] for r in records),min_gap_in=min(r['gap_in'] for r in records),
    min_gap_out=min(r['gap_out'] for r in records),min_dpi_loss=min(r['dpi_loss'] for r in records),
    min_correction=min(r['correction'] for r in records),
    max_compatibility_residual=max(r['compatibility_residual'] for r in records),
    max_pythagorean_residual=max(r['pythagorean_residual'] for r in records),
    max_matrix_ab_difference=max(r['matrix_ab_difference'] for r in records),
    max_discord_ab_difference=max(r['discord_ab_difference'] for r in records),
    max_noncommutation=max(r['noncommutation'] for r in records),
    python=platform.python_version(),numpy=np.__version__,
    limitations='Binary64 supplementary falsification. Near-gap basis reconstruction is conditioned by 1/gap. No interval certificate or proof from this finite scan.',
    source_sha256=hashlib.sha256(Path('source.md').read_bytes()).hexdigest())
(ROOT/'research-scan.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
(ROOT/'research-closest-case.json').write_text(json.dumps(worst,indent=2)+'\n')
np.savez_compressed(ROOT/'research-inputs.npz',rho=np.array(raw_rho),p=np.array(raw_p))
print(json.dumps(summary,indent=2))
assert summary['max_gain']<2e-8
assert summary['max_pythagorean_residual']<2e-8
assert summary['min_dpi_loss']>-2e-8 and summary['min_correction']>-2e-8
assert summary['max_matrix_ab_difference']<2e-12
print('Supplementary adversarial checks: PASS (no referee acceptance)')
