"""Proposer exact checks and supplementary numerical replay; no referee acceptance.
Run with python3 from the project root.
Uses already-installed SymPy/mpmath; independent renewal is retained, unmodified.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,random
import sympy as s
import mpmath as mp
sys.path.insert(0,str(Path('evidence/reproduction').resolve()))
from determinant_a import determinant_cumulants
from renewal_b import periodic_cycle_cumulants
p,d=s.symbols('p d',positive=True)
H=(d*d+1)/(2*d);t=d*p*(2+p)/(1+2*p)**2;z=d*d*p*p/(1+2*p)**3
V=H-2*t;N=3*H*H-1-6*H*t+6*z
Q=3*H*(5*H*H-3)-12*(3*H*H-1)*t+12*H*t*t+24*H*z
PS=4*(d*d-1)*p*p+(12*d*d-4)*p-(d*d-1)**2
PK=8*(d*d-1)*p**3+(-4*d**4+24*d*d-12)*p*p+(2*d**4+12*d*d-6)*p-(d*d-1)**2*(d*d+1)
assert s.factor(2*V*s.diff(N,p)-3*N*s.diff(V,p)-3*(p-1)*PS/(d*(2*p+1)**5))==0
assert s.factor(V*s.diff(Q,p)-2*Q*s.diff(V,p)-6*(p-1)*PK/(d*d*(2*p+1)**6))==0
assert s.factor(s.diff(t,p)-2*d*(1-p)/(1+2*p)**3)==0
print('PASS exact: both derivative factorizations and monotone t(p)')
y,v=s.symbols('y v',positive=True);pu=(y-1)**2/(y*y+y+1);dd=(y**3+1)/(y**3-1)
GS=y**6-3*y**4+2*y**3-3*y**2+1
GK=2*y**8-y**7-8*y**6+9*y**5-8*y**4+9*y**3-8*y**2-y+2
assert s.factor(PS.subs({p:pu,d:dd})-8*(y*y-y+1)**3*GS/((y-1)**4*(y*y+y+1)**4))==0
assert s.factor(PK.subs({p:pu,d:dd})-8*(y*y+1)*(y*y-y+1)**4*GK/((y-1)**6*(y*y+y+1)**6))==0
expansions={}
for name,G in [('S',GS),('K',GK)]:
    poly=s.Poly(s.expand(G.subs(y,v+2)),v)
    assert all(c>0 for c in poly.all_coeffs())
    expansions[name]=[int(c) for c in poly.all_coeffs()]
    print('PASS exact:',name,'positive expansion at y=2:',poly.as_expr())
u=s.symbols('u0:3',positive=True);w=s.symbols('w0:3',positive=True);ss=s.symbols('s')
esc=[u[i]+w[(i-1)%3] for i in range(3)]
c1=sum(u[i]*u[j]+w[i]*w[j] for i,j in ((0,1),(0,2),(1,2)))+sum(u[i]*w[(i+1)%3] for i in range(3));c2=sum(u)+sum(w)
det_without_cycle=s.prod(ss+e for e in esc)-sum(u[i]*w[i]*(ss+esc[(i+2)%3]) for i in range(3))
assert s.expand(det_without_cycle-(ss**3+c2*ss**2+c1*ss+s.prod(u)+s.prod(w)))==0
xx=s.symbols('x0:3');quad=sum(esc[i]*xx[i]**2 for i in range(3))-2*sum(s.sqrt(u[i]*w[i])*xx[i]*xx[(i+1)%3] for i in range(3))
assert s.expand(quad-sum((s.sqrt(u[i])*xx[i]-s.sqrt(w[i])*xx[(i+1)%3])**2 for i in range(3)))==0
aa,bb,cc=s.symbols('a b c');e1=aa+bb+cc;e2=aa*bb+aa*cc+bb*cc
assert s.expand(e2**2-3*aa*bb*cc*e1-((aa*bb-aa*cc)**2+(aa*bb-bb*cc)**2+(aa*cc-bb*cc)**2)/2)==0
print('PASS exact: symmetric determinant, sum-of-squares positivity, coefficient inequality')
r,k,eta=s.symbols('r k eta',positive=True);C=(eta-1)**2;q=C/r**2;h=eta/k**2
B=r*(r-2*k);E=r+(eta-1)*k;FF=eta*r-(eta-1)*k
ur=[eta*E/(k*B),k*FF/E,eta*B/FF];wr=[B/E,k*E/FF,FF/(k*B)]
f=2*r*r*k**3-(r**3-C)*k*k+eta*r*r
def remzero(expr):
    num=s.fraction(s.cancel(expr))[0]
    assert s.factor(s.rem(num,f,k))==0
assert s.factor(s.prod(ur)-eta**2)==0 and s.factor(s.prod(wr)-1)==0
for i in range(3):
    remzero(ur[i]+wr[(i-1)%3]-(r-(h if i==0 else k)))
    assert s.factor(ur[i]*wr[i]-(k*k if i==1 else eta/k))==0
remzero(sum(ur)+sum(wr)-(2*r+q))
c1r=sum(ur[i]*ur[j]+wr[i]*wr[j] for i,j in ((0,1),(0,2),(1,2)))+sum(ur[i]*wr[(i+1)%3] for i in range(3))
remzero(c1r-(r*r+2*r*q))
print('PASS exact: physical rate products, all three escape diagonals, off-diagonal squares and both coefficients')
# Reflection-family rank curve retained as a diagnostic, not needed for global proof.
rr,hh=s.symbols('rr hh',positive=True)
cr1=32/rr+16*rr**2+2/hh+hh**2+4/(rr**2*hh**2)+8*rr*hh
cr2=4/rr**2+8*rr+1/hh**2+2*hh
J=s.factor(s.diff(cr1,rr)*s.diff(cr2,hh)-s.diff(cr1,hh)*s.diff(cr2,rr))
assert s.factor(J+16*(-hh**3*rr+2*hh*rr**3-2*hh+rr)*(hh**3*rr+2*hh*rr**3-2*hh-rr)/(hh**5*rr**5))==0
print('PASS exact: reflection-family rank curve factors into two branches')
def coeff_rates(rates):
    uu,ww=rates[:3],rates[3:];U=uu[0]*uu[1]*uu[2];W=ww[0]*ww[1]*ww[2];D=U-W;HH=(U+W)/D
    c1v=sum(uu[i]*uu[j]+ww[i]*ww[j] for i,j in ((0,1),(0,2),(1,2)))+sum(uu[i]*ww[(i+1)%3] for i in range(3));c2v=sum(rates)
    tv=D*c2v/c1v**2;zv=D*D/c1v**3;vv=HH-2*tv;nn=3*HH*HH-1-6*HH*tv+6*zv
    qq=3*HH*(5*HH*HH-3)-12*(3*HH*HH-1)*tv+12*HH*tv*tv+24*HH*zv
    return U/W,tv,zv,vv,nn,qq
rng=random.Random(2695)
for ratio in (64,729,4096):
    for _ in range(12):
        u0,u1,w0,w1,w2=[F(rng.randint(1,30),rng.randint(1,15)) for _ in range(5)]
        rates=[u0,u1,ratio*w0*w1*w2/u0/u1,w0,w1,w2]
        ka=determinant_cumulants(rates);kb=periodic_cycle_cumulants(rates[:3],rates[3:]);assert ka==kb
        _,_,_,vv,nn,qq=coeff_rates(rates)
        assert [kb[j]/kb[0]**(j+1) for j in (1,2,3)]==[vv,nn,qq]
print('PASS exact: 36 heterogeneous rational samples over three affinities, direct determinant versus independent renewal')
def bisect(fun,lo,hi,steps):
    assert fun(lo)<0<fun(hi)
    for _ in range(steps):
        mid=(lo+hi)/2
        if fun(mid)>0:hi=mid
        else:lo=mid
    return (lo+hi)/2
def evaluate(affinity,dps):
    mp.mp.dps=dps;A=mp.mpf(affinity) if affinity!='log64' else mp.log(64)
    et=mp.exp(A/2);dy=(et+1)/(et-1);HH=(dy*dy+1)/(2*dy);yy=mp.exp(A/6);CC=(et-1)**2
    puv=(yy-1)**2/(yy*yy+yy+1)
    PSf=lambda x:4*(dy*dy-1)*x*x+(12*dy*dy-4)*x-(dy*dy-1)**2
    PKf=lambda x:8*(dy*dy-1)*x**3+(-4*dy**4+24*dy*dy-12)*x*x+(2*dy**4+12*dy*dy-6)*x-(dy*dy-1)**2*(dy*dy+1)
    rows=[]
    for name,fun in [('S',PSf),('K',PKf)]:
        pv=bisect(fun,mp.mpf(0),puv,4*dps)
        rv=(CC/pv)**(mp.mpf(1)/3);qv=CC/rv**2;Lv=rv-qv
        kv=bisect(lambda x:2*x+et/x**2-Lv,yy,rv/2,4*dps)
        bv=rv*(rv-2*kv);ev=rv+(et-1)*kv;fv=et*rv-(et-1)*kv
        rates=[et*ev/(kv*bv),kv*fv/ev,et*bv/fv,bv/ev,kv*ev/fv,fv/(kv*bv)]
        tv=dy*pv*(2+pv)/(1+2*pv)**2;zv=dy*dy*pv*pv/(1+2*pv)**3
        vv=HH-2*tv;nn=3*HH*HH-1-6*HH*tv+6*zv
        qq=3*HH*(5*HH*HH-3)-12*(3*HH*HH-1)*tv+12*HH*tv*tv+24*HH*zv
        Sv=mp.sqrt(A)*nn/vv**mp.mpf('1.5');Kv=A*qq/vv**2
        assert all(x>0 for x in rates)
        Rat,tr,zr,vr,nr,qr=coeff_rates(rates)
        errors=[abs(Rat/et**2-1),abs(tr-tv),abs(zr-zv),abs(vr-vv),abs(nr-nn),abs(qr-qq)]
        assert max(errors)<mp.mpf(10)**(-dps+12)
        rows.append({'observable':name,'p':mp.nstr(pv,65),'r':mp.nstr(rv,65),'q':mp.nstr(qv,65),'k':mp.nstr(kv,65),'rates':[mp.nstr(x,65) for x in rates],'S':mp.nstr(Sv,65),'K':mp.nstr(Kv,65),'max_numeric_identity_residual':mp.nstr(max(errors),6)})
    return rows
records=[]
for av in ['log64','6','12','30']:
    low=evaluate(av,90);high=evaluate(av,170)
    for a,b in zip(low,high):
        assert abs(mp.mpf(a['S'])-mp.mpf(b['S']))<mp.mpf('1e-60')
        assert abs(mp.mpf(a['K'])-mp.mpf(b['K']))<mp.mpf('1e-60')
    records.append({'affinity':av,'precision_digits':[90,170],'values':high})
    print('PASS supplementary numeric: A=',av,'90/170-digit rate/spectral identities agree')
# Exact independent renewal on rational approximants at R=64, through 4 cumulants.
approx=[]
for row in records[0]['values']:
    rrates=[F(x).limit_denominator(10**20) for x in row['rates']]
    rrates[2]=64*rrates[3]*rrates[4]*rrates[5]/rrates[0]/rrates[1]
    ka=determinant_cumulants(rrates);kb=periodic_cycle_cumulants(rrates[:3],rrates[3:]);assert ka==kb
    Rat,tv,zv,vv,nn,qq=coeff_rates(rrates);assert Rat==64
    assert [kb[j]/kb[0]**(j+1) for j in (1,2,3)]==[vv,nn,qq]
    mp.mp.dps=100
    cv=lambda x:mp.mpf(x.numerator)/x.denominator
    Sv=mp.sqrt(mp.log(64))*cv(kb[2])/cv(kb[1])**mp.mpf('1.5')
    Kv=mp.log(64)*cv(kb[3])/cv(kb[1])**2
    assert abs(Sv-mp.mpf(row['S']))<mp.mpf('1e-35')
    assert abs(Kv-mp.mpf(row['K']))<mp.mpf('1e-35')
    approx.append({'observable':row['observable'],'rates':[str(x) for x in rrates],'cumulants':[str(x) for x in kb],'S':mp.nstr(Sv,45),'K':mp.nstr(Kv,45),'scope':'Exact rational determinant/renewal agreement; proximity to optimizer is supplementary numerical, not certified enclosure.'})
    print('PASS exact independent renewal: rational fixed-affinity approximant of',row['observable'],'optimizer')
sourcehash=hashlib.sha256(Path('source.md').read_bytes()).hexdigest()
assert sourcehash=='69eae5ae077a5e4977e2b4141bcc0c02848f2a178b23a7855857b63db1a46ae1'
Path('evidence/research/spectral-envelope-values.json').write_text(json.dumps({'scope':'Exact analytic envelopes N=3 A>=log64; decimal values supplementary, no independent acceptance.','positive_expansion_coefficients':expansions,'precision_replay':records,'rational_renewal_approximants':approx,'source_sha256':sourcehash},indent=2)+'\n')
print('PASS immutable original source hash; all proposer checks complete')
