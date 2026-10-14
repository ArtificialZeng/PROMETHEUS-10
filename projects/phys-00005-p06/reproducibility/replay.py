#!/usr/bin/env python3
"""Replay the retained certificate and checks in a new output directory.

Original scientific files are never overwritten. This is a calculation wrapper,
not a referee-acceptance or publication tool.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='reproducibility/replay-output',
                        help='New directory inside this unpacked project; must not exist.')
    parser.add_argument('--certificate-only', action='store_true')
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        parser.error('--output must be a new directory inside the project')
    if output.exists():
        parser.error('--output already exists; choose a new path')
    (output / 'scripts').mkdir(parents=True)
    (output / 'evidence').mkdir()
    script_files = ['certify_r4_root.py', 'replay_r4_eigenseries.py',
                    'check_r4_symbolic_and_bounds.py']
    for name in script_files:
        shutil.copy2(ROOT / 'scripts' / name, output / 'scripts' / name)
    original = json.loads((ROOT / 'evidence/research-root-certificate.json').read_text())
    module_file = output / 'scripts/certify_r4_root.py'
    spec = importlib.util.spec_from_file_location('retained_certificate', module_file)
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    rec = module.certificate(original['center_exact_decimal'], original['radius_exact_decimal'])
    if not rec['certificate_pass']:
        raise RuntimeError('The replayed certificate did not pass its strict inequalities')
    if rec['preconditioner_exact_decimal'] != original['preconditioner_exact_decimal']:
        raise RuntimeError('Recomputed preconditioner differs; inspect environment before comparison')
    (output / 'evidence/research-root-certificate.json').write_text(json.dumps(rec, indent=2) + '\n')
    print(json.dumps({'stage': 'root-certificate', 'certificate_pass': rec['certificate_pass'],
                      'output': str(output.relative_to(ROOT))}), flush=True)
    if not args.certificate_only:
        for name in script_files[1:]:
            result = subprocess.run([sys.executable, '-B', str(output / 'scripts' / name)],
                                    cwd=output, capture_output=True, text=True)
            (output / (name.removesuffix('.py') + '.log')).write_text(result.stdout + result.stderr)
            print(json.dumps({'stage': name, 'exit_code': result.returncode}), flush=True)
            if result.returncode != 0:
                raise RuntimeError(f'{name} failed; actual stdout/stderr are retained')


if __name__ == '__main__':
    main()
