"""Directed interval arithmetic with integer endpoints on a fixed binary grid.
Only +,-,*,/ are used. Every rounding operation is explicit integer floor/ceil.
No floating point, transcendental library, platform rounding mode or tolerance.
"""
from fractions import Fraction
BITS=384
SCALE=1<<BITS
class I:
    __slots__=('lo','hi')
    def __init__(self,x=0,hi=None):
        if isinstance(x,I):self.lo,self.hi=x.lo,x.hi;return
        if isinstance(x,float):raise TypeError('binary floating input forbidden')
        a=Fraction(x);b=a if hi is None else Fraction(hi)
        if a>b:raise ValueError('reversed interval')
        self.lo=(a.numerator*SCALE)//a.denominator
        self.hi=-((-b.numerator*SCALE)//b.denominator)
    @classmethod
    def raw(cls,lo,hi):
        if lo>hi:raise ValueError('reversed raw endpoints')
        v=object.__new__(cls);v.lo,v.hi=lo,hi;return v
    def __add__(x,y):
        y=interval(y);return I.raw(x.lo+y.lo,x.hi+y.hi)
    __radd__=__add__
    def __neg__(x):return I.raw(-x.hi,-x.lo)
    def __sub__(x,y):return x+-interval(y)
    def __rsub__(x,y):return interval(y)+-x
    def __mul__(x,y):
        y=interval(y);p=[x.lo*y.lo,x.lo*y.hi,x.hi*y.lo,x.hi*y.hi]
        return I.raw(min(p)//SCALE,-((-max(p))//SCALE))
    __rmul__=__mul__
    def __truediv__(x,y):
        y=interval(y)
        if y.lo<=0<=y.hi:raise ZeroDivisionError('interval denominator contains zero')
        p=[(a*SCALE,b) for a in [x.lo,x.hi] for b in [y.lo,y.hi]]
        return I.raw(min(a//b for a,b in p),max(-((-a)//b) for a,b in p))
    def __rtruediv__(x,y):return interval(y)/x
    def __bool__(x):return x.lo!=0 or x.hi!=0
    def __abs__(x):
        if x.lo>=0:return x
        if x.hi<=0:return -x
        return I.raw(0,max(-x.lo,x.hi))
    def contains_zero(x):return x.lo<=0<=x.hi
    def interior_of(x,y):return y.lo<x.lo and x.hi<y.hi
    def exact(x):return {'lo_integer':str(x.lo),'hi_integer':str(x.hi),'denominator_power_of_two':BITS}
    def decimal(x,digits=25):
        # Decimal endpoints are outward rounded too, for human-readable statements.
        q=10**digits
        a=(x.lo*q)//SCALE;b=-((-x.hi*q)//SCALE)
        def fmt(n):
            sign='-' if n<0 else '';n=abs(n)
            return sign+str(n//q)+'.'+str(n%q).zfill(digits)
        return [fmt(a),fmt(b)]
    def __repr__(x):return '['+', '.join(x.decimal())+']'
def interval(x):return x if isinstance(x,I) else I(x)
