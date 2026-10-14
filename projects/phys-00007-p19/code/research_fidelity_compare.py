#!/usr/bin/env python3
"""Published purity formula and independent polarization-tensor twirl comparison."""
from pathlib import Path
from math import comb
import json
import sympy as s
from sympy.physics.wigner import clebsch_gordan
ROOT=Path(__file__).resolve().parents[1]
N=9; j=s.Rational(9,2)
x=s.Symbol('x',real=True)
data=json.loads((ROOT/'evidence/research-20261012-four-support-output-a.json').read_text())
c=s.Matrix([s.sympify(v) for v in data['coefficients_k']])
baseline=json.loads((ROOT/'evidence/reproduce-20261012-input-a.json').read_text())
d=s.zeros(10,1)
for item in baseline['spin_terms']:
 k=(item['twice_m']+N)//2
 d[k]=s.sympify(item['coefficient'],locals={'z':s.S.One})
assert (c.T*c)[0]==1 and (d.conjugate().T*d)[0]==1

def a(t,k):
 return s.Rational(4**t*(-1)**(k+t)*comb(2*N,2*k)*comb(k,t)*comb(2*N-2*t,N-t),(2*k+1)*comb(2*N,N)) if t<=k else s.S.Zero

def purity_F(P):
 return s.Poly(s.expand(sum(x**k*(1-x)**(N-k)*sum(a(t,k)*P[t] for t in range(N+1)) for k in range(N+1))),x)

def complete_purities(P4):
 P=[s.S.One]+P4+[s.S.Zero]*5
 for t in range(5,10):P[t]=P[9-t]
 return P

Pc=complete_purities([s.sympify(data['marginals'][str(t)]['purity']) for t in range(1,5)])
old=json.loads((ROOT/'evidence/reproduce-20261012-output-a.json').read_text())
Pd=complete_purities([s.sympify(old['marginals'][str(t)]['purity'],locals={'z':s.S.One}) for t in range(1,5)])
Fc=purity_F(Pc);Fd=purity_F(Pd)

def tensor_norms(v):
 occupied=[k for k in range(10) if v[k]!=0]
 norms=[]
 for l in range(10):
  amps=[]
  for m in range(-l,l+1):
   z=s.S.Zero
   for k1 in occupied:
    for k2 in occupied:
     if k1-k2!=m:continue
     m1=k1-j;m2=k2-j
     z+=s.conjugate(v[k1])*v[k2]*(-1)**(N-k2)*clebsch_gordan(j,j,l,m1,-m2,m)
   amps.append(s.simplify(z))
  norms.append(s.simplify(sum(z*s.conjugate(z) for z in amps)))
 return norms

def tensor_F(r):
 result=s.S.Zero
 for l in range(10):
  diag=[(-1)**(N-k)*clebsch_gordan(j,j,l,k-j,j-k,0) for k in range(10)]
  # |Tr(e^{-i eta Jz} T_l0)|^2: diagonal pair differences give cos((k-h)eta).
  vl=s.simplify(sum(diag[k]**2 for k in range(10)))
  for diff in range(1,10):
   vl+=2*s.simplify(sum(diag[k]*diag[k+diff] for k in range(10-diff)))*s.chebyshevt(diff,1-2*x)
  result+=r[l]*vl/s.Integer(2*l+1)
 return s.Poly(s.expand(result),x)

rc=tensor_norms(c);rd=tensor_norms(d)
assert sum(rc)==1 and sum(rd)==1 and rc[0]==rd[0]==s.Rational(1,10)
assert rc[1]==rc[2]==rd[1]==rd[2]==0
assert s.simplify(Pc[3]-s.Rational(1,4)-s.Rational(143,588)*rc[3])==0
assert s.simplify(Pd[3]-s.Rational(1,4)-s.Rational(143,588)*rd[3])==0
for label,r,F in [('witness',rc,Fc),('baseline chi=0',rd,Fd)]:
 other=tensor_F(r)
 assert all(s.simplify(v)==0 for v in (F-other).all_coeffs())
 assert F.eval(0)==1
 print('All exact fidelity polynomial coefficients agree:',label,flush=True)
