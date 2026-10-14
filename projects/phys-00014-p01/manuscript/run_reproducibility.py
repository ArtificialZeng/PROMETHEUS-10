"""Replay the accepted checks in a new isolated directory.

The original scientific files are read-only inputs. The legacy scripts write
beside their own code, so copies, rather than originals, are executed.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
INPUTS = [
    "evidence/reproduce/exact_input_map.py",
    "evidence/reproduce/input-a.json",
    "evidence/research/check_exact_certificates.py",
    "evidence/research/replay_physical_measurement.py",
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="reproduction-run",
                        help="new project-relative output directory; must not exist")
    args = parser.parse_args()
    relative = Path(args.output)
    if relative.is_absolute() or ".." in relative.parts:
        parser.error("output must be a project-relative directory without parent traversal")
    stage = ROOT / relative
    if stage.exists():
        parser.error("output already exists; choose a new output directory")
    before = {name: digest(ROOT / name) for name in INPUTS}
    stage.mkdir(parents=True)
    for name in INPUTS:
        target = stage / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        assert digest(target) == before[name]
    commands = [
        "evidence/reproduce/exact_input_map.py",
        "evidence/research/check_exact_certificates.py",
        "evidence/research/replay_physical_measurement.py",
    ]
    runs = []
    for script in commands:
        log = stage / (Path(script).stem + ".log")
        with log.open("w") as output:
            result = subprocess.run([sys.executable, str(stage / script)],
                                    cwd=stage, stdout=output,
                                    stderr=subprocess.STDOUT, check=False)
        runs.append({"script": script, "exit_code": result.returncode,
                     "log": log.relative_to(stage).as_posix(), "log_sha256": digest(log)})
        if result.returncode:
            raise RuntimeError(f"Replay failed: {script}; inspect {log}")
    after = {name: digest(ROOT / name) for name in INPUTS}
    assert after == before, "Original scientific inputs changed"
    exact = json.loads((stage / "evidence/research/exact-certificates.json").read_text())
    moments = json.loads((stage / "evidence/reproduce/exact-input-map.json").read_text())
    measurement = json.loads((stage / "evidence/research/physical-measurement-replay.json").read_text())
    report = {
        "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version, "python_executable": sys.executable,
        "input_sha256": before, "original_inputs_unchanged": True,
        "runs": runs,
        "source_moments_exact_match": moments["all_exact_entries_match"],
        "exact_entries_checked": exact["checked_entries"],
        "exact_failure_count": exact["failure_count"],
        "maximum_direct_risk_residual": measurement["max_direct_risk_residual"],
        "scope": "Replay of the accepted fixed-Bell k=1 formulas and certificates; no new result or referee acceptance. Floating integration is corroboration, not a certified enclosure.",
        "provenance_note": "Embedded legacy job labels identify the original scripts. Copied-script outputs are fresh reruns and do not create workflow audit records."
    }
    (stage / "reproduction-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
