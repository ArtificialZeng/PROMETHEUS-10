# Reproducing the W-neighborhood calculation

Run from the project root. Python 3 standard library only; no external numerical
packages or downloaded papers are needed for the decisive exact calculation.
The writing environment uses Python 3.14.7 and TeX Live's pdflatex/BibTeX.

```
python3 evidence/check_w_cubic_exact.py
python3 evidence/check_w_jacobian_numeric.py
```

The first command prints exact baseline/first/second-order zero checks, the
cubic coefficient -80ab/3, state-path norm 13 and derivative 26. It imports
evidence/radical_algebra.py. That arithmetic code has no cached-output dependency.
The second command is a finite-difference diagnostic, not an exact certificate.
Retained results: evidence/w-cubic-exact-check.log and
evidence/w-jacobian-numeric-check.log. Source constants are a,b>0,
a²=(3+sqrt3)/6, b²=(3-sqrt3)/6, q=i(bY+aZ), V0=q tensor q tensor q.
Controls are left rotations exp(-i theta.sigma/2), qubit-major X,Y,Z order.

Additional original calculations:
```
python3 evidence/w_cubic.py
```
This imports evidence/radical_algebra.py; inspect the script before running because it writes
evidence/w-cubic.json. Run it in a scratch copy, never over frozen accepted
scientific inputs. evidence/w_jacobian.py similarly generates its accepted JSON.
The submitted manuscript only needs the one-dimensional cubic, not the full
three-variable interpolation. All associated input/data/code files are included
explicitly in the handoff manifest.

The scientific argument is evidence/w-local-openness.md. The manuscript gives
the analytic implicit-function elimination and uniform sign proof; code checks
its finite matrix identities but cannot certify the entire analytic argument.
No explicit numerical epsilon or C is produced.

For the clean canonical-source build, run `python3 reproducibility/build.py`
from the project root in a fresh copy without build/write-final. Logs and the PDF
are written to build/write-final. Alternatively build from a directory containing
main.tex and references.bib:
```
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The public handoff scope excludes all third-party fulltext, browser retrieval
logs, job records and audit transcripts. The two primary papers are identified
by DOI 10.1103/PhysRevA.108.022220 and arXiv:2608.21185v1; obtain them from
their publishers. Citation metadata and mathematical attribution are retained.
No license is asserted on behalf of the human author; any public license choice
requires author review.
