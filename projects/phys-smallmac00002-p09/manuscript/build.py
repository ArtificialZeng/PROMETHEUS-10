"""Clean, source-only LaTeX build with no writes to accepted science evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCES=['main.tex','references.bib','figures/waiting.pdf']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    if out.exists():raise SystemExit('Choose a new clean build directory.')
    if ROOT not in out.parents:raise SystemExit('Build directory must be inside this project.')
    out.mkdir(parents=True)
    for name in SOURCES:
        dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/'manuscript'/name,dest)
    command=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-file-line-error','-pdflatex=pdflatex -no-shell-escape %O %S','main.tex']
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1789214400'
    with (out/'clean-build.log').open('w') as log:
        result=subprocess.run(command,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
    record={'command':command,'clean_staging':True,'exit_code':result.returncode,
             'sources':{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in SOURCES}}
    (out/'build-record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'exit_code':result.returncode,'directory':str(out),'log':str(out/'clean-build.log')}))
    raise SystemExit(result.returncode)

if __name__=='__main__':main()
