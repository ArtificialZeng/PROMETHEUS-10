"""Compare completed independent computations; this reads both outputs."""
import json
from pathlib import Path
import numpy as np
P=Path('evidence/research')
A=json.loads((P/'expm-result.json').read_text())
B=json.loads((P/'ode-result.json').read_text())
rows=[]
for a,b in zip(A['samples'],B['samples']):
    assert a['x']==b['x']
    error=float(np.max(np.abs(np.array(a['D'])-np.array(b['D']))))
    rows.append({'x':a['x'],'max_absolute_density_error_times_t_star':error,
                 'A_same_direction_difference':a['D'][0][0]-a['D'][1][1],
                 'B_same_direction_difference':b['D'][0][0]-b['D'][1][1]})
worst=max(x['max_absolute_density_error_times_t_star'] for x in rows)
assert worst<5e-11
refinement=[]
for q in B['phase_refinement']:
    old=next(z for z in B['samples'] if z['x']==q['x'])
    refinement.append({'x':q['x'],'max_density_change':float(np.max(np.abs(np.array(q['D'])-np.array(old['D']))))})
convergence=A['convergence']
changes=[abs(a['entropy_times_t_star']-b['entropy_times_t_star']) for a,b in zip(convergence[:-1],convergence[1:])]
normerror=max(abs(z-1) for z in convergence[-1]['row_sums'])
assert normerror<1e-11
result={'comparison':'A piecewise 3x3 exponentials versus B elementary-jump 5x5 DOP853 absorption flux',
        'samples':rows,'max_absolute_density_discrepancy':worst,
        'diagnostic_tolerance':5e-11,'ODE_phase_refinement':refinement,
        'entropy_successive_changes':changes,'final_joint_normalization_error':normerror,
        'illustrative_entropy_times_t_star':convergence[-1]['entropy_times_t_star'],
        'report_rounded_entropy_times_t_star':0.0030163,
        'independence':'Different matrix construction, vector convention, state basis and propagation algorithm within one agent. Shared protocol and laws. No fresh referee.',
        'limitations':'Floating-point comparison and convergence are diagnostics, not interval quadrature certificates. The sign and infinite integral are proved analytically in proof.md; exact-result.json checks its algebra.'}
(P/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
