"""Independent Fraction rational-polynomial construction of Feshbach bounds.
No Sympy, generator imports or cached results. Same-agent checker only.
"""
from fractions import Fraction as F
import json
from pathlib import Path
T=F(1,100)
def plus(a,b):
 o=a.copy()
 for k,v in b.items():o[k]=o.get(k,F(0))+v
 return {k:v for k,v in o.items() if v}
def times(a,b):
 o={}
 for k,v in a.items():
  for l,w in b.items():o[k+l]=o.get(k+l,F(0))+v*w
 return {k:v for k,v in o.items() if v}
class R:
 def __init__(self,a,b=None):
  self.a=a if isinstance(a,dict) else ({0:F(a)} if a else {})
  self.b=b or {0:F(1)}
 def __add__(self,o):
  o=rr(o);return R(plus(times(self.a,o.b),times(o.a,self.b)),times(self.b,o.b))
 __radd__=__add__
 def __neg__(self):return R({k:-v for k,v in self.a.items()},self.b)
 def __sub__(self,o):return self+-rr(o)
 def __rsub__(self,o):return rr(o)+-self
 def __mul__(self,o):
  o=rr(o);return R(times(self.a,o.a),times(self.b,o.b))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=rr(o);assert o.a;return R(times(self.a,o.b),times(self.b,o.a))
 def __rtruediv__(self,o):return rr(o)/self
 def bound_after_dividing_t(self,k):
  assert not any(j<k and v for j,v in self.a.items())
  a={j-k:v for j,v in self.a.items()};b=self.b
  if b[0]<0:a={j:-v for j,v in a.items()};b={j:-v for j,v in b.items()}
  den=b[0]-sum(abs(v)*T**j for j,v in b.items() if j)
  assert den>0
  return sum(abs(v)*T**j for j,v in a.items())/den

def rr(v):return v if isinstance(v,R) else R(v)
t=R({1:F(1)});D=F(5,2)-F(5,4)*t-F(5,64)*t*t;x=F(5,2)-t
q=lambda n:n+(-1)**n*D-x
r=1/q(4)
for n in [3,2,1]:r=1/(q(n)-(n+1)*t*r)
a=D-x-t*r
r=1/q(1)
for n in [2,3,4]:r=1/(q(n)-n*t*r)
b9=F(15,16)*9-D-F(1,32)-16*t
rl=1/q(8);ru=1/(q(8)-9*t/(b9-x))
for n in [7,6]:rl=1/(q(n)-(n+1)*t*rl);ru=1/(q(n)-(n+1)*t*ru)
bu=5-D-x-5*t*r-6*t*rl;bl=5-D-x-5*t*r-6*t*ru
# Middle determinant from the explicit five path matchings
M=q(1)*q(2)*q(3)*q(4)-2*t*q(3)*q(4)-3*t*q(1)*q(4)-4*t*q(1)*q(2)+8*t*t
bounds={'a':a.bound_after_dividing_t(3),'b_lower':bl.bound_after_dividing_t(3),'b_upper':bu.bound_after_dividing_t(3),
 'offdiag_using_sqrt120_lt11':11*(1/M-F(1,64)).bound_after_dividing_t(1)}
assert all(bounds[k]<F(1,10) for k in ['a','b_lower','b_upper'])
assert bounds['offdiag_using_sqrt120_lt11']<F(1,5)
result={'status':'same_agent_independent_fraction_rational_bounds_pass','bounds':{k:str(v) for k,v in bounds.items()},
 'limitations':'No generator or cached answer inputs, but same model and agent. Does not constitute fresh referee acceptance.'}
Path(__file__).with_name('rational-replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'bounds':{k:float(v) for k,v in bounds.items()},'all_checks_pass':True},indent=2))
