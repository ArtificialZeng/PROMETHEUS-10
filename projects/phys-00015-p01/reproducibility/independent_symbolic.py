"""Fresh exact replay in linear flow/probability coordinates; no discovery imports."""
import json, time
from pathlib import Path
import sympy as s

t,v,L=s.symbols('t v L', real=True)
I=s.I
g=(1-t)/(2*t)
z=(1+I*t)/(1-I*t)
w=(1+I*v)/(1-I*v)
def clean(q):
    return s.cancel(q)
def sym(q):
    return clean((g+1)*(q-1)+g*(1/q-1))
b=2*t/(1+t*t)
sr=clean(z+1/z-2)
lz=sym(z)
def ri(q):
    qc=q.xreplace({I:-I})
    return clean((q+qc)/2),clean((q-qc)/(2*I))
def constrained(l2,hh):
    re,im=ri(l2)
    r2=clean(-(re+im)/sr)
    affinity2=clean((2*g+1)/(g+1)**2*hh-r2/(g*(g+1)))
    return clean(affinity2/b-L*im/b**2)
def generic(H,P,phase=0):
    hc={1:s.Rational(1,2)*H,-1:s.Rational(1,2)*H}
    pc=({1:P/2,-1:P/2} if not phase else {1:-I*P/2,-1:I*P/2})
    pp=clean(2*pc[1]*pc[-1])
    hp=clean(hc[1]*pc[-1]+hc[-1]*pc[1])
    hpp=clean(hc[1]/w*pc[-1]+hc[-1]*w*pc[1])
    l2=clean(2*(lz*pp-g*(z-1)*hp-g*(1/z-1)*hpp))
    for delta in [1,-1]:
        q=clean(z*w**delta)
        out=clean(g*((z-1)+(1/z-1)*w**(-delta))*hc[delta]-lz*pc[delta])
        back=clean(g*((q-1)+(1/q-1)*w**delta)*hc[-delta]-sym(q)*pc[-delta])
        l2=clean(l2+2*out*back/(lz-sym(q)))
    return constrained(l2,s.Rational(1,2)*H**2)

x=t*t
S=L*(1-x)**2+2*t*(1+x)
Dp=(1-x)**2*(v+2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
Dm=(1-x)**2*(v-2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
D=Dp*Dm
Ph=2*t*t*(1+x)*(L*(1-x)**2*(3*x-1)+2*t*(1+x)**2)+(v*v-t*t)*(5*x*x-2*x+1)*S
Pc=L*t*t*(3-x)*(1-x)*(1+x)-2*t**3*(x*x-6*x+1)+v*v*(L*(1-x)*(1+x)*(3*x-1)+2*t*(7*x*x-2*x-1))
Pd=2*t*t*(1+x)*(4*t*t*(1+x)-L*L*(1-x)**3)+(v*v-t*t)*S*S
claimed_hh=t*(1+x)*(1+v*v)*Ph/((1+t)**2*D)
claimed_pp=(1+t)/(1-t)*claimed_hh
claimed_hc=-t*(1+x)**2*Pc/((1+t)*D)
claimed_hs=v*claimed_hc
claimed_det=t*t*(1+x)**2*(1+v*v)*Pd/((1-t)*(1+t)**3*D)

checks=[]
def check(name,actual,expected):
    residual=clean(actual-expected)
    ok=residual==0
    checks.append({'name':name,'exact_zero':ok,'residual':str(residual)})
    print(json.dumps(checks[-1]),flush=True)
    if not ok:
        raise AssertionError(name)
start=time.monotonic()
hh=generic(s.Integer(1),s.Integer(0))
check('generic hh, independently linearized rates',hh,claimed_hh)
pp=generic(s.Integer(0),s.Integer(1))
check('generic pp, independently linearized rates',pp,claimed_pp)
hc=clean((generic(s.Integer(1),s.Integer(1))-hh-pp)/2)
check('cosine cross coefficient',hc,claimed_hc)
hs=clean((generic(s.Integer(1),s.Integer(1),phase=1)-hh-pp)/2)
check('cosine-sine cross coefficient and orientation',hs,claimed_hs)
check('Schur determinant factorization',hh*pp-hc*hc-hs*hs,claimed_det)

def nyquist(H,P):
    q=-z
    out=clean(g*((z-1)-(1/z-1))*H-lz*P)
    back=clean(g*((q-1)-(1/q-1))*H-sym(q)*P)
    direct=clean(2*(lz*P*P-g*(z-1)*H*P+g*(1/z-1)*H*P))
    return constrained(clean(direct+2*out*back/(lz-sym(q))),H*H)
ny_hh=nyquist(s.Integer(1),s.Integer(0))
ny_pp=nyquist(s.Integer(0),s.Integer(1))
ny_hc=clean((nyquist(s.Integer(1),s.Integer(1))-ny_hh-ny_pp)/2)
claimed_ny_hh=2*t*(1+x)*S/((1+t)**2*(5*x*x-2*x+1))
check('Nyquist direct single-alias hh',ny_hh,claimed_ny_hh)
check('Nyquist direct single-alias pp',ny_pp,(1+t)/(1-t)*claimed_ny_hh)
check('Nyquist mixed coefficient vanishes',ny_hc,0)
out={'status':'pass','method':'Linear stationary flows/probabilities; exact rational Fourier-transfer resolvent; single-alias Nyquist calculation','symbols':'Rational identities in t,v,L; t and v real; no numerical substitution used','checks':checks,'elapsed_seconds':time.monotonic()-start}
Path('evidence/independent-symbolic-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass','exact_checks':len(checks),'elapsed_seconds':out['elapsed_seconds']}),flush=True)
