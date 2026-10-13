"""Exact rational root/sign certificates for the analytic endpoint and dual family.

All decisive arithmetic uses Fraction, integer square roots and SymPy Sturm counts.
Floating output is printed only as a readable approximation after the exact checks.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[2]

class I:
    def __init__(self,lo,hi=None):
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def get(x): return x if isinstance(x,I) else I(x)
    def __add__(self,x):
        x=self.get(x);return I(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,x):return self+-self.get(x)
    def __rsub__(self,x):return self.get(x)+-self
    def __mul__(self,x):
        x=self.get(x);z=[self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi];return I(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.get(x);assert not x.lo<=0<=x.hi
        return self*I(1/x.hi,1/x.lo)
    def __rtruediv__(self,x):return self.get(x)/self
    def __pow__(self,n):
        assert n>=0 and int(n)==n
        if n==0:return I(1)
        if n%2==0:
            z=[self.lo**n,self.hi**n];return I(0 if self.lo<=0<=self.hi else min(z),max(z))
        return I(self.lo**n,self.hi**n)
    def sqrt(self,digits=30):
        assert self.lo>=0
        scale=10**digits
        a=isqrt(self.lo.numerator*scale**2//self.lo.denominator)
        b=isqrt(self.hi.numerator*scale**2//self.hi.denominator)
        # Lower truncation, upper strict enclosure; no decimal floating arithmetic.
        return I(F(a,scale),F(b+1,scale))
    def record(self):return {'lower':str(self.lo),'upper':str(self.hi),'readable':[float(self.lo),float(self.hi)]}
    def positive(self):assert self.lo>0;return True
    def negative(self):assert self.hi<0;return True

def endpoint_intervals():
    l=I(F(66454426803,10**11),F(66454426804,10**11))
    r2=I(2).sqrt();t=l.sqrt();delta=2-3*l;p=l/(2*r2);a=2*(1-l)**2-l*l/8
    u=(a/delta).sqrt();v=(2*l*(1-l)/(2*l-1)).sqrt();eta=r2*u/v;beta=2*eta
    y=[(t*u-p)**2,-2*r2*u*(t*u-p),2*r2*(t*u-p),2*u*u+eta*(2*l-v*v),-2*beta*t,eta*v*v,-4*u,I(2),beta,I(0)]
    return l,y,{'sqrt2':r2,'t':t,'delta':delta,'p':p,'a':a,'u':u,'v':v,'eta':eta,'beta':beta}

def main():
    z=s.Symbol('lambda');P=s.Poly(601*z**6-714*z**5+113*z**4-1040*z**3+2080*z**2-1280*z+256,z)
    l,y,d=endpoint_intervals();L=s.Rational(l.lo.numerator,l.lo.denominator);U=s.Rational(l.hi.numerator,l.hi.denominator)
    assert P.count_roots(L,U)==1
    assert P.count_roots(s.Rational(3,5),s.Rational(2,3))==1
    refined=I(F(66454426803317,10**14),F(66454426803318,10**14))
    assert P.count_roots(s.Rational(refined.lo.numerator,refined.lo.denominator),s.Rational(refined.hi.numerator,refined.hi.denominator))==1
    print('PASS: Sturm count exactly1 root in isolating interval and exactly1 in (3/5,2/3)')
    print('Endpoint isolated:',l.lo,l.hi)
    print('PASS: refined exact root interval:',refined.lo,refined.hi)
    AA=(2-3*l)*(16*(1-l)**2-l*l);BB=32*l*(1-l)*(2*l-1);CC=9*l**3
    zz=s.expand((9*z**3-(2-3*z)*(16*(1-z)**2-z*z)-32*z*(1-z)*(2*z-1))**2-4*(2-3*z)*(16*(1-z)**2-z*z)*32*z*(1-z)*(2*z-1))
    assert s.expand(zz-4*P.as_expr())==0
    for k,x in {'A':AA,'B':BB,'C':CC,'C-A-B':CC-AA-BB,'delta':d['delta'],'a':d['a'],'2lambda-1':2*l-1,'w':l*l+l-1}.items():
        x.positive();print('PASS positive:',k,x.record()['readable'])
    # R dual is [[y3,-beta*k],[-beta*k,1+eta]].
    Rdet=y[3]*(1+d['eta'])-(d['beta']*d['t']/d['sqrt2'])**2
    y[3].positive();Rdet.positive()
    print('PASS: dual R positive definite; determinant enclosure',Rdet.record()['readable'])
    for yi in y:assert yi.lo>-60 and yi.hi<60
    print('PASS: all |y_i|<60, hence ||W_H0||op<27*60<2000')
    x=I(l.lo,F(2,3));tx=x.sqrt();r2=d['sqrt2']
    derivative=y[1]/(2*r2*tx)+y[2]/4-y[3]+y[4]*(1-3*x)/(2*tx)+y[5]+3*y[6]*tx/(2*r2)-2*y[7]*(1-x)+2*y[8]*(1-2*x)
    derivative.negative()
    print('PASS: derivative q(lambda) strictly negative on endpoint..2/3:',derivative.record()['readable'])
    # Record a strictly negative, algebraically enclosed expectation at U0=.6646.
    U0=I(F(3323,5000));b=[I(1),U0.sqrt()/r2,U0/4,1-U0,U0.sqrt()*(1-U0),U0,U0*U0.sqrt()/r2,(1-U0)**2,2*U0*(1-U0),U0*U0]
    expectation=sum((yi*bi for yi,bi in zip(y,b)),I(0));expectation.negative()
    print('PASS: H0 expectation on3J at3323/5000 negative:',expectation.record()['readable'])
    report={'status':'pass','arithmetic':'exact Fraction endpoints; sqrt bounds from integer square root at30decimal places; Sturm counts with rational endpoints',
      'polynomial':str(P.as_expr()),'root_interval':l.record(),'refined_root_interval':refined.record(),'root_counts':{'isolating_interval':1,'refined_interval':1,'three_fifths_to_two_thirds':1},
      'branch_checks':{k:x.record() for k,x in {'A':AA,'B':BB,'C':CC,'C-A-B':CC-AA-BB}.items()},
      'endpoint_parameters':{k:x.record() for k,x in d.items()},'dual_y_enclosures':[x.record() for x in y],
      'dual_R_determinant':Rdet.record(),'derivative_on_endpoint_to_two_thirds':derivative.record(),
      'H0_unnormalized_expectation_at_U0':expectation.record(),'U0':'3323/5000','operator_norm_bound':2000,
      'analytic_obligations':'Root branch, endpoint Gram extension, dual Gram blocks, full-space Schur lift and post-loss pullback are proved in evidence/research-endpoint-proof.md; this log is not a fresh referee audit.'}
    (ROOT/'evidence/qutrit-exact-certificate.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
