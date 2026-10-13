#!/usr/bin/env python3
"""Create a fresh local TeX build with no cached auxiliary files.

Run from any working directory. No downloads, installs, or shell execution.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
build_root = ROOT / 'build'
build_root.mkdir(exist_ok=True)
work = Path(tempfile.mkdtemp(prefix='clean-', dir=build_root))
inputs = ['main.tex', 'references.bib', 'figures/cone.tex',
          'tables/trees.tex', 'tables/witness.tex']
for name in inputs:
    target = work / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'manuscript' / name, target)
argv = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
        '-file-line-error', '-recorder', 'main.tex']
with (work / 'build-driver.log').open('w') as log:
    run = subprocess.run(argv, cwd=work, stdout=log, stderr=subprocess.STDOUT)
record = {'started_from_empty_directory': True,
          'completed_at': datetime.now(timezone.utc).isoformat(),
          'command': argv, 'inputs': inputs, 'exit_code': run.returncode,
          'build_directory': str(work.relative_to(ROOT)),
          'pdf': str((work / 'main.pdf').relative_to(ROOT)),
          'build_log': str((work / 'main.log').relative_to(ROOT)),
          'driver_log': str((work / 'build-driver.log').relative_to(ROOT))}
(work / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
raise SystemExit(run.returncode)
