#!/usr/bin/env python3
"""Exact covariance controls and full scaled collision-matrix degree bounds."""
from pathlib import Path
import datetime,json
import sympy as S
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
HERE=args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
x,y,z,U,V,W,m,n,h,b,e=S.symbols('x y z U V W m n h beta epsilon',real=True)
p=S.symbols('p',positive=True)
delta=S.Rational(1,4)
def gm(expr,vars):
    total=0
    for powers,c in S.Poly(S.expand(expr),*vars).terms():
        moment=1
        for q in powers:
            moment*=0 if q%2 else S.factorial2(q-1) if q else 1
        total+=c*moment
    return S.factor(total)
qP=(1+b*(x*x+y*y-2))**2+delta
qR=(1+e*(z**3-3*z))**2+delta
zP=gm(qP,[x,y]);zR=gm(qR,[z])
assert gm(x*qP,[x,y])==gm(y*qP,[x,y])==gm(z*qR,[z])==0
vP=S.factor(gm(x*x*qP,[x,y])/zP)
vR=S.factor(gm(z*z*qR,[z])/zR)
assert S.factor(vP-(S.Rational(5,4)+4*b+12*b*b)/(S.Rational(5,4)+4*b*b))==0
assert S.factor(vR-(S.Rational(5,4)+42*e*e)/(S.Rational(5,4)+6*e*e))==0
assert gm(x*y*qP,[x,y])==0
u40=S.factor(gm((x*x+y*y)**2*qP,[x,y])/(zP*vP*vP))

v=S.Matrix([h*x,h*y,m+h*h*z]);w=S.Matrix([h*U,h*V,n+h*h*W])
def kernel(r):return ((r.dot(r))*S.eye(3)-r*r.T)/2
T=S.diag(h*h,h*h,3-2*h*h)
J=S.diag(1/h,1/h,1/h**2)
A=kernel(v)+(3*S.eye(3)-T)/2
As=(h*h*J*A*J).applyfunc(S.expand);Ks=(h*h*J*kernel(v-w)*J).applyfunc(S.expand)
def pmat(M):
    out=M.applyfunc(lambda v:S.Poly(v,h).as_expr().subs(h*h,p))
    for v in M:
        assert all(k[0]%2==0 for k,c in S.Poly(v,h).terms())
    return out.applyfunc(S.expand)
Ap=pmat(As);Kp=pmat(Ks)
A0=Ap.subs(p,0);K0=Kp.subs(p,0)
assert A0==S.Matrix([[(m*m+3)/2,0,-m*x/2],[0,(m*m+3)/2,-m*y/2],[-m*x/2,-m*y/2,1+(x*x+y*y)/2]])
degreesA=[S.Poly(v,p).degree() if v else -1 for v in Ap]
degreesK=[S.Poly(v,p).degree() if v else -1 for v in Kp]
assert max(degreesA)==max(degreesK)==2
record={'P_raw_mass':str(zP),'P_raw_axis_variance':str(vP),'P_standardized_U4':str(u40),
 'R_raw_mass':str(zR),'R_raw_variance':str(vR),'all_raw_means':'exactly zero','P_raw_offdiagonal':'exactly zero',
 'positive_lower_polynomial_bound':'1/4 for every real beta,epsilon',
 'scaled_A_full':str(Ap),'scaled_pair_kernel_full':str(Kp),'scaled_A_leading':str(A0),'scaled_pair_leading':str(K0),
 'matrix_degree_bounds_in_p':[max(degreesA),max(degreesK)],'pair_scaled_integrand_degree_bound':4,
 'whole_mixture_covariance':'diag(p,p,kappa_p^2*3+p^2*lambdabar)=diag(p,p,3-2p)',
 'limitations':'Exact symbolic algebra and moments. The degree argument assumes fixed local profiles with finite coefficient integrals; actual-mixture posterior/tail estimates are analytic in the accompanying derivation.'}
(HERE/'normalization-and-scaling-exact.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
