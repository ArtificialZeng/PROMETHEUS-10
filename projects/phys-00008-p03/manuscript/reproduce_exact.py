"""Replay the frozen generator program in an isolated output directory.

This is a reproducibility replay, not a new independent scientific referee.
The preserved program must never be run in place after scientific freezing.
"""
from pathlib import Path
import argparse
import importlib.util
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='build/reproduction', help='Fresh project-relative output directory')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    out = (root / args.output).resolve()
    if out == root or root not in out.parents:
        parser.error('Output must be a proper subdirectory of the project')
    if out.exists():
        parser.error('Output must be a fresh directory; preserved outputs are never overwritten')
    source = root / 'evidence/research/exact_family.py'
    if not source.is_file():
        parser.error('The accompanying exact generator program is missing')
    out.mkdir(parents=True)
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('accepted_generator_replay', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT = out
    module.main()

if __name__ == '__main__':
    main()
