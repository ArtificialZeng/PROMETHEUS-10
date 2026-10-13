#!/usr/bin/env python3
"""Packaged exact symbolic replay for the missing-arc manuscript.

The calculation is copied from the accepted independent referee implementation.
Only the CLI, output location, metadata and explanatory header were adapted.
No scientific calculation statement is changed. Reads no input data or caches.
See ../source-map.md for the preserved original and its SHA-256 binding.
"""
import hashlib
import itertools
import json
from pathlib import Path
import argparse
parser = argparse.ArgumentParser(description="Replay exact symbolic identities; reads no input files.")
parser.add_argument("--output-dir", type=Path, default=Path("replay-output"), help="Directory for generated JSON results; relative to the invocation directory")
args = parser.parse_args()
OUTPUT = args.output_dir.resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)

import sympy as S

checks = []
details = {}


def check(name, expr):
    result = S.simplify(expr)
    ok = result == 0
    checks.append({"name": name, "pass": bool(ok), "residual": str(result)})
    print(("PASS " if ok else "FAIL ") + name + ": " + str(result), flush=True)
    if not ok:
        raise AssertionError(name)


def conv(a, b):
    return [S.expand(sum(a[j] * b[k-j] for j in range(k+1))) for k in range(3)]


# Independent source reconstruction: column stochastic return graph.
z, t, d, lam = S.symbols("z t delta lambda", real=True)
P = S.zeros(4)
for j in range(3):
    P[j+1, j] = 1
P[0, 3], P[1, 3] = 1-t, t
check("companion determinant from entries", P.charpoly(z).as_expr().subs(next(iter(P.charpoly(z).as_expr().free_symbols-{t})), z) - (z**4-t*z-(1-t)))
check("companion column conservation", sum((sum(P[:,j])-1)**2 for j in range(4)))
check("companion zero diagonal", S.trace(P))

# Verify the complex arc by reducing powers of its positive square root.
v = S.symbols("v", real=True)
td = 4*d-8*d**2+8*d**3
zd = -d+S.I*v
arc = S.Poly(S.expand(zd**3+zd**2+zd+1-td), v)
arc_reduced = S.rem(arc, S.Poly(v**2-(1-2*d+3*d**2),v)).as_expr()
check("exact companion arc root", arc_reduced)
check("strict separation polynomial", (1-2*d+3*d**2)-(1-d+d**2/2)**2 - (d**2+d**3-d**4/4))
details["arc_parameter_derivative"] = str(S.factor(S.diff(td,d)))

# Source Eq. (1)/S66 uniform ring reconstructed as a row generator.
Q0 = S.zeros(4)
for j in range(4):
    Q0[j,j] = -1
    Q0[j,(j+1)%4] = S.Rational(3,4)
    Q0[j,(j-1)%4] = S.Rational(1,4)
qpoly = Q0.charpoly(lam).as_expr()
qvar = next(iter(qpoly.free_symbols))
qpoly = qpoly.subs(qvar,lam)
check("published ring spectrum", qpoly - lam*(lam+2)*((lam+1)**2+S.Rational(1,4)))
check("stationary ring vector", sum(x*x for x in Q0.T*S.ones(4,1)))
check("ring cycle product ratio", S.Rational(3,4)**4/S.Rational(1,4)**4-81)
details["ring_generator_row_convention"] = [[str(x) for x in row] for row in Q0.tolist()]

# First derivative including every independent escape slack and affinity slack.
c = S.symbols("c0:4", real=True)
uind = S.symbols("u0:3", real=True)
u = list(uind)+[-sum(uind)]
s = S.symbols("s0:4", real=True)
m = S.symbols("m", real=True)
V = S.zeros(4)
for j in range(4):
    V[j,j] = s[j]
    V[j,(j+1)%4] = -S.Rational(3,4)*(c[j]+s[j])+u[j]-S.Rational(3,8)*m
    V[j,(j-1)%4] = -S.Rational(1,4)*(c[j]+s[j])-u[j]+S.Rational(3,8)*m
    V[j,(j+2)%4] = c[j]
l0 = -1+S.I/2
df = -S.trace((l0*S.eye(4)-Q0).adjugate()*V)
l1all = S.expand(-df/S.diff(qpoly,lam).subs(lam,l0)).expand(complex=True)
cb, sb = sum(c)/4, sum(s)/4
check("all-coordinate first real derivative", S.re(l1all)-(-cb+sb))
check("all-coordinate first tangent excess", S.im(l1all)-S.re(l1all)/2+sb+S.Rational(3,4)*m)
details["first_eigenvalue_coefficient"] = str(S.simplify(l1all))

# General chord / mean-zero affinity directions through second order.
# A=Q+I has zero diagonal and row sums 1 when s=m=0.
# Its reduced polynomial is z^3+z^2+(1-P2)z+1-P2-P3,
# where P2 is the sum of reciprocal edge products and P3 the sum
# of the eight oriented simple triangle products. No eigenbasis is used.
A = [[[S.Integer(0)]*3 for k in range(4)] for j in range(4)]
for j in range(4):
    A[j][(j+1)%4] = [S.Rational(3,4),u[j]-S.Rational(3,4)*c[j],-c[j]*u[j]-S.Rational(4,3)*u[j]**2]
    A[j][(j-1)%4] = [S.Rational(1,4),-u[j]-S.Rational(1,4)*c[j],c[j]*u[j]+S.Rational(4,3)*u[j]**2]
    A[j][(j+2)%4] = [S.Integer(0),c[j],S.Integer(0)]
