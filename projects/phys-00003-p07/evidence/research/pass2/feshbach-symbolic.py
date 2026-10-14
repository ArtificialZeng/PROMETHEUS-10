"""Exact rational proposer bounds for the m=2 tuned Rabi doublet.
No cached spectra are inputs. Sympy used for polynomial algebra only.
"""
import sympy as S
import json
from pathlib import Path
T=S.Rational(1,100);t,c,u=S.symbols('t c u')
D=S.Rational(5,2)-S.Rational(5,4)*t+c*t*t;x=S.Rational(5,2)-t
q=lambda n:n+(-1)**n*D-x
p0=S.Integer(1);p1=S.Integer(0)
for n in range(8):p1,p0=p0,S.expand(q(n)*p0-n*t*p1)
poly=S.Poly(S.expand((p0/t**4).subs(c,u-S.Rational(5,64))),u,t)
A=S.Rational(768);B=S.Integer(0);C=S.Rational(45,2)
for (j,k),v in poly.terms():
 if j>=2 and (j,k)!=(2,0):A-=abs(v)*T**k*S.Rational(69,64)**(j-2)
 elif j==1:B+=abs(v)*T**(k-1)
 elif j==0 and k>=2:C-=abs(v)*T**(k-1)
assert A>764 and B<120 and C>22
assert C-B*B*T/(4*A)>22
# tuned Feshbach on sites 0,5; complement middle1..4 and tail6..
D=D.subs(c,-S.Rational(5,64))
q=lambda n:n+(-1)**n*D-x
pm0=S.Integer(1);pm1=S.Integer(0)
for n in range(1,5):pm1,pm0=pm0,S.expand(q(n)*pm0-n*t*pm1) if n>1 else q(n)
Mdet=pm0
r=1/q(4)
for n in [3,2,1]:r=1/(q(n)-(n+1)*t*r)
a=S.cancel(D-x-t*r)
r=1/q(1)
for n in [2,3,4]:r=1/(q(n)-n*t*r)
# tail lower/upper through index9; 9.. infinity positive via quadratic form bound
b9=S.Rational(15,16)*9-D-S.Rational(1,32)-16*t
rtlo=1/q(8);rthi=1/(q(8)-9*t/(b9-x))
for n in [7,6]:
 rtlo=1/(q(n)-(n+1)*t*rtlo)
 rthi=1/(q(n)-(n+1)*t*rthi)
bupper=S.cancel(5-D-x-5*t*r-6*t*rtlo)
blower=S.cancel(5-D-x-5*t*r-6*t*rthi)
def ratbound(f):
 num,den=map(lambda z:S.Poly(z,t),S.fraction(S.cancel(f)))
 if den.eval(0)<0:num=-num;den=-den
 lo=den.eval(0)-sum(abs(v)*T**k for (k,),v in den.terms() if k)
 assert lo>0
 ub=sum(abs(v)*T**k for (k,),v in num.terms())/lo
 return S.factor(ub)
ka=ratbound(a/t**3);kb1=ratbound(bupper/t**3);kb2=ratbound(blower/t**3)
# normalized offdiag difference: sqrt120*t^(5/2)*(1/Mdet-1/64)
kd=ratbound((1/Mdet-S.Rational(1,64))/t)
assert ka<S.Rational(1,10) and kb1<S.Rational(1,10) and kb2<S.Rational(1,10)
assert 11*kd<S.Rational(1,5) # sqrt120<11
out={'parameters':{'omega':'1','t':'g^2','g_range':'0<g<=1/10','Delta_tuned':'5/2-(5/4)g^2-(5/64)g^4'},
 'uniform_window':{'Delta':'5/2-(5/4)g^2+c*g^4','c_range':'[-1,1]','det_A8_div_t4_shifted_terms':[{'u_degree':j,'t_degree':k,'coefficient':str(v)} for (j,k),v in poly.terms()],
 'A':str(A),'B':str(B),'C':str(C),'completed_square_margin':str(C-B*B*T/(4*A)),'simple_bounds':'A>764,B<120,C>22; P<=-764u^2+120t|u|-22t<0'},
 'tuned':{'middle_determinant':str(Mdet),'a':str(a),'b_lower':str(blower),'b_upper':str(bupper),
 'a_div_g6_abs_upper':str(ka),'b_upper_div_g6_abs_upper':str(kb1),'b_lower_div_g6_abs_upper':str(kb2),'offdiag_error_div_g7_abs_upper_using_sqrt120_lt11':str(11*kd),
 'simple_bounds':'diagonal abs<=g^6/10; offdiag error<=g^7/5; F(x) error norm<=3g^6/25'},
 'limitations':'Same-agent algebra verification, not fresh referee acceptance. Analytic resolvent and index proofs are in feshbach-derivation.md.'}
path=Path(__file__).with_name('feshbach-bounds.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'A':float(A),'B':float(B),'C':float(C),'a_bound':float(ka),'b_bounds':[float(kb1),float(kb2)],'offdiag_g7_bound':float(11*kd),'all_assertions_pass':True},indent=2))
