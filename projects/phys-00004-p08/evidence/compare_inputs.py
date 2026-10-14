#!/usr/bin/env python3
"""Compare separately generated A/B inputs through their explicit basis map."""
import json
import hashlib
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent.parent

def load(name):return json.loads((ROOT/'evidence'/name).read_text())

def main():
    a,b=load('results-a.json'),load('results-b.json')
    ma,mb=load('matching-a.json'),load('matching-b.json')
    c,s=sp.symbols('c s')
    relation=sp.groebner([c*c+s*s-1],c,s)
    tests=[]
    for E in (2,3,5,8):
        A=sp.Matrix([[sp.sympify(z) for z in row] for row in ma[f'pumpkin_E{E}']['entries']])
        B=sp.Matrix([[sp.sympify(z) for z in row] for row in mb[f'pumpkin_E{E}']['entries']])
        T=sp.diag(*([sp.Matrix([[c,s],[s,-c]])]*E))
        # Explicit row map R: exchange both continuity blocks and both flux rows,
        # changing both flux signs to the source's towards-vertex convention.
        R=sp.zeros(2*E)
        for j in range(E-1):R[j,E-1+j]=1;R[E-1+j,j]=1
        R[2*E-2,2*E-1]=-1;R[2*E-1,2*E-2]=-1
        difference=B*T-R*A
        remainders=[relation.reduce(sp.expand(z))[1] for z in difference]
        assert all(z==0 for z in remainders)
        tests.append({'E':E,'compared_entries':4*E*E,'nonzero_remainders':0,'status':'pass'})
        # Exact pole multiplicities from A agree with B's separately derived sectors.
        for n in (1,2,3):
            aa=[r for r in a['exact_checks'] if r.get('graph')=='unit pumpkin' and r.get('E')==E and r.get('k')==f'{n}*pi'][0]
            bb=[r for r in b['pumpkin_sector_checks'] if r['E']==E and r['k']==f'{n}*pi'][0]
            assert aa['nullity']==bb['total']==E
    ka=a['perturbed_tree_root']['k'];kb=float(b['perturbed_tree_root']['k'])
    difference=abs(ka-kb)
    assert difference<1e-10
    assert abs(a['tree_lengths']['b_unperturbed']-float(b['tree_lengths']['b_unperturbed']))<1e-14
    for bb in b['star_sector_prediction']:
        aa=[r for r in a['exact_checks'] if r['graph']=='doubled star' and r['k']==bb['k']][0]
        assert aa['nullity']==bb['doubled_total']
    digests={name:hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()
      for name in ('input-a.json','input-b.json','reconstruct_a.py','reconstruct_b.py','matching-a.json','matching-b.json','results-a.json','results-b.json')}
    output={'status':'pass','basis_map':'y=1-x; (alpha,beta)=(c*a+s*b,s*a-c*b); B*T=R*A modulo c^2+s^2=1',
      'exact_row_by_row_checks':tests,'pumpkin_poles_checked':['pi','2*pi','3*pi'],
      'tree_wave_number_absolute_difference':difference,'cross_root_tolerance':1e-10,
      'star_DD_pole_replay':'Doubled half-length 4-star: nullity 3 at pi and 5 at 2*pi, matching original plus all four DD branches',
      'independence':'Two implementations using separate same-agent transcriptions; shared primary source and target. B reads no A artifact. Not a fresh scientific referee.',
      'file_sha256':digests}
    (ROOT/'evidence/comparison-results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
