#!/usr/bin/env python3
"""Independent direct-weight outward enclosure, with no first-checker inputs."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
D=2**256
def sq(x):
    k=isqrt(x.numerator*D*D//x.denominator)
    lo,hi=F(k,D),F(k+1,D)
    assert lo*lo<=x<hi*hi
    return lo,hi

sl,su=sq(F(3)); low,high=2-su,2-sl
rows=[]
for n in range(10):
    assert 0<low<=high<1
    rows.append({'n':n,'t_lower':str(low),'t_upper':str(high)})
    if n<9:
        # g is increasing, as the inverse of the monotone bijection h.
        _,rad_upper=sq(1+6*low-7*low*low)
        rad_lower,_=sq(1+6*high-7*high*high)
        low,high=2*low/(1+low+rad_upper),2*high/(1+high+rad_lower)
assert low>F(1,20)
data={'method':'direct g(t) outward rational square-root enclosure; binary256 scale; no reciprocal-iteration code or output read',
      'iterations':9,'q':3072,'scale':str(D),'rows':rows,
      't9_lower_greater_than_1_over_20':True,'Tc_star3072_over_J_less_than_20':True}
(HERE/'canonical-direct-certificate.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'t9_enclosure_display_only':[float(low),float(high)],'strict_lower_above_1_over_20':True},indent=2))
