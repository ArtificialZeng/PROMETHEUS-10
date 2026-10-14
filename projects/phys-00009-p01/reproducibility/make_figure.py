"""Illustrate the accepted two-particle formulas; never edit frozen evidence.

Run from the project/package root with Python 3.12 and requirements.txt.
The numerical curve is an illustration, not an interval certificate.
"""
import json
import os
import platform
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'build' / 'matplotlib-cache'))
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT / 'build' / 'cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import eigh_tridiagonal
import sympy


def radial_gap(dimension, parameter, digits=80):
    """First positive eigenvalue of the reversible distance chain."""
    with mp.workdps(digits):
        a = mp.mpf(parameter)
        down = [2*d*a + (2 if d == 1 else 0)
                for d in range(dimension+1)]
        up = [2*(dimension-d)*a for d in range(dimension+1)]
        symmetric = mp.matrix(dimension+1)
        for d in range(dimension+1):
            symmetric[d, d] = down[d] + up[d]
        for d in range(dimension):
            entry = -mp.sqrt(up[d]*down[d+1])
            symmetric[d, d+1] = symmetric[d+1, d] = entry
        values, vectors = mp.eigsy(symmetric)
        gap = values[1]
        residual = mp.norm(symmetric*vectors[:, 1] - gap*vectors[:, 1])
        assert gap > 0
        return mp.nstr(gap, digits-5), mp.nstr(residual, 8)


def double_gap(dimension, parameter):
    """Independent assembly directly from the upward/downward rates."""
    a = float(parameter)
    diagonal = np.full(dimension+1, 2*dimension*a)
    diagonal[1] += 2
    off_diagonal = np.array([
        -np.sqrt(2*(dimension-d)*a*(2*(d+1)*a + (2 if d == 0 else 0)))
        for d in range(dimension)])
    return float(eigh_tridiagonal(diagonal, off_diagonal,
                                 eigvals_only=True)[1])


def main():
    mp.mp.dps = 90
    points = []
    ratios = np.unique(np.r_[np.linspace(0.03, 3.0, 181), 1.0])
    max_difference = 0.0
    max_residual = mp.mpf('0')
    for ratio in ratios:
        a = mp.mpf(str(float(ratio)))/35
        parameter = mp.nstr(a, 85)
        high, residual = radial_gap(4, parameter)
        independent = double_gap(4, parameter)
        difference = abs(float(high)-independent)
        max_difference = max(max_difference, difference)
        max_residual = max(max_residual, mp.mpf(residual))
        radial_ratio = mp.mpf(high)/(2*a)
        points.append({'dimension': 4, 'a': parameter,
                       'a_over_a4': float(ratio), 'rho_80dps': high,
                       'radial_ratio': float(radial_ratio),
                       'full_gap_ratio': float(min(mp.mpf(1), radial_ratio)),
                       'residual_norm': residual,
                       'scipy_absolute_difference': difference})
    assert max_difference < 1e-11
    sentinels = []
    for ratio in ['0.03', '1', '3']:
        parameter = mp.nstr(mp.mpf(ratio)/35, 85)
        first, _ = radial_gap(4, parameter, 80)
        second, _ = radial_gap(4, parameter, 120)
        with mp.workdps(125):
            difference = abs(mp.mpf(first)-mp.mpf(second))
            assert difference < mp.mpf('1e-70')
            sentinels.append({'a_over_a4': ratio, 'a': parameter,
                              'absolute_80_vs_120_difference': mp.nstr(difference, 8)})
    thresholds = []
    a_d = Fraction(-1, 3)
    for d in range(2, 65):
        if d >= 4:
            assert a_d > 0
            thresholds.append({'dimension': d, 'threshold_exact': str(a_d),
                               'D_squared_a_D_exact': str(d*d*a_d),
                               'D_squared_a_D': float(d*d*a_d)})
        if d <= 16:
            integral = sum((Fraction(comb(d-1, j), 2*j+1)
                            for j in range(d)), Fraction(0))/(2**(d-1))
            assert a_d == (d-1)*integral-1
        a_d = (d*d*a_d+1)/((d-1)*(2*d+1))
    data = {'scope': 'Illustration of the accepted k=2 homogeneous hypercube formulas.',
            'numeric_status': 'High-precision illustrative values; no rigorous interval enclosures claimed.',
            'working_precision_digits': 80,
            'max_scipy_absolute_difference': max_difference,
            'max_high_precision_residual_norm': mp.nstr(max_residual, 8),
            'precision_sentinels': sentinels, 'curve': points, 'thresholds': thresholds}
    target = ROOT/'reproducibility'/'illustration-data.json'
    target.write_text(json.dumps(data, indent=2)+'\n')
    environment = {'python': platform.python_version(), 'numpy': np.__version__,
                   'scipy': scipy.__version__, 'sympy': sympy.__version__,
                   'mpmath': mp.__version__, 'matplotlib': matplotlib.__version__}
    (ROOT/'reproducibility'/'environment.json').write_text(
        json.dumps(environment, indent=2)+'\n')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'axes.titlesize': 10, 'axes.labelsize': 10,
                         'pdf.fonttype': 42, 'ps.fonttype': 42})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), layout='constrained')
    x = [p['a_over_a4'] for p in points]
    axes[0].plot(x, [p['radial_ratio'] for p in points], '--',
                 color='#496880', lw=1.6, label=r'$\rho_4/(2a)$')
    axes[0].plot(x, [p['full_gap_ratio'] for p in points], '-',
                 color='#aa4b31', lw=2.0, label=r'$\lambda_2/\lambda_1$')
    axes[0].axvline(1, color='#555555', lw=0.8, ls=':')
    axes[0].axhline(1, color='#bbbbbb', lw=0.7, zorder=0)
    axes[0].set(xlabel=r'$a/a_4$  ($a_4=1/35$)', ylabel='Gap ratio',
                title='(a) Four-dimensional crossover', xlim=(0, 3))
    axes[0].legend(frameon=False, loc='upper left')
    axes[1].plot([p['dimension'] for p in thresholds],
                 [p['D_squared_a_D'] for p in thresholds],
                 color='#496880', lw=1.7)
    axes[1].axhline(1, color='#555555', lw=0.9, ls='--', label='Limit = 1')
    axes[1].set(xlabel=r'Dimension $D$', ylabel=r'$D^2a_D$',
                title='(b) Exact threshold sequence', xlim=(4, 64))
    axes[1].legend(frameon=False)
    for axis in axes:
        axis.spines[['top', 'right']].set_visible(False)
        axis.grid(axis='y', alpha=0.18)
    out = ROOT/'manuscript'/'figures'
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out/'crossover.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(out/'crossover.png', dpi=180)
    print(json.dumps({'curve_points': len(points), 'threshold_points': len(thresholds),
                      'max_scipy_absolute_difference': max_difference,
                      'max_high_precision_residual_norm': mp.nstr(max_residual, 8),
                      'precision_sentinels': sentinels, 'environment': environment}))


if __name__ == '__main__':
    main()
