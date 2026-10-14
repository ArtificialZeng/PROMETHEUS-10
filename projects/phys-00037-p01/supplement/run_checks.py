"""Rebuild and check the complete rational witness in a separate output directory."""
import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
output = args.output_dir.resolve()
if output == here or here in output.parents:
    raise ValueError('Use an output directory outside the source supplement directory')
if not __debug__:
    raise RuntimeError('Do not use Python -O: the verifiers rely on exact assertions')
output.mkdir(parents=True, exist_ok=True)
started = time.monotonic()
for name in ['generate_polynomials.py', 'generate_certificate.py',
             'verify_monomials.py', 'verify_cp.py']:
    subprocess.run([sys.executable, str(here/name), '--output-dir', str(output)], check=True)
original = json.loads((here/'certificate.json').read_text())
generated = json.loads((output/'certificate.generated.json').read_text())
if original != generated:
    raise RuntimeError('Fresh generation differs from the supplied complete witness')
mono = json.loads((output/'monomial-check.json').read_text())
cp = json.loads((output/'cp-check.json').read_text())
if mono['status'] != 'pass' or cp['status'] != 'pass':
    raise RuntimeError('An exact replay did not pass')
summary = {
    'status': 'pass',
    'purpose': 'Portable reproduction of the already reviewed statement; no new scientific acceptance',
    'python': platform.python_version(),
    'regenerated_witness_matches': True,
    'rational_coefficients': sum(x['coefficient_count'] for x in original['records']),
    'monomial_source_entries': mono['source_matrix_identities_checked'],
    'cp_source_entries': cp['exact_source_matrix_identities'],
    'gaussian_real_rank': cp['Gaussian_tangent_real_rank'],
    'cp_flip_support_identities': cp['flip_support_identities'],
    'known_baselines': cp['baselines'],
    'numeric_diagnostic_points': len(cp['numerical_diagnostics']),
    'elapsed_seconds': time.monotonic()-started,
}
(output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
