"""Adversarial first-variation and uniform-remainder checks, single worker.

The theorem is analytic. These are numerical attacks, not an interval proof.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import quad
from sinusoidal import perturbative_coefficient

OUT=Path(__file__).resolve().parent
A=np.exp(-.5);D=2*A;W=2*np.sqrt(2/np.pi)
h=(1-A)/4;beta=(1+A)/2;delta=1-beta**2
K=4*W**2*(1+h)**2+4*D*W+4*(beta*W+D)**2/delta
kap=.7

profiles={
    'sine':{'func':lambda z:np.sin(z),'coeffs':[(1,0,1)],'M':1,'jump':False},
    'mixed':{'func':lambda z:.6*np.cos(z)-.4*np.sin(2*z)+.3*np.sin(5*z),
             'coeffs':[(1,.6,0),(2,0,-.4),(5,0,.3)],'M':1.3,'jump':False},
    'square':{'func':lambda z:1. if np.sin(z)>=0 else -1.,
              'coeffs':[(n,0,4/(np.pi*n)) for n in range(1,81,2)],'M':1,'jump':True},
    'high_mode':{'func':lambda z:np.sin(18*z),'coeffs':[(18,0,1)],'M':1,'jump':False},
    'constant':{'func':lambda z:1.,'coeffs':[],'M':1,'jump':False}}


def integrate(fun,mu,jump):
    points=[-10.,10.]
    if jump:
        j0=int(np.floor(kap*(mu-10)/np.pi))
        j1=int(np.ceil(kap*(mu+10)/np.pi))
        points.extend(j*np.pi/kap-mu for j in range(j0,j1+1) if -10<j*np.pi/kap-mu<10)
    else:
        points.extend([-6,-3,-1,0,1,3,6])
    points=sorted(points)
    vals=[quad(fun,a,b,epsabs=2e-12,epsrel=2e-12,limit=300)[0] for a,b in zip(points[:-1],points[1:])]
    return float(sum(vals))


def predicted(t,profile):
    return float(sum(perturbative_coefficient(1/np.sqrt(2),n*kap)*(bn*np.cos(n*t)-an*np.sin(n*t))
                     for n,an,bn in profile['coeffs']))


def response(mu,profile):
    func=profile['func']
    return 16*np.sqrt(2)*A*integrate(
        lambda y:y*np.exp(-y*y)/np.sqrt(np.pi)*np.cos(np.sqrt(2)*y)*func(kap*(mu+y)),mu,profile['jump'])


def direct_sld(mu,eps,profile):
    func=profile['func']
    def entries(y):
        x=mu+y;f=x/np.sqrt(2)+eps*func(kap*x)
        c,s=np.cos(f),np.sin(f)
        return np.array([c*c,c*s,s*s])*np.exp(-y*y)/np.sqrt(np.pi)
    matrices=[]
    for score in (False,True):
        row=[]
        for j in range(3):
            row.append(integrate(lambda y:entries(y)[j]*(2*np.sqrt(2)*y if score else 1),mu,profile['jump']))
        matrices.append(np.array([[row[0],row[1]],[row[1],row[2]]]))
    rho,drho=matrices
    lam,v=np.linalg.eigh(rho);change=v.T@drho@v
    return float(2*np.sum(abs(change)**2/(lam[:,None]+lam[None,:]))),float(1-(lam[1]-lam[0])**2)


def main():
    z=sy.symbols('z',real=True)
    positive_derivative=sy.simplify(sy.diff(z*sy.cosh(z)-sy.sinh(z),z)-z*sy.sinh(z))
    if positive_derivative!=0:raise RuntimeError('Positivity derivative mismatch')
    rows=[];maxdiff=0.;maxratio=0.
    for name,p in profiles.items():
        for t in np.linspace(.071,2*np.pi+.071,17,endpoint=False):
            mu=t/kap
            ga=response(mu,p);gb=predicted(t,p);err=abs(ga-gb)
            maxdiff=max(maxdiff,err)
            for eps in (-.02,.005):
                q,gap=direct_sld(mu,eps,p)
                rem=abs(q-4/np.e-eps*gb)
                bound=K*p['M']**2*eps**2
                ratio=rem/bound
                maxratio=max(maxratio,ratio)
                rows.append({'profile':name,'t':float(t),'epsilon':eps,
                    'response_direct':ga,'response_fourier':gb,'response_error':err,
                    'qfi_density_sld':q,'remainder_absolute':rem,'analytic_bound':float(bound),
                    'remainder_to_bound_ratio':float(ratio),'rank_gap':gap,
                    'rank_gap_lower_bound':float(delta),'in_theorem_radius':bool(abs(eps)*p['M']<=h)})
    record={'job_id':'phys-00003-p10-research-5adb4c33e8c2',
        'method_a':'Direct odd-kernel Gaussian first variation and separately integrated projector/score spectral SLD, split at all square-wave jumps',
        'method_b':'Independent Fourier multiplier formula; square wave coefficients integrated exactly (odd 4/(pi n)) and cutoff n<81',
        'symbolic_positive_multiplier_derivative_difference':str(positive_derivative),
        'constants':{'A':float(A),'D':float(D),'W':float(W),'h':float(h),'beta':float(beta),'delta':float(delta),'K':float(K)},
        'phase_count':17,'profiles':list(profiles),'nonlinear_cases':len(rows),
        'maximum_response_disagreement':maxdiff,'maximum_remainder_to_bound_ratio':maxratio,
        'passed_attack_checks':bool(maxdiff<2e-10 and maxratio<1 and all(x['rank_gap']>=delta and x['in_theorem_radius'] for x in rows)),
        'limitations':'Finite numerical attacks with double quadrature, no formal roundoff enclosure; arbitrary-profile completeness and remainder inequalities are analytic in periodic-variation-proof.md.',
        'cases':rows}
    (OUT/'general-variation-check.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='cases'},indent=2))
    if not record['passed_attack_checks']:raise RuntimeError('General variation attack failed')

if __name__=='__main__':main()
