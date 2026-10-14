"""Check actual Taylor remainders, using 500-digit directed reference bounds.

This checks every panel in the frozen refined certificate. It does not import
the discovery kernel. A pass can establish that the actual final remainder
upper endpoints are safe despite the intermediate ABS initialization defect.
A partial run or a failure cannot establish this statement.
"""
import datetime,json,math,time
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'reproducibility/run-output'
RUN.mkdir(parents=True,exist_ok=True)
START=time.monotonic();LIMIT=240
def polynomial(edges):
    prev=[mp.iv.mpf(1)];now=[mp.iv.mpf(0),mp.iv.mpf(1)]
    for e in edges:
        nxt=[mp.iv.mpf(0)]+now
        for j,x in enumerate(prev):nxt[j]-=e*x
        prev,now=now,nxt
    return now
def coefficients(digits):
    mp.iv.dps=digits
    theta=mp.iv.pi/256
    e=[1/(4*mp.iv.sin((2*l+1)*theta)*mp.iv.sin((2*l-1)*theta)) for l in range(1,128)]
    return [polynomial(e)[::2],polynomial(e[1:])[1::2]]
def low(x):return mp.make_mpf(x._mpi_[0])
def high(x):return mp.make_mpf(x._mpi_[1])
def magnitude(x):return max(abs(low(x)),abs(high(x)))
old=coefficients(250)
mp.iv.dps=85;mp.mp.dps=100
rough=[[mp.iv.mpf([magnitude(x),magnitude(x)]) for x in poly] for poly in old]
precise=coefficients(500)
# Extract maximum absolute encoded endpoints by changing only the sign bit;
# no nearest-rounded scalar absolute value is used for the reference.
def endpoint_abs(t):return (0,t[1],t[2],t[3])
safe=[]
for p in precise:
    safe.append([max(mp.make_mpf(endpoint_abs(x._mpi_[0])),mp.make_mpf(endpoint_abs(x._mpi_[1]))) for x in p])
panels=json.loads((ROOT/'evidence/research/r3-interval-refine.json').read_text())['panels']
data={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'in_progress',
      'certificate':'evidence/research/r3-interval-refine.json','completed_panels':0,
      'checks':0,'violations':[],'original_precision':85,'reference_precision':500,
      'method':'Exact same dyadic center/radius/X; independently transcribed original remainder evaluation compared against a fresh 500-digit outward bound formed from exact-coefficient interval absolute endpoints. No discovery module import.'}
out=RUN/'remainder-fullcheck.json'
def save():
    data['elapsed_seconds']=time.monotonic()-START
    out.write_text(json.dumps(data,indent=2)+'\n')
save()
for i,row in enumerate(panels):
    lo,hi=row['q_interval'];mid=(lo+hi)/2
    mp.iv.dps=85
    q=mp.iv.mpf([lo,hi]);x=q**2
    center=mp.mpf(mid)**2;dx=x-mp.iv.mpf(center)
    radius=magnitude(dx);X=magnitude(x)
    radial=mp.iv.mpf([radius,radius]);xmax=mp.iv.mpf([X,X])
    originals=[]
    for p in rough:
        derivative=mp.iv.mpf(0)
        for k in range(len(p)-1,19,-1):derivative=derivative*xmax+p[k]*math.comb(k,20)
        originals.append(high(derivative*radial**20))
    mp.iv.dps=500
    radial=mp.iv.mpf(radius);xmax=mp.iv.mpf(X)
    for poly_index,p in enumerate(safe):
        derivative=mp.iv.mpf(0)
        for k in range(len(p)-1,19,-1):derivative=derivative*xmax+mp.iv.mpf(p[k])*math.comb(k,20)
        needed=derivative*radial**20
        # Comparisons of mpf encoded values are exact, without rounding.
        valid=originals[poly_index]>=high(needed)
        data['checks']+=1
        if not valid:
            data['violations'].append({'panel_index':i,'q_interval':[lo,hi],'polynomial':poly_index,
                'original_upper':mp.nstr(originals[poly_index],100),
                'reference_lower':mp.nstr(low(needed),100),'reference_upper':mp.nstr(high(needed),100),
                'strictly_below_reference_lower':bool(originals[poly_index]<low(needed))})
    data['completed_panels']=i+1
    if (i+1)%2000==0:
        save();print(json.dumps({'panels':i+1,'checks':data['checks'],'violations':len(data['violations']),'seconds':data['elapsed_seconds']}),flush=True)
    if time.monotonic()-START>LIMIT:
        data['status']='incomplete_time_ceiling';save();print(json.dumps({'status':data['status'],'panels':i+1}));break
else:
    data['status']='pass_actual_remainders_enclosed' if not data['violations'] else 'fail_actual_remainder_upper_bounds'
    save();print(json.dumps({'status':data['status'],'panels':len(panels),'checks':data['checks'],'violations':len(data['violations']),'seconds':data['elapsed_seconds']}),flush=True)
