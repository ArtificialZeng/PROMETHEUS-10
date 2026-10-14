"""Standard-library diagnostic, not a floating-point interval certificate.
Independent finite-u spatial reflection and reset-origin Volterra calculation.
No cached baseline answers, mutable handoffs, or Monte Carlo are read.
Run: python3 evidence/check_joint_tail.py
"""
import math
from pathlib import Path

def Phi(x): return math.erfc(-x/math.sqrt(2))/2
def phi(x): return math.exp(-x*x/2)/math.sqrt(2*math.pi)
def quad(f,a,b,tol=2e-11):
    if a==b: return 0.
    def go(a,b,fa,fm,fb,old,eps,n):
        m=(a+b)/2; fl=f((a+m)/2);fr=f((m+b)/2)
        l=(m-a)*(fa+4*fl+fm)/6;r=(b-m)*(fm+4*fr+fb)/6
        err=l+r-old
        if abs(err)<=15*eps:return l+r+err/15
        if n==0:raise RuntimeError('quadrature depth exhausted')
        return go(a,m,fa,fl,fm,l,eps/2,n-1)+go(m,b,fm,fr,fb,r,eps/2,n-1)
    fa=f(a);fm=f((a+b)/2);fb=f(b)
    return go(a,b,fa,fm,fb,(b-a)*(fa+4*fm+fb)/6,tol,28)

def q(v,r,a):
    if a==0:return .5
    if v==0:return float(a>0)
    # Independent discounted Brownian first-hit formula, verified against last-reset integral.
    al=math.sqrt(2*r);b=abs(a);s=math.sqrt(v)
    g=math.exp(-al*b)*Phi(al*s-b/s)+math.exp(al*b)*Phi(-al*s-b/s)
    return 1-g/2 if a>0 else g/2

def coeff(T,r,a):
    al=math.sqrt(2*r)
    return math.exp(al*a)*(Phi(al*math.sqrt(T))+quad(
        lambda z:2*r*z*Phi(al*z)*q(max(0.,T-z*z),r,a),0,math.sqrt(T)))

def hs(t,u,r,a):
    al=math.sqrt(2*r);d=u-a
    if t==0:return .5*math.exp(al*a)
    z=d/math.sqrt(t);k=al*math.sqrt(t)
    return (math.exp(al*a+r*t)*(Phi(z-k)-Phi(-k))
            +2*math.exp(al*u)*Phi(-z)-math.exp(al*(u+d)+r*t)*Phi(-z-k))

def initial_spatial(T,u,r,a):
    al=math.sqrt(2*r);s=math.sqrt(T)
    def integrand(y):
        j=Phi(y/s) if y>=u else 2*Phi((y-u)/s)-Phi((y-2*u)/s)
        return al/2*math.exp(al*u-al*abs(y-a))*j
    left=a-max(35/al,14*s);right=u+max(35/al,14*s)
    cuts=sorted(set([left,a,0.,u,right]))
    return sum(quad(integrand,l,h,2e-13) for l,h in zip(cuts,cuts[1:])),left,right

def finite(T,u,r,a,n):
    al=math.sqrt(2*r);dt=T/n;scale=math.exp(al*u)
    ts=[i*dt for i in range(n+1)]
    f=[.5 if a==0 else float(a>0)]+[Phi(a/math.sqrt(t)) for t in ts[1:]]
    qg=[f[0]];integ=0.
    for i in range(1,n+1):
        integ+=dt*r/2*(math.exp(-r*ts[i-1])*f[i-1]+math.exp(-r*ts[i])*f[i])
        qg.append(math.exp(-r*ts[i])*f[i]+integ)
    h=[0.]+[2*Phi((a-u)/math.sqrt(t)) for t in ts[1:]]
    j=[0.]+[2*Phi((a-u)/math.sqrt(t))-Phi((a-2*u)/math.sqrt(t)) for t in ts[1:]]
    weights=[dt*r*math.exp(-r*t) for t in ts]
    ja=[0.]
    for i in range(1,n+1):
        value=scale*math.exp(-r*ts[i])*j[i]+weights[i]/2*scale*h[i]*qg[0]
        value+=sum(weights[k]*(scale*h[k]*qg[i-k]+(1-h[k])*ja[i-k]) for k in range(1,i))
        ja.append(value/(1-weights[0]/2))
    jstat,left,right=initial_spatial(T,u,r,a)
    hh=[hs(t,u,r,a) for t in ts]
    terms=[weights[k]*(hh[k]*qg[n-k]+(1-hh[k]/scale)*ja[n-k]) for k in range(n+1)]
    answer=math.exp(-r*T)*jstat+sum(terms[1:-1])+(terms[0]+terms[-1])/2
    first=math.exp(-r*T)*jstat+sum(weights[k]*hh[k]*qg[n-k]*(.5 if k in (0,n) else 1.) for k in range(n+1))
    # Finite spatial truncation: below left use j<=h(left); above right use j<=1.
    tail=scale*(2*Phi((left-u)/math.sqrt(T))+.5*math.exp(-al*(right-a)))
    return answer,first,jstat,tail

