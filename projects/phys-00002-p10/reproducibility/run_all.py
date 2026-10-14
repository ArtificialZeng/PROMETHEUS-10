#!/usr/bin/env python3
"""Replay the manuscript certificates in a new scratch directory.

Reference outputs are consulted only after each calculation has completed.
This is reproduction of accepted calculations, not a fresh scientific audit.
"""
import argparse
import contextlib
import json
import platform
import runpy
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='build/reproduction',
                        help='New scratch directory under build/, relative to project root')
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    if not out.is_relative_to((ROOT / 'build').resolve()) or out == ROOT / 'build':
        raise ValueError('Use a new directory strictly inside build/')
    out.mkdir(parents=True, exist_ok=False)
    environment = {'python': sys.version, 'platform': platform.platform(),
                   'third_party_dependencies': [],
                   'scope': 'Exact algebra and directed full-plane certificate replay'}
    (out / 'environment.json').write_text(json.dumps(environment, indent=2) + '\n')
    paths = ['evidence/alpha-quarter-witness-exact.py',
             'evidence/alpha-quarter-enclosure.py',
             'evidence/alpha-quarter-jensen-enclosure.py',
             'reproducibility/independent_replay.py']
    for name in paths:
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    start = time.monotonic()
    steps = [('evidence/alpha-quarter-witness-exact.py', 'exact.log'),
             ('evidence/alpha-quarter-jensen-enclosure.py', 'decimal.log'),
             ('reproducibility/independent_replay.py', 'integer.log')]
    for name, log in steps:
        print('Running', name, flush=True)
        with (out / log).open('w') as stream:
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                runpy.run_path(str(out / name), run_name='__main__')
    def load(base, name):
        return json.loads((base / name).read_text())
    exact_name = 'evidence/alpha-quarter-witness-exact.json'
    decimal_name = 'evidence/alpha-quarter-jensen-enclosures.json'
    integer_name = 'reproducibility/independent-enclosure.json'
    assert load(out, exact_name) == load(ROOT, exact_name), 'Exact coefficients differ'
    actual = load(out, decimal_name)
    expected = load(ROOT, decimal_name)
    actual.pop('elapsed_seconds', None)
    expected.pop('elapsed_seconds', None)
    assert actual == expected, 'Decimal certificate differs'
    integer = load(out, integer_name)
    assert integer == load(ROOT, integer_name), 'Integer certificate differs'
    assert all(row['strict_violation'] for row in actual['rows'])
    assert integer['strict_frozen_decimal_comparison'] is True
    result = {'status': 'reproduced',
              'exact_coefficients_and_normalization': 'match',
              'decimal_grids': [row['full_plane_upper'] for row in actual['rows']],
              'integer_grid_upper': integer['outward_upper_decimal'],
              'reference_outputs_match': True,
              'elapsed_seconds': time.monotonic() - start,
              'scope': 'One alpha=1/4 product-input counterexample; no new review acceptance'}
    (out / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
