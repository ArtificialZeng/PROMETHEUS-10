#!/usr/bin/env python3
"""Rebuild manuscript PDFs in fresh copies without changing archived PDFs."""
from pathlib import Path
import argparse,json,shutil,subprocess,time,sys
ROOT=Path(__file__).resolve().parents[1]
FROM_MANUSCRIPT={'phys-00002-p01','phys-00002-p15','phys-00004-p01','phys-00004-p02','phys-00007-p01'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project');p.add_argument('--all',action='store_true');p.add_argument('--output-dir',type=Path,default=ROOT/'reproduction-runs');a=p.parse_args()
 if not a.project and not a.all:p.error('choose --project or --all')
 if not shutil.which('latexmk'):p.error('latexmk and a TeX distribution are required; no installation is attempted')
 ids=sorted(x.name for x in (ROOT/'projects').iterdir() if x.is_dir())
 if a.project and a.project not in ids:p.error('unknown project ID')
 out=a.output_dir.resolve()/('tex-'+time.strftime('%Y%m%d-%H%M%S'));out.mkdir(parents=True,exist_ok=False);results=[]
 for ident in ids if a.all else [a.project]:
  work=out/ident;shutil.copytree(ROOT/'projects'/ident,work)
  cwd=work/'manuscript' if ident in FROM_MANUSCRIPT else work
  target='main.tex' if ident in FROM_MANUSCRIPT else 'manuscript/main.tex'
  command=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir=rebuild',target]
  with (work/'compile.log').open('w') as f:
   try:code=subprocess.run(command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=180).returncode
   except subprocess.TimeoutExpired:code=124
  pdf=cwd/'rebuild/main.pdf';row={'project':ident,'exit_code':code,'pdf_exists':pdf.exists(),'command':command,'cwd':'manuscript' if ident in FROM_MANUSCRIPT else '.'};results.append(row);print(json.dumps(row),flush=True)
  (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 sys.exit(any(x['exit_code'] or not x['pdf_exists'] for x in results))
if __name__=='__main__':main()
