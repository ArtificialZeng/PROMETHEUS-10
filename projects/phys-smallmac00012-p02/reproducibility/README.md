# Reproducing the exact five-dimensional certificate

The central all-dimensional commutator-trace identity is proved directly in
`manuscript/main.tex`. The deterministic checker
`code/hypocycloid_gate_no_go.py` verifies the exact five-dimensional witness and
one sign-sensitive, nontranslation-invariant unitary probe.

## Environment used

- Python 3.9.6
- SymPy 1.14.0
- macOS; no compiled extension or network access is required

Install the Python dependency in an isolated environment using
`reproducibility/requirements.txt`. From the project root, run:

```sh
python3 code/hypocycloid_gate_no_go.py
```

The command must terminate with `status=PASS`. Its retained reference output is
`evidence/hypocycloid-gate-no-go.log`.

The program checks, without floating-point tolerances:

1. the immutable source binding expected by the accepted calculation;
2. an exact unitary that does not commute with translation but has circulant
   squared moduli, fixing the Fourier sign convention;
3. simplex normalization and every row/column bracelet class for the rational
   witness;
4. the exact cyclotomic expression for its first Fourier eigenvalue; and
5. strict exclusion from the filled five-hypocycloid.

The script does not search for a unitary realization of the witness. Its
conclusion is instead combined with the analytic commutator-trace proposition:
the witness is bracelet but not unistochastic. The five-site phase-recovery
conjecture remains unresolved.

## Building the manuscript

The manuscript was built with pdfTeX 3.141592653-2.6-1.40.29 and BibTeX 0.99e
from TeX Live 2026. From a clean project-root `build/` directory, run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build manuscript/main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build manuscript/main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build manuscript/main.tex
```

The resulting draft is `build/main.pdf`; `build/main.log` is the retained final
compiler log. `mainNotes.bib` is the nonempty auxiliary bibliography expected
by REVTeX; all scientific references are in `manuscript/references.bib`.
