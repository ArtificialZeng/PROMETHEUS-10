"""Compile the manuscript from the portable bundle root, preserving actual logs."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
output = args.output_dir.resolve()
try:
    relative_output = output.relative_to(root)
except ValueError:
    raise ValueError('Use an output directory inside the portable bundle root')
output.mkdir(parents=True, exist_ok=True)
tex = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
       '-halt-on-error', '-file-line-error', '-recorder',
       '-output-directory', str(output), 'manuscript/main.tex']
commands = [tex, ['bibtex', str(relative_output/'main')], tex, tex]
logs = []
for i, command in enumerate(commands, 1):
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    body = 'COMMAND: '+repr(command)+'\n'+result.stdout
    (output/f'command-{i}.log').write_text(body)
    logs.append(body)
    (output/'build.log').write_text('\n'.join(logs))
    if result.returncode:
        print(result.stdout)
        raise SystemExit(result.returncode)
print(str(output/'main.pdf'))
