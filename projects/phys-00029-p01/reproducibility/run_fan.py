#!/usr/bin/env python3
"""Run the supplied exact checkers in a new output directory.

The frozen sources and supplied comparison data are never rewritten.
Use --symbolic with an interpreter containing SymPy 1.14.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--symbolic", action="store_true")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent/"fan"
    output = args.output.resolve()
    if output == source.resolve() or source.resolve() in output.parents:
        parser.error("output must be outside the supplied fan source directory")
    source_hashes = {
        p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in source.iterdir() if p.is_file()
    }
    output.mkdir(parents=True,exist_ok=False)
    for p in sorted(source.iterdir()):
        if p.is_file():
            shutil.copy2(p,output/p.name)
    scripts = ["check_fan.py","check_canonical_direct.py","homology_replay.py"]
    if args.symbolic:
        scripts.extend(["check_independent.py","check_homology_factor.py","compare_inputs.py"])
    steps = []
    for script in scripts:
        command = [sys.executable,str(output/script)]
        run = subprocess.run(command,cwd=output,text=True,capture_output=True)
        (output/(script+".stdout.log")).write_text(run.stdout or "(no stdout)\n")
        (output/(script+".stderr.log")).write_text(run.stderr or "(no stderr)\n")
        steps.append({"script":script,"returncode":run.returncode})
        if run.returncode != 0:
            print(run.stdout)
            print(run.stderr,file=sys.stderr)
            (output/"summary.json").write_text(json.dumps({"steps":steps,"completed":False},indent=2)+"\n")
            return run.returncode
    actual = json.loads((output/"large-transfer-certificate.json").read_text())
    expected = json.loads((output/"expected-large-transfer-certificate.json").read_text())
    assert all(actual[k] == expected[k] for k in ["U_plus","U_minus","ordering_margin"])
    for prefix in ["canonical-radical","canonical-direct"]:
        actual = json.loads((output/(prefix+"-certificate.json")).read_text())
        expected = json.loads((output/("expected-"+prefix+"-certificate.json")).read_text())
        assert actual["rows"] == expected["rows"]
    if args.symbolic:
        actual = json.loads((output/"independent-chain-certificate.json").read_text())
        expected = json.loads((output/"expected-independent-chain-certificate.json").read_text())
        assert all(actual[k] == expected[k] for k in ["U_plus","U_minus","ordering_margin"])
    after_hashes = {
        p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in source.iterdir() if p.is_file()
    }
    assert source_hashes == after_hashes
    summary = {
        "completed":True,"mode":"exact arithmetic regeneration",
        "symbolic_requested":args.symbolic,"steps":steps,
        "frozen_expected_trace_and_radical_data_match":True,
        "source_directory_unchanged":source_hashes == after_hashes,
        "source_sha256":source_hashes,
        "limitations":"This run checks arithmetic and portability; it is not fresh referee acceptance or external peer review.",
    }
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
