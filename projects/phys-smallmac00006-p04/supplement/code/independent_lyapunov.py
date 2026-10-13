#!/usr/bin/env python3
"""Fresh referee replay: real polynomial Lyapunov obstructions, no proposer imports.

Original-coordinate monomial terms are transcribed from Boros--Hofbauer pp.13,19.
Use X=x-1, Z=alpha*(x-1)+gamma*(y-1), so Xdot=-Z, Zdot=w*X.
Solve (F.grad) H = sum c_m*(w*X**2+Z**2)**m through degree 10.
This is a scalar real homological equation, not the submitted complex conjugacy.
"""
from fractions import Fraction
from math import comb, factorial
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING

PRECISION = 90
DOWN = Context(prec=PRECISION, rounding=ROUND_FLOOR)
UP = Context(prec=PRECISION, rounding=ROUND_CEILING)

class Box:
    __slots__ = ('l','u')
    def __init__(self, lo=0, hi=None):
        if isinstance(lo, Box):
            self.l,self.u=lo.l,lo.u
            return
        if isinstance(lo, float) or isinstance(hi,float):
            raise TypeError('Floating input not permitted')
        if isinstance(lo, Fraction):
            self.l=DOWN.divide(Decimal(lo.numerator),Decimal(lo.denominator))
            self.u=UP.divide(Decimal(lo.numerator),Decimal(lo.denominator))
        else:
            self.l=Decimal(lo)
            self.u=Decimal(lo if hi is None else hi)
        if self.l>self.u: raise ValueError('Reversed endpoints')
    @classmethod
    def pair(cls,l,u):
        ans=object.__new__(cls); ans.l=l; ans.u=u
        if l>u: raise ValueError('Reversed endpoints')
        return ans
    def __add__(self,other):
        if isinstance(other, Tangent): return NotImplemented
        b=Box(other)
        return Box.pair(DOWN.add(self.l,b.l),UP.add(self.u,b.u))
    __radd__=__add__
    def __neg__(self):return Box.pair(self.u.copy_negate(),self.l.copy_negate())
    def __sub__(self,other):return self+-Box(other)
    def __rsub__(self,other):return Box(other)+-self
    def __mul__(self,other):
        if isinstance(other,Tangent):return NotImplemented
        b=Box(other)
        pairs=[(a,c) for a in (self.l,self.u) for c in (b.l,b.u)]
        return Box.pair(min(DOWN.multiply(a,c) for a,c in pairs),max(UP.multiply(a,c) for a,c in pairs))
    __rmul__=__mul__
    def __truediv__(self,other):
        b=Box(other)
        if b.l<=0<=b.u:raise ZeroDivisionError('Denominator interval contains zero')
        pairs=[(a,c) for a in (self.l,self.u) for c in (b.l,b.u)]
        return Box.pair(min(DOWN.divide(a,c) for a,c in pairs),max(UP.divide(a,c) for a,c in pairs))
    def __rtruediv__(self,other):return Box(other)/self
    def __pow__(self,n):
        if n<0:return 1/(self**(-n))
        result=Box(1)
        for _ in range(n):result=result*self
        return result
    def __abs__(self):
        if self.l>=0:return self
        if self.u<=0:return -self
        return Box.pair(Decimal(0),max(self.l.copy_negate(),self.u))
    def __bool__(self):return self.l!=0 or self.u!=0
    def __repr__(self):return '['+str(self.l)+', '+str(self.u)+']'
    def record(self):return [str(self.l),str(self.u)]

class Tangent:
    __slots__=('v','d')
    def __init__(self,v,d=None):
        if isinstance(v,Tangent):self.v,self.d=v.v,v.d;return
        self.v=v;self.d=(v*0,v*0) if d is None else tuple(d)
    def __add__(self,b):
        b=Tangent(b);return Tangent(self.v+b.v,[self.d[i]+b.d[i] for i in range(2)])
    __radd__=__add__
    def __neg__(self):return Tangent(-self.v,[-x for x in self.d])
    def __sub__(self,b):return self+-Tangent(b)
    def __rsub__(self,b):return Tangent(b)+-self
    def __mul__(self,b):
        b=Tangent(b);return Tangent(self.v*b.v,[self.d[i]*b.v+self.v*b.d[i] for i in range(2)])
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Tangent(b)
        return Tangent(self.v/b.v,[(self.d[i]*b.v-self.v*b.d[i])/(b.v*b.v) for i in range(2)])
    def __rtruediv__(self,b):return Tangent(b)/self
    def __pow__(self,n):
        if n<0:return 1/(self**(-n))
        v=Tangent(self.v*0+1)
        for _ in range(n):v=v*self
        return v
    def __bool__(self):return bool(self.v) or any(map(bool,self.d))
    def __repr__(self):return 'Tangent('+repr(self.v)+','+repr(self.d)+')'

def choose(v,n):
    out=v*0+1
    for j in range(n):out=out*(v-j)/(j+1)
    return out

