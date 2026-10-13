# Reproducing the qubit local optimality certificate

This package accompanies **Certified local optimality of a qubit counting process over a finite mean interval**. The result is strict local optimality at fixed mean on the specified connected branch for every mean in [3,6], modulo common unitary basis changes. The global attainment problem remains unresolved. Code execution checks the finite certificate; the manuscript supplies the analytic boundary chart and local sufficiency argument.

The package has no network calls, optimizer dependency, external paper downloads, or machine-specific paths. It uses Python 3.12.14, SymPy 1.14.0 and python-flint 0.9.0 in the verified environment. Exact dependency versions are in `requirements.txt`; use an existing environment with these packages. No installation is performed by any supplied script.

From the directory containing `manuscript/` and `supplement/`, run these foreground commands, sequentially:

```sh
python3 -u supplement/code/algebra.py
python3 -u supplement/code/cover.py
python3 supplement/code/make_table.py
```

The first command independently reconstructs the rational functions from Pauli transfer matrices, including both real and complex tangent Hessian blocks. Only after deriving them does it compare against `data/choi-continuation-functions.json`. It checks 40 exact component identities and the three published reference points m=3,4,6, then writes `results/derived-functions.json` and `results/symbolic-check.json`.

The second command reads those newly reconstructed functions. It recomputes every root inclusion, scaled contraction, adjacent-box join, mean-4 anchor join, derivative enclosure and positivity test. It reads only the rational witnesses from the saved cells: saved success flags are not trusted. All 8,433 cells and 8,432 adjacent joins must pass, with exact endpoints covering [3,6]. It writes `results/cover-results.json` and a progress file. The full replay uses 100 decimal digits of Arb arithmetic. An assertion, arithmetic error, nonzero exit, missing final output, or interrupted run is a failed or incomplete replay, never evidence of a physical instability or proof.

The third command regenerates `manuscript/values.tex`. It evaluates the earlier analytic baseline exactly and checks rounding against the saved pointwise cost enclosures. These three points illustrate the moments; they do not supply the continuous-parameter certification.

All scripts write only regenerated outputs in this package, except for the explicitly regenerated manuscript table. Inputs under `data/` are left unchanged. Replaying after manuscript freezing can change result timestamps; reproduce in a separate copy if preserving a release snapshot matters.

The original complete symbolic and interval computations took roughly five and three minutes, respectively, on the recorded macOS arm64 environment. They run one scientific process at a time and do not use GPU or parallel workers. Peak memory and cross-platform runtime bounds were not measured. No claim is made that arbitrary older package versions reproduce the same interval widths.

The defining moments and chart appear in the manuscript. `data/choi-kkt-certificate.json` contains the exact mean-4 anchor coordinates, radii and preconditioner. `data/choi-continuation-cells.jsonl` contains exact rational mean endpoints, centers, radii and preconditioners for the whole cover. The two independently written mathematical implementations share the same model, witness boxes, SymPy and Arb libraries; they are not independent arithmetic libraries.

The supplied code and numerical data were generated within this research project. The package includes no third-party full papers, downloaded library code, private conversations or account information. Attribution to prior counting constructions and Arb is in the manuscript bibliography. A public license and repository deposit remain author decisions; no distribution license or completed deposit is invented here.
