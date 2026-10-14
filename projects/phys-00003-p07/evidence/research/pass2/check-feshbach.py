"""Same-agent independent arithmetic replay; not independent referee acceptance.
Determinant uses path matchings and Fraction polynomials, not Sympy recurrence.
Pointwise full-operator checks use exact rational Sturm and Fraction LDL.
"""
from fractions import Fraction as F
import json,itertools,math
from pathlib import Path
BASE=Path(__file__).resolve().parent
def count(N,g,D,x,correction=F(0)):
    # Integer determinant sequence of the head, rational edge squares.
    Q=math.lcm(g.denominator,D.denominator,x.denominator)
    gp=int(g*g*Q*Q);xp=int(x*Q);dp=int(D*Q)
    prev=1;prior=0;lastsign=1;negative=0
    for n in range(N):
        q=n*Q+(-1)**n*dp-xp
        if n==N-1:
            d=correction.denominator;r=correction.numerator
            nxt=(q*d-Q*r)*prev-n*gp*d*prior
        else:nxt=q*prev-n*gp*prior
        if nxt:
            sign=1 if nxt>0 else -1
            negative+=sign!=lastsign;lastsign=sign
        elif n==N-1:raise ArithmeticError('zero endpoint determinant')
        prior,prev=prev,nxt
    return negative

def count_bounds(N,g,D,parity,x):
    assert parity==1
    b=F(3,4)*N-abs(D)-F(1,8)-4*g*g
    assert b>x
    corr=N*g*g/(b-x)
    lower=count(N,g,D,x);upper=count(N,g,D,x,corr)
    return {'x':str(x),'tail_lower_bound':str(b),'schur_correction_upper':str(corr),
            'count_lower':lower,'count_upper':upper}


def add(a,b):
 o=a.copy()
 for k,v in b.items():o[k]=o.get(k,F(0))+v
 return {k:v for k,v in o.items() if v}
def mul(a,b):
 o={}
 for (j,k),v in a.items():
  for (l,m),w in b.items():o[(j+l,k+m)]=o.get((j+l,k+m),F(0))+v*w
 return {k:v for k,v in o.items() if v}
def diag(n):
 # independent transcription with c=u-5/64
 s=(-1)**n
 return {(0,0):F(n)+F(5,2)*(s-1),(0,1):1-s*F(5,4),(1,2):F(s),(0,2):-s*F(5,64)}
p={};matchings=0
for mask in range(1<<7):
 if mask&(mask<<1):continue
 used=set();term={(0,0):F(1)}
 for e in range(7):
  if mask>>e&1:used|={e,e+1};term=mul(term,{(0,1):F(-(e+1))})
 for n in range(8):
  if n not in used:term=mul(term,diag(n))
 p=add(p,term);matchings+=1
assert all(k>=4 for j,k in p)
p={(j,k-4):v for (j,k),v in p.items()}
r=json.loads((BASE/'feshbach-bounds.json').read_text())
ref={(v['u_degree'],v['t_degree']):F(v['coefficient']) for v in r['uniform_window']['det_A8_div_t4_shifted_terms']}
assert p==ref
T=F(1,100);U=F(69,64);A=F(768);B=F(0);C=F(45,2)
for (j,k),v in p.items():
 if j>=2 and (j,k)!=(2,0):A-=abs(v)*T**k*U**(j-2)
 elif j==1:
  assert k>=1;B+=abs(v)*T**(k-1)
 elif j==0 and k>=2:C-=abs(v)*T**(k-1)
assert A>764 and B<120 and C>22
assert A==F(r['uniform_window']['A']) and B==F(r['uniform_window']['B']) and C==F(r['uniform_window']['C'])
assert F(120)**2*T/(4*764)<22
assert F(3,25)+F(11,10)*(F(11,64)+F(3,250))==F(128905,400000)<F(1,3)
# Rational enclosure of sqrt120; squared checks exact
sqrtlo=F(109544511501033,10**13);sqrthi=F(109544511501034,10**13)
assert sqrtlo**2<120<sqrthi**2
kaplo=sqrtlo/64;kaphi=sqrthi/64

def ldl(N,g,D,x,corr):
 neg=0;p=None
 for n in range(N):
  q=F(n)+(-1)**n*D-x-(corr if n==N-1 else 0)
  if n:q-=n*g*g/p
  assert q
  neg+=q<0;p=q
 return neg
cases=[]
for g in [F(1,10),F(1,20),F(1,50),F(1,100)]:
 t=g*g;D=F(5,2)-F(5,4)*t-F(5,64)*t*t;x=F(5,2)-t;R=g**6/3
 endpoints=[x-kaphi*g**5-R,x-kaplo*g**5+R,x+kaplo*g**5-R,x+kaphi*g**5+R]
 expected=[2,3,3,4];results=[]
 for e,want in zip(endpoints,expected):
  v=count_bounds(80,g,D,1,e)
  assert v['count_lower']==v['count_upper']==want
  corr=F(v['schur_correction_upper'])
  assert ldl(80,g,D,e,F(0))==ldl(80,g,D,e,corr)==want
  results.append(v)
 cases.append({'g':str(g),'Delta':str(D),'endpoints':results,'expected_counts':expected})
# Uniform-window boundaries and its cancellation center: exact counts at target
windows=[]
for g,c in itertools.product([F(1,10),F(1,20),F(1,100)],[F(-1),F(1),F(-5,64),F(0)]):
 D=F(5,2)-F(5,4)*g*g+c*g**4;x=F(5,2)-g*g
 v=count_bounds(80,g,D,1,x)
 assert v['count_lower']==v['count_upper']==3
 windows.append({'g':str(g),'c':str(c),'Delta':str(D),'count_at_target':v})
output={'status':'same_agent_checks_pass','matching_terms':matchings,'polynomial_coefficients':len(p),'matching_polynomial_equals_recurrence':True,'uniform_sign_arithmetic_pass':True,
 'rational_sqrt120':[str(sqrtlo),str(sqrthi)],'tuned_curve_exact_endpoint_cases':cases,'window_endpoint_cases':windows,
 'limitations':'Finite samples are consistency tests only. The uniform result uses the analytic derivation and exact coefficient estimates. Not fresh referee acceptance.'}
(BASE/'feshbach-replay.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'matching_terms':matchings,'polynomial_coefficients':len(p),'certified_tuned_endpoints':16,'window_counts':len(windows),'alternative_ldl_checks':32,'all_checks_pass':True},indent=2))
