"""Same-proposer independent reconstruction, not referee acceptance.

High-precision backward sector chains, outgoing Bloch contacts and explicit
Slater-event counting are rebuilt without polynomial coefficients or cached
scattering values. The interval kernel is imported only for comparisons.
The final exported partition is checked with exact rational arithmetic.
"""
import argparse, datetime, fractions, hashlib, importlib.util, itertools, json, math
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]

def load_kernel():
    p=ROOT/'evidence/research/r3-interval-enclosure.py'
    spec=importlib.util.spec_from_file_location('enclosure_for_comparison',p)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj

def independent(q,digits=320):
    with mp.workdps(digits):
        q=mp.mpf(q);n=128;scale=mp.mpf(1)/100;E0=mp.mpf(5000);t=mp.mpf(10000)
        delta=scale*q;E=E0+delta;theta=mp.pi/(2*n)
        gf=scale/(2*mp.sin(theta));gc=mp.mpf(200000)
        V2=2*t*t*gf/mp.sqrt(E0*(4*t-E0))
        # Independent outgoing Bloch representation of the lead boundary.
        cosk=1-E/(2*t);sink=mp.sqrt(1-cosk*cosk)
        sigma=-V2/t*(cosk+1j*sink)
        sigma0=V2*(E0-2*t)/(2*t*t);gamma=V2/t*sink
        hops2=[scale*scale/(4*(mp.sin(l*mp.pi/n)**2-mp.sin(theta)**2)) for l in range(1,n)]
        hops2.append(gf*gc)
        phases=[]
        for sector in range(3):
            old=mp.mpc(1);cur=mp.mpc(delta-2*gc*mp.sin(2*mp.pi*sector/3))
            for site in range(n-1,-1,-1):
                diag=delta+(sigma0-sigma if site==0 else 0)
                old,cur=cur,diag*cur-hops2[site]*old
            phases.append(1-2j*gamma*old/cur)
        S=mp.matrix(3,3)
        for a in range(3):
            for b in range(3):
                S[a,b]=sum(phases[k]*mp.exp(2j*mp.pi*(a-b)*k/3) for k in range(3))/3
        f=[1/(1+mp.exp(delta-l)) for l in (1,-3,-24)]
        T=[[abs(S[a,b])**2 for b in range(3)] for a in range(3)]
        currents=[sum(T[a][b]*(f[a]-f[b]) for b in range(3)) for a in range(3)]
        entropy=sum(mp.mpf(l)*j for l,j in zip((1,-3,-24),currents))
        states=[s for size in range(4) for s in itertools.combinations(range(3),size)]
        mgf=mp.mpf(0);eventj=[mp.mpf(0) for _ in range(3)];sumprob=mp.mpf(0)
        marginal=[mp.mpf(0) for _ in range(3)]
        for incoming in states:
            pin=mp.fprod(f[a] if a in incoming else 1-f[a] for a in range(3))
            for outgoing in states:
                if len(incoming)!=len(outgoing):continue
                amplitude=mp.mpc(1) if not incoming else mp.det(mp.matrix([[S[a,b] for b in incoming] for a in outgoing]))
                prob=pin*abs(amplitude)**2
                counts=[int(a in incoming)-int(a in outgoing) for a in range(3)]
                sumprob+=prob;mgf+=prob*mp.exp(-24*counts[0]);marginal[counts[0]+1]+=prob
                for a in range(3):eventj[a]+=prob*counts[a]
        chi=mp.log1p(marginal[2]*mp.expm1(-24)+marginal[0]*mp.expm1(24));residual=24*currents[0]-4*entropy-chi
        fmatrix=mp.diag(f);left=mp.diag([mp.exp(24),1,1]);right=mp.diag([mp.exp(-24),1,1])
        determinant=mp.det(mp.eye(3)-fmatrix+fmatrix*(S.H*left*S*right))
        identity_error=max(abs(sum(S[k,a].conjugate()*S[k,b] for k in range(3))-int(a==b)) for a in range(3) for b in range(3))
        return {'values':[mp.mpf(scale*x) for x in (residual,currents[0],entropy,chi)],
                'u':mp.mpf(T[0][1]),'v':mp.mpf(T[0][2]),
                'unitarity_error':mp.mpf(identity_error),'probability_error':mp.mpf(abs(sumprob-1)),
                'event_current_error':mp.mpf(max(abs(x-y) for x,y in zip(currents,eventj))),
                'determinant_fock_relative_error':mp.mpf(abs(determinant-mgf)/max(1,abs(mgf))),
                'count_probability_min':mp.mpf(min(marginal))}

