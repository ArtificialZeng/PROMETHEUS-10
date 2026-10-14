#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction
import json
b=Path(__file__).resolve().parent
a=json.loads((b/'large-transfer-certificate.json').read_text())
c=json.loads((b/'independent-chain-certificate.json').read_text())
r={k:a[k]==c[k] for k in ['U_plus','U_minus','ordering_margin']}
assert all(r.values())
f=Fraction(a['ordering_margin'])
r['ordering_margin_display_only']=float(f)
r['ordering_margin_strictly_greater_than_1']=f>1
assert f>1
r['independence']='integer symmetric transfer matrix versus original physical bond-satisfaction chain recursion; neither code reads the other or its outputs'
p=json.loads((b/'canonical-radical-certificate.json').read_text())['rows'][-1]
q=json.loads((b/'canonical-direct-certificate.json').read_text())['rows'][-1]
overlap=max(Fraction(p['t_lower']),Fraction(q['t_lower']))<=min(Fraction(p['t_upper']),Fraction(q['t_upper']))
assert overlap
r['independently_computed_canonical_weight_intervals_overlap']=overlap
(b/'input-comparison.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
