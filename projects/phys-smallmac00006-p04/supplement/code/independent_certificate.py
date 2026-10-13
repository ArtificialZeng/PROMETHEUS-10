#!/usr/bin/env python3
"""Strict independent real-Lyapunov root and sign enclosure.

Only imports fresh referee code, never submitted algorithms or focus outputs.
The center and radius are copied as rational proposals from the frozen claim.
The inverse is generated from this checker's own derivative calculation.
"""
import json,time,resource,platform,sys
from pathlib import Path
from fractions import Fraction
from independent_lyapunov import Box,Tangent,target,calibration,PRECISION

START=time.perf_counter()
ROOT=Path(__file__).resolve().parents[1]
centers=['1.012821998680314600068208268899051820974352006',
         '3.112895114354931694231478861591838762886663535']
radius=Fraction('1e-20')
x0=[Box(v) for v in centers]
# Box finite-decimal endpoints can be entered exactly, without a binary float.
X=[x+Box('-1e-20','1e-20') for x in x0]
def derivative_inputs(xs):return [Tangent(xs[i],[Box(int(i==j)) for j in range(2)]) for i in range(2)]
center,mc=target(*derivative_inputs(x0),max_focus=3)
J0=[[center[i].d[j] for j in range(2)] for i in (1,2)]
mid=[[ (Fraction(v.l)+Fraction(v.u))/2 for v in row] for row in J0]
detmid=mid[0][0]*mid[1][1]-mid[0][1]*mid[1][0]
assert detmid!=0
Rrat=[[mid[1][1]/detmid,-mid[0][1]/detmid],[-mid[1][0]/detmid,mid[0][0]/detmid]]
R=[[Box(v) for v in row] for row in Rrat]
f,meta=target(*derivative_inputs(X),max_focus=4)
J=[[f[i].d[j] for j in range(2)] for i in (1,2)]
M=[[Box(int(i==j))-sum((R[i][k]*J[k][j] for k in range(2)),Box(0)) for j in range(2)] for i in range(2)]
shift=[-sum((R[i][k]*center[k+1].v for k in range(2)),Box(0)) for i in range(2)]
image=[x0[i]+shift[i]+sum((M[i][j]*Box('-1e-20','1e-20') for j in range(2)),Box(0)) for i in range(2)]
norms=[sum(map(abs,row),Box(0)) for row in M]
det=J[0][0]*J[1][1]-J[0][1]*J[1][0]
leading=f[3].v*meta['w'].v**4/2
rank_b=-(X[1]-1)*(2*X[1]-1)/(32*X[1])
inside=all(X[i].l<image[i].l<=image[i].u<X[i].u for i in range(2))
contract=all(n.u<1 for n in norms)
rank=(det.l>0 or det.u<0)
negative=(f[3].v.u<0)
legal=all(meta[k].v.l>0 for k in ('a','K','w')) and meta['b'].v.l>-1 and meta['d'].v.l>1 and (1+meta['b'].v*meta['d'].v).l>0
residuals_contain_zero=all(v.v.l<=0<=v.v.u for row in meta['residuals'] for v in row)
# At simultaneous lower zeros: c3=2*F2/w^2, c4=2*F3/w^3 modulo lower c3.
# Therefore det D(c3,c4)=4/w^5 * det D(F2,F3) on their common zero set.
converted_det=det*meta['w'].v**5/4
unfolding=-(1+meta['b'].v*meta['d'].v)/(2*X[1]-1)*rank_b*converted_det
print('METHOD real homogeneous Lyapunov scalar equations; decimal directed endpoints',PRECISION,flush=True)
print('CENTER',centers,'RADIUS',str(radius),flush=True)
print('CENTER c3,c4',[center[i].v for i in (1,2)],flush=True)
print('J independent c3,c4',J,flush=True)
print('DET independent',det,flush=True)
print('CONTRACTION_ROW_SUMS',norms,flush=True)
print('IMAGE_MINUS_CENTER',[image[i]-x0[i] for i in range(2)],flush=True)
print('c5 interval',f[3].v,flush=True)
print('F4 at common lower zero, by positive leading conversion',leading,flush=True)
print('det D(F2,F3) at common zero',converted_det,flush=True)
print('det full original-parameter unfolding',unfolding,flush=True)
tests={'strict_inclusion':inside,'contraction':contract,'restricted_rank_two':rank,
       'fourth_obstruction_negative':negative,'legal_parameters':legal,
       'all_polynomial_residuals_enclose_zero':residuals_contain_zero,
       'nonzero_first_focus_b_derivative':rank_b.u<0,
       'full_unfolding_determinant_negative':unfolding.u<0}
print('TESTS',tests,flush=True)
cal,cm=calibration()
calF3=cal[2]*cm['w']**3/2
assert cal[:2]==[0,0]
assert calF3==Fraction(-4375,884736)
# Return coefficient (2*pi/sqrt(7/8))*F3 = -625*pi*sqrt(7/2)/110592.
assert calF3*Fraction(8,7)==Fraction(-625,110592)
endpoint,em=target(Fraction(1),Fraction(22,7))
assert endpoint[:2]==[0,0]
assert endpoint[2]*em['w']**3/2==Fraction(-18125,2404233216)
assert all(v==0 for row in cm['residuals'] for v in row)
assert all(v==0 for row in em['residuals'] for v in row)
out={'job_id':'phys-smallmac00006-p04-referee-327806750a38',
     'method':'independent real scalar Lyapunov homological recurrence through degree ten; original field jet through nine',
     'arithmetic':'Python decimal.Context ROUND_FLOOR and ROUND_CEILING on each endpoint operation; no numerical tolerance',
     'precision_decimal_digits':PRECISION,'centers_exact_decimal':centers,'radius_exact':str(radius),
     'box':[v.record() for v in X],'center_obstructions':[center[i].v.record() for i in (1,2)],
     'jacobian_box':[[v.record() for v in row] for row in J],
     'preconditioner_rational':[[str(v) for v in row] for row in Rrat],
     'jacobian_determinant':det.record(),'contraction_row_sums':[v.record() for v in norms],
     'image':[v.record() for v in image],'image_minus_center':[(image[i]-x0[i]).record() for i in range(2)],
     'fourth_obstruction':f[3].v.record(),'F4_at_common_zero':leading.record(),
     'normal_form_restricted_det_at_common_zero':converted_det.record(),
     'full_unfolding_determinant':unfolding.record(),
     'parameters':{k:meta[k].v.record() for k in ('a','h','b','d','K','w')},
     'tests':tests,'exact_baseline':{'calibration_obstructions':list(map(str,cal)),
     'calibration_F3':str(calF3),'target_endpoint_F3':str(endpoint[2]*em['w']**3/2)},
     'independence':'No proposer code/cache imported. Rational candidate center is only a proposal. Source ODE, real-jet generation, real scalar homological solver, arithmetic backend, preconditioner and proof of inclusion are reconstructed here.',
     'limitations':'Interval constants use a different triangular focus convention. Equality and determinant conversions are justified in audit/science.md, and only asserted on the common lower-zero locus. No explicit finite-amplitude epsilon is certified.',
     'runtime_seconds':time.perf_counter()-START,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'python':sys.version,'platform':platform.platform()}
(ROOT/'audit/independent-certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print('runtime_seconds',out['runtime_seconds'],'peak_rss_bytes_macos',out['peak_rss_bytes_macos'],flush=True)
assert all(tests.values())
