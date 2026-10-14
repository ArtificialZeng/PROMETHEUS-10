"""Exact tensor Bernstein test for four resolvent coefficients on the ordered cube.

F=E is the worst sixth attenuation. A=x0, B=x0*x1,..., E=x0*...*x4.
No positivity is inferred when even one Bernstein coefficient is negative.
"""
import itertools,json,math,time
from pathlib import Path

import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output-dir', type=Path, required=True)
_args = _parser.parse_args()
_OUTPUT = _args.output_dir.resolve()
_HERE = Path(__file__).resolve().parent
if _OUTPUT == _HERE or _HERE in _OUTPUT.parents:
    raise ValueError('Select an output directory outside the source supplement directory')
_OUTPUT.mkdir(parents=True, exist_ok=True)
if not __debug__:
    raise RuntimeError('Exact assertions require Python without -O')
import numpy as np

raw=json.loads((_OUTPUT / 'polynomials.json').read_text())
records=[]
for row in raw['coefficients']:
    terms={}
    for powers,co in row['terms']:
        aa,bb,cc,dd,ee,ff=powers
        pp=(aa,bb,cc,dd,ee+ff) # F=E
        rr=tuple(sum(pp[j:]) for j in range(5))
        terms[rr]=terms.get(rr,0)+int(co)
    terms={p:c for p,c in terms.items() if c}
    deg=tuple(max(p[j] for p in terms) for j in range(5))
    arr=np.zeros(tuple(n+1 for n in deg),dtype=object)
    for p,c in terms.items():arr[p]=c
    scales=[]
    for axis,n in enumerate(deg):
        scale=math.lcm(*(math.comb(n,j) for j in range(n+1)))
        scales.append(scale)
        T=np.array([[math.comb(i,j)*scale//math.comb(n,j) if j<=i else 0
                     for j in range(n+1)] for i in range(n+1)],dtype=object)
        arr=np.moveaxis(arr,axis,0)
        shape=arr.shape
        arr=(T@arr.reshape(n+1,-1)).reshape(shape)
        arr=np.moveaxis(arr,0,axis)
    neg=[]
    zeros=0
    for p in np.ndindex(arr.shape):
        if arr[p]<0:neg.append([list(p),str(arr[p])])
        if arr[p]==0:zeros+=1
    rec={'k':row['k'],'ratio_degrees':list(deg),'coefficient_count':arr.size,
         'common_denominator':str(math.prod(scales)),'minimum_scaled_coefficient':str(min(arr.flat)),
         'negative_count':len(neg),'zero_count':zeros,'negative_examples':neg[:20],
         'status':'exact_nonnegative_bernstein_cover' if not neg else 'inconclusive_negative_coefficients'}
    if not neg:
        rec['all_scaled_coefficients']=[str(v) for v in arr.flat]
    records.append(rec)
    print(json.dumps({k:v for k,v in rec.items() if k!='all_scaled_coefficients'}),flush=True)
(_OUTPUT / 'certificate.generated.json').write_text(json.dumps({'method':'exact integer tensor Bernstein basis, scaled by recorded positive denominators','status':'pass' if all(r['negative_count']==0 for r in records) else 'inconclusive','records':records},indent=2)+'\n')