pair = [S.Integer(0)]*3
tri = [S.Integer(0)]*3
for i,j in itertools.combinations(range(4),2):
    p = conv(A[i][j],A[j][i])
    pair = [S.expand(x+y) for x,y in zip(pair,p)]
for i,j,k in itertools.combinations(range(4),3):
    for cyc in [(i,j,k),(i,k,j)]:
        p = conv(conv(A[cyc[0]][cyc[1]],A[cyc[1]][cyc[2]]),A[cyc[2]][cyc[0]])
        tri = [S.expand(x+y) for x,y in zip(tri,p)]
f0 = z**3+z**2+(1-pair[0])*z+1-pair[0]-tri[0]
f1 = -pair[1]*(z+1)-tri[1]
f2 = -pair[2]*(z+1)-tri[2]
z0 = S.I/2
fprime = S.diff(f0,z).subs(z,z0)
z1 = S.expand(-f1.subs(z,z0)/fprime).expand(complex=True)
z2 = S.expand(-(f2.subs(z,z0)+S.diff(f1,z).subs(z,z0)*z1+S.diff(f0,z,2).subs(z,z0)*z1**2/2)/fprime).expand(complex=True)
check("chord first coefficient", z1+cb*(1+S.I/2))
K = S.expand(S.im(z2)-S.re(z2)/2)
H = S.hessian(K,uind)
Hclaimed = S.Matrix([[-S.Rational(14,3),-S.Rational(4,3),-S.Rational(10,3)],[-S.Rational(4,3),-S.Rational(8,3),-S.Rational(4,3)],[-S.Rational(10,3),-S.Rational(4,3),-S.Rational(14,3)]])
check("complete arbitrary-direction Hessian", sum((H-Hclaimed)[i,j]**2 for i in range(3) for j in range(3)))
ustar = S.solve([S.diff(K,x) for x in uind],uind)
uexpect = [(-3*c[0]+6*c[1]+3*c[2]-6*c[3])/40,(-6*c[0]-3*c[1]+6*c[2]+3*c[3])/40,(3*c[0]-6*c[1]-3*c[2]+6*c[3])/40]
check("quadratic optimizer", sum((ustar[x]-y)**2 for x,y in zip(uind,uexpect)))
sp, tp = c[0]+c[2], c[1]+c[3]
dp, ep = (c[0]-c[2])/2, (c[1]-c[3])/2
Kmax = S.factor(K.subs(ustar))
check("quadratic maximum", Kmax-S.Rational(2,5)*(dp**2+ep**2)+S.Rational(5,64)*(sp-tp)**2)
du = S.Matrix([x-ustar[x] for x in uind])
check("full completion of square", K-Kmax-(du.T*H*du)[0]/2)
check("triangle constrained coefficient", S.Rational(2,5)*((sp/4)**2+(tp/4)**2)-S.Rational(5,64)*(sp-tp)**2-((sp+tp)**2/80-S.Rational(21,320)*(sp-tp)**2))
check("normalization of 1/5 coefficient", (sp+tp)**2/80-cb**2/5)
details["quadratic_form_from_characteristic_invariants"] = str(K)
details["real_second_eigenvalue_coefficient"] = str(S.re(z2))
details["imag_second_eigenvalue_coefficient"] = str(S.im(z2))
details["hessian_leading_minors"] = [str(H[:k,:k].det()) for k in range(1,4)]
assert all((-1)**k*H[:k,:k].det()>0 for k in range(1,4))
details["quadratic_optimizer"] = {str(k):str(vv) for k,vv in ustar.items()}
details["quadratic_maximum"] = str(Kmax)

# Independent derivative check of the primary Jensen Hessian at gamma=0,
# sigma=1/2, on 0<v=sin(phi)<=1, 0<r=exp(xi)<2v.
r, vv = S.symbols("r v", positive=True)
J = S.log(r)+S.log(2*r*vv+1)-S.log(2*vv-r)
Jv = S.diff(J,vv)
hxx = S.simplify(r*S.diff(r*S.diff(J,r),r))
hpp = S.simplify((1-vv**2)*S.diff(J,vv,2)-vv*Jv)
hpx_without_cos = S.simplify(r*S.diff(Jv,r))
detH = S.factor(hpp*hxx-(1-vv**2)*hpx_without_cos**2)
N, M = r*vv+S.Rational(1,2), vv/r-S.Rational(1,2)
positive_decomp = (S.Rational(5,4)*vv**2*(S.Rational(1,2)*(r+1/r))**2+S.Rational(1,4)*(1-vv**2)*(S.Rational(1,2)*(r-1/r)-2*vv)**2)/(N**3*M**3)
check("primary strict Jensen Hessian determinant", detH-positive_decomp)
check("primary strict Jensen Hessian trace", hpp+hxx-(r**(-2)/M**2-r**2/N**2))
details["Jensen_determinant"] = str(detH)
details["strictness_argument"] = "N,M>0; v>0 and r>0 make the first numerator summand strictly positive; 1-v^2>=0. Trace>0 follows N/r-M*r=(r+1/r)/2>0. Domain xi<log(2 sin phi) is convex."

out = {"implementation":"Independent characteristic invariants / adjugate / implicit root; no Fourier resolvent, no imported discovery code or cache.","sympy_version":S.__version__,"checks":checks,"all_pass":all(c["pass"] for c in checks),"details":details,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"limitations":"Exact algebra checks are not by themselves the universal nonattainment proof. The analytic uniformity, rigidity, compactness and physical-domain arguments are in the accompanying manuscript."}
(OUTPUT/"symbolic-results.json").write_text(json.dumps(out,indent=2)+"\n")
print("ALL EXACT CHECKS PASSED",flush=True)
