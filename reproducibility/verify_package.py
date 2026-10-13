#!/usr/bin/env python3
"""Cross-platform verification of the full packaged tree."""
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SUMS=ROOT/'reproducibility/SHA256SUMS'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def ignored(path):
 parts=set(path.parts)
 return bool(parts & {'.git','.venv','__pycache__','reproduction-runs'}) or path.suffix=='.pyc'
def main():
 expected={}
 for line in SUMS.read_text().splitlines():
  digest,relative=line.split('  ',1);expected[relative]=digest
 errors=[]
 for relative,digest in expected.items():
  path=ROOT/relative
  if not path.is_file():errors.append(f'missing {relative}')
  elif sha(path)!=digest:errors.append(f'hash mismatch {relative}')
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=SUMS and not ignored(p.relative_to(ROOT))}
 extras=sorted(actual-set(expected))
 errors.extend(f'unlisted file {item}' for item in extras)
 for error in errors:print(error,file=sys.stderr)
 print(f'verified={len(expected)-sum(1 for e in errors if not e.startswith("unlisted"))} listed={len(expected)} extras={len(extras)} ok={not errors}')
 return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
