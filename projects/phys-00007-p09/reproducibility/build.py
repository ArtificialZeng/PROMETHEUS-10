"""Clean local manuscript build; no scientific evidence is modified."""
import os
from pathlib import Path
import subprocess
import json

root = Path(__file__).resolve().parents[1]
out = root / 'build' / 'write-final'
if out.exists():
    raise SystemExit('Use a fresh build/write-final directory; retain existing logs.')
out.mkdir(parents=True)
env = os.environ.copy()
env['BIBINPUTS'] = str(root / 'manuscript') + os.pathsep
records = []
latex = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
         '-recorder', '-output-directory=' + str(out), 'main.tex']
steps = [(latex, root / 'manuscript'), (['bibtex', 'main'], out),
         (latex, root / 'manuscript'), (latex, root / 'manuscript')]
for n, (command, cwd) in enumerate(steps, 1):
    run = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    (out / ('pass-' + str(n) + '.txt')).write_text(run.stdout + run.stderr)
    records.append({'command': command, 'cwd': str(cwd), 'exit_code': run.returncode})
    (out / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
    if run.returncode:
        raise SystemExit(run.returncode)
print(json.dumps({'status': 'built', 'pdf': str(out / 'main.pdf')}))
