#!/usr/bin/env python3
"""Replay accepted calculations in a fresh project-local copy, never in frozen evidence."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
replays = ROOT / "build" / "replays"
replays.mkdir(parents=True, exist_ok=True)
stage = Path(tempfile.mkdtemp(prefix="replay-", dir=replays))
(stage / "evidence").mkdir()
(stage / "outputs").mkdir()
originals = [ROOT / "evidence" / "verify_flagged_twist_exact.py",
             ROOT / "evidence" / "replay_flagged_twist_graded.py"]
before = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
          for p in originals}
for source in originals:
    shutil.copy2(source, stage / "evidence" / source.name)
checker = ROOT / "reproducibility" / "occupied_minor_checker.py"
shutil.copy2(checker, stage / checker.name)
records = []
for script in ["evidence/verify_flagged_twist_exact.py",
               "occupied_minor_checker.py",
               "evidence/replay_flagged_twist_graded.py"]:
    command = [sys.executable, script]
    result = subprocess.run(command, cwd=stage, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = stage / "outputs" / (Path(script).stem+".log")
    log.write_text(result.stdout)
    records.append({"script":script,"returncode":result.returncode,
                    "log":str(log.relative_to(ROOT))})
    print(script, "exit", result.returncode)
    if result.returncode:
        print(result.stdout[-4000:])
        raise SystemExit(result.returncode)
exact = json.loads((stage / "evidence" / "flagged-twist-exact.json").read_text())
minor = json.loads((stage / "outputs" / "occupied-minor-results.json").read_text())
assert exact["witness"]["F_parent"] == minor["N34_certificate"]["F_parent"]
assert exact["witness"]["exp_Delta"] == minor["N34_certificate"]["exp_Delta"]
after = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
         for p in originals}
assert before == after
summary = {"status":"completed", "meaning":"Replay assertions only; no new referee or release acceptance",
           "stage":str(stage.relative_to(ROOT)), "checks":records,
           "exact_agreement":{"F_parent":exact["witness"]["F_parent"],
                              "exp_Delta":exact["witness"]["exp_Delta"]},
           "original_code_bytes_unchanged":True}
(stage / "outputs" / "summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