def fraction(x):return fractions.Fraction.from_float(x)

def partition_check(path):
    data=json.loads(path.read_text());panels=data.get('panels',[])
    assert panels,'No completed panel certificate'
    assert data['status']=='positive_residual_enclosed_proposer_only',data['status']
    assert panels[0]['q_interval'][0]==-8192 and panels[-1]['q_interval'][1]==16384
    sum_width=fractions.Fraction(0);totals=[[fractions.Fraction(0),fractions.Fraction(0)] for _ in range(4)]
    for i,row in enumerate(panels):
        lo,hi=row['q_interval'];assert lo<hi
        if i:assert panels[i-1]['q_interval'][1]==lo
        # Exact subtraction validates the kernel's binary64 integration width.
        width=fraction(hi)-fraction(lo);assert fraction(hi-lo)==width
        sum_width+=width
        for k,(lower,upper) in enumerate(row['integrated_ranges']):
            assert math.isfinite(lower) and math.isfinite(upper) and lower<=upper
            totals[k][0]+=fraction(lower);totals[k][1]+=fraction(upper)
    assert sum_width==24576
    tails=data['results'][-1]['analytic_tail_bounds'];names=['Delta','J','sigma_over_kB','chi_minus24']
    out={}
    for k,name in enumerate(names):
        tail=fraction(tails[name]);lo=totals[k][0]-tail;hi=totals[k][1]+tail
        out[name]=[math.nextafter(float(lo),-math.inf),math.nextafter(float(hi),math.inf)]
    assert out['Delta'][0]>0 and out['J'][0]>0 and out['sigma_over_kB'][0]>0
    return {'status':'pass','panels':len(panels),'q_coverage':[-8192,16384],'exact_rational_width':str(sum_width),
            'kernel_width_subtractions_exact':True,'exact_rational_exported_panel_sums_with_tails':out,
            'fallback_active_panels':sum(not p['transmission_denominator_validated'] for p in panels),
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate');ap.add_argument('--output',default='evidence/research/r3-independent-check.json')
    ap.add_argument('--partition-only',action='store_true');args=ap.parse_args()
    data={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope':'Same-proposer independent reconstruction and exported certificate audit; no referee acceptance',
          'independence':'Rebuilds physical boundary/chain using outgoing Bloch solution, reversed scalar sector recurrences and explicit Slater minors; does not read cached scattering or quadrature values. Comparison alone imports interval kernel. Shared fixed parameters, primary sources, mpmath library and proposer.'}
    if not args.partition_only:
        kernel=load_kernel();rows=[]
        points=[-4,-2,-1.125,-1.03125,-1,-0.9990234375,-0.99609375,-0.99,-0.875,-0.5,-0.03125,0,0.03125,0.5,0.875,0.99,0.99609375,0.9990234375,1,1.03125,1.125,2,4]
        for q in points:
            ind=independent(q);r,ok=kernel.ranges(float(q),float(q));u,v,_=kernel.transmissions(float(q),float(q))
            contain=[kernel.lower(bound)<=val<=kernel.upper(bound) for val,bound in zip(ind['values'],r)]
            contain.extend([kernel.lower(u)<=ind['u']<=kernel.upper(u),kernel.lower(v)<=ind['v']<=kernel.upper(v)])
            assert all(contain),(q,contain)
            for key in ('unitarity_error','probability_error','event_current_error','determinant_fock_relative_error'):
                assert ind[key]<mp.mpf('1e-130'),(q,key,str(ind[key]))
            assert ind['count_probability_min']>=0
            rows.append({'q':q,'kernel_range_contains_independent_values':contain,'denominator_validated':ok,
                         **{k:str(v) for k,v in ind.items() if k!='values'},'independent_scaled_density':[str(x) for x in ind['values']]})
        data['point_checks']=rows;data['point_status']='pass'
    if args.certificate:data['partition_check']=partition_check(ROOT/args.certificate)
    data['status']='completed_proposer_check'
    (ROOT/args.output).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'point_checks':len(data.get('point_checks',[])),'partition_check':data.get('partition_check')}))

if __name__=='__main__':main()
