#!/usr/bin/env python3
"""Recompute both global certificates without modifying shipped reference data."""
import argparse
import contextlib
import datetime
import io
import json
import platform
from fractions import Fraction
from pathlib import Path
import interval_cells
import decimal_grid


def main():
    if not __debug__:
        raise SystemExit('Run without -O: arithmetic assertions are required.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='replay-output')
    args = parser.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    reference = json.loads((Path(__file__).parent / 'certificate.json').read_text())
    progress = io.StringIO()
    with contextlib.redirect_stdout(progress):
        integer = interval_cells.run(65536)
        dec = decimal_grid.run()
    assert integer['full_domain_affine_pass']
    assert integer['global_lower'] == reference['integer_cells']['global_lower']
    assert integer['minimum_cell_indices'] == reference['integer_cells']['minimum_cell_indices']
    assert integer['scalar_enclosures'] == reference['scalar_enclosures']
    assert dec['all_assertions_passed']
    for actual, expected in [('sample_minimum_lower', 'sample_minimum_lower'),
                             ('continuum_correction_upper', 'correction_upper'),
                             ('continuum_lower', 'continuum_lower')]:
        assert Fraction(dec[actual]) == Fraction(reference['grid'][expected])
    result = {
        'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python': platform.python_version(),
        'integer_cells': integer,
        'decimal_nodes': dec,
        'comparison_with_shipped_certificate': 'pass',
        'scope': reference['scope'],
        'parallel_workers': 1,
    }
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'progress.log').write_text(progress.getvalue())
    print(json.dumps({'pass': True, 'output': str(out / 'results.json'),
                      'integer_seconds': integer['seconds'],
                      'decimal_seconds': dec['seconds'],
                      'gap_lower': integer['scalar_enclosures']['strict_gap']['lower_decimal']},
                     indent=2))


if __name__ == '__main__':
    main()
