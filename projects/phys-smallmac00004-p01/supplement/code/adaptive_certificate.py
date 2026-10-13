#!/usr/bin/env python3
"""Fresh referee: independent adaptive rational-box proof replay.

Written from primary channel spectra and the submitted analytic inequalities.
Does not read/import proposer code, numeric optima, caches or certificate output.
Arb 256-bit arithmetic is shared infrastructure, not a second arithmetic library.
Uses z (not z^2), adaptive dyadic boxes, cancelled entropy differences, b=4p(1-p).
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import argparse, json, time, resource, sys, hashlib
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import flint
from flint import arb, ctx

JOB = 'phys-smallmac00004-p01-referee-64603a9bf05d'
P0, P1 = Q(27,250), Q(221,2000)
R0, RT, Z0 = Q(93,100), Q(7,8), Q(99,100)
KL, KU = Q(3,250), Q(11,1000)

def A(q):
    q = Q(q)
    return arb(q.numerator) / q.denominator

def box(l, h):
    return A(l).union(A(h))

def entropy_at(r):
    # H(r), with endpoints imposed from the known physical domain.
    if r == 0: return arb(1)
    if r == 1: return arb(0)
    v = (1-r)/2
    w = (1+r)/2
    return -(v*v.log()+w*w.log())/LN2

def H(r):
    lo, hi = max(arb(0),r.lower()), min(arb(1),r.upper())
    assert lo <= hi and lo >= 0 and hi <= 1
    # H is decreasing on [0,1]. Both endpoint balls enclose exact values.
    return entropy_at(hi).union(entropy_at(lo))

def psi_at(r):
    if r == 0: return arb(1)
    # Use elementary logarithms rather than Arb's atanh.
    return ((1+r).log()-(1-r).log())/(2*r)

def L(r):
    lo,hi=max(arb(0),r.lower()),r.upper()
    assert lo >= 0 and hi < 1 and lo <= hi
    return psi_at(lo).union(psi_at(hi))

def params(p):
    return 3*p, 1-2*p, 4*p*(1-p)

def radial_d(p,r):
    q,a,b=params(p)
    return (1-q)*b*(L(a)-L(a*r))/(2*LN2)

def condition(name, ends):
    p=box(*ends[0]); q,a,b=params(p)
    if name=='center_positive':
        return (1-q)*(1-H(a))-q
    if name=='transverse_convex':
        return q-(1-q)*a**4
    if name=='tail_coefficient_positive':
        return (1-q)*a*a-q
    if name=='lower_inner':
        return radial_d(p,A(R0))-A(KL)
    if name=='lower_outer':
        r=box(*ends[1])
        # E(r)-E(RT): cancel the shared environmental entropy exactly.
        e_difference=(1-q)*(H(a*r)-H(a*A(RT)))-q*(H(r)-H(A(RT)))
        return e_difference+(radial_d(p,r)-A(KL))*r*r
    if name=='upper_compact':
        z=box(*ends[1])
        t=(1-b*(1-z*z)).sqrt()
        return A(KU)-(-(1-2*q)*L(z)+(1-q)*b*L(t))/(2*LN2)
    if name=='upper_tail':
        coeff=(1-q)*a*a-q
        delta=(-b.log()/2+(2/(1+A(Z0))).log())/A(Z0)
        bound=(-coeff*L(A(Z0))+(1-q)*b*delta)/(2*LN2)
        return A(KU)-bound
    raise ValueError(name)

def certify(name,domain,max_boxes,seconds):
    pending=[(domain,0)]
    stats={'name':name,'domain':[[str(x),str(y)] for x,y in domain],
           'evaluated':0,'accepted_leaves':0,'max_depth':0,
           'minimum_certified_lower':None,'worst_box':None}
    full_volume=Q(1)
    for lo,hi in domain: full_volume*=hi-lo
    accepted_volume=Q(0)
    digest=hashlib.sha256()
    start=time.monotonic()
    while pending:
        if stats['evaluated']>=max_boxes or time.monotonic()-start>seconds:
            stats.update(status='incomplete',pending_boxes=len(pending))
            return stats
        ends,depth=pending.pop()
        margin=condition(name,ends)
        stats['evaluated']+=1
        stats['max_depth']=max(stats['max_depth'],depth)
        if margin>0:
            stats['accepted_leaves']+=1
            vol=Q(1)
            for lo,hi in ends: vol*=hi-lo
            accepted_volume+=vol
            leaf=json.dumps([[str(x),str(y)] for x,y in ends],separators=(',',':'))
            digest.update((leaf+'\n').encode())
            if stats['minimum_certified_lower'] is None or margin.lower()<min_margin:
                min_margin=margin.lower()
                stats['minimum_certified_lower']=str(min_margin)
                stats['worst_box']=[[str(x),str(y)] for x,y in ends]
        else:
            if depth>=48:
                stats.update(status='unresolved_box',margin=str(margin),box=[[str(x),str(y)] for x,y in ends])
                return stats
            # Deterministic subdivision: compare widths normalized to the domain.
            k=max(range(len(ends)),key=lambda i:(ends[i][1]-ends[i][0])/(domain[i][1]-domain[i][0]))
            lo,hi=ends[k]; mid=(lo+hi)/2
            left=list(ends); right=list(ends)
            left[k]=(lo,mid); right[k]=(mid,hi)
            pending.append((right,depth+1)); pending.append((left,depth+1))
    assert accepted_volume==full_volume
    stats.update(status='pass',exact_accepted_volume=str(accepted_volume),
                 exact_domain_volume=str(full_volume),leaf_partition_sha256=digest.hexdigest(),
                 seconds=time.monotonic()-start)
    return stats

def main():
    global LN2
    ap=argparse.ArgumentParser()
    ap.add_argument('--precision',type=int,default=256)
    ap.add_argument('--max-boxes',type=int,default=250000)
    ap.add_argument('--seconds-per-check',type=float,default=80)
    ap.add_argument('--output',default='audit/referee-interval-replay.json')
    args=ap.parse_args(); ctx.prec=args.precision; LN2=arb(2).log()
    start=time.monotonic()
    domains={x:[(P0,P1)] for x in ['center_positive','transverse_convex','tail_coefficient_positive','lower_inner','upper_tail']}
    domains['lower_outer']=[(P0,P1),(R0,Q(1))]
    domains['upper_compact']=[(P0,P1),(Q(0),Z0)]
    records=[]
    for name,dom in domains.items():
        rec=certify(name,dom,args.max_boxes,args.seconds_per_check)
        records.append(rec); print(json.dumps(rec,sort_keys=True),flush=True)
    result={'job_id':JOB,'created_at':datetime.now(timezone.utc).isoformat(),
            'precision_bits':ctx.prec,'python':sys.version,'python_flint':flint.__version__,
            'independence':'New script; no proposer code/cache imports. Shared proof inequalities and Arb arithmetic. Different interval variable, adaptive exact partitions, log evaluation and cancelled entropy expression.',
            'all_pass':all(r['status']=='pass' for r in records),'checks':records,
            'elapsed_seconds':time.monotonic()-start,'max_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'limitations':'Analytic reductions and monotonicity are reviewed in science.md; arithmetic replay is conditional on those arguments. No claim outside frozen p interval.'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print('FINAL '+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result['all_pass'] else 1

if __name__=='__main__': raise SystemExit(main())
