#!/usr/bin/env python3
"""Integer fixed-point outward intervals; rational atan remainder; no libm."""
import json,math,time
from fractions import Fraction as R
from pathlib import Path
S=10**30
K=60
class I:
 def __init__(self,l,u=None):self.l=l;self.u=l if u is None else u
 @staticmethod
 def rat(p,q=1):return I(p*S//q,-((-p*S)//q))
 def __add__(self,b):return I(self.l+b.l,self.u+b.u)
 def __neg__(self):return I(-self.u,-self.l)
 def __sub__(self,b):return self+-b
 def __mul__(self,b):
  c=[self.l*b.l,self.l*b.u,self.u*b.l,self.u*b.u];return I(min(c)//S,-((-max(c))//S))
 def divint(self,n):return I(self.l//n,-((-self.u)//n))
 def __truediv__(self,b):
  assert b.l>0
  vals=[R(self.l*S,b.l),R(self.l*S,b.u),R(self.u*S,b.l),R(self.u*S,b.u)]
  l=min(vals);u=max(vals);return I(l.numerator//l.denominator,-((-u.numerator)//u.denominator))
 def out(self):return [str(R(self.l,S)),str(R(self.u,S))]
 def floats(self):return [self.l/S,self.u/S]
ONE=I.rat(1)
def small_atan(p,q):
 if p<0:return -small_atan(-p,q)
 assert 2*p<=q
 t=I.rat(p,q);sq=t*t;term=t;res=I(0)
 for k in range(K):
  a=term.divint(2*k+1);res=res+a if k%2==0 else res-a;term=term*sq
 # after even number K, partial sum is lower; next positive term bounds tail
 return I(res.l,res.u+term.divint(2*K+1).u)
PI=small_atan(1,5)*I.rat(16)-small_atan(1,239)*I.rat(4)
def atan(p,q=1):
 if p<0:return -atan(-p,q)
 if p>q:return PI.divint(2)-atan(q,p)
 if 2*p>q:return PI.divint(4)+small_atan(p-q,p+q)
 return small_atan(p,q)
def F(p,q=1):return I.rat(1,2)+atan(p,q)/PI

def M4bound(b):
 # inverse quadratic derivative bounds via differentiating D*v=1.
 a=1+(b+1)**2;d1=max(2*(b+1),2*a-2*(b+1));d2=2*a
 B=[a]
 for k in range(1,5):B.append(a*(k*d1*B[k-1]+(k*(k-1)//2)*d2*(B[k-2] if k>=2 else 0)))
 # A=F((1-t)/t); A'=-1/(pi E), E=t²+(1-t)².
 # pi>3, E>=1/2, |E'|<=2, E''=4.
 C=[R(2)]
 for k in range(1,4):C.append(2*(k*2*C[k-1]+(k*(k-1)//2)*4*(C[k-2] if k>=2 else 0)))
 AA=[R(1)]+[C[k-1]/3 for k in range(1,5)]
 return sum(R(math.comb(4,k))*AA[k]*B[4-k] for k in range(5))/3

def q2_simpson(b,N=8192):
 assert N%2==0
 acc=I(0)
 for i in range(N+1):
  t=R(i,N);d=t*t+((b+1)*t-1)**2
  A=ONE if i==0 else F(N-i,i)
  g=A/(PI*I.rat(d.numerator,d.denominator))
  acc=acc+g*I.rat(1 if i in (0,N) else (4 if i%2 else 2))
 val=acc.divint(3*N);err=M4bound(b)/ (180*N**4)
 ei=I.rat(err.numerator,err.denominator)
 return I(val.l-ei.u,val.u+ei.u),err

# Rational spatial grid: dense central interval, geometric negative tail.
def grid(b,h=R(1,32),L=R(4096)):
 xs=[-L];v=-L
 while v < -8:
  v=min(R(-8),v*R(7,8));xs.append(v)
 v=R(-8)
 while v<b:
  v=min(b,v+h);xs.append(v)
 return xs

def q2_monotone(b,h=R(1,32)):
 xs=grid(b,h);cdf=[F(x.numerator,x.denominator) for x in xs]
 # Entire left tail: 0<=integrand<=1, improves lower using value at -L.
 lb=F((b-xs[0]).numerator,(b-xs[0]).denominator)
 low=cdf[0]*lb;up=cdf[0]
 for j in range(1,len(xs)):
  mass=cdf[j]-cdf[j-1]
  if mass.l<0:raise RuntimeError('negative mass interval')
  l=F((b-xs[j]).numerator,(b-xs[j]).denominator)
  u=F((b-xs[j-1]).numerator,(b-xs[j-1]).denominator)
  low=low+mass*l;up=up+mass*u
 return I(low.l,up.u)

def q3_lower(b):
 xs=grid(b,R(1,16),R(64));cdf=[F(x.numerator,x.denominator) for x in xs]
 low=I(0);up=I(0)
 # discard entire left tail for lower bound, bound by its CDF mass for upper
 up=cdf[0]
 prev=q2_monotone(b-xs[0],R(1,16))
 for j in range(1,len(xs)):
  mass=cdf[j]-cdf[j-1];cur=q2_monotone(b-xs[j],R(1,16))
  low=low+mass*I(cur.l);up=up+mass*I(prev.u);prev=cur
 return I(low.l,up.u),len(xs)

def main():
 start=time.time();rows=[]
 for b in [R(1808,1000),R(1809,1000)]:
  q1=F(b.numerator,b.denominator);q2,err=q2_simpson(b)
  c2=q2-q1*q1
  row=dict(b=str(b),Q1=q1.floats(),Q2=q2.floats(),c2=c2.floats(),Q1_exact=q1.out(),Q2_exact=q2.out(),c2_exact=c2.out(),simpson_N=8192,M4_bound=str(M4bound(b)),simpson_error_bound=str(err))
  rows.append(row);print(json.dumps(row),flush=True)
 b=R(1808,1000);q3,n=q3_lower(b)
 upperb=R(1809,1000);u1=F(upperb.numerator,upperb.denominator);u2,_=q2_simpson(upperb)
 c3=q3-u1*u2
 row=dict(uniform_b_interval=['1.808','1.809'],Q3_at_left=q3.floats(),Q3_at_left_exact=q3.out(),uniform_c3_lower=str(R(c3.l,S)),uniform_c3_lower_decimal=c3.l/S,outer_nodes=n)
 rows.append(row);print(json.dumps(row),flush=True)
 assert rows[0]['c2'][0]>0 and rows[1]['c2'][1]<0 and c3.l>0
 result=dict(arithmetic='outward integer fixed-point intervals, scale 10^30; rational alternating atan with explicit remainder; no libm',rows=rows,elapsed_seconds=time.time()-start,checks='PASS: endpoint c2 signs; uniform positive c3 on closed bracket')
 Path('evidence/interval-survival-result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(checks=result['checks'],elapsed_seconds=result['elapsed_seconds'])),flush=True)
if __name__=='__main__':main()
