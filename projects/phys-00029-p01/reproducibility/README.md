# Reproducing the finite planar counterexample

This package reproduces the unchanged N=1024 uniform-J, zero-field periodic Euclidean witness: 1025 sites per primitive cell, q_max=2055, and Tc/J>2/log(11/10)>20>Tc_star(2055)/J. Read manuscript/main.tex for the analytic geometry, homology transfer, thermodynamic theorem, and exact canonical interpolation. Arithmetic alone does not establish these hypotheses.

Use Python 3.11 or later. The primary checks use only the standard library. The optional symbolic checks use SymPy 1.14.0, listed in requirements.txt. The actual environment used is recorded in environment.json.

From the package root, run in an output directory that does not already exist:

    python3 reproducibility/run_fan.py --output build/fan-check

For the symbolic weighted Kac-Ward and full-polynomial cross-checks, use an interpreter with the listed SymPy version:

    python3 reproducibility/run_fan.py --symbolic --output build/fan-symbolic-check

The driver copies all scripts and expected arithmetic into the new output directory and executes the copies there. It never reruns a writer in the accepted scientific evidence directory. Each script's actual stdout/stderr is saved, and summary.json records return codes. Scripts assert the decisive exact comparisons and fail on a mismatch.

The delivered fan/check_fan.py, check_independent.py, check_canonical_direct.py, check_homology_factor.py, and compare_inputs.py are byte-identical copies of the accepted research checkers. They reconstruct geometry, traces, original small-N homology, weighted Kac-Ward criticality, and both finite-radical representations. The metadata written by those original scripts retains its historical proposer context; it is not a new scientific review.

fan/homology_replay.py adapts the accepted referee's standard-library original-edge elimination into a portable calculation. It checks all four sectors against brute enumeration at N=1,2,3 for t=1/21,1/5,1/3, then sums the N=1024 original graph at t=1/21. It checks the signed quantity, the manuscript's explicit integer inequality, and the exact trace normalization. It also regenerates the triangular-parent/Laves-Star and N=1 temperature calibrations with rational radicals and a bounded logarithm series. Expected referee arithmetic is read only after the corresponding calculation. This portability adaptation is not an independent referee.

The expected-*.json files contain original generated rational/integer arithmetic, not experimental data or copied third-party tables. The driver compares exact U_plus, U_minus, the ordering margin, and all radical endpoints. The direct homology checker compares all original sector integers with the accepted referee certificate. Decimal displays are explanatory; they are never used for a sign or separating inequality.

All central physical conclusions are nonperturbative, at fixed finite N, in the infinite-volume graph model. No Monte Carlo, fit, finite-size extrapolation, rounded canonical constant, or N-to-infinity embedding enters the proof. The program does not determine the large fan's exact critical temperature, a minimum witness, or an optimal replacement bound.

To compile the manuscript from the package root with an existing TeX installation containing REVTeX 4.2, TikZ, and latexmk:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/paper manuscript/main.tex

The figure is imported from manuscript/figures/fan.tex and the bibliography from manuscript/references.bib. Standard TeX packages are not redistributed. The package includes no downloaded third-party paper PDFs, private job logs, account data, or historical drafts. SOURCE_MAP.md links the primary articles and the exact source locations. All publication, author, and external review decisions remain pending.
