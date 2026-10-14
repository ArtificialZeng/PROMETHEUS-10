#!/usr/bin/env python3
"""Independent N12 direct many-body ground trace and actual physical state swap.

This controlled numerical replay reads no scan, eigenvector proposal or certificate.
The physical half-filled ground vector comes from integer spin/JW hopping entries.
"""
from pathlib import Path
import json, itertools, math
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as sla
import scipy.linalg as la

OUT=Path(__file__).resolve().parent
N=12;l=6
basis=[m for m in range(1<<N) if m.bit_count()==N//2]
index={m:i for i,m in enumerate(basis)}
rows=[];cols=[]
for i,m in enumerate(basis):
    for j in range(N-1):
        if ((m>>j)&1)!=((m>>(j+1))&1):
            rows.append(index[m^(3<<j)]);cols.append(i)
H=sparse.csr_matrix((-np.ones(len(rows)),(rows,cols)),shape=(len(basis),)*2)
ev,v=sla.eigsh(H,k=2,which='SA',tol=2e-15,v0=np.ones(len(basis)))
order=np.argsort(ev);ev=ev[order];v=v[:,order];psi=v[:,0]
res=float(np.linalg.norm(H@psi-ev[0]*psi))
full=np.zeros(1<<N);full[basis]=psi
ab=full.reshape((1<<l,1<<l))
rho=ab.T@ab

def annihilation(j):
    a=np.zeros((1<<l,1<<l))
    for m in range(1<<l):
        if m&(1<<j):a[m^(1<<j),m]=(-1)**((m&((1<<j)-1)).bit_count())
    return a
c=[annihilation(j) for j in range(l)]
C=np.array([[np.trace(rho@(c[i].T@c[j])) for j in range(l)] for i in range(l)])
nu,V=la.eigh(C);nu=nu[::-1];V=V[:,::-1]
phi=np.sqrt(2/(l+1))*np.sin(np.arange(1,l+1)[:,None]*np.arange(1,l+1)[None,:]*np.pi/(l+1))
eps=-2*np.cos(np.arange(1,l+1)*np.pi/(l+1))
W=phi@V.T

def exterior(W):
    out=np.zeros((1<<l,1<<l))
    subsets=[[j for j in range(l) if m&(1<<j)] for m in range(1<<l)]
    for a,A in enumerate(subsets):
        for b,B in enumerate(subsets):
            if len(A)==len(B):
                out[a,b]=np.linalg.det(W[np.ix_(A,B)]) if A else 1.
    return out

GW=exterior(W);Gphi=exterior(phi)
aligned=GW@rho@GW.T
HA=-sum((c[j].T@c[j+1]+c[j+1].T@c[j] for j in range(l-1)),np.zeros((1<<l,)*2))
num=np.diag([m.bit_count() for m in range(1<<l)])
parity=np.diag([(-1)**m.bit_count() for m in range(1<<l)])
alpha=Gphi[:,6];beta=Gphi[:,9]
S=np.eye(1<<l)-np.outer(alpha,alpha)-np.outer(beta,beta)+np.outer(alpha,beta)+np.outer(beta,alpha)
swapped=S@aligned@S.T
EA=float(np.trace(rho@HA));Ealign=float(np.trace(aligned@HA));Eswap=float(np.trace(swapped@HA))
q=np.array([math.prod(nu[j] if m&(1<<j) else 1-nu[j] for j in range(l)) for m in range(1<<l)])
energy=np.array([sum(eps[j] for j in range(l) if m&(1<<j)) for m in range(1<<l)])
diag=Gphi.T@aligned@Gphi
ps=la.eigvalsh(rho)[::-1];Es=la.eigvalsh(HA)
Epass=float(ps@Es)
K=c[0].T@c[3].T@c[2]@c[1]
gate_modes=la.expm(-1j*np.pi/2*(K+K.T))
gate_site=Gphi@gate_modes@Gphi.T
gated=gate_site@aligned@gate_site.conj().T
gate_gain=float(np.real(np.trace((aligned-gated)@HA)))
marginal14=nu[0]*(1-nu[1])*(1-nu[2])*nu[3]
marginal23=(1-nu[0])*nu[1]*nu[2]*(1-nu[3])
formula_gate=float((eps[0]+eps[3]-eps[1]-eps[2])*(marginal14-marginal23))
checks={
    'ground_energy_error':abs(float(ev[0])-sum(-2*np.cos(k*np.pi/(N+1)) for k in range(1,N//2+1))),
    'ground_vector_residual':res,'rho_trace_error':abs(np.trace(rho)-1),
    'Gaussian_alignment_unitarity_error':float(np.linalg.norm(GW.T@GW-np.eye(1<<l))),
    'aligned_mode_density_difference':float(np.max(np.abs(diag-np.diag(q)))),
    'one_body_alignment_energy_difference':abs(Ealign-float(nu@eps)),
    'swap_unitarity_error':float(np.linalg.norm(S.T@S-np.eye(1<<l))),
    'swap_number_commutator':float(np.linalg.norm(S@num-num@S)),
    'swap_parity_commutator':float(np.linalg.norm(S@parity-parity@S)),
    'swap_work_formula_error':abs((Ealign-Eswap)-(energy[9]-energy[6])*(q[9]-q[6])),
    'quartic_gate_work_formula_error':abs(gate_gain-formula_gate),
    'quartic_gate_number_commutator':float(np.linalg.norm(gate_site@num-num@gate_site)),
    'quartic_gate_unitarity_error':float(np.linalg.norm(gate_site.conj().T@gate_site-np.eye(1<<l)))}
assert all(x<2e-11 for x in checks.values())
assert Ealign-Eswap>6.7e-7 and gate_gain>6.7e-7 and Ealign-Epass>1.35e-6
# Gap to the next half-filled state is 4 sin[pi/(2(N+1))] > 4/(N+1).
# A conservative 8*r/(4/(N+1)) expectation/density bound is recorded; the
# certified rational computation, rather than this floating replay, is decisive.
record={'N':N,'l':l,'basis':'ordered-site Fock mask, low l bits A; half-filled integer Hamiltonian sector',
        'method':'direct sparse integer many-body ground state, ordinary tensor partial trace, exterior-power orbital alignment and explicit rank-state swap',
        'independence':'reads no scan/proposal/certificate data; different direct state representation, same worker',
        'ground_energy':float(ev[0]),'half_filled_next_gap':float(ev[1]-ev[0]),
        'conservative_density_replay_error_estimate':8*res/(4/(N+1)),
        'checks':checks,'rho_A':rho.tolist(),'C_A':C.tolist(),'nu_desc':nu.tolist(),
        'physical_one_body_mode_matrix':phi.tolist(),'orbitals_alignment_W':W.tolist(),
        'physical_state_alpha_site_Fock':alpha.tolist(),'physical_state_beta_site_Fock':beta.tolist(),
        'direct_density_spectrum_desc':ps.tolist(),'physical_many_body_spectrum':Es.tolist(),
        'E_initial':EA,'E_align':Ealign,'E_after_swap':Eswap,'E_passive':Epass,
        'swap_gain':Ealign-Eswap,'full_gain':Ealign-Epass,
        'quartic_gate_gain':gate_gain,'quartic_gate_formula':formula_gate,
        'quartic_generator':'d1^dagger d4^dagger d3 d2 + h.c.; U=exp[-i(pi/2)K]',
        'limitations':'controlled floating replay, not interval certificate or fresh referee; negligible density eigenvalues may be slightly negative due to roundoff and are preserved without clipping'}
(OUT/'fock-replay.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k in ('checks','E_initial','E_align','E_after_swap','E_passive','swap_gain','full_gain','quartic_gate_gain','quartic_gate_formula','conservative_density_replay_error_estimate')},indent=2))
print('Direct actual-marginal Fock replay passed at stated 2e-11 tolerance; exact checker remains decisive.')
