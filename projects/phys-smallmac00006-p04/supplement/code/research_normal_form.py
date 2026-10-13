#!/usr/bin/env python3
"""Target degree-nine normal form, direct ODE transcription.
Rational operations in R[s]/(s^2+omega2), supporting mp and interval dual scalars.
No target focus values are read. Reuses the calibrated conjugacy method, not outputs.
"""
import time,json,resource
from pathlib import Path

class Dual:
    __slots__=('v','da','dh')
    def __init__(self,v,da=0,dh=0):self.v,self.da,self.dh=v,da,dh
    def __add__(x,y):
        if not isinstance(y,Dual):y=Dual(y)
        return Dual(x.v+y.v,x.da+y.da,x.dh+y.dh)
    __radd__=__add__
    def __neg__(x):return Dual(-x.v,-x.da,-x.dh)
    def __sub__(x,y):return x+-dual(y)
    def __rsub__(x,y):return dual(y)+-x
    def __mul__(x,y):
        if not isinstance(y,Dual):y=Dual(y)
        return Dual(x.v*y.v,x.da*y.v+x.v*y.da,x.dh*y.v+x.v*y.dh)
    __rmul__=__mul__
    def __truediv__(x,y):
        if not isinstance(y,Dual):y=Dual(y)
        q=x.v/y.v
        return Dual(q,(x.da-q*y.da)/y.v,(x.dh-q*y.dh)/y.v)
    def __rtruediv__(x,y):return dual(y)/x
    def __bool__(x):return bool(x.v) or bool(x.da) or bool(x.dh)
def dual(x):return x if isinstance(x,Dual) else Dual(x)

W=1
class C:
    __slots__=('a','b')
    def __init__(self,a=0,b=0):self.a,self.b=a,b
    def __add__(x,y):
        if not isinstance(y,C):y=C(y)
        return C(x.a+y.a,x.b+y.b)
    __radd__=__add__
    def __neg__(x):return C(-x.a,-x.b)
    def __sub__(x,y):return x+-cc(y)
    def __rsub__(x,y):return cc(y)+-x
    def __mul__(x,y):
        if not isinstance(y,C):y=C(y)
        return C(x.a*y.a-W*x.b*y.b,x.a*y.b+x.b*y.a)
    __rmul__=__mul__
    def __truediv__(x,y):
        y=cc(y)
        den=y.a*y.a+W*y.b*y.b
        return C((x.a*y.a+W*x.b*y.b)/den,(x.b*y.a-x.a*y.b)/den)
    def conj(x):return C(x.a,-x.b)
    def __bool__(x):return bool(x.a) or bool(x.b)
def cc(x):return x if isinstance(x,C) else C(x)
Z=C();ONE=C(1);S=C(0,1)
def clean(p):return {k:v for k,v in p.items() if v}
def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items():out[k]=out.get(k,Z)+v
    return clean(out)
def scale(p,c):return clean({k:v*c for k,v in p.items()})
def mul(p,q,n):
    out={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            if i+j+k+l<=n:
                key=(i+k,j+l);out[key]=out.get(key,Z)+a*b
    return clean(out)
def powers(p,n):
    out=[{(0,0):ONE}]
    for _ in range(n):out.append(mul(out[-1],p,n))
    return out
def compose(p,h,hb,n):
    hp,bp=powers(h,n),powers(hb,n)
    return add(*(scale(mul(hp[i],bp[j],n),a) for (i,j),a in p.items() if i+j<=n))
def diff(p,axis):
    out={}
    for key,a in p.items():
        k=list(key)
        if k[axis]:
            c=k[axis];k[axis]-=1;out[tuple(k)]=a*c
    return out
def conj(p):return {(j,i):a.conj() for (i,j),a in p.items()}
def binoms(a,n):
    out=[a*0+1]
    for j in range(n):out.append(out[-1]*(a-j)/(j+1))
    return out

def focus(a,h,n=9,check=False,b_override=None):
    global W
    d=h*(h-1)/2;b=(a*h-1)/d if b_override is None else b_override
    K=a/(1+b*d);W=K*a*(d-1)
    aa,bb,yy=binoms(a,n),binoms(b,n),binoms(-a*0-1,n)
    f={};g={}
    for i in range(n+1):
        for j in range(n+1-i):
            if i+j==0:continue
            v=aa[i]*bb[j];inv=yy[j] if i==0 else a*0
            f[(i,j)]=C(inv-v);g[(i,j)]=C(K*(-inv+d*v))
    half=(a*0+1)/2
    u={(1,0):C(half),(0,1):C(half)}
    v={(1,0):C(-a/(2*(1+b)),-1/(2*(1+b))),
       (0,1):C(-a/(2*(1+b)),1/(2*(1+b)))}
    fc,gc=compose(f,u,v,n),compose(g,u,v,n)
    F=add(fc,scale(add(scale(fc,a),scale(gc,1+b)),C(0,1/W)))
    # Linear part is algebraically S*z on the Hopf surface. Remove roundoff only
    # after its exact symbolic derivation in the report; no nonlinear coefficient is reset.
    F[(1,0)]=S;F.pop((0,1),None)
    H={(1,0):ONE};G={(1,0):S};res=[]
    for k in range(2,n+1):
        R=add(compose(F,H,conj(H),k),scale(mul(diff(H,0),G,k),-1),scale(mul(diff(H,1),conj(G),k),-1))
        hn,gn={},{}
        for j in range(k+1):
            l=k-j;v=R.get((j,l),Z)
            if j-l==1:gn[(j,l)]=v
            else:hn[(j,l)]=v/(S*(j-l-1))
        H=add(H,hn);G=add(G,gn)
        if check:
            R=add(compose(F,H,conj(H),k),scale(mul(diff(H,0),G,k),-1),scale(mul(diff(H,1),conj(G),k),-1))
            res.append(max([abs(v.a)+abs(v.b) for v in R.values()]+[0]))
    out=[G.get((j+1,j),Z).a for j in range(1,(n+1)//2)]
    return out,{'d':d,'b':b,'K':K,'omega2':W,'residuals':res,'G':G}

if __name__=='__main__':
    from mpmath import mp
    mp.dps=55;start=time.perf_counter()
    a0=mp.mpf('1.01282');h0=(1+mp.sqrt(1+8*mp.mpf('3.28862')))/2
    print('initial',a0,h0,[mp.nstr(x,25) for x in focus(a0,h0)[0]],flush=True)
    calls=[0]
    def fun(a,h):
        f,_=focus(a,h,7);calls[0]+=1
        print('root_call',calls[0],mp.nstr(a,18),mp.nstr(h,18),*[mp.nstr(x,8) for x in f[1:]],flush=True)
        return f[1],f[2]
    a,h=mp.findroot(fun,(a0,h0),tol=mp.mpf('1e-47'),maxsteps=15)
    f,meta=focus(a,h,9,True)
    out={'method':'A direct original ODE, complex homological conjugacy to degree 9',
         'precision_decimal_digits':mp.dps,'a':str(a),'h':str(h),
         'parameters':{k:str(meta[k]) for k in ['b','d','K','omega2']},
         'real_resonant_coefficients':[str(x) for x in f],
         'conjugacy_residual_by_degree':[str(x) for x in meta['residuals']],
         'normal_form':[{'j':j,'k':k,'real':str(v.a),'s_coefficient':str(v.b)} for (j,k),v in meta['G'].items()],
         'elapsed_seconds':time.perf_counter()-start,
         'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'High precision discovery, not interval enclosure, proof or cycle count.'}
    Path('evidence/research/normal-form-discovery.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)
