"""Exact symbolic checks and direct principal-minor checks of physical dual witnesses.

Run with the pre-existing research Python. No SDP results are used by this checker.
"""
from pathlib import Path
from itertools import combinations
import json, hashlib
import sympy as S
ROOT=Path(__file__).resolve().parent.parent
p=S.symbols('p',real=True)
m=1-3*p+3*p*p
q=m/p
r=(2*p-1)/(1-p)
h2=(m-(2*q-1)**2)/4
x2=r*r*h2/(1-q)**2
L=(1+x2)/r
R=(2*q-1)/(1-q)+2*r*h2/(1-q)**2
D=S.factor(R-L)
target=p**3*(8*m-3)/(4*(1-p)**2*(2*p-1)*(3*p-1)**2)
assert S.factor(D-target)==0
print('D identity PASS:',D)
assert S.factor(q-1-(p-1)*(3*p-1)/p)==0
assert S.factor(h2+(1-m)/4-q*(1-q))==0
assert S.factor(p**2+(1-p)**2-p*(1-p)-m)==0
print('Normalization and all overlap-modulus identities PASS (orbit, cross, final pair).')
V=(L+R)/2
eta=r*D/(4*(1+r))
A=1+V+eta
C1=p*V*V/(1-p)**2
C2=x2/(1-q)+(q+2*r*h2/(1-q))/(1-q)**2
step=eta/(2*(C1+C2+1))
assert S.factor(p*V/(1-p)-x2-A-(r*D/2-eta))==0
assert S.factor((q+2*r*h2/(1-q))/(1-q)-A-(D/2-eta))==0
print('Both zero-step Schur slack identities PASS.')
t=S.symbols('t',positive=True)
assert S.factor(p*V/(1-p)-p*V/(1-p+t*V)-t*p*V*V/((1-p)*(1-p+t*V)))==0
assert S.factor((q+2*r*h2/(1-q))/(1-q)-(q+2*r*h2/(1-q)-t*x2)/(1-q+t)-t*((q+2*r*h2/(1-q))/(1-q)+x2)/(1-q+t))==0
print('Both finite-step loss identities PASS; analytic bounds are in proof.')

rows=[]
omega=(-1+S.sqrt(3)*S.I)/2
for pp in [S.Rational(71,100),S.Rational(705,1000),S.Rational(7042,10000)]:
    sub=lambda f:S.factor(f.subs(p,pp))
    mm,qq,hh2,rr,vv,ee,aa,ss=map(sub,[m,q,h2,r,V,eta,A,step])
    hh=S.sqrt(hh2); kk=S.sqrt((1-mm)/4)
    xx=rr*hh/(1-qq)
    states=[S.Matrix([S.sqrt(pp),0,S.sqrt(1-pp)*omega**j]) for j in range(3)]
    states += [S.Matrix([S.sqrt(qq),(hh+sgn*S.I*kk)/S.sqrt(qq),0]) for sgn in [1,-1]]
    Y=ss*S.Matrix([[aa,xx,0],[xx,-1,0],[0,0,-vv]])
    assert S.simplify(S.trace(Y)-ss*ee)==0 and ss*ee>0
    mins=[]
    for j,psi in enumerate(states):
        assert S.simplify((psi.H*psi)[0]-1)==0
        B=(psi*psi.H-Y).applyfunc(S.simplify)
        minors=[]
        for k in range(1,4):
            for inds in combinations(range(3),k):
                z=S.simplify(S.expand_complex(B.extract(inds,inds).det()))
                assert z.is_positive is True,(pp,j,inds,z)
                minors.append(str(z))
        mins.append(minors)
    for i,j in combinations(range(5),2):
        aij=S.simplify((states[i].H*states[j])[0])
        assert S.simplify(S.expand_complex(aij*S.conjugate(aij))-mm)==0
    row={'p':str(pp),'squared_overlap':str(mm),'step':str(ss),'eta':str(ee),
         'trace_Y':str(ss*ee),'uniform_prior_error_lower_bound':str(ss*ee/5),
         'positive_principal_minors_by_state':mins}
    rows.append(row)
    print('Direct exact 3x3 test PASS: p=',pp,'m=',mm,'35 principal minors positive; 10 overlaps equal; Tr(Y)>0.')
out={'mode':'exact','sympy_version':S.__version__,'source_sha256':hashlib.sha256((ROOT/'source.md').read_bytes()).hexdigest(),
     'scope':'Three exact interior checks support, but do not replace, the all-parameter analytic proof.',
     'points':rows}
(ROOT/'evidence/five-state-exact-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print('Original source SHA256:',out['source_sha256'])
