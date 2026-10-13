#!/usr/bin/env python3
"""Exact directed dyadic Krawczyk enclosure of target focus root and L4 sign."""
import json,time,resource,sys
from pathlib import Path
from fractions import Fraction
from research_normal_form import focus,Dual
from dyadic_interval import I,BITS
start=time.perf_counter()
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'evidence/research/certificate-input.json').read_text())
# All proposals below are fixed rationals. Only integer interval verification follows.
centers=r['center_decimal_rationals'];radius=r['radius_decimal_rational']
x0=[I(v) for v in centers];X=[v+I('-'+radius,radius) for v in x0]
Rtext=r['preconditioner_exact_decimal_rationals']
R=[[I(v) for v in row] for row in Rtext]
print('center',centers,'radius',radius,'R',Rtext,flush=True)
f0,_=focus(*x0,7)
fbox,meta=focus(Dual(X[0],I(1),I(0)),Dual(X[1],I(0),I(1)),9)
J=[[v.da,v.dh] for v in fbox[1:3]]
M=[[I(int(i==j))-sum((R[i][k]*J[k][j] for k in range(2)),I(0)) for j in range(2)] for i in range(2)]
shift=[-sum((R[i][j]*f0[j+1] for j in range(2)),I(0)) for i in range(2)]
Y=[x0[i]+shift[i]+sum((M[i][j]*(X[j]-x0[j]) for j in range(2)),I(0)) for i in range(2)]
row_norm=[sum((abs(v) for v in row),I(0)) for row in M]
det=J[0][0]*J[1][1]-J[0][1]*J[1][0]
# R is the exact decimal rational matrix in Rtext, enclosed by dyadic R above.
Rrat=[[Fraction(v) for v in row] for row in Rtext]
Rdet=Rrat[0][0]*Rrat[1][1]-Rrat[0][1]*Rrat[1][0]
assert Rdet!=0
inclusion=all(Y[i].interior_of(X[i]) for i in range(2))
contraction=all(v.hi<I(1).lo for v in row_norm)
sign=fbox[3].v.hi<0
rank=not det.contains_zero()
print('F(center)',[str(v) for v in f0],flush=True)
print('J(X)',J,'det',det,flush=True)
print('Krawczyk shift',shift,'image-center',[Y[i]-x0[i] for i in range(2)],'row norm',row_norm,flush=True)
print('focus bounds',[v.v for v in fbox],flush=True)
print('included',inclusion,'contraction',contraction,'L4negative',sign,'rank',rank,flush=True)
def rec(v):return {'decimal_outward':v.decimal(45),'exact_dyadic':v.exact()}
out={'job_id':'phys-smallmac00006-p04-research-ca0344333939','arithmetic':'integer endpoints, fixed binary grid, explicit outward rounding',
 'precision_bits':BITS,'center_decimal_rationals':centers,'radius_decimal_rational':radius,
 'box':[rec(x) for x in X],'F_center':[rec(v) for v in f0[1:3]],
 'jacobian_box':[[rec(v) for v in row] for row in J],
 'preconditioner_exact_decimal_rationals':Rtext,'jacobian_determinant':rec(det),
 'krawczyk_image':[rec(v) for v in Y],'krawczyk_image_minus_center':[rec(Y[i]-x0[i]) for i in range(2)],
 'contraction_row_norms':[rec(v) for v in row_norm],
 'focus_box':[rec(v.v) for v in fbox],
 'parameter_box':{k:rec(meta[k].v) for k in ['b','d','K','omega2']},
 'tests':{'strict_krawczyk_inclusion':inclusion,'contraction':contraction,'negative_degree9_real_resonance':sign,'rank_two_restricted_focus_map':rank,'preconditioner_nonsingular_exact':True},
 'scope':'Algebraic coefficient enclosure and root existence for computed normal-form map. Correct interpretation, independent computation, full unfolding and original ODE proof require the accompanying argument and fresh referee.',
 'elapsed_seconds':time.perf_counter()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(root/'evidence/research/interval-certificate.json').write_text(json.dumps(out,indent=2)+'\n')
assert inclusion and contraction and sign and rank
print('elapsed',out['elapsed_seconds'],'peak_rss',out['peak_rss_bytes_macos'],flush=True)
