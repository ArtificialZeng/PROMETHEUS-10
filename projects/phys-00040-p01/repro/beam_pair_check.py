#!/usr/bin/env python3
"""Exact new product-profile pair reconstruction, then independent comparison.

No prior code imported. Shared input is the physical kernel/normalization.
The lower-dimensional IBP identities are explicit assumptions checked in prose.
"""
from pathlib import Path
import datetime, json
import sympy as S

import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
HERE=args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
x,y,m,n,U,V,gx,gy,ux,uy,t,tw=S.symbols('x y m n U V gx gy ux uy t tw',real=True)
b,fx,fy,ik=S.symbols('b fx fy ik',positive=True)
coords=S.Matrix([x,y]);delta=S.Matrix([gx-ux,gy-uy,t-tw]);d=m-n
kernel=S.Matrix([[d*d/2,0,-d*(x-U)/2],[0,d*d/2,-d*(y-V)/2],[-d*(x-U)/2,-d*(y-V)/2,((x-U)**2+(y-V)**2)/2]])

# Independent product-profile partner integrations: centering, covariance,
# score IBP and local transverse-longitudinal independence.
def partner(expr):
    ans=0
    trans={(0,0,0,0):1,(1,0,0,0):0,(0,1,0,0):0,
           (2,0,0,0):b,(0,2,0,0):b,(1,1,0,0):0,
           (0,0,1,0):0,(0,0,0,1):0,(0,0,2,0):fx,(0,0,0,2):fy,
           (1,0,1,0):-1,(0,1,0,1):-1,(1,0,0,1):0,(0,1,1,0):0}
    long={0:1,1:0,2:ik}
    for powers,c in S.Poly(S.expand(expr),U,V,ux,uy,tw).terms():
        tr=trans[powers[:4]];zr=long[powers[4]]
        ans+=c*tr*zr
    return S.factor(ans)

M2k=(kernel*delta).applyfunc(partner)
M1k=partner((delta.T*kernel*delta)[0])
r2=x*x+y*y;K=x*gx+y*gy;G=gx*gx+gy*gy;d0=1+r2/2;B=m*m+3
M1k_target=d*d*G/2-d*(K-2)*t+(r2+2*b)*t*t/2+d*d*(fx+fy)/2+(r2+2*b)*ik/2
assert S.factor(M1k-M1k_target)==0

Ibar,Cpartner=S.symbols('Ibar Cpartner',real=True)
# Complete both label sums' conservation substitutions; no partner Fisher
# temperature closure is made. The center-weighted Fisher terms stay constant.
def labels_no_fisher(expr):
    out=0
    for (pn,pb),c in S.Poly(S.expand(expr),n,b).terms():
        assert (pn,pb) in [(0,0),(1,0),(2,0),(0,1)]
        out+=c*{(0,0):1,(1,0):0,(2,0):3,(0,1):1}[(pn,pb)]
    return S.factor(out)
M2=M2k.applyfunc(labels_no_fisher)
A0=S.Matrix([[B/2,0,-m*x/2],[0,B/2,-m*y/2],[-m*x/2,-m*y/2,d0]])
sv=S.Matrix([gx,gy,t]);M2_target=A0*sv+S.Matrix([0,0,m])
assert all(S.factor(v)==0 for v in M2-M2_target)
M1=B*G/2-m*K*t+2*m*t+d0*t*t+r2*Ibar/2+Cpartner

# A second exact algebraic layer integrates local transverse and longitudinal
# factors without Gaussian moment closure. L=Delta P/P, ell=R''/R.
aa,JP,U4,K2,I,J,S3,T4,ELL2=S.symbols('a JP U4 K2 I J S3 T4 ELL2',real=True)
L,KK,dd,GG,rr,tt,ll=S.symbols('L KK dd GG rr tt ll',real=True)
Q=B*L/2-m*KK*tt+dd*ll
M=B*GG/2-m*KK*tt+2*m*tt+dd*tt*tt+rr*Ibar/2+Cpartner
trans={
 (0,0,0,0,0):1,(1,0,0,0,0):0,
 (2,0,0,0,0):ELL2,(1,0,0,1,0):2*ELL2-2*JP,
 (1,1,0,0,0):S.Symbol('E_LK'),(1,0,1,0,0):2,(1,0,0,0,1):4,
 (0,1,0,0,0):-2,(0,2,0,0,0):K2,
 (0,1,0,1,0):S.Symbol('E_KG'),(0,1,1,0,0):-2-4*aa,
 (0,1,0,0,1):S.Symbol('E_Kr2'),
 (0,0,1,0,0):1+aa,(0,0,2,0,0):1+2*aa+U4/4,
 (0,0,1,1,0):S.Symbol('E_dG'),(0,0,1,0,1):S.Symbol('E_dr2')}
