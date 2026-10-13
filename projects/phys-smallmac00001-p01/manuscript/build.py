"""Clean local REVTeX/BibTeX build; run from any working directory.

Only the dedicated build/clean directory is replaced. Sources and scientific
evidence are never modified. A complete command log is retained in build/.
"""
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
target = PROJECT / 'build/clean'
if target.exists():
    shutil.rmtree(target)
target.mkdir(parents=True)
for name in ('main.tex', 'references.bib', 'values.tex'):
    shutil.copy2(PROJECT / 'manuscript' / name, target / name)
commands = [
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
    ['bibtex', 'main'],
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
]
with (PROJECT / 'build/write-build.log').open('w') as log:
    log.write('Clean build started UTC: ' + datetime.now(timezone.utc).isoformat() + '\n')
    for command in commands:
        log.write('\nCOMMAND: ' + ' '.join(command) + '\n')
        log.flush()
        result = subprocess.run(command, cwd=target, stdout=log, stderr=subprocess.STDOUT, timeout=120)
        log.write('EXIT_CODE: ' + str(result.returncode) + '\n')
        log.flush()
        if result.returncode:
            raise SystemExit(result.returncode)
shutil.copy2(target / 'main.pdf', PROJECT / 'build/main.pdf')
print('Clean build completed:', PROJECT / 'build/main.pdf')
