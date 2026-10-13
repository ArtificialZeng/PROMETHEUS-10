# Exact reproduction of the two-qutrit APPT purity certificate

The manuscript proves that every APPT state on C^3 tensor C^3 has purity at
most 17/121, with unique ordered equality spectrum (3,1,1,1,1,1,1,1,1)/11.
The proof uses a three-cut outer polytope. Its completeness argument is in the
paper; the programs implement finite exact checks rather than replace that
argument. There is no Monte Carlo, optimization tolerance, or floating-point
feasibility decision.

Run from the top-level folder of this manuscript package:

```sh
python3 supplement/verify_vertices.py --compare supplement/vertices.json --output reproduction-run/vertices.json
python3 supplement/verify_clipping.py --output reproduction-run/clipping.json
```

The first command solves all 495 raw-spectrum active bases using Python's
`fractions.Fraction`, generates the full vertex set, and only then reads the
distributed certificate for comparison. Expected results: 72 singular bases,
63 feasible bases including duplicates, 49 distinct vertices, maximum 17/121,
one maximizing spectrum, runner-up 5/36. It checks all 14 principal minors of
the two source matrices at the equality spectrum.

The second command uses incremental halfspace clipping and exact active-rank
filtering, with cuts reconstructed from three Schmidt partial-transpose
spectra. Expected stage vertex counts are 15, 31, 49, with respective maxima
25/169, 1/7, 17/121. It also checks both source LMIs coefficientwise and the
maximally mixed, rank-eight uniform, and pure control spectra. Its mathematical
functions preserve the separate pre-manuscript replay. Both programs use
the standard library and share rational arithmetic; they are not formally
verified software, and running them is not human peer review.

`vertices.json` contains every ordered spectrum, all nine gap weights, three
cut slacks, purity, and the nonnegative difference from 17/121. All numbers are
exact fraction strings. The table is not a sample. To regenerate its TeX into
a disposable output directory without changing the supplied sources:

```sh
python3 supplement/verify_vertices.py --compare supplement/vertices.json --table reproduction-run/vertices.tex
```

The generated file agrees byte for byte with `manuscript/vertices.tex` under
the supplied program. At most four positive gap weights is a proved property
of vertices of this outer polytope, not an imposed restriction on physical
spectra. No APPT claim is made about a general vertex of the outer polytope.

To compile the article, use the existing TeX installation:

```sh
python3 manuscript/build.py
```

This recreates only the generated `build/clean` directory, copies the three
manuscript inputs there, then runs pdfLaTeX, BibTeX, and two further pdfLaTeX
passes with shell escape disabled. The output is `build/clean/main.pdf`, and
the complete command output is `build/clean-build.log`. No download or software
installation is performed. The required TeX packages are listed in
`environment.json`.

The distributed programs and data contain no external papers or private
workflow logs. The human author must review the argument, code, citations,
authorship details, AI disclosure, and intended journal policies before any
submission. No external submission or public data deposit has taken place.
