"""Direct finite-generator replay, without imports from submitted research code."""
import json, math
from pathlib import Path
import numpy as np
import scipy.linalg as la
import scipy.optimize as opt
import sympy as sp

checks=[]
def record(name,**data):
    obj={'name':name,**data};checks.append(obj);print(json.dumps(obj),flush=True)

# Independently transcribed from OBS primary PDF p.2 Eqs.(2)-(10).
n=7;u=8;d=1
R=sp.zeros(n)
for i in range(n):
    R[(i+1)%n,i]=u;R[(i-1)%n,i]=d;R[i,i]=-u-d
pi=sp.ones(n,1)/n
assert R*pi==sp.zeros(n,1)
assert [sum(R[:,i]) for i in range(n)]==[0]*n
currents=[pi[i]*u-pi[(i+1)%n]*d for i in range(n)]
assert currents==[sp.Integer(1)]*n
affinity=n*sp.log(sp.Rational(u,d));sigma=(u-d)*sp.log(sp.Rational(u,d))
assert sp.simplify(currents[0]*affinity-sigma)==0
eig=la.eigvals(np.array(R).astype(float))
theta=2*math.pi/n
fourier=np.array([u*(np.exp(1j*m*theta)-1)+d*(np.exp(-1j*m*theta)-1) for m in range(n)])
err=max(min(abs(e-z) for z in fourier) for e in eig)
nonzero=sorted([e for e in eig if abs(e)>1e-10],key=lambda e:e.real,reverse=True)
lead=next(e for e in nonzero if e.imag>0)
a=-lead.real;b=lead.imag
sig=float(sigma.evalf(30));N=b/(2*math.pi*a);DS=2*math.pi*sig/b
DS8=2*math.pi*float(affinity)/(n*math.sin(theta))
N9=math.cos(math.pi/n)/math.sin(math.pi/n)*math.tanh(float(affinity)/(2*n))/(2*math.pi)
DS10=4*math.pi/math.sin(theta)*math.atanh(2*math.pi*N*math.tan(math.pi/n))
assert err<1e-11 and abs(DS-DS8)<1e-11 and abs(N-N9)<1e-12 and abs(DS-DS10)<1e-11
assert b>=a and nonzero[0].real-nonzero[2].real>0
record('primary uniform n=7,u=8,d=1 reconstruction',status='pass',stationarity='exact rational',J=str(currents[0]),sigma_exact=str(sigma),characteristic_polynomial=str(R.charpoly().as_expr()),spectrum_max_error=err,a=a,b=b,N=N,DeltaS=DS,Y=sig*a/b**2,nonzero_leading_gap=float(nonzero[0].real-nonzero[2].real),published_equations=[8,9,10])

# Nonuniform direct entropy convention check; no given stationary vector.
uf=np.array([2.,3.,5.,7.,11.,13.,17.]);df=np.array([1.,2.,1.,3.,2.,4.,3.])
def forward(u,d):
    nn=len(u);M=np.zeros((nn,nn))
    for i in range(nn):
        M[(i+1)%nn,i]=u[i];M[(i-1)%nn,i]=d[i];M[i,i]=-u[i]-d[i]
    return M
Rf=forward(uf,df);C=Rf.copy();C[-1,:]=1;rhs=np.zeros(7);rhs[-1]=1
pstat=la.solve(C,rhs);f=pstat*uf;rev=np.roll(pstat*df,-1);j=f-rev
edge=float(np.dot(j,np.log(f/rev)))
direct=0.;rate=0.
for i in range(7):
    for k in [(i+1)%7,(i-1)%7]:
        fij=pstat[i]*Rf[k,i];gij=pstat[k]*Rf[i,k]
        direct+=fij*math.log(fij/gij);rate+=fij*math.log(Rf[k,i]/Rf[i,k])
JA=float(j.mean()*np.log(uf/df).sum())
assert min(pstat)>0 and max(abs(j-j.mean()))<1e-12
assert max(abs(edge-direct),abs(edge-rate),abs(edge-JA))<1e-10
record('heterogeneous stationary entropy normalization',status='pass',pi=pstat.tolist(),stationarity_residual=float(max(abs(Rf@pstat))),current_spread=float(max(abs(j-j.mean()))),edge_entropy=edge,directed_flow_entropy=direct,source_directed_rate_entropy=rate,current_affinity_entropy=JA)

def direct_setup(n):
    th=2*math.pi/n;t=math.tan(math.pi/n);g=(1-t)/(2*t)
    Q=forward(np.full(n,n*(g+1)),np.full(n,n*g)).T
    f=np.exp(1j*th*np.arange(n));left=np.conjugate(f)/n
    lam=n*((g+1)*(np.exp(1j*th)-1)+g*(np.exp(-1j*th)-1))
    border=np.zeros((n+1,n+1),dtype=complex)
    border[:n,:n]=Q-lam*np.eye(n);border[:n,n]=f;border[n,:n]=left
    lu=la.lu_factor(border)
    return t,g,Q,f,left,lam,lu

def curvature(n,h,p,setup):
    t,g,Q,f,left,lam,lu=setup
    prev=np.roll(h,1)
    u1=n*(g*h-(g+1)*p);d1=n*(g*prev-g*p)
    u2=2*n*((g+1)*p*p-g*h*p);d2=2*n*(g*p*p-g*prev*p)
    Q1=forward(u1,d1).T;Q2=forward(u2,d2).T
    lam1=left@(Q1@f)
    assert abs(lam1)<1e-9
    rhs=np.r_[-Q1@f,0j];fdot=la.lu_solve(lu,rhs)[:n]
    lam2=left@(Q2@f+2*Q1@fdot)
    lr=-2*n*(1-math.cos(2*math.pi/n))
    r2=-(lam2.real+lam2.imag)/lr
    A2=(2*g+1)/(g+1)**2*np.sum(h*h)-n*r2/(g*(g+1))
    A0=n*math.log((g+1)/g);b=lam.imag
    return float(A2/b-A0*lam2.imag/b**2)

