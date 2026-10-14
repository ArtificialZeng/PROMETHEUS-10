#!/usr/bin/env python3
"""High-precision proposal and elementary interval contraction for R4 equations.

Only +,-,*,/,sin,cos and pi from mpmath.iv enter the certificate. findroot and
the numerical inverse merely propose an exact decimal center/preconditioner.
"""
import json
import math
from pathlib import Path

import mpmath as mp

ORDER=7
mp.mp.dps=100
mp.iv.dps=80

class AD:
    def __init__(self,val,grad=None):
        self.val=val
        self.grad=[mp.iv.mpf(0) for _ in range(3)] if grad is None else grad
    @staticmethod
    def cast(x):
        return x if isinstance(x,AD) else AD(mp.iv.mpf(x))
    def __add__(self,other):
        other=AD.cast(other)
        return AD(self.val+other.val,[x+y for x,y in zip(self.grad,other.grad)])
    __radd__=__add__
    def __neg__(self):return AD(-self.val,[-x for x in self.grad])
    def __sub__(self,other):return self+-AD.cast(other)
    def __rsub__(self,other):return AD.cast(other)+-self
    def __mul__(self,other):
        other=AD.cast(other)
        return AD(self.val*other.val,[x*other.val+self.val*y for x,y in zip(self.grad,other.grad)])
    __rmul__=__mul__
    def __truediv__(self,other):
        other=AD.cast(other)
        return AD(self.val/other.val,[(x*other.val-self.val*y)/(other.val*other.val) for x,y in zip(self.grad,other.grad)])
    def __rtruediv__(self,other):return AD.cast(other)/self
    def sin(self):return AD(mp.iv.sin(self.val),[mp.iv.cos(self.val)*x for x in self.grad])
    def cos(self):return AD(mp.iv.cos(self.val),[-mp.iv.sin(self.val)*x for x in self.grad])

def mul(a,b):
    z=a[0]*0
    out=[z for _ in range(ORDER+1)]
    for i in range(min(len(a),ORDER+1)):
        for j in range(min(len(b),ORDER+1-i)):
            out[i+j]=out[i+j]+a[i]*b[j]
    return out

def power(a,k):
    r=[a[0]*0 for _ in range(ORDER+1)];r[0]=r[0]+1
    for _ in range(k):r=mul(r,a)
    return r

def inv(a):
    r=[a[0]*0 for _ in range(ORDER+1)];r[0]=1/a[0]
    for k in range(1,ORDER+1):
        r[k]=-sum(a[j]*r[k-j] for j in range(1,min(len(a),k+1)))/a[0]
    return r

def residues(v,c,d,interval=False):
    zero=v*0
    one=zero+1
    u=one/2
    tau=AD(2*mp.iv.pi) if interval else 2*mp.pi
    s=u*u+v*v-c
    vals=[zero for _ in range(4)]
    for idx,(rho,omega) in enumerate(((u,v),(v,u))):
        h=[2*rho*(rho*rho-omega*omega),5*rho*rho-omega*omega,4*rho,one]+[zero]*4
        p=[zero]+h[:-1]
        z=[rho,one]+[zero]*6
        p3=[aa-s*bb for aa,bb in zip(power(z,3),z)]
        q=[aa-d*bb for aa,bb in zip(mul(z,p),p3)]
        if idx==0:
            # tau*u=pi exactly, avoiding an unnecessary trigonometric enclosure.
            sr=zero;cr=-one
        elif interval:
            sr=(tau*rho).sin();cr=(tau*rho).cos()
        else:
            sr=mp.sin(tau*rho);cr=mp.cos(tau*rho)
        derivs=[sr,cr,-sr,-cr]
        sn=[];tp=one
        for k in range(ORDER+1):
            sn.append(tp*derivs[k%4]/math.factorial(k));tp=tp*tau
        hi=inv(h)
        for j,n in enumerate((1,3,5,7)):
            vals[j]=vals[j]+2*mul(mul(sn,power(q,n-1)),power(hi,n+1))[n]
    return vals

def equations(v,c,d):return tuple(residues(v,c,d)[1:])

def encode(iv):
    lo,hi=iv._mpi_
    return {'lower_decimal_display':mp.nstr(mp.mpf(lo),90),
            'upper_decimal_display':mp.nstr(mp.mpf(hi),90),
            'binary_endpoints_exact':[list(lo),list(hi)]}

def upper(iv):return mp.mpf(iv._mpi_[1])

