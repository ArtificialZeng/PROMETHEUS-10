"""Arb enclosures for a uniform all-ensemble partial theorem.

Exact rational parameter rectangle; interval extensions use endpoint monotonicity.
The analytic reduction and endpoint tail argument are in research-envelope-proof.md.
This code checks scalar inequalities, not scientific novelty or referee acceptance.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json, time, resource, sys, argparse
from pathlib import Path
from fractions import Fraction as Q
import flint
from flint import arb, fmpq, ctx

def A(x):
    if isinstance(x,Q):return arb(fmpq(x.numerator,x.denominator))
    return arb(x)

def ball(lo,hi):return A(lo).union(A(hi))

def hp(r):
    if r==1:return A(0)
    r=A(r);t=(1+r)/2
    return -(t*t.log()+(1-t)*(1-t).log())/A(2).log()

def H(lo,hi):
    assert 0<=lo<=hi<=1
    return hp(hi).union(hp(lo))

def lp(r):
    if r==0:return A(1)
    r=A(r);return r.atanh()/r

def L(lo,hi):
    assert 0<=lo<=hi<1
    return lp(lo).union(lp(hi))

def Ly(lo,hi):
    assert 0<=lo<=hi<1
    def v(y):
        if y==0:return A(1)
        t=A(y).sqrt();return t.atanh()/t
    return v(lo).union(v(hi))

def pars(pl,ph):
    p=ball(pl,ph);q=3*p;al=1-2*ph;ah=1-2*pl
    a=ball(al,ah);b=ball(1-ah*ah,1-al*al)
    return p,q,a,b,al,ah

def eq(pl,ph,rl,rh):
    p,q,a,b,al,ah=pars(pl,ph)
    return (1-q)*(H(al*rl,ah*rh)-H(al,ah))-q*H(rl,rh)

def d(pl,ph,rl,rh):
    p,q,a,b,al,ah=pars(pl,ph)
    return (1-q)*b*(L(al,ah)-L(al*rl,ah*rh))/(2*A(2).log())

def gprime(pl,ph,yl,yh):
    p,q,a,b,al,ah=pars(pl,ph)
    # t^2=a^2+(1-a^2)y is increasing in both a and y.
    tl=al*al+(1-al*al)*yl;th=ah*ah+(1-ah*ah)*yh
    return (-(1-2*q)*Ly(yl,yh)+(1-q)*b*Ly(tl,th))/(2*A(2).log())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--precision',type=int,default=192)
    ap.add_argument('--np',type=int,default=100);ap.add_argument('--nr',type=int,default=500)
    ap.add_argument('--ny',type=int,default=1000);ap.add_argument('--tag',default='192')
    args=ap.parse_args();ctx.prec=args.precision;start=time.monotonic()
    plo,phi=Q(27,250),Q(221,2000);k=Q(3,250);ku=Q(11,1000);r0=Q(93,100);trial=Q(7,8);z0=Q(99,100);y0=z0*z0
    summaries={};failures=[]
    def check(name,val,box):
        if not val>0:failures.append(dict(check=name,box=box,arb=str(val)))
        # Float summaries are readable diagnostics only. Assertions use Arb ordering.
        low=float(val.lower())
        if name not in summaries or low<summaries[name]['minimum_lower_bound_float']:
            summaries[name]=dict(minimum_lower_bound_float=low,arb_at_worst_box=str(val),box=box)
        summaries[name]['boxes_checked']=summaries[name].get('boxes_checked',0)+1
    counts={}
    for i in range(args.np):
        pl=plo+(phi-plo)*i/args.np;ph=plo+(phi-plo)*(i+1)/args.np
        p,q,a,b,al,ah=pars(pl,ph);pb=[str(pl),str(ph)]
        check('transverse_squared_convexity',q-(1-q)*a**4,pb)
        check('center_nonnegative',eq(pl,ph,Q(0),Q(0)),pb)
        check('interior_lower_envelope',d(pl,ph,r0,r0)-A(k),pb)
        # For z>=z0, L(t)-L(z)<=(-log b/2+log(2/(1+z0)))/z0.
        aa=(1-q)*a*a-q
        check('tail_A_positive',aa,pb)
        tail=(-aa*lp(z0)+(1-q)*b*(-b.log()/2+(A(2)/(1+A(z0))).log())/A(z0))/(2*A(2).log())
        check('diagonal_derivative_tail',A(ku)-tail,pb)
        for j in range(args.nr):
            rl=r0+(1-r0)*j/args.nr;rh=r0+(1-r0)*(j+1)/args.nr
            value=eq(pl,ph,rl,rh)-eq(pl,ph,trial,trial)+(d(pl,ph,rl,rh)-A(k))*ball(rl*rl,rh*rh)
            check('exterior_lower_envelope',value,pb+[str(rl),str(rh)])
        for j in range(args.ny):
            yl=y0*j/args.ny;yh=y0*(j+1)/args.ny
            check('diagonal_derivative_compact',A(ku)-gprime(pl,ph,yl,yh),pb+[str(yl),str(yh)])
    # Replace local minimizer counters by exact declared box counts.
    for name in summaries:
        summaries[name]['boxes_checked']=args.np*(args.nr if name=='exterior_lower_envelope' else args.ny if name=='diagonal_derivative_compact' else 1)
    record=dict(job_id=os.environ.get('PHYSICS_JOB_ID'),status='pass' if not failures else 'fail',
        precision_bits=ctx.prec,parameter_interval=[str(plo),str(phi)],q='3p',kappa_lower=str(k),kappa_upper=str(ku),
        radius_split=str(r0),trial_radius=str(trial),tail_z_split=str(z0),
        partition=dict(p=args.np,R=args.nr,y=args.ny),checks=summaries,failures=failures,
        elapsed_seconds=time.monotonic()-start,maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        python=sys.version,python_flint=flint.__version__,
        scope='Strict enclosures for analytic quadratic-envelope conditions. Original interval [0.08,0.125] is not fully covered. Same-worker certificate, pending fresh referee.',
        arithmetic='Exact Fraction grid; Arb rational conversion, outward arithmetic and union. H decreases and L increases; zero entropy and L(0)=1 evaluated by exact continuous limits. No grid maximum used as continuum upper bound.')
    path=Path('evidence')/f'research-envelope-certificate-{args.tag}.json'
    path.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2),flush=True)
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
