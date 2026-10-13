"""Directed Decimal node certificate. See README.md and the manuscript."""
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json, time, platform, decimal

PREC=48
DN=Context(prec=PREC,rounding=ROUND_FLOOR)
UP=Context(prec=PREC,rounding=ROUND_CEILING)
NEAR=Context(prec=PREC,rounding=ROUND_HALF_EVEN)

class I:
    def __init__(self,lo,hi=None):
        self.lo=lo if isinstance(lo,D) else D(lo)
        self.hi=self.lo if hi is None else (hi if isinstance(hi,D) else D(hi))
        assert self.lo<=self.hi
    def __add__(a,b):
        b=b if isinstance(b,I) else I(b)
        return I(DN.add(a.lo,b.lo),UP.add(a.hi,b.hi))
    __radd__=__add__
    def __neg__(a): return I(a.hi.copy_negate(),a.lo.copy_negate())
    def __sub__(a,b): return a+(-(b if isinstance(b,I) else I(b)))
    def __rsub__(a,b): return I(b)+(-a)
    def __mul__(a,b):
        b=b if isinstance(b,I) else I(b)
        return I(min(DN.multiply(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)),
                 max(UP.multiply(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)))
    __rmul__=__mul__
    def __truediv__(a,b):
        b=b if isinstance(b,I) else I(b)
        assert b.lo>0 or b.hi<0
        return a*I(DN.divide(D(1),b.hi),UP.divide(D(1),b.lo))
    def ln(a):
        assert a.lo>0
        # Decimal.ln is correctly rounded to nearest; neighboring representable
        # values therefore enclose the true logarithm, independently at each end.
        return I(NEAR.next_minus(NEAR.ln(a.lo)),NEAR.next_plus(NEAR.ln(a.hi)))
    def pair(a): return [str(a.lo),str(a.hi)]

def rat(q):
    q=F(q)
    return I(DN.divide(D(q.numerator),D(q.denominator)),
             UP.divide(D(q.numerator),D(q.denominator)))

def atan_rational(x,terms=40):
    total=sum(((-1)**n*x**(2*n+1)/F(2*n+1) for n in range(terms)),F(0))
    nextterm=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(total,total+nextterm),max(total,total+nextterm)

aa=atan_rational(F(1,5)); bb=atan_rational(F(1,239))
PI_LO=16*aa[0]-4*bb[1]; PI_HI=16*aa[1]-4*bb[0]
PI=I(rat(PI_LO).lo,rat(PI_HI).hi)
assert PI_LO>3 and PI_HI<F(22,7)
COS_R=rat(F(22,7)**60/F(factorial(60))).hi
SIN_R=rat(F(22,7)**61/F(factorial(61))).hi

def cos(x):
    assert x.lo>=0 and F(x.hi)<=F(22,7)
    xx=x*x; term=I(1); result=term
    for n in range(1,30):
        term=-(term*xx)/((2*n-1)*(2*n))
        result=result+term
    return result+I(COS_R.copy_negate(),COS_R)

def sin(x):
    assert x.lo>=0 and F(x.hi)<=F(22,7)
    xx=x*x; term=x; result=term
    for n in range(1,30):
        term=-(term*xx)/((2*n)*(2*n+1))
        result=result+term
    return result+I(SIN_R.copy_negate(),SIN_R)

LN2=I(2).ln()
def entropy(c):
    p=(1+c)/2; q=(1-c)/2
    return -(p*p.ln()+q*q.ln())/LN2

N=32768
SCALE=10**25
def low_int(x):
    z=F(x.lo)*SCALE
    return z.numerator//z.denominator

def run():
    start=time.monotonic()
    b0,b1,k=I('59.07'),I('-54.87'),I('99.45')
    prefix=None; minim=None; argmin=None; prefix_idx=None
    for j in range(N+1):
        theta=PI*j/(2*N)
        if j==0: c,s=I(1),I(0)
        elif j==N: c,s=I(-1),I(0)
        else: c=cos(2*theta); s=entropy(c)
        a=low_int(s/2-b0*c-k*theta)
        b=low_int(s/2-b1*c+k*theta)
        if prefix is None or a<prefix: prefix,prefix_idx=a,j
        value=prefix+b
        if minim is None or value<minim: minim,argmin=value,[prefix_idx,j]
    lower=F(minim,SCALE)
    error=F(21489,50)*F(22,7)/(4*N)
    assert lower-error>F(-211,50)
    off0,off1=sin(I('.6')),-sin(I('.4'))
    d=(off0-off1)/2; w=rat(F(66,125)); q=d/sin(w)
    w0=(I('.5')-q*w)/(1-q)
    L=I('-4.22')+b0*off0+b1*off1-k*I('.5')
    U=q*entropy(sin(w)); gap=L-U
    assert q.lo>0 and q.hi<1 and w0.lo>0 and w0.hi<1
    assert L.lo>D('.7758') and U.hi<D('.7653') and gap.lo>D('.0105')
    result={'classification':'independent standard-library arithmetic replay, same worker; fresh referee pending',
       'reads_other_outputs':False,'N':N,'precision':PREC,
       'pi_enclosure':PI.pair(),'cosine_remainder_bound':str(COS_R),'sine_remainder_bound':str(SIN_R),
       'sample_minimum_lower':str(lower),'continuum_correction_upper':str(error),
       'continuum_lower':str(lower-error),'minimizer_indices':argmin,
       'q':q.pair(),'w0':w0.pair(),'L':L.pair(),'U':U.pair(),'gap':gap.pair(),
       'all_assertions_passed':True,
       'environment':{'python':platform.python_version(),'decimal':decimal.__version__,
          'libmpdec':getattr(decimal,'__libmpdec_version__','unknown'),'parallel_workers':1},
       'seconds':time.monotonic()-start,
       'limitations':'Independent elementary-function implementation and arithmetic backend; same exact witness, grid-covering argument and researcher. This is not external or fresh-context peer review.'}
    return {key: value for key, value in result.items() if key not in ('classification', 'limitations')}