def closed(n):
    t=math.tan(math.pi/n);x=t*t;L=math.log((1+t)/(1-t));S=L*(1-x)**2+2*t*(1+x)
    sectors=[]
    for k in range(1,(n-1)//2+1):
        v=math.tan(math.pi*k/n)
        Dp=(1-x)**2*(v+2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
        Dm=(1-x)**2*(v-2*t)**2+4*t**4*v*v+t*t*(1+6*x-3*x*x)
        D=Dp*Dm
        Ph=2*t*t*(1+x)*(L*(1-x)**2*(3*x-1)+2*t*(1+x)**2)+(v*v-t*t)*(5*x*x-2*x+1)*S
        Pc=L*t*t*(3-x)*(1-x)*(1+x)-2*t**3*(x*x-6*x+1)+v*v*(L*(1-x)*(1+x)*(3*x-1)+2*t*(7*x*x-2*x-1))
        hh=t*(1+x)*(1+v*v)*Ph/((1+t)**2*D);pp=(1+t)/(1-t)*hh
        hc=-t*(1+x)**2*Pc/((1+t)*D);hs=v*hc
        block=np.array([[hh,0,hc,hs],[0,hh,-hs,hc],[hc,-hs,pp,0],[hs,hc,0,pp]])
        sectors.append((k,block))
    if n%2==0:
        hh=2*t*(1+x)*S/((1+t)**2*(5*x*x-2*x+1))
        sectors.append((n//2,np.diag([hh,(1+t)/(1-t)*hh])))
    return sectors

def basis(n):
    ang=2*math.pi*np.arange(n)/n;vectors=[]
    for k,block in closed(n):
        c=np.cos(k*ang);si=np.sin(k*ang);zero=np.zeros(n)
        if block.shape==(4,4):vectors.extend([(c,zero),(si,zero),(zero,c),(zero,si)])
        else:vectors.extend([(c,zero),(zero,c)])
    return vectors

for n in [5,6,7,8,11,12]:
    setup=direct_setup(n);vectors=basis(n);dim=len(vectors)
    diag=np.array([curvature(n,h,p,setup) for h,p in vectors])
    H=np.diag(diag)
    for i in range(dim):
        for j in range(i+1,dim):
            h=vectors[i][0]+vectors[j][0];p=vectors[i][1]+vectors[j][1]
            H[i,j]=H[j,i]=(curvature(n,h,p,setup)-diag[i]-diag[j])/2
    expected=la.block_diag(*[block for k,block in closed(n)])
    err=float(np.max(np.abs(H-expected)));mineig=float(np.linalg.eigvalsh(H).min())
    assert err<1e-9 and mineig>0
    record('full direct constrained Hessian',status='pass',n=n,dimension=dim,max_block_residual=err,min_eigenvalue=mineig,method='linear-rate derivatives and direct bordered eigenvector solve; all mixed directions by polarization')

# Independently restore the exact nonlinear finite generator on fixed q=1.
n=8;setup=direct_setup(n);t,g,Q,f,left,lam,lu=setup
angles=2*math.pi*np.arange(n)/n
h=.7*np.cos(angles)+.3*np.sin(3*angles)+.2*(-1.)**np.arange(n)
p=.5*np.sin(angles)+.25*np.cos(2*angles)-.15*(-1.)**np.arange(n)
pred=curvature(n,h,p,setup);Y0=math.log((g+1)/g)/math.sin(2*math.pi/n)
def restored(eps):
    pi=(1+eps*p)/n
    def calc(r):
        flows=g+r+eps*g*h
        u=(flows+1)/pi;d=np.roll(flows,1)/pi
        R=forward(u,d);eig=la.eigvals(R)
        eligible=[z for z in eig if z.imag>1e-7]
        z=min(eligible,key=lambda z:abs(z-lam))
        return flows,R,z
    rr=opt.brentq(lambda r:calc(r)[2].real+calc(r)[2].imag,-g*.1,g*.1,xtol=1e-14)
    flows,R,z=calc(rr);A=np.log((flows+1)/flows).sum();y=A*(-z.real)/(z.imag*z.imag)
    other=[e for e in la.eigvals(R) if abs(e)>1e-7 and abs(e-z)>1e-7 and abs(e-z.conjugate())>1e-7]
    assert np.min(flows)>0 and np.min(pi)>0 and np.max(abs(R@pi))<1e-10
    assert z.real-max(e.real for e in other)>0 and abs(z.real+z.imag)<1e-10
    return y
finite=[]
for eps in [0.01,0.003,0.001,0.0003]:
    val=(restored(eps)+restored(-eps)-2*Y0)/eps**2
    finite.append({'epsilon':eps,'finite_curvature':val,'predicted':pred,'absolute_error':abs(val-pred)})
assert finite[-1]['absolute_error']<1e-5
record('nonlinear fixed-coherence finite difference with leading ordering',status='pass',n=n,checks=finite,interpretation='numerical diagnostic only; exact proof is symbolic reduction plus analytic sign argument')
out={'status':'pass','checks':checks,'independence':'No discovery imports, input matrices, stationary vectors or eigenvalue caches read. Parameters transcribed from primary source/model; submitted closed formulas used only as comparison targets.'}
Path('evidence/independent-direct-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass','checks_completed':len(checks)}),flush=True)
