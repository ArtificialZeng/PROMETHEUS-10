"""Regenerate table and data plot from exact, cross-checked rational values.

Writes only table-rows.tex, display-data.json and the specified figure outputs.
Run only on an unfrozen draft or in a copy before renewing release review.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import os
import runpy

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'build/matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

v = runpy.run_path(str(ROOT / 'reproducibility/scalar_certificate.py'))
original = json.loads((ROOT / 'evidence/layered-exact-a.json').read_text())
assert v['a0'] == F(original['activities'][0])
assert v['a1'] == F(original['activities'][1])
assert [v[k] for k in ['x', 'y', 't']] == [
    F(original['distributions'][1][i]) for i in [0, 3, 7]]
labels = [r'$\Act_0$', r'$\Act_1$', r'$\overline{\Act}_2$', '$x$', '$y$', '$t$']
rows = [label + ' & ' + str(n) + r' \\' for label, n in zip(labels, v['nums'])]
(ROOT / 'manuscript/table-rows.tex').write_text('\n'.join(rows)+'\n')
record = {'arithmetic': 'exact rationals; floats only for display',
          'class_sizes': [3, 4, 4], 'energies_in_epsilon': [0, 1, 64],
          'p0_per_vertex': [str(v[k]) for k in ['u','v','w']],
          'p1_per_vertex': [str(v[k]) for k in ['x','y','t']],
          'activity0': str(v['a0']), 'activity1': str(v['a1']),
          'mean_activity': str((v['a0']+v['a1'])/2),
          'enclosure_denominator': 10**12, 'enclosure_lower_numerators': v['nums']}
(ROOT / 'reproducibility/display-data.json').write_text(json.dumps(record,indent=2)+'\n')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.labelsize': 8, 'legend.fontsize': 7,
                     'pdf.fonttype': 42, 'ps.fonttype': 42})
fig, (graph, ax) = plt.subplots(1, 2, figsize=(7.0, 2.55),
                              gridspec_kw={'width_ratios':[1,1.05]})
coordinates = {0:(0,.5),1:(0,1.5),2:(0,2.5),
               3:(1.7,0),4:(1.7,1),5:(1.7,2),6:(1.7,3),
               7:(3.4,.6),8:(4.35,0),9:(3.4,2.4),10:(4.35,3)}
for left,right in original['edges']:
    px,py=coordinates[left]; qx,qy=coordinates[right]
    graph.plot([px,qx],[py,qy],color='#818B95',linewidth=.7,zorder=1)
for i in range(11):
    px,py=coordinates[i]
    color= '#D1DEE8' if i<3 else ('#EDD1A3' if i<7 else '#C5DFD0')
    label= ('a'+str(i)) if i<3 else (('b'+str(i-3)) if i<7 else ('c'+str(i-7)))
    graph.scatter([px],[py],s=200,color=color,edgecolors='#33424F',
                  linewidths=.7,zorder=2)
    graph.text(px,py,label,fontsize=7,ha='center',va='center',zorder=3)
graph.set_xlim(-.45,4.8); graph.set_ylim(-.6,3.4)
graph.set_axis_off()
graph.set_title('(a) Four-regular proposal graph',fontsize=9,pad=4)
graph.text(0,-.45,r'$A$: $E=0$',ha='center',fontsize=8)
graph.text(1.7,-.45,r'$B$: $E=\epsilon$',ha='center',fontsize=8)
graph.text(3.85,-.45,r'$C$: $E=64\epsilon$',ha='center',fontsize=8)
ax.set_title('(b) Occupation during cooling',fontsize=9,pad=4)
pos = [0,1,2]; width = .33
initial = [float(F(x)) for x in record['p0_per_vertex']]
after = [float(F(x)) for x in record['p1_per_vertex']]
ax.bar([x-width/2 for x in pos], initial, width,
       label=r'Initial Gibbs state $p^{(0)}$', color='#BBC8D3',
       edgecolor='#34495E', linewidth=.6)
ax.bar([x+width/2 for x in pos], after, width,
       label=r'After one update $p^{(1)}$', color='#176B87',
       edgecolor='#173F52', linewidth=.6, hatch='//')
ax.set_xticks(pos, [r'$A$: $E=0$', r'$B$: $E=\epsilon$', r'$C$: $E=64\epsilon$'])
ax.set_ylabel('Probability per microstate')
ax.set_ylim(0, .135)
ax.set_yticks([0,.025,.05,.075,.10,.125])
ax.tick_params(axis='both', labelsize=7, direction='out', length=3)
ax.spines[['top','right']].set_visible(False)
ax.set_axisbelow(True)
ax.grid(axis='y', color='#DEDEDE', linewidth=.5)
ax.legend(loc='upper right', frameon=False, handlelength=1.4)
fig.tight_layout(pad=.6)
target=ROOT/'manuscript/figures/occupations.pdf'
fig.savefig(target, metadata={'Title':'Per-microstate occupation during Glauber cooling',
                             'Author':'Xiaojian Zeng','Creator':'Matplotlib from exact rational data',
                             'CreationDate':None,'ModDate':None})
fig.savefig(ROOT/'build/occupations-preview.png', dpi=180)
print('Exact scalar formulas match preserved full-matrix certificate; table and figure regenerated.')
