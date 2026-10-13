"""Portable, single-process replay with outputs isolated from scientific inputs."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CORE_HASH = "d4cf606fe32a87bba0e3b015f3340dd0665443ad64f4a1ba1667f007faf12121"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["source", "bounds", "certificate96", "certificate80", "certificate", "controls", "solve"])
    parser.add_argument("--length", type=int, default=80, help="Even physical cutoff for optional fresh GMRES generation")
    parser.add_argument("--witness", help="For certificate: NPZ path relative to this reproducibility directory")
    parser.add_argument("--out", default="output", help="Output directory relative to this reproducibility directory")
    args = parser.parse_args()
    out = (HERE / args.out).resolve()
    if not out.is_relative_to(HERE) or out == HERE or out.is_relative_to(HERE / "data") or out.is_relative_to(HERE / "reference"):
        parser.error("Outputs must stay in a separate subdirectory of reproducibility, outside data and reference")
    out.mkdir(parents=True, exist_ok=True)
    for name in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"]:
        os.environ[name] = "1"
    sys.dont_write_bytecode = True
    path = HERE / "checker_core.py"
    if hashlib.sha256(path.read_bytes()).hexdigest() != CORE_HASH:
        raise RuntimeError("Checker core differs from the archived implementation")
    spec = importlib.util.spec_from_file_location("certificate_core", path)
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    core.OUT = out
    def save(name, obj):
        # These are replay outputs, never an acceptance or a referee job record.
        record = {"execution": "manuscript_replay", "precision_bits": core.ctx.prec,
                  "implementation_sha256": CORE_HASH, **obj}
        (out / name).write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps(record, indent=2), flush=True)
    core.save = save
    if args.command == "source":
        core.source()
    elif args.command == "bounds":
        save("bounds.json", core.constants()[1])
    elif args.command.startswith("certificate"):
        if args.command == "certificate":
            if not args.witness:
                parser.error("certificate requires --witness")
            witness = (HERE / args.witness).resolve()
            if not witness.is_relative_to(HERE) or not witness.is_file():
                parser.error("--witness must name a file within reproducibility")
        else:
            length = args.command.removeprefix("certificate")
            witness = HERE / "data" / f"witness{length}.npz"
        core.certificate(str(witness))
    elif args.command == "controls":
        core.controls()
    else:
        if args.length < 4 or args.length % 2:
            parser.error("--length must be even and at least four")
        core.solve(args.length)

if __name__ == "__main__":
    main()
