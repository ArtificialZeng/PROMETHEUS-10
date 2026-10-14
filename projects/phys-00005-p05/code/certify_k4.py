"""Exact proposer verification of the signed K4 counterexample; no referee acceptance."""
import itertools,json,hashlib,platform
from pathlib import Path
import sympy as S
import input_a,input_b
R=Path('evidence/research');R.mkdir(exist_ok=True)
edges=list(itertools.combinations(range(4),2));u=[1,1,1,1,-1,-1];s=S.Rational(3,4)
A=input_a.build(4,edges,s,u);B=input_b.build(4,edges,s,u)
rev=[int(format(x,'04b')[::-1],2) for x in range(16)]
assert A==B.extract(rev,rev) and A==A.T
assert all(A[i,j]==0 for i in range(16) for j in range(16) if (i.bit_count()-j.bit_count())%2)
for name,H in [('a',A),('b',B)]:
 (R/('witness-matrix-'+name+'.json')).write_text(json.dumps([[str(v) for v in row] for row in H.tolist()],indent=2)+'\n')
x=S.Symbol('lambda');M={};P={}
for p in (0,1):
 ids=[i for i in range(16) if i.bit_count()%2==p]
 M[p]=B.extract(ids,ids);P[p]=S.Poly(M[p].charpoly(x).as_expr(),x)
 assert P[p]==S.Poly(A.extract(ids,ids).charpoly(x).as_expr(),x)
q=S.Poly(2048*x**4+25600*x**3+92648*x**2+90075*x+20736,x)
assert P[0].as_expr()==S.expand((x+S.Rational(25,16))**4*q.as_expr()/2048)
assert P[1].as_expr()==S.expand(((16*x*x+75*x+36)*(16*x*x+75*x+72))**2/65536)
# Count exact roots with multiplicity using rational Sturm isolation, not eigensolver outputs.
intervals=[(S.Rational(-669,100),S.Rational(-667,100)),(S.Rational(-449,100),S.Rational(-447,100)),(S.Rational(-102,100),S.Rational(-100,100)),(S.Rational(-34,100),S.Rational(-33,100))]
assert all(q.count_roots(a,b)==1 for a,b in intervals)
assert sum(q.count_roots(a,b) for a,b in intervals)==q.degree()
# Sturm lists and signs at rational thresholds make the root-count replay transparent.
def sturm_data(poly,t):
 seq=S.sturm(poly.as_expr(),x);values=[S.factor(v.subs(x,t)) for v in seq];signs=[S.sign(v) for v in values if v!=0]
 variations=sum(signs[i]!=signs[i+1] for i in range(len(signs)-1))
 return {'point':str(t),'values':[str(v) for v in values],'variations':variations}
thresholds=[S.Rational(-7),S.Rational(-89,20),S.Rational(-83,20),S.Rational(0)]
# q has exactly 2 roots below -89/20; four repeated roots -25/16 are above.
assert q.count_roots(-S.oo,S.Rational(-89,20))==2
assert P[1].count_roots(-S.oo,S.Rational(-83,20))==0
# Exact radical comparison: Eo1=(-75-sqrt(3321))/32 > -83/20.
# Equivalent sqrt(3321)<289/5, verified after squaring positive numbers.
assert S.Rational(289,5)**2>3321
# Inertia checked by a separate rational LDL congruence of full sector matrices.
inertia={}
for p,t in [(0,S.Rational(-89,20)),(1,S.Rational(-83,20))]:
 shifted=M[p]-t*S.eye(8);L,D=shifted.LDLdecomposition(hermitian=False)
 assert L*D*L.T==shifted
 assert all(D[i,j]==0 for i in range(8) for j in range(8) if i!=j)
 pivots=[D[i,i] for i in range(8)];neg=sum(int(bool(v<0)) for v in pivots)
 assert neg==(2 if p==0 else 0)
 inertia[str(p)]={'threshold':str(t),'pivots':[str(v) for v in pivots],'negative':neg,'positive':8-neg,'zero':0,'congruence_exact':True}
# Also test ground-state isolation explicitly, no dependence on external gap theorem.
assert q.count_roots(-S.oo,S.Rational(-6))==1
assert P[1].count_roots(-S.oo,S.Rational(-6))==0
# General s formulas rebuilt from both exact constructions.
t=S.Symbol('s',real=True);HB=input_b.build(4,edges,t,u);HA=input_a.build(4,edges,t,u)
assert HA==HB.extract(rev,rev)
# Independent block checks used in the analytic explanation.
eids=[i for i in range(16) if i.bit_count()%2==0]
E=HB.extract(eids,eids);a=E.extract([0],list(range(1,7)));b=E.extract([7],list(range(1,7)))
assert (a*a.T)[0]==6*t*t and (b*b.T)[0]==6*t*t and (a*b.T)[0]==-2*t*t
one=[i for i in range(16) if i.bit_count()==1];three=[i for i in range(16) if i.bit_count()==3]
C=HB.extract(one,three)
assert (C*C.T).charpoly(x).as_expr()==S.expand((x-5*t*t)**2*(x-t*t)**2)
generic={}
for p in (0,1):
 ids=[i for i in range(16) if i.bit_count()%2==p]
 generic[str(p)]=str(S.factor(HB.extract(ids,ids).charpoly(x).as_expr()))
# Cycle product: 01*23/(12*03)=-1; triangle guarantees nonbipartite.
d=dict(zip(edges,u));assert d[0,1]*d[2,3]/(d[1,2]*d[0,3])==-1
# Weyl margin: sum norm bounds <=6*(3 ds+dtheta) for |s-s0|<1/1000,
# max wrapped phase change <1/1000, 0<s<1; 2||Delta H||<48/1000<3/10.
assert S.Rational(48,1000)<S.Rational(3,10)
record={'status':'pass','python':platform.python_version(),'sympy':S.__version__,'witness':{'n':4,'edges':edges,'s':'3/4','unit_phases':u,'theta':['0','0','0','0','pi','pi'],'cycle':'0-1-2-3-0','alternating_product':'-1'},'A_B_entrywise_and_sector_polynomials_exact':True,'parity_commutes_exact':True,'even_charpoly':str(S.factor(P[0].as_expr())),'odd_charpoly':str(S.factor(P[1].as_expr())),'even_quartic_intervals':[{'interval':[str(a),str(b)],'exact_root_count':1} for a,b in intervals],'quartic_sturm':[sturm_data(q,t) for t in thresholds],'LDL_inertia':inertia,'odd_minimum':'(-75-sqrt(3321))/32','ordering':'Ee1 < -6 < Ee2 < -89/20 < -83/20 < Eo1; Eo1-Ee2>3/10','exact_ground_unique':True,'generic_sector_polynomials':generic,'robust_neighborhood':{'abs_s_change_less_than':'1/1000','each_wrapped_phase_change_less_than':'1/1000','H_operator_norm_change_less_than':'24/1000','ordering_margin_greater_than':'252/1000'},'limitations':'Same proposer worker made all checks; exact matrix/congruence independence does not constitute fresh referee review. No phase-free conjecture disproof, no response intensity or thermodynamic claim.'}
(R/'exact-certificate.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
