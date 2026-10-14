"""Refine a completed, audited interval certificate without dropping panels.

The starting exported ranges are already outward enclosures. Only selected
panels are recomputed; a stable parent certificate is an explicit input.
No stored quadrature or point estimates are used as integral bounds.
"""
import argparse,datetime,fractions,heapq,importlib.util,json,math,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('fixed_kernel',ROOT/'evidence/research/r3-interval-enclosure.py')
k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
iv=k.iv

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=300);ap.add_argument('--target-width',type=float,default=.0048)
    args=ap.parse_args();start=time.monotonic();parent=ROOT/'evidence/research/r3-interval-enclosure.json'
    old=json.loads(parent.read_text());assert old['status']=='positive_residual_enclosed_proposer_only'
    data={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'in_progress',
          'parent_certificate':'evidence/research/r3-interval-enclosure.json','kernel':'evidence/research/r3-interval-enclosure.py',
          'fixed_model':'evidence/research/r1-tightbinding-model.md','setup':k.setup_record,
          'mode':'interval_ranges_not_quadrature_estimates','target_width':args.target_width,
          'limitations':'Same-proposer validated range refinement; no referee acceptance','results':[]}
    output=ROOT/'evidence/research/r3-interval-refine.json';heap=[];serial=0;failures=0
    for p in old['panels']:
        lo,hi=p['q_interval'];vals=[iv.mpf(v) for v in p['integrated_ranges']]
        serial+=1;heapq.heappush(heap,(-float(k.upper(vals[0])-k.lower(vals[0])),serial,lo,hi,vals,p['transmission_denominator_validated']))
    total=[iv.mpf(0) for _ in range(4)]
    for row in heap:total=[x+y for x,y in zip(total,row[4])]
    def save():
        data['elapsed_seconds']=time.monotonic()-start;output.write_text(json.dumps(data,indent=2)+'\n')
    def report(stage):
        tails=k.tail_bounds();values=[x+k.hull(-k.upper(t),k.upper(t)) for x,t in zip(total,tails)]
        row={'stage':stage,'active_panels':len(heap),'new_evaluated_panels':serial-len(old['panels']),
             'new_fallback_evaluations':failures,
             'integral_enclosures':dict(zip(['Delta','J','sigma_over_kB','chi_minus24'],map(k.numeric,values))),
             'analytic_tail_bounds':dict(zip(['Delta','J','sigma_over_kB','chi_minus24'],[k.numeric(t)[1] for t in tails]))}
        data['results'].append(row);save();print(json.dumps(row),flush=True);return values
    def panel(lo,hi):
        nonlocal serial,failures
        vals,ok=k.ranges(lo,hi)
        assert fractions.Fraction(hi-lo)==fractions.Fraction(hi)-fractions.Fraction(lo)
        vals=[x*iv.mpf(hi-lo) for x in vals];serial+=1;failures+=int(not ok)
        return (-float(k.upper(vals[0])-k.lower(vals[0])),serial,lo,hi,vals,ok)
    report('initial_from_validated_parent');last_report=start
    while float(k.upper(total[0])-k.lower(total[0]))>args.target_width and time.monotonic()-start<args.seconds:
        _,_,lo,hi,previous,_=heapq.heappop(heap);mid=(lo+hi)/2;assert lo<mid<hi
        left,right=panel(lo,mid),panel(mid,hi);heapq.heappush(heap,left);heapq.heappush(heap,right)
        replaced=[]
        for current,oldrange,a,b in zip(total,previous,left[4],right[4]):
            lower=iv.mpf(k.lower(current))-iv.mpf(k.lower(oldrange))+iv.mpf(k.lower(a))+iv.mpf(k.lower(b))
            upper=iv.mpf(k.upper(current))-iv.mpf(k.upper(oldrange))+iv.mpf(k.upper(a))+iv.mpf(k.upper(b))
            replaced.append(k.hull(k.lower(lower),k.upper(upper)))
        total=replaced
        if time.monotonic()-last_report>=20:report('refinement');last_report=time.monotonic()
    ordered=sorted(heap,key=lambda x:x[2]);assert ordered[0][2]==-8192 and ordered[-1][3]==16384
    assert all(a[3]==b[2] for a,b in zip(ordered[:-1],ordered[1:]))
    assert sum((fractions.Fraction(r[3])-fractions.Fraction(r[2]) for r in ordered),fractions.Fraction(0))==24576
    total=[iv.mpf(0) for _ in range(4)]
    for row in ordered:total=[x+y for x,y in zip(total,row[4])]
    values=report('final');width=float(k.upper(values[0])-k.lower(values[0]))
    if width<=args.target_width and all(k.lower(values[i])>0 for i in [0,1,2]):data['status']='positive_residual_enclosed_proposer_only'
    else:data['status']='width_target_incomplete';data['obstacle']='Bounded refinement did not meet requested width'
    data['panels']=[{'q_interval':[r[2],r[3]],'integrated_ranges':[k.numeric(x) for x in r[4]],'transmission_denominator_validated':r[5]} for r in ordered]
    save();print(json.dumps({'status':data['status'],'seconds':data['elapsed_seconds']}),flush=True)

if __name__=='__main__':main()