def certificate(center_strings,radius_string):
    center=[mp.iv.mpf(s) for s in center_strings]
    radius=mp.iv.mpf(radius_string)
    X=[x+mp.iv.mpf(['-'+radius_string,radius_string]) for x in center]
    variables=[]
    for j,x in enumerate(X):
        grad=[mp.iv.mpf(1 if j==k else 0) for k in range(3)]
        variables.append(AD(x,grad))
    fv=residues(*variables,interval=True)[1:]
    J=[[fv[j].grad[k] for k in range(3)] for j in range(3)]
    point=[mp.mpf(s) for s in center_strings]
    Jpoint=mp.matrix([[mp.diff(lambda zz:equations(*(point[:k]+[zz]+point[k+1:]))[j],point[k]) for k in range(3)] for j in range(3)])
    Ymp=Jpoint**-1
    Ystrings=[[mp.nstr(Ymp[j,k],65) for k in range(3)] for j in range(3)]
    Y=[[mp.iv.mpf(ss) for ss in row] for row in Ystrings]
    pointvals=residues(*(AD(x) for x in center),interval=True)[1:]
    F0=[ff.val for ff in pointvals]
    E=[[mp.iv.mpf(1 if j==k else 0)-sum(Y[j][l]*J[l][k] for l in range(3)) for k in range(3)] for j in range(3)]
    correction=[-sum(Y[j][k]*F0[k] for k in range(3)) for j in range(3)]
    rows=[sum(abs(ee) for ee in row) for row in E]
    image_bounds=[abs(correction[j])+rows[j]*radius for j in range(3)]
    strict=[upper(bb)<mp.mpf(radius_string) for bb in image_bounds]
    contract=all(upper(rr)<1 for rr in rows)
    # A fixed point of x-YF(x) is a zero: ||I-YJ||<1 implies invertibility of YJ,
    # and hence of the square matrix Y. The contraction is in the infinity norm.
    allvals=residues(*variables,interval=True)
    v,c,d=variables
    a=v*v/(4*c);b=AD(1)/4+v*v-c-a
    product=a*b*c*d
    f1=(product*allvals[0]).val
    positivity=[mp.mpf(ad.val._mpi_[0])>0 for ad in (a,b,c,d)]
    result={'method':'Banach contraction with interval-enclosed analytic Jacobian and exact decimal preconditioner',
            'interval_library':'mpmath.iv; elementary arithmetic and sin/cos/pi only',
            'mpmath_version':mp.__version__,'interval_dps':mp.iv.dps,
            'center_coordinates':['v','J3_squared','J4_squared'],
            'center_exact_decimal':center_strings,'radius_exact_decimal':radius_string,
            'preconditioner_exact_decimal':Ystrings,
            'box':list(map(encode,X)),'F_at_center':list(map(encode,F0)),
            'jacobian_box':[[encode(e) for e in row] for row in J],
            'I_minus_Y_J':[[encode(e) for e in row] for row in E],
            'center_correction':list(map(encode,correction)),
            'contraction_row_bounds':list(map(encode,rows)),
            'image_offset_upper_bounds':list(map(encode,image_bounds)),
            'strict_self_mapping_by_coordinate':strict,'strict_contraction':contract,
            'positive_squared_couplings':positivity,'linear_response_enclosure':encode(f1),
            'linear_response_excludes_zero':upper(f1)<0,
            'certificate_pass':all(strict) and contract and all(positivity) and upper(f1)<0}
    return result

def main():
    refined=mp.findroot(equations,(mp.mpf('1.548768524924036'),mp.mpf('1.2954401557316686'),mp.mpf('0.6861553432828776')),tol=mp.mpf('1e-90'),maxsteps=30)
    center_strings=[mp.nstr(zz,65) for zz in refined]
    rec=certificate(center_strings,'1e-40')
    u=mp.mpf(1)/2;v,c,d=refined
    a=v*v/(4*c);b=u*u+v*v-c-a
    rec['numerical_proposal']={'v_c_d':[mp.nstr(zz,95) for zz in refined],
        'J':[mp.nstr(mp.sqrt(zz),95) for zz in (a,b,c,d)],
        'residue_equations_at_proposal':[mp.nstr(zz,15) for zz in equations(*refined)],
        'linear_response':mp.nstr(a*b*c*d*residues(*refined)[0],95),
        'abcd':mp.nstr(a*b*c*d,95)}
    Path('evidence/research-root-certificate.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'certificate_pass':rec['certificate_pass'],
        'strict_self_mapping_by_coordinate':rec['strict_self_mapping_by_coordinate'],
        'strict_contraction':rec['strict_contraction'],
        'row_norm_upper':[rr['upper_decimal_display'] for rr in rec['contraction_row_bounds']],
        'center':center_strings,'linear_response':rec['numerical_proposal']['linear_response'],
        'abcd':rec['numerical_proposal']['abcd']}),flush=True)
    assert rec['certificate_pass']

if __name__=='__main__':main()
