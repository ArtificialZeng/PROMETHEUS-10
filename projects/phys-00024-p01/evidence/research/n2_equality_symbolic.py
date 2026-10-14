#!/usr/bin/env python3
"""Independent symbolic deficit determinant in a complete 2x2 canonical form."""
import json
import sympy as sp

r,h,x,t,z=sp.symbols('r h x t z', real=True)
s=sp.sqrt(10)
c=sp.symbols('c', real=True)
A=sp.Matrix([[r+sp.I*h+x,t],[-t,r+sp.I*h-x]])
P=sp.kronecker_product(A.T,sp.eye(2))
Q=sp.kronecker_product(sp.eye(2),A)
H=P.conjugate().T*P+sp.Rational(1,2)*Q.conjugate().T*Q-sp.Rational(3,4)*(P.conjugate().T*Q+Q.conjugate().T*P)
N=2*(r*r+h*h+x*x+t*t)
deficit=c*N*sp.eye(4)-H
print('canonical_A =',A,flush=True)
det=sp.expand(deficit.det(method='domain-ge'))
print('generic_c_determinant_computed',flush=True)
det=sp.expand(det.subs(c,(3+s)/4))
Phi=(19+6*s)*(r+sp.I*h)**2-(x*x-t*t)
predicted=sp.expand(N*N*Phi*sp.conjugate(Phi)/64)
residual=sp.expand(det-predicted)
assert residual==0
print('exact_determinant_identity_residual =',residual)
print('deficit_determinant = N^2 |det(A)+(3/2)(3+sqrt(10))tr(A)^2|^2 / 64')
print('canonical_Phi =',Phi)
print('determinant_at_nilpotent =',sp.simplify(det.subs({h:0,r:0,t:x})))
