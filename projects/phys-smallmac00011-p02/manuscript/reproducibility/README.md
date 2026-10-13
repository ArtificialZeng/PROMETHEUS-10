# Reproducing Figure 1

Run from the project root with Python 3.13 (tested with Python 3.13, NumPy 2.4.2,
SciPy 1.15.3, and Matplotlib 3.10.0):

```sh
MPLCONFIGDIR=/private/tmp/phys-00011-p02-mpl \
python manuscript/reproducibility/make_figure.py
```

The script writes `two_regime_scaling.csv` in this directory and both PDF and
PNG renderings in `../figures/`. It reconstructs the reverse-depolarizing Choi
matrix from the three Pauli Kraus operators. For the positive-overlap example
it numerically optimizes the assisted mutual information and the two-pole
Holevo ensemble for a pure-replacement perturbation. For the zero-overlap
example it evaluates the exact Pauli-channel formulas at
`Q=diag(0.6,0.3,0.1)`.

The calculation uses ordinary double precision and is a diagnostic
visualization of the analytic asymptotics, not a certified error enclosure.
The analytic proof is in `../main.tex`; independent convention checks are
recorded outside the submission bundle in
`../../audit/referee_replay.py` and `../../audit/referee_replay.log`.
