#!/usr/bin/env python3
"""Exact symbolic and finite-Gibbs checks. No scientific file/cache reads.

Source transcription: preprint Eq. (1), local sum p.5, Eq. (12) p.6.
Independent central route: two different variables a,b, antisymmetric and
symmetric compatibility equations; derive their sum and product without
composing or dividing the original rational map.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import argparse
import datetime
import hashlib
import json
import platform
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='reproducibility/outputs')
args = parser.parse_args()
OUT = (ROOT / args.output_dir).resolve()
if not OUT.is_relative_to(ROOT) or OUT == ROOT:
    raise SystemExit('Output must be a subdirectory of the project.')
if sys.flags.optimize:
    raise SystemExit('Assertions are required; do not run Python with -O.')
OUT.mkdir(parents=True, exist_ok=True)
checks = []
def check(name, condition, detail=None):
    assert bool(condition), name
    checks.append({"name": name, "status": "pass", "detail": detail})
    print("PASS", name, flush=True)
def identical(name, lhs, rhs):
    check(name, sp.expand(lhs-rhs) == 0)
def positive_coefficients(name, expr, *gens):
    pp = sp.Poly(sp.expand(expr), *gens)
    check(name, all(c > 0 for c in pp.coeffs()), {"nonzero_monomials":len(pp.terms())})
    return [{"powers":list(m), "coefficient":str(c)} for m,c in pp.terms()]

t,h,u,v,a,b = sp.symbols("t h u v a b", positive=True)
z = sp.Matrix([1,u,v])
# Matrix representation transcribed from physical pair factors.
sibling = sp.Matrix([[1,h,h**2],[h,1,h],[h**2,h,1]])
parent = sp.Matrix([[1,t,t**2],[t,1,t],[t**2,t,1]])
local = []
weights = []
for i in range(3):
    q = sp.diag(*list(parent.row(i))) * sibling * sp.diag(*list(parent.row(i)))
    direct = 0
    for j,k in product(range(3), repeat=2):
        w = t**(abs(i-j)+abs(i-k))*h**abs(j-k)
        identical("local weight %d%d%d"%(i,j,k), q[j,k], w)
        weights.append({"parent":i,"left":j,"right":k,
                        "exponents_t_h":[abs(i-j)+abs(i-k),abs(j-k)]})
        direct += w*z[j]*z[k]
    expr = sp.expand((z.T*q*z)[0])
    identical("matrix and spin sum component %d"%i, expr, direct)
    local.append(expr)
identical("reflection plane invariant", local[2].subs(v,1), local[0].subs(v,1))
N = sp.expand(local[1].subs(v,1))
D = sp.expand(local[0].subs(v,1))
N_printed = u**2+4*t*h*u+2*t**2*(h**2+1)
D_printed = t**2*u**2+2*t*h*(t**2+1)*u+t**4+2*t**2*h**2+1
identical("rendered source numerator", N, N_printed)
identical("rendered source denominator", D, D_printed)
positive_coefficients("N positive at all positive inputs",N,t,h,u)
positive_coefficients("D positive at all positive inputs",D,t,h,u)
for i in range(3):
    identical("nearest-neighbor h=1 factorization component %d"%i,
              local[i].subs(h,1), (parent.row(i).dot(z))**2)
identical("zero nearest-neighbor coupling t=1 gives f=1",N.subs(t,1),D.subs(t,1))
identical("nearest-neighbor scalar baseline",
          N.subs(h,1)*(t*u+t**2+1)**2,
          D.subs(h,1)*(u+2*t)**2)

n2,n1,n0 = [sp.expand(N).coeff(u,j) for j in [2,1,0]]
d2,d1,d0 = [sp.expand(D).coeff(u,j) for j in [2,1,0]]
identical("n2=1",n2,1)
identical("d2=t^2",d2,t**2)
Fab = sp.expand(a*D.subs(u,b)-N.subs(u,b))
Fba = sp.expand(b*D.subs(u,a)-N.subs(u,a))
L = d0+n1
anti = sp.expand(L+a+b-t**2*a*b)
identical("antisymmetric two-cycle identity",Fab-Fba,(a-b)*anti)
reduced_sum = 2*(d0*(a+b)+(d1+1)*a*b-n0)
identical("symmetric two-cycle identity",Fab+Fba+(a+b)*anti,reduced_sum)
# If a!=b is a cycle, anti=0. Write s=a+b,p=ab.
# t^2*p=s+L, d0*s+(d1+1)*p=n0.
A = sp.expand(t**2*d0+d1+1)
B = sp.expand((d1+1)*L-t**2*n0)
C = sp.expand(d0*L+n0)
identical("linear system yields p=C/A",A*L-B,t**2*C)
A_submitted = t**6+2*t**4*h**2+2*t**3*h+t**2+2*t*h+1
B_submitted = (2*t**7*h+4*t**5*h**3+2*t**5*h+6*t**4*h**2+
               4*t**3*h**3-t**4+2*t**3*h+10*t**2*h**2+6*t*h+1)
C_submitted = (t**8+4*t**6*h**2+4*t**4*h**4+4*t**5*h+8*t**3*h**3+
               2*t**4+6*t**2*h**2+2*t**2+4*t*h+1)
identical("independently derived A equals submitted A",A,A_submitted)
identical("independently derived B equals submitted B",B,B_submitted)
identical("independently derived C equals submitted C",C,C_submitted)
positive_coefficients("strict bound A>t^6",A-t**6,t,h)
positive_coefficients("strict bound C>t^8",C-t**8,t,h)
positive_coefficients("strict bound B>1-t^4",B-(1-t**4),t,h)
# The remaining logical inequalities use only real order:
# s>0 -> B<0 -> t>1; 0<-B<t^4-1.
# Then B^2<(t^4-1)^2<t^8<4*t^14<4*A*C.
# But a,b real imply A^2*(a-b)^2=B^2-4*A*C >=0, contradiction.
Q = A*u**2+B*u+C
square = t**2*(t**2*u-sp.Rational(1,2))**2
remainder = sp.expand(Q-square)
remainder_terms = positive_coefficients("submitted square remainder has positive coefficients",
                                        remainder,t,h,u)
check("square remainder has constant 1",remainder.subs({t:0,h:0,u:0}) == 1)
check("square remainder has 24 monomials",len(remainder_terms)==24)
# Secondary audit of the author's composition identity: Q here was derived
# from the independent a,b route, not extracted by polynomial division.
E = sp.expand(d2*N**2+d1*N*D+d0*D**2)
H = sp.expand(n2*N**2+n1*N*D+n0*D**2-u*E)
identical("full homogeneous composition identity",H,(N-u*D)*Q)
positive_coefficients("composition denominator is positive",E,t,h,u)
identical("published diagonal excluded baseline",Q.subs({t:2,h:2}),
          237*u**2+2505*u+3225)
identical("off-diagonal transcription discriminator",Q.subs({t:2,h:3}),
          417*u**2+6573*u+10137)
identical("diagonal B has a manifest positive expression",
          B.subs(h,t),6*t**8+12*t**6+11*t**4+6*t**2+1)

# Fresh exact parameter attacks; not used as the all-parameter proof.
diagnostics=[]
for tt,hh in [(sp.Rational(3,2),sp.Rational(1,1000)),
              (sp.Rational(7),sp.Rational(1,10**8)),
              (sp.Rational(1,1000),sp.Rational(1000)),
              (sp.Rational(1),sp.Rational(11,13)),
              (sp.Rational(2),sp.Rational(2))]:
    aa,bb,cc=[x.subs({t:tt,h:hh}) for x in [A,B,C]]
    delta=bb**2-4*aa*cc
    if bb<0:
        check("negative-B strict chain at t=%s h=%s"%(tt,hh),
              bb**2<(tt**4-1)**2<tt**8<4*tt**14<4*aa*cc)
    for uu in [sp.Rational(1,10**5),sp.Rational(5,7),sp.Rational(10**5)]:
        check("Q>1 exact attack t=%s h=%s u=%s"%(tt,hh,uu),
              Q.subs({t:tt,h:hh,u:uu})>1)
    diagnostics.append({"t":str(tt),"h":str(hh),"A":str(aa),"B":str(bb),
                        "C":str(cc),"discriminant":str(delta)})
check("retained B-positive Delta-positive control",
      any(sp.Rational(x["B"])>0 and sp.Rational(x["discriminant"])>0
          for x in diagnostics))

# Independent standard-library rational finite-cylinder calculation.
tf,hf = F(3,2),F(2,5)
def psi(i,j,k):
    return tf**(abs(i-j)+abs(i-k))*hf**abs(j-k)
def update(m):
    return [sum((psi(i,j,k)*m[j]*m[k] for j,k in product(range(3),repeat=2)),F(0))
            for i in range(3)]
def normalize(m):
    return [x/m[0] for x in m]
m2=[F(1),F(5,7),F(1)]
m1=normalize(update(m2))
m0=normalize(update(m1))
lambda1=update(m2)[0]
lambda0=update(m1)[0]
def kernel(i,j,k,child,current,lam):
    return psi(i,j,k)*child[j]*child[k]/(lam*current[i])
for i in range(3):
    check("level-0 kernel normalized parent=%d"%i,
          sum((kernel(i,j,k,m1,m0,lambda0) for j,k in product(range(3),repeat=2)),F(0))==1)
    check("level-1 kernel normalized parent=%d"%i,
          sum((kernel(i,j,k,m2,m1,lambda1) for j,k in product(range(3),repeat=2)),F(0))==1)
cylinders={}
unnormalized={}
for x in product(range(3),repeat=7):
    p=(m0[x[0]]/sum(m0)*
       kernel(x[0],x[1],x[2],m1,m0,lambda0)*
       kernel(x[1],x[3],x[4],m2,m1,lambda1)*
       kernel(x[2],x[5],x[6],m2,m1,lambda1))
    w=psi(x[0],x[1],x[2])*psi(x[1],x[3],x[4])*psi(x[2],x[5],x[6])
    for leaf in range(3,7):
        w*=m2[x[leaf]]
    cylinders[x]=p
    unnormalized[x]=w
partition=sum(unnormalized.values())
check("2187 finite-cylinder probabilities normalized",sum(cylinders.values())==1)
check("2187 cylinders equal direct Hamiltonian weights",
      all(cylinders[x]==w/partition for x,w in unnormalized.items()))
for x3 in product(range(3),repeat=3):
    marginal=sum((p for x,p in cylinders.items() if x[:3]==x3),F(0))
    lower=(m0[x3[0]]/sum(m0))*kernel(*x3,m1,m0,lambda0)
    assert marginal==lower
check("all 27 first-generation marginals project consistently",True)
# Check internal-site DLR specification for every exterior spin assignment.
# Node 1 has neighbors 0,2(sibling),3,4. Node 2 is outside the volume.
for outer in product(range(3),repeat=6):
    r,s,l1,l2,r1,r2=outer
    probabilities=[cylinders[(r,i,s,l1,l2,r1,r2)] for i in range(3)]
    energies=[tf**(abs(i-r)+abs(i-l1)+abs(i-l2))*hf**abs(i-s)
              for i in range(3)]
    ptotal,etotal=sum(probabilities),sum(energies)
    assert all(probabilities[i]*etotal==energies[i]*ptotal for i in range(3))
check("729 internal-site DLR conditionals retain crossing sibling bond",True)

results={
 "schema":1,"status":"pass",
 "independence":"Two-variable sum/product elimination and Hamiltonian matrix reconstruction, separate from the integer composition checker. This is the packaged replay of a previously constructed check, not a new independent review.",
 "created_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "environment":{"python":sys.version,"sympy":sp.__version__,"platform":platform.platform()},
 "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 "arithmetic":"exact integers/rationals and exact symbolic polynomial identities; no floating point",
 "checks":checks,"check_count":len(checks),
 "source_reconstruction":{"weights":weights,"full_update":[str(x) for x in local],"N":str(N),"D":str(D)},
 "independent_cycle_reduction":{
    "antisymmetric_factor":str(anti),
    "symmetric_reduction":str(reduced_sum),
    "A":str(A),"B":str(B),"C":str(C),
    "necessary_relations":["a+b=-B/A","a*b=C/A","A^2*(a-b)^2=B^2-4*A*C"],
    "contradiction":"If a,b>0 and a!=b form a cycle, then B<0, t>1 and B^2<(t^4-1)^2<t^8<4*t^14<4*A*C, contradicting real a,b.",
    "denominators":"D(a),D(b),A,t^2 are positive. Division by a-b is only after assuming a!=b."
 },
 "secondary_submitted_certificate":{"square":str(square),"positive_remainder":str(remainder),
                                     "positive_remainder_terms":remainder_terms},
 "diagnostic_cases":diagnostics,
 "finite_cylinder_check":{"vertices":7,"configurations":2187,"lower_marginals":27,
                          "internal_DLR_exteriors":729,"t":str(tf),"h":str(hf),
                          "terminal_message":[str(x) for x in m2],
                          "scope":"Exact finite sanity check; infinite DLR conclusion rests on the analytic telescoping argument in the article."}
}
(OUT/"symbolic-check.json").write_text(json.dumps(results,indent=2)+"\n")
print("RESULT",json.dumps({"status":"pass","checks":len(checks),"file":str((OUT/"symbolic-check.json").relative_to(ROOT))}),flush=True)
