#!/usr/bin/env python3
"""Display analytic geometry and certified bound values; no numerical proof here."""
import argparse
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'build' / 'matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(ROOT / 'manuscript' / 'figures' / 'bias-gap.pdf'))
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads((Path(__file__).parent / 'certificate.json').read_text())
    sc = data['scalar_enclosures']
    low = float(sc['L_off']['lower_decimal'])
    upper = float(sc['U_mid']['upper_decimal'])
    d = (math.sin(.6) + math.sin(.4)) / 2
    off = (math.sin(.6), -math.sin(.4))
    blue, red, gray = '#0072B2', '#D55E00', '#444444'
    plt.rcParams.update({'font.size': 9, 'axes.labelsize': 9,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(3.36, 3.95),
                                gridspec_kw={'height_ratios': [1.15, 1]},
                                layout='constrained')
    x = np.linspace(.438, .592, 601)
    boundary = np.cos(np.arccos(x) + 1.0)
    ax.fill_between(x, boundary, -.345, color=blue, alpha=.09, linewidth=0)
    ax.plot(x, boundary, color=gray, linewidth=1.3)
    ax.plot(x, x - 2*d, '--', color=gray, linewidth=1)
    ax.plot(d, -d, 'o', color=blue, markersize=5)
    ax.plot(*off, '^', color=red, markersize=6)
    ax.annotate(r'$C^{\rm mid}$', (d, -d), xytext=(-14, 14),
                textcoords='offset points', color=blue)
    ax.annotate(r'$C^{\rm off}$', off, xytext=(-35, -22),
                textcoords='offset points', color=red)
    ax.text(.445, -.36, r'$Q_{1/2}$', color=blue)
    ax.set(xlim=(.438, .592), ylim=(-.517, -.345), xlabel=r'$C_0$', ylabel=r'$C_1$')
    ax.set_title('(a) Fixed correlation difference', loc='left', fontsize=9)
    ax.set_aspect('equal', adjustable='box')
    bx.hlines(upper, -.16, .16, color=blue, linewidth=2)
    bx.hlines(low, .84, 1.16, color=red, linewidth=2)
    bx.annotate('', (0, .7505), (0, upper),
                arrowprops={'arrowstyle': '-|>', 'color': blue, 'lw': 1.7})
    bx.annotate('', (1, .7900), (1, low),
                arrowprops={'arrowstyle': '-|>', 'color': red, 'lw': 1.7})
    bx.text(-.17, upper+.0012, r'$U_{\rm mid}$', color=blue, fontsize=9)
    bx.text(.87, low-.004, r'$L_{\rm off}$', color=red, fontsize=9)
    bx.annotate('', (.51, low), (.51, upper),
                arrowprops={'arrowstyle': '<->', 'color': gray, 'lw': 1})
    bx.text(.45, .771, r'$>0.0105$', rotation=90, ha='right', va='center', fontsize=8)
    bx.set_xticks([0, 1], ['Center', 'Off-center'])
    bx.set(xlim=(-.35, 1.35), ylim=(.748, .793), ylabel='Entropy (bits per round)')
    bx.set_yticks([.75, .76, .77, .78, .79])
    bx.grid(axis='y', alpha=.15)
    bx.set_title('(b) Bounds, not optimized entropies', loc='left', fontsize=9)
    fig.savefig(out, metadata={'Creator': 'Matplotlib; AI-assisted code',
                              'CreationDate': None, 'ModDate': None})
    fig.savefig(out.with_suffix('.png'), dpi=200)
    print(json.dumps({'figure': str(out), 'source': 'supplement/certificate.json',
                      'L_off_display': low, 'U_mid_display': upper,
                      'precision_note': 'Floating point is used for display only.'}, indent=2))


if __name__ == '__main__':
    main()
