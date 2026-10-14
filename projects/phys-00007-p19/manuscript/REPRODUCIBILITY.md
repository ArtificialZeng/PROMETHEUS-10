# Reproducing the manuscript

The main text and its appendix give the complete exact counterexample and the
finite coefficient bounds. The programs below are an additional reproduction
route. They establish no global optimum and do not confer referee acceptance.

Python 3.10 or later is needed for the wrappers. The recorded symbolic
environment was Python 3.12.14, SymPy 1.14.0, NumPy 2.5.3 and SciPy 1.18.1;
the package requirements are `code/research_requirements.txt`. The isolated
coefficient certificate needs only the Python standard library.

From the source-package root, run:

```sh
python3 manuscript/check_certificate.py
python3 manuscript/run_reproduction.py --python /path/to/existing/python --output build/reproduction
python3 manuscript/build.py --output build/manuscript
```

Use an existing interpreter containing the recorded dependencies for the second
command. No script downloads papers or installs software. The requested output
directories must not exist; previous runs are retained rather than overwritten.
The build requires a TeX distribution with REVTeX 4.2, AMS packages, booktabs,
hyperref, BibTeX, and latexmk. It needs no custom class, style, figure, or font.

The coefficient checker independently encodes the constants printed in the
appendix and reproduces the integer square gap, both radical enclosures,
the full q bound, and the full phi4 bound. It is a writing check of accepted
arithmetic, not a newly independent scientific review.

The replay wrapper copies eight unchanged scientific programs and four defining
input JSON files into the new output directory. It then runs these sequentially:

1. `reproduce_full_qubit_a.py`: full 512-amplitude trace of the complete published
   phase family, with k=m+j.
2. `reproduce_schmidt_b.py`: separately specified Schmidt reduction in q=j-m.
3. `compare_reconstructions.py`: exact convention-map comparison and additional
   generic representation tests; floating tests are diagnostics only.
4. `research_recoupling.py`: known Wigner-6j identity used for tensor convention
   checks. Its linear-programming relaxation is a diagnostic, not a physical
   state or a manuscript result.
5. `research_four_support_a.py`: ordinary full-qubit trace of the counterexample.
6. `research_four_support_b.py`: the separately specified counterexample input
   and the opposite-count Schmidt Gram matrices.
7. `research_verify_four_support.py`: exact coefficient/marginal comparison,
   with additional rational/radical and integer sign checks.
8. `research_fidelity_compare.py`: full fidelity via purity and polarization
   tensors, coefficient equality, rational interval bounds, and the all-phase
   comparison on the stated angle interval.

Each subprocess has a retained log. `reproduction-report.json` records the actual
exit codes and the copied input/code hashes. Generated outputs lie entirely
inside the isolated directory. Running the original programs directly in the
accepted project root would replace frozen output files; use the wrapper.

The two symbolic reconstructions share the state definitions and SymPy.
The extra rational checks use different arithmetic but share the physical
premises. These checks and the separate workflow review do not substitute for
the named author's scientific review or external peer review.

The source package contains project-created TeX, BibTeX, code, state input data,
instructions and the author handoff. It excludes downloaded third-party papers,
private job logs, journal web captures, and internal workflow handoffs. Scientific
primary sources are identified by DOI and version in `manuscript/source-map.md`.
