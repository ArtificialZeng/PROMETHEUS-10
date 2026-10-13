#!/usr/bin/env python3
"""Verify packaged SmallMac artifacts without changing them."""
from pathlib import Path
import argparse, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/'reproducibility/small_mac_projects.json').read_text())
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def check(row):
 project=ROOT/'projects'/row['id']; errors=[]
 manifest=project/'ARTIFACTS.sha256'
 for line in manifest.read_text().splitlines():
  expected,relative=line.split('  ',1); path=project/relative
  if not path.is_file():errors.append(f'missing {relative}')
  elif sha(path)!=expected:errors.append(f'hash mismatch {relative}')
 if sha(project/'paper.pdf')!=row['pdf_sha256']:errors.append('paper hash mismatch')
 return errors
def main():
 p=argparse.ArgumentParser();p.add_argument('--project',choices=[x['id'] for x in MANIFEST]);p.add_argument('--all',action='store_true');p.add_argument('--list',action='store_true');a=p.parse_args()
 if a.list: print(json.dumps(MANIFEST,ensure_ascii=False,indent=2));return 0
 if not a.project and not a.all:p.error('choose --project or --all')
 failed=False
 for row in MANIFEST if a.all else [next(x for x in MANIFEST if x['id']==a.project)]:
  errors=check(row); print(json.dumps({'project':row['id'],'ok':not errors,'errors':errors},ensure_ascii=False));failed|=bool(errors)
 return int(failed)
if __name__=='__main__':raise SystemExit(main())
