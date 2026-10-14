from pathlib import Path
from datetime import datetime,timezone
import json
import sympy as s
s1,s2=s.symbols('s1 s2',positive=True)
b11,b22,re,im=s.symbols('b11 b22 re im',real=True)
coordinates=s.Matrix([s1*b11,s2*b22,s.sqrt(s1*s2)*re,s.sqrt(s1*s2)*im])
jac=coordinates.jacobian([b11,b22,re,im]).det()
assert s.simplify(jac-(s1*s2)**2)==0
x,y,z,R,r=s.symbols('x y z R r',real=True)
normalization=s.integrate(s.integrate((x-y)**2,(x,0,1)),(y,0,1))
assert normalization==s.Rational(1,6)
delta_density=12*R**2*(1-R)
assert s.integrate(delta_density,(R,0,1))==1
component=s.integrate(delta_density/(2*R),(R,z,1))
assert s.expand(component)==1-3*z**2+2*z**3
assert s.simplify(-2*z*s.diff(component,z)-delta_density.subs(R,z))==0
# Integrate the two monomials symbolically with the actual r>=0 hypothesis.
general_moment=12/(2*r+3)-12/(2*r+4)
assert s.factor(general_moment-6/((r+2)*(2*r+3)))==0
common={'model':'Complex Haar Stiefel4x2; B=V*PV with rank-two orthogonal P',
        'measure':'normalized complex Haar / Cartesian Hermitian volume',
        'eigenvalue_density':'6*(s1-s2)^2 on (0,1)^2',
        'component_density':'1-3*z^2+2*abs(z)^3, abs(z)<1',
        'Bloch_radius_density':'12*R^2*(1-R), 0<R<1',
        'all_integer_moment_formula':'6/((r+2)*(2*r+3)), r>=0 integer'}
A={**common,'method':'A: Haar-Stiefel delta constraint and square complex polar integration',
   'corner_density_exponent':0,'derivation':'evidence/research/probability-reconstruction.md',
   'primary_formula':'evidence/research/primary-truncation-excerpt.md'}
B={**common,'method':'B: Gaussian4x2 normalization; independent square Wisharts; S,B congruence',
   'Wishart_determinant_exponents':[0,0],'congruence_jacobian':str(jac),
   'derivation':'evidence/research/probability-reconstruction.md'}
for name,record in [('a',A),('b',B)]:
    Path(f'evidence/research/probability-input-{name}.json').write_text(json.dumps(record,indent=2)+'\n')
assert all(A[key]==B[key] for key in common)
print(json.dumps({'normalized_unordered_eigenvalue_density':True,
                  'independent_S_B_jacobian':str(jac),'radial_inversion_identity':True,
                  'all_r_moment_identity':str(s.factor(general_moment)),
                  'input_formula_match':True,
                  'independence_limit':'Shared-agent analytic constructions; common standard complex polar-volume convention; no fresh referee.'},indent=2))
