# Reproducing the half-line obstruction

This directory contains a complete single-process certificate replay for the
restricted result in the accompanying manuscript. It does not certify a phase
boundary, exceptional point, lifetime, or finite-perturbation strong zero mode.
No finite-size extrapolation is used.

Use Python 3.12 with the versions recorded in environment.json and
requirements.txt. The project was checked with NumPy 2.3.5, SciPy 1.18.1,
SymPy 1.14.0, python-flint 0.9.0 and Matplotlib 3.11.2. The interval
precision is 224 bits. All commands below run in the foreground. No package
installer, account, external service or model process is invoked.

From the parent directory containing manuscript and reproducibility, run:

    python3 -B reproducibility/replay.py --help
    python3 -B reproducibility/replay.py source
    python3 -B reproducibility/replay.py bounds
    python3 -B reproducibility/replay.py certificate96
    python3 -B reproducibility/replay.py certificate80
    python3 -B reproducibility/replay.py controls
    python3 -B reproducibility/plot_bounds.py
    python3 -B manuscript/build.py

In the original local environment the scientific interpreter is
python3; substitute that for
python3 in the scientific commands if using that existing environment.
The build additionally needs the existing pdflatex, bibtex, pdfinfo
and pdftotext executables. It copies the manuscript sources into
build/clean, rebuilds from scratch with shell escape disabled, and writes
build/main.pdf, the final compiler log build/build.log, the full command
transcript build/commands.log, and extracted text. The PDF date is fixed
to 2026-09-12 UTC for reproducible compilation; actual execution provenance
is kept separately.

The replay driver sets numeric library thread counts to one. It writes only
under reproducibility/output by default, and never overwrites the data
or reference directories. --out chooses another separate subdirectory.
Run the driver, not checker_core.py directly: the core is an unchanged
historical independent implementation with its original output defaults
and provenance identifiers. The driver substitutes output handling and
records executions as manuscript replays, not as new referee acceptances.

data/witness96.npz and data/witness80.npz store exact binary complex
coefficients in Q1_cubic. The full array is antisymmetric in its two B
indices; coefficients with B indices in increasing order represent the
independent exterior basis. The array shapes are (95,96,96) and
(79,80,80). Array entries are treated as dyadic rationals. The checker
does not use eigenvectors or a previously reported residual as an answer.
The original 96-site witness used a spectral generator; the 80-site
witness was generated independently by nearest-neighbour GMRES from zero.
Their source hashes and origin paths are mapped in the local dossier
manuscript/reproduction-provenance.json.

Expected results are retained in reference/. The historical records preserve
the original implementer's identity and original project-relative input names.
Those names document provenance; portable execution reads the copies in
data/, checks their actual coefficients and prints new input hashes.
The replay output names retain the original core's filename prefixes.

The source command checks nine exact occupation-bit/Pauli cases through
six sites, the quadratic/quartic Majorana identities, parity, the left-row
recurrences, and the published Hermitian gap limit. The bounds command proves
the two-coordinate root by an interval contraction and encloses the analytic
inverse and functional constants. Both witness certificates include the
physical cutoff-crossing links, complete omitted geometric source and
normalization correction. The controls command compares direct Clifford
multiplication against the determinant contraction on 156 quintic
coefficients and detects deletion of the physical cutoff-crossing bond.

The expected infinite real-part enclosures, rounded outwards, are:

| Witness | Lower bound on Re Phi/t | Upper bound | Proves Re Phi/t > 0.0001 |
| --- | ---: | ---: | --- |
| 96 sites | 0.0001054530 | 0.0001525309 | yes |
| Independent 80 sites | 0.0000796284 | 0.0001783554 | no; excludes zero |

The figure uses these certified intervals and the exact real band extrema,
not a statistical fit. Its JSON records the outward-rounded plotted values.
The integer residual multiplier is 1248632935. The 96-site total weighted
residual is below 1.885174e-14 in units of t; the functional error is below
2.353890e-5 t.

For an optional fresh generation, with potentially much higher memory use
than certificate replay:

    python3 -B reproducibility/replay.py solve --length 80
    python3 -B reproducibility/replay.py certificate --witness output/referee-Q1-L80.npz

Recomputed floating witnesses can differ across BLAS implementations.
Their own interval certificate, rather than array equality or matching
decimal digits, determines what can be concluded. No new generation is
required to check the supplied exact dyadic witnesses.

The manuscript's analytic sections are essential: the code alone does not
establish the bounded half-line similarity, all-degree localized-kernel
uniqueness, domain of the local derivation, or summation by parts at infinity.
No external peer review or human author approval is represented by a
successful replay.
