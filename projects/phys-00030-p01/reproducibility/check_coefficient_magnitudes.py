"""Independently reconstruct the exact coefficient-magnitude bound in the packet.

No proposer module is imported. Exact rational comparisons of binary interval
endpoints distinguish inward rounding from mere numerical differences.
"""
import inspect,json
from fractions import Fraction
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'reproducibility/run-output'
RUN.mkdir(parents=True,exist_ok=True)
def polynomial(edges):
    before=[mp.iv.mpf(1)];now=[mp.iv.mpf(0),mp.iv.mpf(1)]
    for edge in edges:
        nxt=[mp.iv.mpf(0)]+now
        for j,value in enumerate(before):nxt[j]-=edge*value
        before,now=now,nxt
    return now

def reconstruct(digits):
    mp.iv.dps=digits
    angle=mp.iv.pi/256
    edges=[1/(4*mp.iv.sin((2*l+1)*angle)*mp.iv.sin((2*l-1)*angle)) for l in range(1,128)]
    return [polynomial(edges)[::2],polynomial(edges[1:])[1::2]]

def exact(t):
    sign,mantissa,exponent,bits=t
    return (-1 if sign else 1)*Fraction(mantissa)*(Fraction(2)**exponent)

def absolute_endpoints(interval):
    a,b=map(exact,interval._mpi_)
    assert a*b>=0
    return sorted([abs(a),abs(b)])

submitted_coefficients=reconstruct(250)
mp.iv.dps=85;mp.mp.dps=100
submitted_abs=[]
for poly in submitted_coefficients:
    arr=[]
    for p in poly:
        lo=mp.make_mpf(p._mpi_[0]);hi=mp.make_mpf(p._mpi_[1])
        rounded=max(abs(lo),abs(hi))
        arr.append(mp.iv.mpf([rounded,rounded]))
    submitted_abs.append(arr)

# An independent higher-precision enclosure of the same exact coefficients,
# formed entirely with directed interval operations, not point minimization.
high_coefficients=reconstruct(500)
issues=[];checks=[]
for p,(old,new,absarr) in enumerate(zip(submitted_coefficients,high_coefficients,submitted_abs)):
    for i,(oldcoef,newcoef,bound) in enumerate(zip(old,new,absarr)):
        oldlo,oldhi=absolute_endpoints(oldcoef)
        newlo,newhi=absolute_endpoints(newcoef)
        actual_upper=exact(bound._mpi_[1])
        not_enclosing_original=actual_upper<oldhi
        strictly_below_exact=actual_upper<newlo
        row={'polynomial':'F(q)=FE(q^2)' if p==0 else 'B(q)=q BE(q^2)',
             'coefficient_index_in_q_squared_polynomial':i,
             'power_of_q':2*i if p==0 else 2*i+1,
             'fails_to_enclose_250_digit_input_interval':not_enclosing_original,
             'strictly_below_500_digit_exact_coefficient_lower':strictly_below_exact}
        if strictly_below_exact:
            row.update({'submitted_ABS_upper_exact_fraction':str(actual_upper),
                        'exact_coefficient_magnitude_lower_fraction_500_digits':str(newlo),
                        'exact_positive_shortfall_lower_fraction':str(newlo-actual_upper),
                        'shortfall_lower_decimal':mp.nstr(mp.mpf((newlo-actual_upper).numerator)/(newlo-actual_upper).denominator,12)})
            issues.append(row)
        checks.append(row)

record={'status':'failed_outward_bound' if issues else 'no_strict_underestimate_identified',
        'implementation_under_audit':'evidence/research/r3-interval-enclosure.py:ABS initialization and absupper',
        'trust_base':'mpmath 1.3.0 directed trigonometric/polynomial intervals at 250 and 500 decimal digits; exact Python rational endpoint comparison',
        'total_coefficients':len(checks),'original_interval_enclosure_failures':sum(x['fails_to_enclose_250_digit_input_interval'] for x in checks),
        'strict_exact_coefficient_magnitude_underestimates':len(issues),
        'mpf_abs_implementation':inspect.getsource(type(mp.mpf(1)).__abs__),
        'interpretation':'These are strict invalid upper bounds used in the order-20 remainder sum. This establishes a gap in the submitted outward error proof, not a disproof of the physical witness. Diagnostic numerical agreement and exact panel resummation do not bound this omitted error.',
        'strict_witnesses':issues,'all_checks':checks}
(RUN/'coefficient-magnitudes.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['status','total_coefficients','original_interval_enclosure_failures','strict_exact_coefficient_magnitude_underestimates']}))
if issues:print(json.dumps(issues[0],indent=2))
assert issues,'No actual exact-coefficient underestimation was demonstrated'
