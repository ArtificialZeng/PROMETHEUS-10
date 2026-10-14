"""Input B: independently entered scalar graph amplitudes and Bloch-axis factors.
Does not read input A or import its script. Exact rational algebra, standard library.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json,math
# Algebra: r^2=3, a^2=(3+r)/6, b^2=(3-r)/6, i^2=-1.
# All constants use the positive real embedding r,a,b and imaginary i.
@lru_cache(None)
def reduce(e):
 e=list(e)
 for j in range(4):
  if e[j]>=2:
   e[j]-=2
   base=reduce(tuple(e))
   if j in (0,3):return tuple((m,c*(3 if j==0 else -1)) for m,c in base)
   shifted=e.copy();shifted[0]+=1
   out=dict((m,c/2) for m,c in base)
   for m,c in reduce(tuple(shifted)):out[m]=out.get(m,Q(0))+c*(Q(1,6) if j==1 else Q(-1,6))
   return tuple((m,c) for m,c in out.items() if c)
 return ((tuple(e),Q(1)),)
class F:
 def __init__(self,v=0):self.d=v if isinstance(v,dict) else ({(0,0,0,0):Q(v)} if v else {})
 def __add__(self,o):
  o=o if isinstance(o,F) else F(o);d=self.d.copy()
  for m,c in o.d.items():d[m]=d.get(m,Q(0))+c
  return F({m:c for m,c in d.items() if c})
 __radd__=__add__
 def __neg__(self):return F({m:-c for m,c in self.d.items()})
 def __sub__(self,o):return self+-asf(o)
 def __rsub__(self,o):return asf(o)+-self
 def __mul__(self,o):
  o=asf(o);d={}
  for m,c in self.d.items():
   for n,h in o.d.items():
    for p,v in reduce(tuple(x+y for x,y in zip(m,n))):d[p]=d.get(p,Q(0))+c*h*v
  return F({m:c for m,c in d.items() if c})
 __rmul__=__mul__
 def conj(self):return F({m:c*(-1 if m[3] else 1) for m,c in self.d.items()})
 def __eq__(self,o):return self.d==asf(o).d
 def val(self):
  constants=[math.sqrt(3),math.sqrt((3+math.sqrt(3))/6),math.sqrt((3-math.sqrt(3))/6),1j]
  return sum(complex(c)*math.prod(v**p for v,p in zip(constants,m)) for m,c in self.d.items())
 def record(self):return [{'powers_r_a_b_i':list(m),'rational':str(c)} for m,c in sorted(self.d.items())]
def asf(v):return v if isinstance(v,F) else F(v)
def symbol(j):
 e=[0]*4;e[j]=1;return F({tuple(e):Q(1)})
r,a,b,i=[symbol(j) for j in range(4)]
zero=F();one=F(1)
q=[[i*a,b],[-b,-i*a]] # separately transcribed q=i(bY+aZ), standard Y.
I=[[one,zero],[zero,one]];X=[[zero,one],[one,zero]]
Y=[[zero,-i],[i,zero]];Z=[[one,zero],[zero,-one]]
def dag(m):return [[z.conj() for z in row] for row in zip(*m)]
def mul(m,n):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*n)] for row in m]
def same(m,n):return all(x==y for row,col in zip(m,n) for x,y in zip(row,col))
def scale(v,m):return [[v*z for z in row] for row in m]
def add(m,n):return [[x+y for x,y in zip(row,col)] for row,col in zip(m,n)]
def kron(m,n):return [[x*y for x in row for y in col] for row in m for col in n]
def tensor(f):
 m=[[one]]
 for v in f:m=kron(m,v)
 return m
def record(m):return [[z.record() for z in row] for row in m]

# Stable extracted arithmetic and matrix primitives; no benchmark output writes.