L=s.Matrix([[s.sympify(v) for v in row] for row in json.loads((ROOT/'evidence/research-20261012-recoupling.json').read_text())['lambda']])
assert (L*s.Matrix(rc)-s.Matrix(rc)).applyfunc(s.simplify)==s.zeros(10,1)
assert (L*s.Matrix(rd)-s.Matrix(rd)).applyfunc(s.simplify)==s.zeros(10,1)
print('Both actual pure states obey published recoupling relation exactly.')
diff=s.Poly(s.expand(Fc.as_expr()-Fd.as_expr()),x)
assert all(diff.nth(k)==0 for k in range(3))
gap=s.simplify(Pd[3]-Pc[3])
assert s.simplify(diff.nth(3)+s.Rational(16128,5)*gap)==0
assert a(3,3)==s.Rational(16128,5)
print('Delta F coefficient at eta^6:',-s.Rational(252,5)*gap)
print('Fidelity difference in x=sin^2(eta/2):',s.factor(diff.as_expr()))

# Rigorous finite-domain control: enclose radical polynomial coefficients by
# rational interval arithmetic, then bound q(x)=DeltaF/x^3 for 0<x<=1/100.
from fractions import Fraction as Q
intervals={42:(Q(648074,100000),Q(648075,100000)),273:(Q(1652271,100000),Q(1652272,100000))}
for n,(lo,hi) in intervals.items():assert 0<lo and lo*lo<n<hi*hi
def interval(v):
 v=s.expand(v)
 b=v.coeff(s.sqrt(42));g=v.coeff(s.sqrt(273));r=s.simplify(v-b*s.sqrt(42)-g*s.sqrt(273))
 assert all(z.is_Rational for z in (r,b,g)),v
 lo=hi=Q(str(r))
 for n,z in [(42,b),(273,g)]:
  z=Q(str(z));p,q=intervals[n]
  lo+=z*(p if z>=0 else q);hi+=z*(q if z>=0 else p)
 return lo,hi
eps=Q(1,100)
qcoeff=[diff.nth(k) for k in range(3,10)]
enclosures=[interval(v) for v in qcoeff]
upper=enclosures[0][1]+sum(max(abs(lo),abs(hi))*eps**i for i,(lo,hi) in enumerate(enclosures[1:],1))
assert upper<0,upper
# All members of Eq.65 share P1,P2,P3; chi=0 has minimal P4.
# Verify phi4<0 at the same small-angle interval without numerical sampling.
phi4=s.Poly(s.expand(-s.Rational(4,5)*sum((a(4,k)+a(5,k))*x**k*(1-x)**(N-k) for k in range(4,10))),x)
assert all(phi4.nth(k)==0 for k in range(4))
phi_upper=Q(str(phi4.nth(4)))+sum(abs(Q(str(phi4.nth(k))))*eps**(k-4) for k in range(5,10))
assert phi_upper<0
print('Rational coefficient enclosure gives DeltaF/x^3 <=',upper,'<0 for 0<x<=1/100.')
print('phi4/x^4 <=',phi_upper,'<0 there; chi=0 is best published-family member there.')
print('Thus F_witness(eta)<F_published_chi(eta) for every chi in [0,pi/2] and 0<eta<=2 asin(1/10).')
out={'source_purity_formula':'Quantum 4,285 Eqs.41--45; N=9',
 'independent_formula':'SU(2) twirl in normalized polarization tensors; F=sum_l r_l |Tr(U_z T_l0)|^2/(2l+1)',
 'witness_multipole_norms':[str(v) for v in rc],'baseline_chi0_multipole_norms':[str(v) for v in rd],
 'exact_purity_channel_and_lambda_checks':True,
 'witness_F_polynomial_coefficients_ascending':[str(Fc.nth(k)) for k in range(10)],
 'baseline_F_polynomial_coefficients_ascending':[str(Fd.nth(k)) for k in range(10)],
 'difference_coefficients_ascending':[str(diff.nth(k)) for k in range(10)],
 'exact_independent_fidelity_polynomial_match':True,
 'eta6_coefficient':str(-s.Rational(252,5)*gap),
 'radical_enclosures':{str(n):[str(lo),str(hi)] for n,(lo,hi) in intervals.items()},
 'difference_divided_by_x3_coefficient_enclosures':[[str(lo),str(hi)] for lo,hi in enclosures],
 'x_domain':'0<x=sin^2(eta/2)<=1/100; positive-angle domain 0<eta<=2 asin(1/10) radians',
 'deltaF_divided_by_x3_upper_bound':str(upper),'phi4_divided_by_x4_upper_bound':str(phi_upper),
 'interpretation':'Witness strictly lowers the unknown-axis rotation-average fidelity compared with every member of published Eq.65 on this certified interval; no claim of optimality or other-angle comparison.'}
(ROOT/'evidence/research-20261012-fidelity-comparison.json').write_text(json.dumps(out,indent=2)+'\n')

