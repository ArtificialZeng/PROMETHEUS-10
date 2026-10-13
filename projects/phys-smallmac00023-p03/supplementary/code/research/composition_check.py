"""Exact nine-matrix-unit post-loss identity used to cover all lambda."""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
t,r=s.symbols('t r',nonnegative=True)
alpha=s.symbols('alpha',nonnegative=True)

def act(m,n,u,dephase=False):
    out=s.zeros(3)
    factor=2**(-s.Rational((m-n)**2,2)) if dephase else 1
    for ell in range(min(m,n)+1):
        out[m-ell,n-ell]+=factor*s.sqrt(s.binomial(m,ell)*s.binomial(n,ell))*(1-u*u)**ell*u**(m+n-2*ell)
    return out

def main():
    for m in range(3):
        for n in range(3):
            N=act(m,n,t,True);lhs=s.zeros(3)
            for a in range(3):
                for b in range(3):lhs+=N[a,b]*act(a,b,r)
            assert (lhs-act(m,n,t*r,True)).applyfunc(s.expand)==s.zeros(3)
    # Real pure-loss Kraus; alpha=sqrt(1-r^2) in the physical domain.
    K0=s.diag(1,r,r*r);K1=s.zeros(3);K1[0,1]=alpha;K1[1,2]=s.sqrt(2)*r*alpha
    K2=s.zeros(3);K2[0,2]=alpha*alpha
    tp=sum((K.T*K for K in [K0,K1,K2]),s.zeros(3))
    assert (tp-s.eye(3)).applyfunc(lambda x:s.rem(s.Poly(x,alpha),s.Poly(alpha*alpha-(1-r*r),alpha)).as_expr().expand())==s.zeros(3)
    print('PASS: E_(r^2) composed with N_(t^2,ln2)=N_((rt)^2,ln2), all9 matrix units and81 entry residuals exactly zero')
    print('PASS: loss Kraus sum K^T K=I3, hence adjoint unital, for0<=r<=1; output remains inH3')
    (ROOT/'evidence/qutrit-composition-check.json').write_text(json.dumps({'status':'pass','identity':'E_mu composed with N_lambda,ln2=N_mu*lambda,ln2','parameters':'lambda=t^2,mu=r^2; t,r in[0,1]','coverage':'all9 input matrix units, all81 output residuals; exact polynomial algebra','trace_preservation':'all9 entries of sum K^T K-I exactly zero after alpha^2=1-r^2','physical_admissibility':'alpha>=0 and real on physical domain, finite loss Kraus completely positive and preserve invariantH3','use':'primal postcomposition below endpoint; adjoint unital CP pullback of strict dual above2/3'},indent=2)+'\n')

if __name__=='__main__':main()
