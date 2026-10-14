#!/usr/bin/env python3
"""Exact continuant identities and conservative rational uniform bounds."""
import hashlib
import json
import platform
import sys
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
import sympy as sp

def main():
    a,b,c,d,x,z=sp.symbols('a b c d x z',nonzero=True)
    j1,j2,j3,j4=sp.symbols('j1 j2 j3 j4',positive=True)
    B=sp.zeros(5)
    for k,j in enumerate([j1,j2,j3,j4]):B[k,k+1]=B[k+1,k]=j
    B[4,4]=1/x
    M=z*sp.eye(5)-B
    sub={j1*j1:a,j2*j2:b,j3*j3:c,j4*j4:d}
    det=sp.expand(M.det()).subs(sub)
    minor=sp.expand(M[1:5,1:5].det()).subs(sub)
    p=z**4-(a+b+c)*z**2+a*c
    p3=z**3-(a+b)*z
    q=z*p-d*p3
    n0=z**3-(b+c)*z
    n1=z*n0-d*(z*z-b)
    checks={'determinant_identity':sp.simplify(-x*det-(p-x*q))==0,
        'first_site_minor_identity':sp.simplify(-x*minor-(n0-x*n1))==0,
        'resolvent_numerator_identity':sp.simplify(n0*q-n1*p+a*b*c*d)==0,
        'cross_chain_inverse_cofactor':sp.simplify((z*sp.eye(4)-B[:4,:4]).adjugate()[0,3]-j1*j2*j3)==0}
    assert all(checks.values())
    # Root-box outer bounds, all deliberately coarse and exact rationals.
    cert=json.loads(Path('evidence/research-root-certificate.json').read_text())
    vv,cc,dd=map(Q,cert['center_exact_decimal']);r=Q(cert['radius_exact_decimal'])
    parameter_checks={'v_gt_3_over_2':vv-r>Q(3,2),'v_gt_15487_over_10000':vv-r>Q(15487,10000),'v_lt_31_over_20':vv+r<Q(31,20),
        'c_gt_12954_over_10000':cc-r>Q(12954,10000),
        'c_lt_12955_over_10000':cc+r<Q(12955,10000),
        'd_positive_and_lt_687_over_1000':dd-r>0 and dd+r<Q(687,1000),
        'd_gt_6861_over_10000':dd-r>Q(6861,10000)}
    v2_upper=Q(31,20)**2
    s_upper=Q(1,4)+v2_upper-Q(12954,10000)
    p_min=Q(15,4)*(4-v2_upper)
    ratio_upper=2+Q(687,1000)*2*(4+Q(136,100))/5
    product_upper=Q(1,4)*v2_upper*Q(136,100)*Q(687,1000)
    b_lower=Q(1,4)+Q(15487,10000)**2-Q(12955,10000)-v2_upper/(4*Q(12954,10000))
    outer_checks={'s_lt_136_over_100':s_upper<Q(136,100),
        'p_min_gt_5_on_radius_2':p_min>5,'q_over_p_lt_4':ratio_upper<4,
        'abcd_lt_1':product_upper<1,
        'x0_M_lt_1':Q(1,16)*4<1,
        'high_weight_denominator_gt_half':Q(253,256)**4>Q(1,2),
        'J2_gt_9_over_10':b_lower>Q(81,100),
        'J2_gradient_l1_lt_3':Q(41,10)/Q(18,10)<3,
        'duhamel_amplitude_parameter_bound_lt_40_radius':6*2*Q(22,7)<40}
    # e^(4pi) < e^(88/7); pi<22/7. Exact Taylor series plus a geometric tail.
    yy=Q(88,7);term=Q(1);summ=term
    for k in range(1,101):
        term*=yy/k;summ+=term
    first_tail=term*yy/101
    exp_upper=summ+first_tail/(1-yy/102)
    outer_checks['exp_4pi_lt_300000_via_rational_Taylor_bound']=exp_upper<300000
    assert all(parameter_checks.values()) and all(outer_checks.values())
    # Low coefficients n>=9: |f_n|<=24000*4^(n-1).
    low_C=Q(24000)*4**8/(1-Q(1,4))*Q(1,16)
    high_C=Q(2);total_C=low_C+high_C
    assert total_C==131072002
    out={'symbolic_checks':checks,'parameter_outer_box_checks':parameter_checks,
         'uniform_bound_checks':outer_checks,
         'rational_values':{'p_min_lower':str(p_min),'q_over_p_upper':str(ratio_upper),
            'abcd_upper':str(product_upper),'exp_88_over_7_upper_numerator':str(exp_upper.numerator),
            'exp_88_over_7_upper_denominator':str(exp_upper.denominator)},
         'constants':{'tau':'2pi','contour_radius':'2','x0':'1/16','coefficient_bound':'|f_n|<=24000*4^(n-1), n>=1',
            'low_remainder_bound':'|f_low(x)-ell*x|<=2097152000*x^9<=131072000*x^8',
            'high_remainder_bound':'|a_high(x)|<=2*x^8','C':str(total_C)},
         'scope':'Exact algebra and rational estimates supporting the uniform proof. Root existence comes from the separate contraction certificate; no acceptance is inferred.'}
    Path('evidence/research-symbolic-and-bound-check.json').write_text(json.dumps(out,indent=2)+'\n')
    env={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),
        'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,'mpmath':mp.__version__,
        'installations_performed':False,'interval_operations_used':'elementary arithmetic, sin, cos, pi; mp.findroot only proposes center'}
    Path('evidence/research-environment.json').write_text(json.dumps(env,indent=2)+'\n')
    print(json.dumps({'symbolic_checks':checks,'parameter_outer_box_checks':parameter_checks,
        'uniform_bound_checks':outer_checks,'C':str(total_C),'x0':'1/16'}))

if __name__=='__main__':main()
