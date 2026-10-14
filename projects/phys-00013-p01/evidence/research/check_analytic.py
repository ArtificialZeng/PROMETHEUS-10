"""Exact normalization/orthogonality/moment checks for the analytic derivation."""
from pathlib import Path
import json
import sympy as s
x,y,R,z=s.symbols('x y R z', real=True)
w=s.Rational(105,16)*s.sqrt(x)*(1-x)**2
assert s.integrate(w,(x,0,1))==1
assert s.integrate(x*w,(x,0,1))==s.Rational(1,3)
# Reconstruct the published qubit purity density under I=(1+x)/2.
purity=s.Symbol('I',real=True)
published=s.Rational(105,2)*(1-purity)**2*s.sqrt(2*purity-1)
assert s.simplify(published.subs(purity,(1+x)/2)/2-w)==0
assert s.integrate(s.integrate(6*(x-y)**2,(x,0,1)),(y,0,1))==1
assert s.integrate(12*R**2*(1-R),(R,0,1))==1
positive_z=s.integrate(6*R*(1-R),(R,z,1))
assert s.expand(positive_z)==1-3*z**2+2*z**3
assert s.simplify(-2*z*s.diff(positive_z,z)-12*z**2*(1-z))==0
moments=[]
for r in range(9):
    observed=s.integrate(12*R**(2*r+2)*(1-R),(R,0,1))
    expected=s.Rational(6,(r+2)*(2*r+3))
    assert observed==expected
    moments.append({'r':r,'moment':str(observed)})
# The argument for arbitrary r is elementary integration, not this finite table.
polys=[s.jacobi(r,2,s.Rational(1,2),2*x-1) for r in range(5)]
for r,p in enumerate(polys):
    for t in range(r):
        assert s.integrate(s.expand(p*polys[t]) * w,(x,0,1))==0
    assert s.integrate(s.expand(p*p)*w,(x,0,1))>0
q1=x-s.Rational(1,3)
conditional_mean=s.Rational(2,5)*x+s.Rational(1,5)
assert s.expand(conditional_mean-s.Rational(1,3))==s.Rational(2,5)*q1
joint_purity_moment=s.integrate((1+x)*(1+conditional_mean)*w/4,(x,0,1))
assert joint_purity_moment==s.Rational(74,165)
result={'published_marginal_reproduced_exactly':True,'marginal_mean_t':'1/3',
        'projection_density_normalized':True,'radial_density_normalized':True,
        'component_to_radial_inversion_exact':True,'integer_moments_checked':moments,
        'Jacobi_orthogonality_through_degree':4,'conditional_first_moment':str(conditional_mean),
        'cross_single_qubit_purity_moment':'74/165',
        'limitations':'These symbolic checks validate algebraic consequences of the analytic inputs. They do not independently prove the Haar orbit law or certify novelty; those require primary source reconstruction and the complete proof.'}
Path('evidence/research/analytic-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
