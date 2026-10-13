#!/usr/bin/env python3
"""Rebuild SmallMac manuscripts in disposable copies; archived PDFs stay unchanged."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
ROWS=json.loads((ROOT/'reproducibility/small_mac_projects.json').read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--project',choices=[x['id'] for x in ROWS]);p.add_argument('--all',action='store_true');p.add_argument('--output-dir',type=Path,default=ROOT/'reproduction-runs');p.add_argument('--timeout',type=int,default=240);a=p.parse_args()
 if not a.project and not a.all:p.error('choose --project or --all')
 if not shutil.which('latexmk'):p.error('latexmk and a TeX distribution are required; no installation is attempted')
 chosen=ROWS if a.all else [next(x for x in ROWS if x['id']==a.project)]
 out=a.output_dir.resolve()/('small-mac-tex-'+time.strftime('%Y%m%d-%H%M%S'));out.mkdir(parents=True,exist_ok=False);results=[]
 for row in chosen:
  ident=row['id'];work=out/ident;shutil.copytree(ROOT/'projects'/ident,work)
  attempts=[(work/'manuscript',['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir=rebuild','main.tex']),(work,['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir=rebuild','manuscript/main.tex'])]
  code=1;used=None;pdf=None;citations_clean=False
  for n,(cwd,command) in enumerate(attempts,1):
   log=work/f'compile-attempt-{n}.log';used={'cwd':str(cwd.relative_to(work)) or '.', 'command':command,'log':log.name}
   with log.open('w') as f:
    try:code=subprocess.run(command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout).returncode
    except subprocess.TimeoutExpired:code=124
   candidate=cwd/'rebuild/main.pdf'
   final_log=cwd/'rebuild/main.log'
   log_text=final_log.read_text(errors='replace') if final_log.is_file() else ''
   unresolved=(not final_log.is_file() or 'undefined citations' in log_text.lower() or 'there were undefined references' in log_text.lower() or ('citation' in log_text.lower() and 'undefined' in log_text.lower()) or ('reference' in log_text.lower() and 'undefined' in log_text.lower()) or 'please (re)run biber' in log_text.lower())
   if code==0 and candidate.is_file() and not unresolved:pdf=candidate;citations_clean=True;break
   if code==0 and candidate.is_file() and unresolved:code=65
  result={'project':ident,'exit_code':code,'pdf_exists':bool(pdf),'citations_clean':citations_clean,'attempt':used};results.append(result);print(json.dumps(result),flush=True);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 return int(any(x['exit_code'] or not x['pdf_exists'] or not x['citations_clean'] for x in results))
if __name__=='__main__':raise SystemExit(main())
