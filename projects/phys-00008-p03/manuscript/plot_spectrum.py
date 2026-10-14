"""Deterministic illustration of the accepted analytical spectrum; no fitting."""
from pathlib import Path
import os
import json

HERE = Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(HERE / '.matplotlib-cache'))
os.environ.setdefault('XDG_CACHE_HOME', str(HERE / '.cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    theta = np.linspace(0.0, np.pi / 2, 401)
    plus = np.cos(theta / 2) ** 2
    minus = np.sin(theta / 2) ** 2
    small = np.geomspace(1e-4, 1.0, 401)
    gap = np.sin(small / 2) ** 2
    record = {
        'definition': 'Analytical branches on [0,pi/2]; not eigenvalue fits or convergence data',
        'theta': theta.tolist(), 'lambda_plus': plus.tolist(), 'lambda_minus': minus.tolist(),
        'small_theta': small.tolist(), 'exact_formula_gap_samples': gap.tolist(),
        'quadratic_asymptote': (small ** 2 / 4).tolist(),
        'generic_multiplicities': {'zero': 16, 'one': 32, 'plus': 8, 'minus': 8},
        'limitations': 'Binary64 display samples; the all-parameter proof is analytical.'
    }
    (HERE / 'spectrum-data.json').write_text(json.dumps(record, indent=2) + '\n')
    plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.65), layout='constrained')
    ax = axes[0]
    ax.plot(theta, plus, color='#285c8f', linewidth=2, label=r'$\lambda_+=(1+\cos\theta)/2$')
    ax.plot(theta, minus, color='#ad5720', linewidth=2, label=r'$\lambda_-=(1-\cos\theta)/2$')
    ax.axhline(1, color='0.35', linewidth=1, linestyle=':')
    ax.axhline(0, color='0.35', linewidth=1, linestyle=':')
    ax.set(xlabel=r'$\theta$', ylabel='Tangent eigenvalue', xlim=(0, np.pi / 2), ylim=(-.03, 1.03))
    ax.set_xticks([0, np.pi / 4, np.pi / 2], ['0', r'$\pi/4$', r'$\pi/2$'])
    ax.legend(loc='center left', fontsize=8.5, frameon=False)
    ax.set_title('(a) Spectrum branches', fontsize=10)
    ax = axes[1]
    ax.loglog(small, gap, color='#285c8f', linewidth=2, label=r'$\sin^2(\theta/2)$')
    ax.loglog(small, small ** 2 / 4, color='#ad5720', linewidth=1.4, linestyle='--', label=r'$\theta^2/4$')
    ax.set(xlabel=r'$\theta$', ylabel=r'$1-\lambda_+$', xlim=(1e-4, 1.0))
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    ax.set_title('(b) Gap near the endpoint', fontsize=10)
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
    out = HERE / 'figures'
    out.mkdir(exist_ok=True)
    fig.savefig(out / 'spectrum.pdf', metadata={'Title': 'Exact local tangent spectrum', 'Creator': 'Matplotlib analytical plot'})
    plt.close(fig)
    print(json.dumps({'figure': 'manuscript/figures/spectrum.pdf', 'samples': 'manuscript/spectrum-data.json', 'numpy': np.__version__, 'matplotlib': matplotlib.__version__}))

if __name__ == '__main__':
    main()