def remainder(T,u,r,a):
    al=math.sqrt(2*r);d=u-a
    return math.exp(al*a+r*T)*Phi((al*T-d)/math.sqrt(T))+2*math.exp(al*u)*(math.exp(-r*T)*Phi(-u/math.sqrt(T))+r*T*Phi(-d/math.sqrt(T)))

def main():
    lines=[]
    def log(s):lines.append(s);print(s)
    log('Proposer diagnostic: ordinary doubles, no rigorous roundoff enclosure; exact proof is joint-tail-proof.md.')
    for a in [-2,-.4,.4,2]:
        for v in [.05,1,3]:
            r=.7
            direct=math.exp(-r*v)*Phi(a/math.sqrt(v))+quad(lambda z:0. if z==0 else 2*r*z*math.exp(-r*z*z)*Phi(a/z),0,math.sqrt(v))
            assert abs(q(v,r,a)-direct)<1e-9
    log('Post-reset q: discounted Brownian hitting formula vs last-reset Gaussian integral, both signs and v=0.05,1,3: PASS (<1e-9).')
    for T,r,a,u in [(1,1,0,3),(1,1,0,5),(1,1,0,8),(1,1,-1,5),(1,1,1,6),(.15,.3,-.4,2),(2,3,.5,9),(3,.2,-2,6)]:
        c=coeff(T,r,a);al=math.sqrt(2*r)
        lo=math.exp(al*a)*Phi(al*math.sqrt(T))
        hi=lo+math.exp(al*a)*quad(lambda z:2*r*z*Phi(al*z),0,math.sqrt(T))
        assert lo<c<hi
        v1=finite(T,u,r,a,300);v2=finite(T,u,r,a,600)
        rem=remainder(T,u,r,a);refine=abs(v1[0]-v2[0])
        extra=2*r*T*math.exp(al*u)*Phi(-(u-a)/math.sqrt(T))
        first_quad=math.exp(-r*T)*v2[2]+quad(lambda z:2*r*z*math.exp(-r*z*z)*hs(z*z,u,r,a)*q(max(0.,T-z*z),r,a),0,math.sqrt(T))
        assert abs(first_quad-c)<=rem+2e-10
        assert abs(v2[0]-c)<=rem+10*refine+1e-9
        assert -10*refine-1e-10 <=v2[0]-v2[1]<=extra+10*refine+1e-10
        lost=hs(T,u,r,a)-v2[2]
        assert -1e-9<=lost<=2*math.exp(al*u)*Phi(-u/math.sqrt(T))+1e-9
        log(f'T={T:g} r={r:g} a={a:g} u={u:g}: C={c:.12g}, published=[{lo:.12g},{hi:.12g}], finite_volterra={v2[0]:.12g}, first_segment_grid={v2[1]:.12g}, first_segment_adaptive={first_quad:.12g}, extra_bound={extra:.4g}, |finite-C|={abs(v2[0]-c):.4g}, R={rem:.4g}, mesh_delta={refine:.4g}, spatial_tail_bound={v2[3]:.3g}; PASS')
    al=math.sqrt(2);I=Phi(al)+(al*phi(al)-Phi(al)+.5)/2
    exact0=Phi(al)+I/2
    assert abs(coeff(1,1,0)-exact0)<1e-9
    log(f'a=0 analytic midpoint check C={exact0:.15g}; q(0) strict=0, quadrature right limit=1/2.')
    # Attack the elementary uniform bound (7) across its switch at d=m.
    for al in [.01,.3,1.4142135623730951,5]:
        for d in [.01,.5,3,10]:
            for m in [0,d*.999,d,d*1.001,d+1,d+5]:
                L=math.exp(-al*(d-m))/2 if d>=m else 1-math.exp(al*(d-m))/2
                diff=math.exp(al*m)/2-math.exp(al*d)*L
                assert diff>=-1e-6*max(1,math.exp(al*m))
                assert diff<=math.exp(al*m)/2*(m>d)+1e-6*max(1,math.exp(al*m))
    log('Laplace tail switch attacks PASS; reset-origin Volterra uses exact renewal kernel and all reset counts, not a time-stepped Brownian simulation.')
    log('Mesh refinement and spatial tail bounds are diagnostics. They are not certified discretization enclosures; exact conclusions rely on proof (2)-(8).')
    Path(__file__).with_name('joint-tail-check.log').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