def real_jet(terms,alpha,gamma,w,N):
    """Each term is (coefficient_x, coefficient_y, exponent_x, exponent_y).
    Constants disappear after translating the equilibrium. Original time retained.
    Dense homogeneous arrays index the power of Z, not X.
    """
    zero=alpha*0
    fx={k:[zero for _ in range(k+1)] for k in range(1,N+1)}
    gz={k:[zero for _ in range(k+1)] for k in range(1,N+1)}
    for cx,cy,px,py in terms:
        xp=[choose(px,k) for k in range(N+1)]
        yp=[choose(py,k) for k in range(N+1)]
        for total in range(1,N+1):
            for old_y in range(total+1):
                c=xp[total-old_y]*yp[old_y]/(gamma**old_y)
                for j in range(old_y+1):
                    coeff=c*comb(old_y,j)*((-alpha)**(old_y-j))
                    fx[total][j]=fx[total][j]+cx*coeff
                    gz[total][j]=gz[total][j]+(alpha*cx+gamma*cy)*coeff
    # The exact linear identity is proved analytically in the audit.
    return fx,gz

def focus_from_terms(terms,alpha,gamma,w,max_focus=4):
    zero=alpha*0; one=zero+1
    N=2*max_focus+1
    fx,gz=real_jet(terms,alpha,gamma,w,N)
    H={2:[w,zero,one]}
    coefficients=[]; residuals=[]
    for n in range(3,N+2):
        B=[zero for _ in range(n+1)]
        for k in range(2,n):
            degree=n-k+1
            if degree not in H:continue
            for j,hj in enumerate(H[degree]):
                for s in range(k+1):
                    if degree-j:
                        B[j+s]=B[j+s]+(degree-j)*hj*fx[k][s]
                    if j:
                        B[j-1+s]=B[j-1+s]+j*hj*gz[k][s]
        if n%2==0:
            m=n//2
            # Average X^(2p) Z^(2q) on Q=1; odd monomials average to zero.
            c=zero
            for j in range(0,n+1,2):
                p=(n-j)//2;q=j//2
                weight=Fraction(factorial(2*p)*factorial(2*q),4**m*factorial(p)*factorial(q)*factorial(m))
                c=c+B[j]*weight/(w**p)
            coefficients.append(c)
            rhs=[-B[j]+(c*comb(m,j//2)*w**(m-j//2) if j%2==0 else zero) for j in range(n+1)]
        else:rhs=[-v for v in B]
        # Solve w(j+1) h_(j+1) -(n-j+1) h_(j-1) = rhs_j.
        # Even n: h0=0 fixes the one-dimensional radial kernel.
        # Odd n: determine h0 from the last equation using the homogeneous chain.
        base=[zero for _ in range(n+1)]; kernel=[zero for _ in range(n+1)];kernel[0]=one
        for j in range(n):
            base[j+1]=(rhs[j]+((n-j+1)*base[j-1] if j else zero))/(w*(j+1))
            kernel[j+1]=((n-j+1)*kernel[j-1] if j else zero)/(w*(j+1))
        h0=(-rhs[n]-base[n-1])/kernel[n-1] if n%2 else zero
        hn=[base[j]+h0*kernel[j] for j in range(n+1)]
        H[n]=hn
        residuals.append([-rhs[j]+(w*(j+1)*hn[j+1] if j<n else zero)-((n-j+1)*hn[j-1] if j else zero) for j in range(n+1)])
    return coefficients,{'w':w,'H':H,'residuals':residuals,'linear_fx':fx[1],'linear_gz':gz[1]}

def target(a,h,max_focus=4,b_override=None):
    d=h*(h-1)/2
    b=(a*h-1)/d if b_override is None else b_override
    K=a/(1+b*d);w=K*a*(d-1)
    one=a*0+1
    # p.19: inv-y column (1,-K); x^a*y^b column (-1,K*d).
    terms=[(one,-K,a*0,-one),(-one,K*d,a,b)]
    result,meta=focus_from_terms(terms,a,1+b,w,max_focus)
    meta.update({'a':a,'h':h,'b':b,'d':d,'K':K})
    return result,meta

def calibration():
    q=Fraction(1,4);r=Fraction(15,8);K=Fraction(4,3)
    terms=[(Fraction(1),K*(q+Fraction(1,2)),Fraction(0),-q),
           (Fraction(-1),K*r,Fraction(1),Fraction(1,2))]
    alpha=Fraction(1);gamma=q+Fraction(1,2);w=Fraction(7,8)
    return focus_from_terms(terms,alpha,gamma,w,3)

if __name__=='__main__':
    import time,json,resource,sys
    started=time.perf_counter()
    c,m=calibration()
    print('CALIBRATION c2,c3,c4 =',c,flush=True)
    print('CALIBRATION original-time radial F3 =',c[2]*m['w']**3/2,flush=True)
    print('CALIBRATION all homological residuals exact zero:',all(v==0 for row in m['residuals'] for v in row),flush=True)
    f,m=target(Fraction(1),Fraction(22,7),4)
    print('SOURCE_ENDPOINT c2,c3,c4,c5 =',f,flush=True)
    print('SOURCE_ENDPOINT F3 =',f[2]*m['w']**3/2,flush=True)
    print('SOURCE_ENDPOINT all residuals exact zero:',all(v==0 for row in m['residuals'] for v in row),flush=True)
    a=Box('1.012821998680314600068208268899051820974352006')
    h=Box('3.112895114354931694231478861591838762886663535')
    c,m=target(a,h)
    print('CENTER independent focus obstructions:',c,flush=True)
    print('CENTER F4 leading conversion:',c[3]*m['w']**4/2,flush=True)
    print('elapsed_seconds',time.perf_counter()-started,'peak_rss_bytes_macos',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)
