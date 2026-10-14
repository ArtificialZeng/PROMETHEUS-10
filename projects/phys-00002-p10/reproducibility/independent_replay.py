#!/usr/bin/env python3
"""Coordinate-space reduction and integer interval integration, portable copy.
No proposer modules, result files, or caches imported.
"""
from fractions import Fraction as F
from math import comb, factorial, prod, isqrt
import json,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
# Exact algebra in Q(sqrt2), polynomial coordinates (x,s,y,p).
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def times(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def sc(a,c):return (a[0]*c,a[1]*c)
def pa(a,b):
 out=dict(a)
 for k,v in b.items():out[k]=plus(out.get(k,(F(0),F(0))),v)
 return {k:v for k,v in out.items() if any(v)}
def pm(a,b):
 out={}
 for ka,va in a.items():
  for kb,vb in b.items():
   k=tuple(x+y for x,y in zip(ka,kb));out[k]=plus(out.get(k,(F(0),F(0))),times(va,vb))
 return {k:v for k,v in out.items() if any(v)}
def ps(a,c):return {k:sc(v,c) for k,v in a.items()}
def gm(n):return F(prod(range(1,n,2)),2**(n//2)) if n%2==0 else F(0)
def exact():
 # Beam-splitter coordinate rotation, P=f((q1+q2)/sqrt2)f((q1-q2)/sqrt2).
 # f(q)=20-sqrt2/2+sqrt2*q². Joint wavefunction = Gaussian *P/401.
 c=(F(20),F(-1,2));z=(0,0,0,0)
 b={z:c,(2,0,0,0):(F(0),F(1,2)),(0,0,2,0):(F(0),F(1,2))}
 P=pa(pm(b,b),{(2,0,2,0):(F(-2),F(0))})
 def shifted(sign,poly=P):
  out={}
  for (nx,ns,ny,np),v in poly.items():
   for k in range(nx+1):
    key=(nx-k,k,ny,0);out[key]=plus(out.get(key,(F(0),F(0))),sc(v,F(comb(nx,k)*sign**k)))
  return out
 kernel=pm(shifted(1),shifted(-1));W={}
 for (nx,ns,ny,_),v in kernel.items():
  if ny%2:continue
  # Fourier Gaussian moments: shifted Gaussian has mean ip and variance1/2.
  for k in range(ns//2+1):
   np=ns-2*k
   if np%2:raise AssertionError('Unexpected imaginary term')
   factor=gm(ny)*F(comb(ns,2*k))*gm(2*k)*(-1)**(np//2)/401**2
   key=(nx,0,0,np);W[key]=plus(W.get(key,(F(0),F(0))),sc(v,factor))
 W={k:v for k,v in W.items() if any(v)}
 Q={z:(F(1),F(0)),(2,0,0,0):(F(-2,401),F(20,401)),(0,0,0,2):(F(-2,401),F(-20,401)),(4,0,0,0):(F(1,802),F(0)),(2,0,0,2):(F(1,401),F(0)),(0,0,0,4):(F(1,802),F(0))}
 assert W==pm(Q,Q)
 norm=(F(0),F(0))
 for (nx,_,__,np),v in W.items():norm=plus(norm,sc(v,gm(nx)*gm(np)))
 assert norm==(1,0)
 # Published one-photon nodal benchmark, reconstructed in coordinates:
 # psi1(q)=sqrt2*q*Gaussian; rotation gives P1=x²-y².
 P1={(2,0,0,0):(F(1),F(0)),(0,0,2,0):(F(-1),F(0))}
 K1=pm(shifted(1,P1),shifted(-1,P1));W1={}
 for (nx,ns,ny,_),v in K1.items():
  for k in range(ns//2+1):
   np=ns-2*k
   assert np%2==0 and ny%2==0
   key=(nx,0,0,np)
   factor=gm(ny)*F(comb(ns,2*k))*gm(2*k)*(-1)**(np//2)
   W1[key]=plus(W1.get(key,(F(0),F(0))),sc(v,factor))
 W1={k:v for k,v in W1.items() if any(v)}
 Q1={z:(F(-1),F(0)),(2,0,0,0):(F(1),F(0)),(0,0,0,2):(F(1),F(0))}
 assert W1==pm(Q1,Q1)
 print('Published eq24 one-photon baseline: exact W=e^-R*(R-1)^2/pi; nodal circle retained',flush=True)
 print(json.dumps({'exact_coordinate_reduction':'W=e^-R Q²/pi, all coefficients match','normalization':str(norm),'Q':{str(k):[str(x) for x in v] for k,v in Q.items()},'input_norm':'(400+1)/401=1; product input; no truncation','vacuum_baseline':'4*pi^(3/4) from Gaussian integral'},indent=2),flush=True)
# Integer fixed-point interval arithmetic; denominator S. No Decimal library.
S=10**35
class V:
 def __init__(self,l,h=None):self.l=l;self.h=l if h is None else h
 def __add__(a,b):return V(a.l+b.l,a.h+b.h)
 def __neg__(a):return V(-a.h,-a.l)
 def __sub__(a,b):return a+-b
 def __mul__(a,b):
  t=[a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h];return V(min(t)//S,-((-max(t))//S))
 def __truediv__(a,b):
  assert b.l>0
  return a*V(S*S//b.h,-((-S*S)//b.l))
 def sqrt(a):
  assert a.l>=0
  lo=isqrt(a.l*S);hi=isqrt(a.h*S)
  return V(lo,hi+(hi*hi<a.h*S))
 def square(a):
  if a.l<=0<=a.h:return V(0,-((-max(a.l*a.l,a.h*a.h))//S))
  return a*a
 def upper(a):return V(a.h)
 def text(a):return [str(F(a.l,S)),str(F(a.h,S))]
def rat(n,d=1):return V(n*S//d,-((-n*S)//d))
ZERO=rat(0);ONE=rat(1)
def exp_pos(x):
 assert x.l>=0 and x.h<=25*S
 term=ONE;total=ONE
 for n in range(1,161):term=term*x/rat(n);total=total+term
 nextterm=term*x/rat(161);rem=nextterm/(ONE-x/rat(162))
 return V(total.l,total.h+rem.h)
def decay(x):return ONE/exp_pos(x/rat(4))
def atan(k):
 f=sum((F((-1)**j,(2*j+1)*k**(2*j+1)) for j in range(100)),F(0));e=F(1,201*k**201)
 return rat((f-e).numerator,(f-e).denominator)+V(0,rat((2*e).numerator,(2*e).denominator).h)
PI=rat(16)*atan(5)-rat(4)*atan(239)
SQ2=rat(2).sqrt();PREF=ONE/PI.sqrt().sqrt()
def trig(x,cos=False):
 term=ONE if cos else x;total=term
 for k in range(1,61):
  d=(2*k-1)*(2*k) if cos else (2*k)*(2*k+1)
  term=term*x*x/rat(d);total=total-term if k%2 else total+term
 d=121*122 if cos else 122*123
 rem=(term*x*x/rat(d)).h
 return V(total.l-rem,total.h+rem)
def cert(nr=1600,nt=128):
 # Q=(401-2R+R²/2+20sqrt2 R cos2theta)/401.
 dtheta=PI/rat(2*nt);angles=[]
 for j in range(nt):
  a=PI*rat(j,nt);b=PI*rat(j+1,nt)
  ca=trig(a,True);cb=trig(b,True)
  angles.append((V(cb.l,ca.h),(trig(b)-trig(a))/(rat(2)*dtheta)))
 total=ZERO;counts=[0,0,0]
 for i in range(nr):
  a=rat(100*i,nr);b=rat(100*(i+1),nr);r=V(a.l,b.h)
  ea=decay(a);eb=decay(b)
  m0=rat(4)*(ea-eb)
  m1=rat(4)*((a+rat(4))*ea-(b+rat(4))*eb)
  m2=rat(4)*((a*a+rat(8)*a+rat(32))*ea-(b*b+rat(8)*b+rat(32))*eb)
  base=rat(401)*m0-rat(2)*m1+m2/rat(2)
  qrbase=rat(401)-rat(2)*r+r.square()/rat(2)
  for cr,avg in angles:
   q=(qrbase+rat(20)*SQ2*r*cr)/rat(401)
   M=dtheta*m0;J=dtheta*(base+rat(20)*SQ2*m1*avg)/rat(401)
   if q.l>=0:A=J;counts[0]+=1
   elif q.h<=0:A=-J;counts[1]+=1
   else:
    l=V(q.l);h=V(q.h)
    A=((h+l)*J-rat(2)*h*l*M)/(h-l);counts[2]+=1
   total=total+(M*A).upper().sqrt().upper()
  if i%400==0:print('integer interval progress',i,flush=True)
 interior=rat(2)*PREF*total
 # Independent simple tail bound Q<=1+ (2+20sqrt2)R/401+R²/802.
 # For R>=100 and R>=1, |Q|< 2 R², so sqrt|Q|<sqrt2 R.
 tail=rat(16)*PI*PREF*SQ2*rat(26)*decay(rat(100))
 full=interior+tail;vac=rat(4)*PI*PREF
 assert full.h < rat(943718,100000).l
 assert vac.l > rat(943892,100000).h
 upper15=-((-full.h)//10**20)
 result={'grid':[nr,nt],'cutoff_R':100,'fixed_point_digits':35,'meaning':'interior/full_plane intervals enclose the evaluated upper-bound expression, not lower bounds on the physical integral','interior':interior.text(),'tail':tail.text(),'full_plane':full.text(),'vacuum':vac.text(),'strict_frozen_decimal_comparison':True,'counts':counts,'outward_upper_decimal':str(upper15//10**15)+'.'+str(upper15%10**15).zfill(15)}
 (ROOT/'independent-enclosure.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 start=time.monotonic();exact();cert();print('elapsed_seconds',time.monotonic()-start)
