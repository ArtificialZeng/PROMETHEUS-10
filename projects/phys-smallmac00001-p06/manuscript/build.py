#!/usr/bin/env python3
"""Build in a new project-local directory, retaining complete compiler output."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='build/write-clean',
                    help='New or empty directory relative to the project root')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = (root / args.output_dir).resolve()
out.relative_to(root)
if out.exists() and any(out.iterdir()):
    parser.error('The output directory must be new or empty; choose another path.')
out.mkdir(parents=True, exist_ok=True)
copies = []
for name in ('main.tex', 'references.bib'):
    src = root / 'manuscript' / name
    dst = out / name
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    assert digest == hashlib.sha256(dst.read_bytes()).hexdigest()
    copies.append({'source': str(src.relative_to(root)),
                   'staged': str(dst.relative_to(root)), 'sha256': digest})
command = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
           '-file-line-error', '-recorder', 'main.tex']
result = subprocess.run(command, cwd=out, capture_output=True, text=True)
(out / 'build-console.log').write_text(result.stdout + result.stderr)
record = {'command': command, 'cwd': str(out.relative_to(root)),
          'exit_code': result.returncode, 'clean_build_directory': True,
          'staged_sources': copies,
          'console_log': str((out / 'build-console.log').relative_to(root))}
pdf = out / 'main.pdf'
if pdf.exists():
    record['pdf'] = str(pdf.relative_to(root))
    record['pdf_sha256'] = hashlib.sha256(pdf.read_bytes()).hexdigest()
(out / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
raise SystemExit(result.returncode)
