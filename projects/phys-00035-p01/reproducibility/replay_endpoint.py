#!/usr/bin/env python3
"""Replay the certificate and table from only their portable source programs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    clean = Path(tempfile.mkdtemp(prefix='endpoint-replay-', dir=ROOT/'reproducibility'))
    for name in ['endpoint_certificate.py', 'make_endpoint_table.py']:
        shutil.copyfile(ROOT/'reproducibility'/name, clean/name)
    commands = [[sys.executable, 'endpoint_certificate.py', '--output', 'certificate.json'],
                [sys.executable, 'make_endpoint_table.py', '--input', 'certificate.json',
                 '--output', 'anchors.tex']]
    console = []
    for command in commands:
        result = subprocess.run(command, cwd=clean, capture_output=True, text=True, timeout=90)
        console.extend(['COMMAND '+' '.join(command), result.stdout, result.stderr,
                        'EXIT '+str(result.returncode)])
        (clean/'replay.log').write_text('\n'.join(console)+'\n')
        if result.returncode:
            raise RuntimeError('Replay failed: '+str(clean/'replay.log'))
    comparisons = []
    for new, old in [('certificate.json', 'reproducibility/endpoint-certificate.json'),
                     ('anchors.tex', 'manuscript/endpoint-anchors.tex')]:
        equal = (clean/new).read_bytes() == (ROOT/old).read_bytes()
        comparisons.append({'reference': old, 'regenerated': str((clean/new).relative_to(ROOT)),
                            'equal_bytes': equal, 'reference_sha256': sha(ROOT/old),
                            'regenerated_sha256': sha(clean/new)})
        assert equal
    record = {'status': 'completed', 'fresh_directory': str(clean.relative_to(ROOT)),
              'commands': commands, 'comparisons': comparisons,
              'log': str((clean/'replay.log').relative_to(ROOT)),
              'meaning': 'Writer portability check using the same certificate program and SymPy. It is not an independent scientific referee or an independent software stack.'}
    (clean/'summary.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
