#!/usr/bin/env python3
"""Verify portable portfolio metadata and per-project hashes; no inference."""
from pathlib import Path, PurePosixPath
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    data=json.loads((ROOT/'reproducibility/portfolio.json').read_text());items=data['projects'];by={x['id']:x for x in items};errors=[]
    if len(by)!=len(items):errors.append('duplicate public project ID')
    counts={c:sum(x['counted_as_distinct'] and x['category']==c for x in items) for c in data['counts']}
    if counts!=data['counts']:errors.append('category counts differ')
    if sum(x['counted_as_distinct'] for x in items)!=data['canonical_entries']:errors.append('canonical count differs')
    if len(items)!=data['stored_manuscripts']:errors.append('stored manuscript count differs')
    for x in items:
        pp=PurePosixPath(x['pdf'])
        if pp.is_absolute() or '..' in pp.parts:errors.append(x['id']+': unsafe PDF path');continue
        pdf=ROOT/x['pdf']
        if not pdf.is_file() or sha(pdf)!=x['pdf_sha256']:errors.append(x['id']+': PDF mismatch')
        if x['canonical_id'] not in by or not by[x['canonical_id']]['counted_as_distinct']:errors.append(x['id']+': invalid canonical target')
        if x['category']=='proofs' and x['original_status']!='proved':errors.append(x['id']+': proof scope mismatch')
        if x['category']=='disproofs' and x['original_status']!='disproved':errors.append(x['id']+': disproof scope mismatch')
        p=ROOT/'projects'/x['id']
        for f in x.get('code_files',[])+x.get('reproduction_guides',[]):
            if not (p/f).is_file():errors.append(x['id']+': missing '+f)
        sums=p/'ARTIFACTS.sha256'
        if sums.is_file():
            for line in sums.read_text().splitlines():
                hh,name=line.split('  ',1)
                if not (p/name).is_file() or sha(p/name)!=hh:errors.append(x['id']+': public artifact hash mismatch '+name)
    print(json.dumps({'ok':not errors,'stored':len(items),'canonical':data['canonical_entries'],'counts':counts,'errors':errors},ensure_ascii=False))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