long={(0,0):1,(1,0):0,(2,0):I,(3,0):S3,(4,0):T4,
      (0,1):0,(1,1):S3/2,(2,1):2*T4/3,(0,2):J+T4/3}
def local(expr):
    out=0
    for powers,c in S.Poly(S.expand(expr),L,KK,dd,GG,rr,tt,ll).terms():
        zval=long[powers[5:]]
        if zval==0:continue
        out+=c*trans[powers[:5]]*zval
    return S.factor(out)
Qmass=local(Q);assert Qmass==0
QM=local(Q*M);Q2=local(Q*Q)
row=S.factor(QM-2*Q2)
target=-B*B*JP/2-2*(1+2*aa+U4/4)*J+(3+5*m*m-m*m*K2)*I-m*aa*S3+B*Ibar
assert S.factor(row-target)==0
angular=-B*B*JP/2-2*(1+2*aa+U4/4)*J+(9+5*m*m-m*m*K2)*I-m*aa*S3
assert S.factor(row-angular-(B*Ibar-6*I))==0
lam=S.symbols('lam',positive=True)
gaussian=angular.subs({JP:2/aa**2,U4:8*aa**2,K2:8,I:1/lam,J:1/lam**2,S3:0})
gaussian_target=-B**2/aa**2+3*(3-m*m)/lam-(4*aa**2+4*aa+2)/lam**2
assert S.factor(gaussian-gaussian_target)==0

# Exact square-completion, moment-bound and sign constants.
Ac=S.symbols('A',positive=True)
skew=-2*Ac*(I**2+S3**2/(4*I))-m*aa*S3
skew_square=-2*Ac*I**2-Ac/(2*I)*(S3+m*aa*I/Ac)**2+m*m*aa*aa*I/(2*Ac)
assert S.factor(skew-skew_square)==0
uu=S.symbols('u',positive=True)
kbound=1-16/(uu-4)+2/uu
assert S.factor(kbound-1+2*(7*uu+4)/(uu*(uu-4)))==0
assert S.Rational(128,9)>14
assert 1-S.Rational(9,14)==S.Rational(5,14)
assert -S.Rational(5,28)*2*9==-S.Rational(45,14)

record={'method':'New direct leading two-particle variation with general product-profile IBP moments; no prior implementation imported.',
 'pair_kernel':str(kernel),'partner_M1':str(M1k),'partner_M1_residual':'0','partner_M2':str(M2),'partner_M2_residual':'zero vector',
 'local_Q0':str(Q),'local_Q0_mass':str(Qmass),'local_Q0_M1':str(QM),'local_Q0_squared':str(Q2),
 'pair_row':str(row),'pair_row_residual':'0','angular_coefficient':str(angular),'row_redistribution':str(B*Ibar-6*I),
 'weighted_redistribution':'sum w_j B_j=6 and Ibar=sum w_j I_j => 6 Ibar-6 Ibar=0',
 'gaussian_control_residual':'0','skew_square_residual':'0','transverse_bounds':['JP>=2/a^2','K2>=4+16/(u-4)','K2<=4+sqrt(2 JP U4)','JP U4>=max(2u,128/(u-4)^2)>=14'],
 'c_m2_coefficient_upper_minus_one':str(S.factor(kbound-1)),'final_local_bound':'C<=-(5/28)(m^2+3)^2 JP<=-45/(14a^2)',
 'weighted_bound':'sum w C<=-45/14 from sum w a=1','limitations':'Exact algebra checks do not themselves prove the IBP, flow differentiability, or overlap/tail hypotheses; these are derived in product-pair-and-sign-derivation.md. Proposer verification only.'}
(HERE/'product-pair-exact.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
