# Reproducibility guide

This local supplement supports the restricted result in `manuscript/main.tex`. It does not test global entanglement-of-purification additivity, boundary probability tables, product tables, larger auxiliary splits, or finite-distance competitors.

## Environment

The recorded successful runs used CPython 3.12.14 with the versions pinned in `requirements.txt` on macOS. A clean environment may be prepared with a standard Python virtual environment and `python -m pip install -r reproducibility/requirements.txt`. No package installation was performed by the writing job.

## Exact central check

From the root of an unpacked copy of the handoff bundle, run:

```sh
python evidence/research/pass2-8ac137aacbe0/check_phase_identity.py
```

Expected outcome: 45 symmetric coefficient checks, `completed=true`, and `all_zero_polynomials=true` in `symbolic-phase-identity.json`. The computation is exact in `QQ[x,y,z,w]`; its recorded output is included. The denominator and the reason it is nonzero on the strict physical domain are stated in Appendix A of the manuscript.

## Floating diagnostics

The analytic implementation and the separate high-precision tensor/partial-trace replay can be run with:

```sh
python evidence/research/pass2-8ac137aacbe0/analytic_curvature.py
python evidence/research/pass2-8ac137aacbe0/replay_curvature.py
python evidence/research/pass2-8ac137aacbe0/replay_curvature.py --refine-near-product
```

The recorded summaries and logs are included alongside the scripts. These calculations check marginal preservation, auxiliary unitarity, and convergence of selected curvature evaluations. They are not interval certificates and are not the proof of the sign theorem.

The one-copy/reference-limit reconstruction can be replayed from its separately transcribed inputs with:

```sh
python evidence/reproduction/retry-b37ce308cf7f/reconstruct_a.py
python evidence/reproduction/retry-b37ce308cf7f/reconstruct_b.py
python evidence/reproduction/retry-b37ce308cf7f/compare_and_baseline.py
```

Run all commands only in an unpacked copy or a scratch copy. The active project contains a hash-frozen accepted scientific snapshot; running these scripts in place would overwrite recorded outputs and invalidate that provenance even if the recalculated values agree.

## Interpretation

The exact polynomial checker supports the phase identity. The analytic graph-Laplacian and remainder arguments are written out in the manuscript and in `quadratic-form.md`. Numerical files are diagnostics only. A successful rerun is not peer review, human scientific approval, or a resolution of the original additivity question.
