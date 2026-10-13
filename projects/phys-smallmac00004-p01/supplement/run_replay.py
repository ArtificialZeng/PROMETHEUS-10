#!/usr/bin/env python3
"""Run the supplied accepted implementations sequentially in a NEW local folder.

No downloads, installation, background processes, or model calls are performed.
Historical job strings inside the copied programs are not current audit metadata.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True,help='New directory strictly inside the project/archive root')
    args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT) or out==ROOT:
        raise SystemExit('Output must be strictly inside the project/archive root.')
    out.mkdir(parents=True,exist_ok=False)
    (out/'evidence').mkdir();(out/'audit').mkdir()
    env=dict(os.environ)
    env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
    # The copied research program may record this environment variable. It must
    # not be mistaken for a fresh reviewer identity when a reader reruns it.
    env.pop('PHYSICS_JOB_ID',None)
    jobs=[
        ('adaptive',[sys.executable,str(ROOT/'supplement/code/adaptive_certificate.py'),'--output','adaptive.json']),
        ('stinespring',[sys.executable,str(ROOT/'supplement/code/stinespring_checks.py')]),
        ('uniform192',[sys.executable,str(ROOT/'supplement/code/uniform_certificate.py'),'--tag','replay192']),
        ('uniform256',[sys.executable,str(ROOT/'supplement/code/uniform_certificate.py'),'--precision','256','--np','160','--nr','700','--ny','1400','--tag','replay256']),
    ]
    records=[]
    for name,command in jobs:
        start=time.monotonic()
        with (out/(name+'.log')).open('w') as log:
            result=subprocess.run(command,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        records.append({'name':name,'returncode':result.returncode,'seconds':time.monotonic()-start,'log':name+'.log'})
        if result.returncode:
            (out/'run-summary.json').write_text(json.dumps({'runs':records,'all_pass':False},indent=2)+'\n')
            raise SystemExit(result.returncode)
        print(name+': passed',flush=True)
    a=json.loads((out/'adaptive.json').read_text())
    s=json.loads((out/'audit/referee-source-replay.json').read_text())
    u=[json.loads((out/f'evidence/research-envelope-certificate-replay{p}.json').read_text()) for p in (192,256)]
    assert a['all_pass'] and s['all_pass'] and all(c['status']=='pass' for c in u)
    expected_a=json.loads((ROOT/'supplement/data/adaptive-certificate.json').read_text())
    for actual,expected in zip(a['checks'],expected_a['checks']):
        for key in ['name','domain','evaluated','accepted_leaves','exact_accepted_volume','exact_domain_volume','leaf_partition_sha256']:
            assert actual[key]==expected[key],(key,actual,expected)
    summary={'all_pass':True,'runs':records,'adaptive_leaf_partition_matches_supplied_record':True,
             'scope':'Arithmetic and source-code replay only; no new scientific or release verdict.'}
    (out/'run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
