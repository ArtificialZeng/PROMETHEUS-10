# Reproducing the periodic waiting-time counterexample

The analytic proof is in `manuscript/main.tex`. The scripts verify its algebra and illustrate its magnitude; floating-point quadrature does not establish the strict sign.

The model is a triangle with dimensionless symmetric edge rates `(r,1,1)`, `(1,r,1)`, `(1,1,r)` for one time unit each. The visible events are `1->2` and `2->1`. The exact result holds for each fixed `r>0`, `r!=1`; numerical data and the explicit rational bound concern `r=10`. All densities are joint in the next label and delay. Entropy rates in the data are multiplied by `t_star`.

From the project root, with an existing Python environment containing the recorded packages:

```sh
python3 reproducibility/run.py --mode quick --output reproducibility/runs/quick
python3 reproducibility/run.py --mode independent --output reproducibility/runs/independent
python3 reproducibility/run.py --mode full --output reproducibility/runs/full
```

Each command requires a new output directory. The runner copies the scientific implementations there and runs them sequentially with numerical-library threads limited to one. It never overwrites the supplied data. `quick` replays two exact constructions; `independent` also runs the five-state Poisson uniformization calculation with Gauss order 24 and delay cutoff 80. `full` additionally regenerates the original three-state matrix-exponential convergence sequence (up to order 64), the separate absorbing-chain DOP853 samples and their comparison. No random numbers or seeds are involved. Maximum matrix size is 5 by 5. A per-command ceiling of 600 seconds is enforced; measured replay usage is in the local output logs. Cross-platform wall times are not promised.

The independent implementation was originally constructed in a separate verification context without importing the discovery code or its numeric answers. The distributed file preserves its original comments; rerunning it now is a replay of that implementation, not another independent scientific review.

`data/expm-result.json`, `ode-result.json`, `comparison.json` and `exact-result.json` retain the original scientific outputs. `data/independent-q16.json` and `independent-q24.json` contain the numeric portions of the independent replay. Table 1 uses their actual convergence values. The text reports only the descriptive value `0.0030163/t_star`. The conservative sign bound is `27/(4480*20000**7)`, and the full analytic logarithmic-tail bound at `H=80` is below `2.051e-13/t_star`. These serve different purposes: no tail error is subtracted from the exact nonnegative-integrand sign proof.

To reproduce the figure in a fresh location without changing the supplied figure/data:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 reproducibility/plot.py --figure reproducibility/runs/figure-check.pdf --data reproducibility/runs/figure-check.json
```

The plot evaluates the accepted matrix-exponential waiting-law formula with 32-point phase quadrature and overlays the accepted independent ODE samples. Its curves are numerical illustrations with no certified quadrature enclosure. `environment.json` and `requirements.txt` record the available writing/replay environment; the original research data retain their own environment records.

For the PDF, TeX Live with `pdflatex`, `bibtex`, `latexmk` and the standard packages listed in `main.tex` is sufficient. Run:

```sh
python3 manuscript/build.py --output build/rebuilt
```

This also requires a new build directory, stages only the declared TeX/Bib/figure sources, runs LaTeX without shell escape, and retains all logs. No third-party full papers, browser conversations, credentials or private research logs are part of the submission file list. This is a local draft requiring author review and the separate release checks described in `AUTHOR_HANDOFF.md`.
