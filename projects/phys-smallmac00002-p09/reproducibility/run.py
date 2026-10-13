"""Run finite-state replays in a new output directory, preserving source data.

quick: exact researcher algebra plus the separate referee algebra.
independent: quick plus Poisson uniformization (q=24, H=80).
full: quick plus original exponential/ODE scans and comparison, then uniformization.
"""
from pathlib import Path
import argparse
import datetime
import json
import os
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['quick','independent','full'],default='quick')
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise SystemExit('Choose a new output directory; no existing results will be overwritten.')
    if ROOT != out and ROOT not in out.parents:
        raise SystemExit('Output must be inside this manuscript project.')
    out.mkdir(parents=True)
    (out/'evidence/research').mkdir(parents=True)
    (out/'src').mkdir()
    for source in (ROOT/'reproducibility/src').glob('*.py'):
        shutil.copyfile(source,out/'src'/source.name)
    env = os.environ.copy()
    env.update({'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1',
                'MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
    tasks=[('exact',['research_exact.py']),('independent-exact',['independent_replay.py'])]
    if args.mode=='full':
        tasks += [('expm',['research_expm.py']),('ode',['research_ode.py']),
                  ('comparison',['research_compare.py'])]
    if args.mode in ['independent','full']:
        tasks += [('independent-numeric',['independent_replay.py','--numeric','--order','24','--horizon','80'])]
    record={'mode':args.mode,'python':sys.version,'platform':platform.platform(),
            'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'numeric_library_threads':1,'runs':[]}
    for label,argv in tasks:
        command=[sys.executable,str(out/'src'/argv[0])]+argv[1:]
        began=time.perf_counter()
        with (out/(label+'.log')).open('w') as log:
            done=subprocess.run(command,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600)
        record['runs'].append({'label':label,'exit_code':done.returncode,
                               'elapsed_seconds':time.perf_counter()-began,'log':label+'.log'})
        (out/'run-record.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record['runs'][-1]),flush=True)
        if done.returncode:
            raise SystemExit(done.returncode)
    print('All requested replays completed. Numerical agreement is not an interval certificate.')

if __name__=='__main__':
    main()
