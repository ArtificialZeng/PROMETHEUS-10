#!/usr/bin/env python3
"""Replay manuscript checks in disposable copies; never overwrite archived evidence."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
J={
'phys-00002-p01':[
['evidence/research_interval_rank_two_neighborhood.py','--precision','256','--json','replay-256.json','--log','replay-256.log'],
['evidence/research_interval_rank_two_neighborhood.py','--precision','320','--json','replay-320.json','--log','replay-320.log'],
['evidence/verify_interval_rank_two_neighborhood.py','--json','replay-independent.json','--log','replay-independent.log']],
'phys-00002-p02':[['scripts/verify_fourier_n4.py','--project','.','--json-out','replay.json','--log-out','replay.log']],
'phys-00002-p06':[['manuscript/reproduce_witness.py']],
'phys-00002-p15':[['code/check_fixed_gap.py','--output','replay-gap.json'],['code/check_trace_bound.py','--output','replay-trace.json']],
'phys-00003-p01':[['scripts/quotient_symbolic.py'],['scripts/verify_quotient.py'],['scripts/quotient_wick.py'],['scripts/compare_quotient_methods.py'],['scripts/baseline_poisson.py'],['scripts/baseline_wick.py'],['scripts/compare_inputs.py']],
'phys-00004-p01':[['evidence/verify_gadc_coefficients.py'],['evidence/verify_gadc_quadratic_proof.py'],['evidence/compare_and_baseline.py','compare'],['evidence/compare_and_baseline.py','baseline']],
'phys-00004-p02':[['reproducibility/verify_counterexample.py']],
'phys-00005-p01':[['code/counterexample_spectral_a.py','--output','replay-a.json','--log','replay-a.log'],['code/counterexample_commutant_b.py','--output','replay-b.json','--log','replay-b.log'],['code/compare_counterexample.py','--method-a','replay-a.json','--method-b','replay-b.json','--output','replay-compare.json','--log','replay-compare.log']],
'phys-00006-p01':[['code/certify_alpha_plus.py'],['code/certify_counterexample.py'],['code/verify_counterexample_independent.py']],
'phys-00007-p01':[['manuscript/reproduce.py','--output','replay.json']]}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',choices=J);p.add_argument('--all',action='store_true');p.add_argument('--list',action='store_true');p.add_argument('--output-dir',type=Path,default=ROOT/'reproduction-runs');p.add_argument('--timeout',type=int,default=900);a=p.parse_args()
 if a.list: print(json.dumps(J,indent=2));return
 if not a.all and not a.project:p.error('choose --project or --all')
 run=a.output_dir.resolve()/time.strftime('%Y%m%d-%H%M%S');run.mkdir(parents=True,exist_ok=False);results=[]
 for ident in J if a.all else [a.project]:
  work=run/ident;shutil.copytree(ROOT/'projects'/ident,work)
  for n,args in enumerate(J[ident],1):
   start=time.monotonic();log=work/f'check-{n:02}.log';status='exit-zero'
   try:
    with log.open('w') as f:r=subprocess.run([sys.executable,*args],cwd=work,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout,env={**os.environ,'MPLBACKEND':'Agg'})
    code=r.returncode
   except subprocess.TimeoutExpired:code=124;status='timeout'
   if code and status!='timeout':status='failed'
   row={'project':ident,'step':n,'command':['python',*args],'exit_code':code,'status':status,'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(run))};results.append(row);print(json.dumps(row),flush=True)
   (run/'results.json').write_text(json.dumps(results,indent=2)+'\n')
   if code:break
 print('Results:',run/'results.json');sys.exit(any(x['exit_code'] for x in results))
if __name__=='__main__':main()
