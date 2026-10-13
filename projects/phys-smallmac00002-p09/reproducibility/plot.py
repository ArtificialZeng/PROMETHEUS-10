"""Render the manuscript figure from its finite-state waiting-law formula.

No logarithmic integral is inferred from the curves. The ODE markers are the
accepted separately constructed absorption-chain data. Defaults regenerate
the authored figure and its numeric inputs, so run before manuscript freeze.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'build/matplotlib-cache'))
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

spec = importlib.util.spec_from_file_location('propagator', ROOT/'reproducibility/src/research_expm.py')
propagator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(propagator)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--figure', type=Path, default=ROOT/'manuscript/figures/waiting.pdf')
    parser.add_argument('--data', type=Path, default=ROOT/'reproducibility/data/figure-data.json')
    args = parser.parse_args()
    x = np.linspace(.005, 3., 301)
    short_x = np.geomspace(.001, .12, 100)
    laws = np.array([propagator.density(float(t), 32) for t in x])
    short_laws = np.array([propagator.density(float(t), 32) for t in short_x])
    ode = json.loads((ROOT/'reproducibility/data/ode-result.json').read_text())
    markers = [r for r in ode['samples'] if .04 <= r['x'] <= 3]
    record = {'r':10,'time_unit':'t_star','phase_gauss_order':32,
              'x':x.tolist(),'A':laws[:,0,0].tolist(),'B':laws[:,1,1].tolist(),
              'short_x':short_x.tolist(),
              'difference_over_x3':((short_laws[:,0,0]-short_laws[:,1,1])/short_x**3).tolist(),
              'markers':markers,'exact_limit':-1.125,
              'scope':'Floating-point illustration; strict sign and integrability are proved analytically.'}
    plt.rcParams.update({'font.size':9,'axes.labelsize':10,'legend.fontsize':8,
                         'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,
                         'axes.spines.right':False})
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.55,2.65), layout='constrained')
    ax.plot(x, laws[:,0,0], color='#155e85', lw=1.5, label=r'$A$: $+\to+$')
    ax.plot(x, laws[:,1,1], color='#b94b26', lw=1.5, ls='--', label=r'$B$: $-\to-$')
    for i,j,marker,color in [(0,0,'o','#155e85'),(1,1,'s','#b94b26')]:
        ax.scatter([m['x'] for m in markers],[m['D'][i][j] for m in markers],
                   s=19,marker=marker,facecolors='none',edgecolors=color,zorder=3)
    ax.set(xlabel=r'Delay $x=\tau/t_*$',ylabel='Dimensionless waiting density',xlim=(0,3))
    ax.legend(frameon=False,loc='upper right')
    ax.text(.02,.97,'(a)',transform=ax.transAxes,va='top')
    bx.semilogx(short_x, record['difference_over_x3'], color='#155e85',lw=1.5)
    bx.axhline(-1.125,color='#404040',ls='--',lw=1,label=r'Exact limit $-9/8$')
    bx.set(xlabel=r'Delay $x=\tau/t_*$',ylabel=r'$[A(x)-B(x)]/x^3$',xlim=(.001,.12))
    bx.legend(frameon=False,loc='upper left',bbox_to_anchor=(.01,.88))
    bx.text(.02,.97,'(b)',transform=bx.transAxes,va='top')
    for a in (ax,bx):a.grid(axis='y',alpha=.18,lw=.5)
    args.figure.parent.mkdir(parents=True,exist_ok=True)
    args.data.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.figure,metadata={'Title':'Same-direction waiting densities at r=10','Author':'Xiaojian Zeng','CreationDate':None,'ModDate':None})
    plt.close(fig)
    args.data.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'figure':str(args.figure),'data':str(args.data),'phase_order':32,
                      'curve_points':len(x),'short_delay_points':len(short_x),
                      'independent_ODE_markers':len(markers)}))

if __name__ == '__main__':
    main()
