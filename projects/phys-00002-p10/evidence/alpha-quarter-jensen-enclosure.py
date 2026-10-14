#!/usr/bin/env python3
"""Directed full-plane upper enclosure for identical (|0>+t|2>)/sqrt(1+t²).
Weighted Cauchy/Jensen on polar cells; abs chord handles sign changes exactly.
40 digit Decimal, analytic Gaussian moments, certified elementary functions.
"""
import importlib.util, math, time, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sp=importlib.util.spec_from_file_location('iv',ROOT/'evidence/alpha-quarter-enclosure.py');iv=importlib.util.module_from_spec(sp);sp.loader.exec_module(iv)
D=iv.D;add=iv.add;sub=iv.sub;mul=iv.mul;sqrt=iv.sqrt;exp=iv.exp;point=iv.point;rat=iv.rat;sq=iv.sq;PI=iv.PI
DOWN=iv.DOWN;UP=iv.UP
T=rat(1,20);T2=sq(T);DEN=add(point(1),T2);CROSS=mul(iv.S2,T)
def div(a,b):
 assert b[0]>0
 return mul(a,(DOWN.divide(D(1),b[1]),UP.divide(D(1),b[0])))
def trig(x,cosine=False):
 v=point(0)
 for k in range(65):
  n=2*k+(0 if cosine else 1)
  term=divint(powiv(x,n),math.factorial(n))
  v=add(v,term) if k%2==0 else sub(v,term)
 n=130+(0 if cosine else 1)
 rem=divint(powiv(x,n),math.factorial(n))[1]
 return add(v,(-rem,rem))
def divint(a,n):return mul(a,rat(1,n))
def powiv(a,n):
 v=point(1)
 for _ in range(n):v=mul(v,a)
 return v
def radial(a,b):
 a=point(a);b=point(b);ea=exp(mul(rat(-1,4),a));eb=exp(mul(rat(-1,4),b))
 m0=mul(point(4),sub(ea,eb))
 m1=mul(point(4),sub(mul(add(a,point(4)),ea),mul(add(b,point(4)),eb)))
 def f(x):return add(add(sq(x),mul(point(8),x)),point(32))
 m2=mul(point(4),sub(mul(f(a),ea),mul(f(b),eb)))
 J=add(mul(DEN,m0),add(mul(mul(point(-2),T2),m1),mul(mul(rat(1,2),T2),m2)))
 return m0,m1,J

def calc(nr,nt):
 # R in [0,100], theta in [0,pi/2]. Four equal quadrants by cos(2theta).
 dt=mul(PI,rat(1,2*nt));angles=[]
 for j in range(nt):
  u=mul(PI,rat(j,nt));v=mul(PI,rat(j+1,nt))
  cu=trig(u,True);cv=trig(v,True)
  cavg=div(sub(trig(v),trig(u)),mul(point(2),dt))
  angles.append(((cv[0],cu[1]),cavg))
 total=point(0);signcounts=[0,0,0]
 for i in range(nr):
  a=D(100)*i/nr;b=D(100)*(i+1)/nr;r=(a,b)
  m0,m1,Jbase=radial(a,b)
  # Natural range Q. Exact rational t ensures physical normalized input.
  Ab=add(DEN,add(mul(mul(point(-2),T2),r),mul(mul(rat(1,2),T2),sq(r))))
  for cr,cavg in angles:
   qrange=div(add(Ab,mul(CROSS,mul(r,cr))),DEN)
   mass=mul(m0,dt)
   J=div(mul(dt,add(Jbase,mul(mul(CROSS,cavg),m1))),DEN)
   lo,hi=qrange
   if lo>=0:Jabs=J;signcounts[0]+=1
   elif hi<=0:Jabs=iv.neg(J);signcounts[1]+=1
   else:
    # |q| <= slope*q + intercept on [lo,hi]. Chord of convex |q|.
    slope=div(add(point(hi),point(lo)),sub(point(hi),point(lo)))
    intercept=div(mul(point(-2),mul(point(hi),point(lo))),sub(point(hi),point(lo)))
    Jabs=add(mul(slope,J),mul(intercept,mass));signcounts[2]+=1
   assert Jabs[1]>=0
   upper=sqrt((D(0),max(D(0),mul(mass,Jabs)[1])))[1]
   total=(D(0),UP.add(total[1],upper))
  if i%256==0:print('progress',nr,nt,i,flush=True)
 # phase plane .5 dR dtheta, four quadrants.
 interior=mul(mul(point(2),iv.PREF),total)
 # Cartesian Q coefficients: constant1, x²/p² and quartic sum.
 # sum |coeff| <= (1+t²+4t²+2sqrt2*t+2t²)/(1+t²).
 C=div(add(add(DEN,mul(point(6),T2)),mul(point(2),CROSS)),DEN)
 tail=mul(mul(mul(point(16),PI),iv.PREF),mul(sqrt(C),mul(point(26),exp(point(-25)))))
 full=(D(0),UP.add(interior[1],tail[1]))
 return {'radial_R_cells':nr,'quadrant_angular_cells':nt,'R_cutoff':100,'interior_upper':str(interior[1]),'tail_upper':str(tail[1]),'full_plane_upper':str(full[1]),'vacuum_lower':str(iv.VAC[0]),'strict_violation':full[1]<iv.VAC[0],'sign_cells_positive_negative_straddling':signcounts}
def main():
 start=time.monotonic();out={'t':'1/20','alpha':'1/4','precision':40,'method':'Directed weighted Cauchy/Jensen polar cells, absolute-value chord across zeros, analytic full-plane tail','rows':[]}
 for nr,nt in [(800,64),(1600,128)]:
  row=calc(nr,nt);out['rows'].append(row);out['elapsed_seconds']=time.monotonic()-start
  (ROOT/'evidence/alpha-quarter-jensen-enclosures.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(row),flush=True)
  # Retain a second rigorous refinement, even after the first strict bound.
if __name__=='__main__':main()
