"""Adversarial structural checks; analytic proof remains uniform-bound-proof.md."""
import json, itertools
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.special import expit
from scipy.optimize import linprog

OUT=Path(__file__).parent
rng=np.random.default_rng(327654)
perms=list(itertools.permutations(range(3)))
Ps=[np.eye(3)[list(p)] for p in perms]
columns=np.stack([p.ravel() for p in Ps],axis=1)
V=np.diag([1.,0.,0.]);eye=np.eye(3)
def moments(U,f):
    F=np.diag(f);Q=U.conj().T@V@U
    A=V-Q;B=V+Q-2*Q@V
    j=np.trace(F@A).real
    v=np.trace(F@B-(F@A)@(F@A)).real
    cur=f-abs(U)**2@f
    L=np.log(f/(1-f))
    return j,v,L@cur
def events(U,f):
    means=np.zeros(3);q2=0.
    for bits in itertools.product([0,1],repeat=3):
        incoming=[i for i,b in enumerate(bits) if b]
        p=float(np.prod([f[i] if bits[i] else 1-f[i] for i in range(3)]))
        for outgoing in itertools.combinations(range(3),len(incoming)):
            prob=1. if not incoming else abs(np.linalg.det(U[np.ix_(outgoing,incoming)]))**2
            delta=np.array(bits,float)
            delta[list(outgoing)]-=1
            means+=p*prob*delta;q2+=p*prob*delta[0]**2
    return means[0],q2-means[0]**2,np.log(f/(1-f))@means
def phi(j,v):return j*np.arcsinh(j/v) if v>0 else 0.

rows=[];max_reconstruction=max_concavity=max_event=max_entropy=0.
for k in range(180):
    Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    U,_=np.linalg.qr(Z)
    f=expit(rng.uniform(-20,20,3)) if k%3 else expit(rng.uniform(-3,3,3))
    j,v,s=moments(U,f)
    ej,ev,es=events(U,f)
    max_event=max(max_event,abs(ej-j),abs(ev-v));max_entropy=max(max_entropy,abs(es-s))
    T=abs(U)**2
    lp=linprog(np.zeros(6),A_eq=columns,b_eq=T.ravel(),bounds=[(0,None)]*6,method='highs')
    assert lp.success
    w=lp.x
    jm=[];vm=[];sm=[]
    for P in Ps:
        jj,vv,ss=moments(P,f);jm.append(jj);vm.append(vv);sm.append(ss)
    jm,vm,sm=map(np.array,[jm,vm,sm])
    predicted=w@vm+w@(jm*jm)-(w@jm)**2
    max_reconstruction=max(max_reconstruction,float(np.max(abs(T-(columns@w).reshape(3,3)))))
    max_concavity=max(max_concavity,abs(v-predicted))
    assert np.min(sm-.9*np.array([phi(x,y) for x,y in zip(jm,vm)]))>-2e-12
    assert s>=.9*phi(j,v)-2e-12
    rows.append({'occupations':f.tolist(),'j':j,'v':v,'entropy':s,
                 'ratio':s/phi(j,v) if abs(j)>1e-12 else None,
                 'permutation_weights':w.tolist()})

integration=[]
for k in range(40):
    indices=rng.choice(len(rows),size=9,replace=False);weights=rng.uniform(.01,3,9)
    jj=np.array([rows[i]['j'] for i in indices]);vv=np.array([rows[i]['v'] for i in indices])
    J=weights@jj;C=weights@vv
    lhs=weights@np.array([phi(x,y) for x,y in zip(jj,vv)])
    rhs=phi(J,C)
    assert lhs>=rhs-2e-12
    integration.append({'signed_J':J,'C2':C,'integrated_phi':lhs,'phi_of_integrals':rhs})

x=sp.symbols('x',real=True)
h=x*sp.asinh(x)
exact=sp.simplify(sp.diff(h,x,2)-(2+x*x)/(1+x*x)**sp.Rational(3,2))
assert exact==0
res={'scope':'Same-proposer finite structural tests and exact symbolic identity; not global proof or referee acceptance.',
     'fixtures':len(rows),'signed_integral_fixtures':len(integration),
     'max_birkhoff_reconstruction_error':max_reconstruction,
     'max_variance_concavity_identity_error':max_concavity,
     'max_event_vs_determinant_moment_error':max_event,
     'max_all_reservoir_entropy_error':max_entropy,
     'exact_convexity_derivative_difference':str(exact),
     'fixtures_data':rows,'integration_data':integration}
(OUT/'structural-check-data.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['fixtures_data','integration_data']},indent=2))
