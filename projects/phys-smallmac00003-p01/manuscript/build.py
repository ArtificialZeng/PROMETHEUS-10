#!/usr/bin/env python3
"""Build the complete manuscript in a fresh, project-local generated directory."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build' / 'clean'
SOURCES = ('main.tex', 'references.bib', 'vertices.tex')


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    for name in SOURCES:
        shutil.copyfile(ROOT / 'manuscript' / name, BUILD / name)
    latex = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
             '-halt-on-error', '-file-line-error', '-recorder', 'main.tex']
    commands = [latex, ['bibtex','main'], latex, latex]
    logpath = ROOT / 'build' / 'clean-build.log'
    with logpath.open('w') as log:
        for cmd in commands:
            log.write('$ '+' '.join(cmd)+'\n')
            log.flush()
            result = subprocess.run(cmd, cwd=BUILD, stdout=log, stderr=subprocess.STDOUT)
            log.write('exit_code='+str(result.returncode)+'\n')
            if result.returncode:
                print('Build failed; see '+str(logpath))
                return result.returncode
    print(json.dumps({'pdf':'build/clean/main.pdf','log':'build/clean-build.log',
                      'source_copies_sha256':{name:hashlib.sha256((BUILD/name).read_bytes()).hexdigest()
                                               for name in SOURCES}}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
