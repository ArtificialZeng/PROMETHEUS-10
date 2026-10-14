#!/usr/bin/env python3
"""Compile the endpoint manuscript in a fresh project-local directory."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['main.tex', 'endpoint.tex', 'references.bib', 'tree-family.tex', 'endpoint-anchors.tex']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for name in ['pdflatex', 'bibtex', 'pdfinfo', 'pdftotext']:
        if not shutil.which(name):
            raise RuntimeError('Required installed tool unavailable: '+name)
    build = ROOT/'build'; build.mkdir(exist_ok=True)
    (ROOT/'evidence').mkdir(exist_ok=True)
    clean = Path(tempfile.mkdtemp(prefix='endpoint-clean-', dir=build))
    for name in SOURCES:
        shutil.copyfile(ROOT/'manuscript'/name, clean/name)
    latex = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
             '-no-shell-escape', '-recorder', 'main.tex']
    commands = [latex, ['bibtex', 'main'], latex, latex]
    transcript = []; env = dict(os.environ); env['SOURCE_DATE_EPOCH'] = '1791936000'
    for step, command in enumerate(commands, 1):
        result = subprocess.run(command, cwd=clean, env=env, capture_output=True, text=True)
        transcript.extend(['STEP '+str(step)+': '+' '.join(command),
                           result.stdout, result.stderr, 'EXIT '+str(result.returncode)])
        (build/'write-e8b228-build-console.log').write_text('\n'.join(transcript)+'\n')
        if result.returncode:
            raise RuntimeError('Build failed; inspect build/write-e8b228-build-console.log')
    for suffix in ['pdf', 'log', 'bbl', 'blg', 'fls', 'aux']:
        shutil.copyfile(clean/('main.'+suffix), build/('main.'+suffix))
    log = (build/'main.log').read_text(errors='replace')
    fatal = [v for v in log.splitlines() if v.startswith('!') or 'Fatal error' in v or 'Emergency stop' in v]
    unresolved = [v for v in log.splitlines() if re.search(r'undefined|Rerun to get cross-references|Label\(s\) may have changed', v, re.I)]
    boxes = [v for v in log.splitlines() if 'Overfull' in v or 'Underfull' in v]
    info = subprocess.run(['pdfinfo', str(build/'main.pdf')], check=True, capture_output=True, text=True).stdout
    text = subprocess.run(['pdftotext', '-layout', str(build/'main.pdf'), '-'], check=True, capture_output=True, text=True).stdout
    (build/'main.txt').write_text(text); (build/'pdfinfo.txt').write_text(info)
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    record = {'status': 'compiled', 'meaning': 'Writer validation; fresh release review is still required.',
              'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'fresh_build_directory': str(clean.relative_to(ROOT)), 'commands': commands,
              'sources': {'manuscript/'+n: sha(ROOT/'manuscript'/n) for n in SOURCES},
              'pdf': 'build/main.pdf', 'pdf_sha256': sha(build/'main.pdf'),
              'build_log': 'build/main.log', 'build_log_sha256': sha(build/'main.log'),
              'console_log': 'build/write-e8b228-build-console.log', 'pages': pages,
              'text_extraction_nonempty': bool(text.strip()), 'fatal_diagnostics': fatal,
              'unresolved_diagnostics': unresolved, 'box_warnings': boxes}
    (ROOT/'evidence/write-e8b228-build-check.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'pages': pages, 'fatal': fatal, 'unresolved': unresolved,
                      'box_warnings': boxes, 'fresh_directory': str(clean.relative_to(ROOT))}))
    if fatal or unresolved or not text.strip():
        raise RuntimeError('Unresolved compilation issue')


if __name__ == '__main__':
    main()
