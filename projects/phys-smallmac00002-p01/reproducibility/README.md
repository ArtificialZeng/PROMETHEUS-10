# Reproducing the SOS two-cycle exclusion

Run all commands from the top-level directory containing `manuscript/` and
`reproducibility/`. No primary papers, private records, network downloads or
cached scientific inputs are required by these checkers.

The proof applies to t,h,u>0, t=exp(beta J), h=exp(beta J1), finite real
couplings and finite beta>0. Each vertex has two children and each sibling
bond is counted once. Only positive reflection-symmetric messages (1,u,1)
that are homogeneous within each generation are covered.

## Exact checks

Use Python 3.9 or newer. `check_integer.py` needs only the standard library.
`check_symbolic.py` additionally needs SymPy; the tested version is 1.14.0,
recorded in `requirements.txt`. Use an existing environment with these
dependencies. Do not run either checker with Python's `-O` option.

```sh
python3 reproducibility/check_integer.py --output-dir reproducibility/rerun
python3 reproducibility/check_symbolic.py --output-dir reproducibility/rerun
```

Each invocation writes its JSON result to the chosen project-relative
directory and prints the checks. The integer checker also saves a text log.
The default output directory is `reproducibility/outputs`; use a new output
directory to preserve earlier results.

`check_integer.py` enumerates all 27 local Hamiltonian weights and performs
sparse integer polynomial operations. It checks H=P Q, with 97 nonzero
coefficients in H, the 75 positive monomials of the composition denominator,
and the 24 positive coefficients in four times the remainder of
Q-t^2(t^2u-1/2)^2. There are no floating-point comparisons.

`check_symbolic.py` instead reconstructs the update from parent and sibling
matrices and derives the two-variable sum/product elimination. It performs
87 named checks, including the composition identity, the positivity premises,
the known h=1 and diagonal limits, and exact rational diagnostics. Its
seven-vertex calculation checks all 2187 probabilities against direct
Hamiltonian weights, all 27 first-generation marginals, and all 729 exterior
assignments for an internal-site conditional with a crossing sibling bond.

The files under `expected/` are actual outputs of the packaged programs.
The symbolic result records Python, SymPy and platform versions. Timestamps
and environment strings can differ on another machine; compare equations,
coefficient lists, exact fractions, counts and pass/fail results. These two
programs use different representations; rerunning them is reproducibility,
not an additional independent scientific review.

The symbolic checks establish complete polynomial identities and positive
coefficient premises. Their rational parameter examples are diagnostics,
not evidence extrapolated to a continuum. The inequality chain and the
infinite-tree Gibbs construction are proved analytically in the article.
No perturbative order, finite-size extrapolation, empirical uncertainty or
floating-point tolerance enters the result. CPU and memory demands are small:
in the recorded local replay the integer and symbolic programs finished in
about 0.03 s and 0.35 s respectively; timings are environment dependent and
are not a performance claim.

## Building the article

An existing TeX installation must provide `pdflatex`, `bibtex`, the standard
`article` class, Latin Modern fonts, AMS packages, geometry, microtype,
booktabs, natbib, hyperref and url. No journal-specific class is required.

```sh
python3 manuscript/build.py --output-dir build/reproduced
```

The output directory must be empty. The script copies the complete authored
TeX/Bib input, runs pdfLaTeX, BibTeX and two further pdfLaTeX passes, and
retains `main.log`, `main.blg`, `main.fls` and `build-transcript.log` beside
`main.pdf`. It disables shell escape. The fixed build epoch and suppressed
PDF timestamps make repeated builds comparable; a different TeX installation
can still change PDF bytes. The source uses no figures or external data files.

The supplied files are a local author-review draft. External submission,
public deposition, licensing and human approval remain separate decisions.
