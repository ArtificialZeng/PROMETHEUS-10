"""Independent computational-basis/radial-angular integration of the PVM risk.
Does not read star-moment input coefficients or exact-certificate script.
The only shared inputs are the frozen physical model and proposed measurement.
"""
from pathlib import Path
import json,sys,time
import numpy as np
import scipy.linalg as la
from numpy.polynomial.legendre import leggauss
import mpmath as mp

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
a=np.pi/4
pauli=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
bell=np.array([1,0,0,1],complex)/np.sqrt(2)
signs=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)
vectors=np.array([np.kron((np.eye(2)-1j*np.einsum('i,iab->ab',v,pauli))/2,np.eye(2))@bell for v in signs])
M=np.einsum('ja,jb->jab',vectors,vectors.conj())
assert np.max(np.abs(vectors.conj()@vectors.T-np.eye(4)))<1e-14
assert np.max(np.abs(M.sum(axis=0)-np.eye(4)))<1e-14
mp.mp.dps=80
am=mp.pi/4
# Obtain q again by a defining radial quadrature, not the reproduced primitive.
qm=mp.quad(lambda r:r**3*mp.sin(r)*mp.cos(r),[0,am])/am**3
records=[]
start=time.monotonic()
for noise in [0,0.5,0.1,0.9,1]:
    Q=float((1-mp.mpf(str(noise)))*qm)
    estimates=2*Q*signs
    exact_target=float(mp.pi**2/80-4*((1-mp.mpf(str(noise)))*qm)**2)
    for nr,nmu,nphi in [(16,6,12),(32,10,20),(64,14,28)]:
        xx,ww=leggauss(nr);rr=(xx+1)*a/2;wr=ww*a/2*3*rr**2/a**3
        mu,wmu=leggauss(nmu);phi=np.arange(nphi)*2*np.pi/nphi
        dirs=np.array([[np.sqrt(1-u*u)*np.cos(p),np.sqrt(1-u*u)*np.sin(p),u] for u in mu for p in phi])
        wa=np.repeat(wmu/(2*nphi),nphi)
        theta=(rr[:,None,None]*dirs[None,:,:]).reshape(-1,3)
        radii=np.repeat(rr,len(dirs));weights=(wr[:,None]*wa[None,:]).ravel()
        ns=np.tile(dirs,(nr,1))
        # Direct computational U, rather than any integrated spin moment.
        u=np.cos(radii)[:,None,None]*np.eye(2)-1j*np.sin(radii)[:,None,None]*np.einsum('ti,iab->tab',ns,pauli)
        vv=np.einsum('tab,bk->tak',u,bell.reshape(2,2)).reshape(-1,4)
        probs=(1-noise)*np.abs(vv@vectors.conj().T)**2+noise/4
        outcome=weights@probs
        first=np.einsum('t,tj,ti->ji',weights,probs,theta)
        posterior=first/outcome[:,None]
        cost=np.sum((theta[:,None,:]-estimates[None,:,:])**2,axis=2)/3
        risk=float(np.einsum('t,tj,tj->',weights,probs,cost))
        rec={'lambda':noise,'quadrature':[nr,nmu,nphi],'grid_points':len(weights),'probability_normalization_max_residual':float(np.max(np.abs(probs.sum(axis=1)-1))),
             'prior_normalization_residual':abs(float(weights.sum())-1),'outcome_probabilities':outcome.tolist(),'posterior_means':posterior.tolist(),'estimator_max_error':float(np.max(np.abs(posterior-estimates))),
             'risk_direct_computational':risk,'exact_formula_80digit_radial_quadrature_float':exact_target,'absolute_formula_residual':abs(risk-exact_target)}
        assert rec['probability_normalization_max_residual']<2e-14
        assert rec['estimator_max_error']<2e-13
        assert rec['absolute_formula_residual']<2e-13
        records.append(rec);print(json.dumps(rec),flush=True)

# Check the independent, previously integrated computational input A without
# using it to determine the new radial coefficient or direct risks.
inp=json.loads((ROOT/'evidence/reproduce/input-a.json').read_text())
def decode(m):return np.array(m['real'])+1j*np.array(m['imag'])
ga=[decode(m) for m in inp['runs'][-1]['Gamma']]
input_residuals={}
for j in range(4):
    input_residuals[f'outcome_{j}_probability']=abs(np.trace(ga[0]@M[j]).real-0.25)
    input_residuals[f'outcome_{j}_first_moment']=float(np.max(np.abs(np.array([np.trace(g@M[j]).real for g in ga[1:]])-float(qm)*signs[j]/2)))
assert max(input_residuals.values())<2e-14
mpvalues=[{'lambda':v,'q':'%s'%qm,'Q':'%s'%((1-mp.mpf(str(v)))*qm),'posterior_radius':'%s'%(2*mp.sqrt(3)*(1-mp.mpf(str(v)))*qm),'risk':'%s'%(mp.pi**2/80-4*((1-mp.mpf(str(v)))*qm)**2)} for v in [0,0.5,1]]
rec={'job_id':'phys-00014-p01-research-f15bfc274f9b','method':'Independent computational Pauli/Bell construction and full three-dimensional volume-prior integration. q independently recomputed by 80-digit radial quadrature; no star-coefficient cache used.',
     'independence':'Same proposer worker; distinct raw-channel computation rather than exact star proof. Not a fresh referee.',
     'basis_vectors_computational':{'real':vectors.real.tolist(),'imag':vectors.imag.tolist()},'integrations':records,'comparison_to_reproduced_computational_input':input_residuals,'high_precision_values':mpvalues,'elapsed_seconds':time.monotonic()-start,
     'error_control':'Three quadrature resolutions with largest probability/risk/posterior residuals recorded. Directional dependence has finite degree <=4; radial functions smooth. Double-precision integration and 80-digit values are corroboration only: the all-noise exact claim is justified by the separate symbolic algebra and written factorizations, not these samples.',
     'max_direct_risk_residual':max(r['absolute_formula_residual'] for r in records)}
(OUT/'physical-measurement-replay.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps({k:v for k,v in rec.items() if k not in ['integrations','basis_vectors_computational']},indent=2))
