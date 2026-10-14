"""Replay exact factorizations in the analytic sign proof. No numerical sign gate."""
import json
from pathlib import Path
import sympy as s

r=json.loads(Path('evidence/research-symbolic-curvature.json').read_text())
t,v,L=s.symbols('t v L',positive=True,real=True);x=t*t
S=L*(1-x)**2+2*t*(1+x)
Ph1=(5*x*x-2*x+1)*S
Ph=2*t*t*(1+x)*(L*(1-x)**2*(3*x-1)+2*t*(1+x)**2)+(v*v-t*t)*Ph1
Pd=2*t*t*(1+x)*(4*t*t*(1+x)-L*L*(1-x)**3)+(v*v-t*t)*S*S
Dm=(1-x)**2*(v-2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
Dp=(1-x)**2*(v+2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
hh=t*(1+x)*(1+v*v)*Ph/((1+t)**2*Dm*Dp)
det=t*t*(1+x)**2*(1+v*v)*Pd/((1-t)*(1+t)**3*Dm*Dp)
Pc=L*t*t*(3-x)*(1-x)*(1+x)-2*t**3*(x*x-6*x+1)+v*v*(L*(1-x)*(1+x)*(3*x-1)+2*t*(7*x*x-2*x-1))
hc=-t*(1+x)**2*Pc/((1+t)*Dm*Dp)
env={'t':t,'v':v,'L':L}
checks={
 'hh_reduction':s.cancel(hh-s.sympify(r['hh'],locals=env))==0,
 'det_reduction':s.cancel(det-s.sympify(r['det'],locals=env))==0,
 'hc_reduction':s.cancel(hc-s.sympify(r['hc'],locals=env))==0,
 'pp_ratio':s.cancel(s.sympify(r['pp'],locals=env)-(1+t)/(1-t)*hh)==0,
 'cross_phase_ratio':s.cancel(s.sympify(r['hs'],locals=env)-v*s.sympify(r['hc'],locals=env))==0,
 'scalar_lower_bound_difference':s.expand((1+x)**2-(1-x)*(1-3*x)-2*x*(3-x))==0,
 'Ph_slope_positive_polynomial':s.expand(5*x*x-2*x+1-(5*(x-s.Rational(1,5))**2+s.Rational(4,5)))==0,
 'Nyquist_hh':s.cancel(s.limit(hh,v,s.oo)-t*(1+x)*S/(1+t)**2/(5*x*x-2*x+1))==0,
}
# Use these exact identities together with the explicit inequalities in the proof.
# SymPy has not been asked to decide a universal transcendental inequality.
result={'checks':checks,'Ph':str(Ph),'Pd':str(Pd),'S':str(S),'Dminus':str(Dm),'Dplus':str(Dp),
        'method':'rational-function equality over Q(t,v,L); signs proved analytically in evidence/research-local-proof.md',
        'status':'pass' if all(checks.values()) else 'fail'}
Path('evidence/research-curvature-sign-identities.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not all(checks.values()):raise SystemExit(1)
