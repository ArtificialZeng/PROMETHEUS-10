"""Clean foreground LaTeX build from an explicit dependency set.

Run from anywhere in the package: python3 -B reproducibility/build_manuscript.py
Preserved compiler files stay under a unique build/clean-* directory.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT = ROOT / 'build' / ('clean-' + stamp)
sources = ['manuscript/main.tex', 'manuscript/references.bib',
           'manuscript/table-rows.tex', 'manuscript/figures/occupations.pdf',
           'reproducibility/scalar_certificate.py']
for name in sources:
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / name, target)
commands = [['pdflatex', '-no-shell-escape', '-halt-on-error', '-interaction=nonstopmode',
             '-file-line-error', '-recorder', 'main.tex'],
            ['bibtex','main'],
            ['pdflatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode',
             '-file-line-error','-recorder','main.tex'],
            ['pdflatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode',
             '-file-line-error','-recorder','main.tex']]
records = []
for number, command in enumerate(commands,1):
    result = subprocess.run(command, cwd=OUT/'manuscript', capture_output=True,
                            text=True, timeout=90)
    log = OUT / ('command-'+str(number)+'.log')
    log.write_text(result.stdout+result.stderr,encoding='utf-8')
    records.append({'command':command,'exit_code':result.returncode,
                    'log':log.relative_to(ROOT).as_posix()})
    if result.returncode:
        print(result.stdout[-6000:]+result.stderr[-2000:])
        raise RuntimeError('Compiler failed; see '+str(log))
pdf=OUT/'manuscript/main.pdf'
assert pdf.read_bytes().startswith(b'%PDF-')
record={'built_at':datetime.now(timezone.utc).isoformat(), 'clean_build':True,
        'source_files':sources,'source_sha256':{
            f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources},
        'commands':records,'pdf':pdf.relative_to(ROOT).as_posix(),
        'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'final_build_log':(OUT/'manuscript/main.log').relative_to(ROOT).as_posix(),
        'bibtex_log':(OUT/'manuscript/main.blg').relative_to(ROOT).as_posix(),
        'dependency_record':(OUT/'manuscript/main.fls').relative_to(ROOT).as_posix()}
(OUT/'build-record.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
