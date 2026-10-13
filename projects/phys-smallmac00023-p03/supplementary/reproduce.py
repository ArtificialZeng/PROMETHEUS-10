"""Sequential exact reproduction in a new isolated directory, without reference mutation."""
from pathlib import Path
import argparse
import contextlib
import datetime
import json
import os
import runpy
import shutil
import sys
import sympy

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists; choose a fresh directory.')
    if output == base or base.is_relative_to(output):
        parser.error('Output must not contain the supplied supplement.')
    expected = os.environ.get('PHYSICS_PYTHON')
    if expected and sys.executable != expected:
        parser.error('Infrastructure blocker: interpreter differs from PHYSICS_PYTHON.')
    output.mkdir(parents=True)
    shutil.copytree(base/'code', output/'code')
    shutil.copytree(base/'evidence', output/'evidence')
    versions = {'python_executable': sys.executable, 'python': sys.version,
                'sympy': sympy.__version__,
                'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    for name in ('numpy', 'scipy'):
        try:
            module = __import__(name)
            versions[name] = module.__version__
        except ImportError:
            versions[name] = 'not installed; not needed for decisive checks'
    (output/'environment.json').write_text(json.dumps(versions, indent=2)+'\n')
    order = ['reproduction/input_a_number_states.py', 'reproduction/input_b_kraus.py',
             'reproduction/compare_inputs.py', 'reproduction/qubit_baseline.py',
             'research/reduce_extension.py', 'research/exact_certificate.py',
             'research/endpoint_symbolic_replay.py', 'research/composition_check.py']
    try:
        with (output/'replay.log').open('w') as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                for name in order:
                    print('Running', name, flush=True)
                    runpy.run_path(str(output/'code'/name), run_name='__main__')
                    print('Completed', name, flush=True)
        comparisons = {}
        for reference in sorted((base/'evidence').glob('*.json')):
            generated = output/'evidence'/reference.name
            comparisons[reference.name] = (json.loads(reference.read_text()) ==
                                           json.loads(generated.read_text()))
        assert all(comparisons.values()), comparisons
        report = {'status': 'pass', 'scripts_completed': order,
                  'reference_records_equal': comparisons,
                  'limitations': 'Symbolic/sign reproduction; full-space lift and '
                                 'parameter coverage also require the analytic manuscript argument.'}
    except Exception as exc:
        (output/'comparison.json').write_text(json.dumps(
            {'status': 'failed', 'exception': repr(exc)}, indent=2)+'\n')
        raise
    (output/'comparison.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
