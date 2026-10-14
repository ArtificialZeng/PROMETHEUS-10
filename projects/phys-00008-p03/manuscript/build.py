"""Clean foreground TeX/BibTeX build using only declared manuscript inputs."""
from pathlib import Path
import argparse
import subprocess
import os
import json
import hashlib
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='build/clean', help='Fresh project-relative directory')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    out = (root / args.output).resolve()
    if out == root or root not in out.parents or out.exists():
        parser.error('Output must be a new proper subdirectory of the project')
    out.mkdir(parents=True)
    env = dict(os.environ)
    env['BIBINPUTS'] = str(here) + os.pathsep + env.get('BIBINPUTS', '')
    tex = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
           '-recorder', '-output-directory=' + str(out), str(here / 'main.tex')]
    commands = [(tex, here), (['bibtex', 'main'], out), (tex, here), (tex, here)]
    provenance = {'started_at': datetime.now(timezone.utc).isoformat(), 'commands': [],
                  'inputs': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [here / 'main.tex', here / 'references.bib', here / 'figures/spectrum.pdf']}}
    with (out / 'compiler-stdout.log').open('w') as log:
        for command, cwd in commands:
            result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=90)
            log.write('COMMAND ' + json.dumps(command) + '\nCWD ' + str(cwd) + '\n')
            log.write(result.stdout + result.stderr + '\n')
            log.flush()
            provenance['commands'].append({'argv': command, 'cwd': str(cwd.relative_to(root)),
                                            'returncode': result.returncode})
            if result.returncode:
                provenance['status'] = 'failed'
                (out / 'build-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
                print(result.stdout[-6000:] + result.stderr[-3000:])
                raise SystemExit(result.returncode)
    provenance.update({'status': 'completed', 'completed_at': datetime.now(timezone.utc).isoformat(),
                       'pdf': str((out / 'main.pdf').relative_to(root)),
                       'pdf_sha256': hashlib.sha256((out / 'main.pdf').read_bytes()).hexdigest()})
    (out / 'build-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps(provenance))

if __name__ == '__main__':
    main()
