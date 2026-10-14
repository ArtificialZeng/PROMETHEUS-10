# Reproduce the scientific checks

From the bundle root run:

    python3 reproducibility/check.py > replay.log

Python 3 standard library only; deterministic rational rates are generated in main().
No installation, network call, input cache or paper download is required. The code
compares full-ring eigenvector derivatives against killed-chain backward raw moments
and formal Laplace inversion, and verifies inverse-generator traces and polynomial
certificates. Adapted from the independent local referee replay, removing only its
administrative snapshot-hash preamble; no science algorithm or test case was changed.

Expected final output: 84 exact tilted-generator bond comparisons; 16 passage cases;
analytic certificate checks all pass. Stress-case rates span 10^-6 to 10^6.
The N=8 slow-link benchmark has c=(1/14,1/49,-1/1372,-1/4802).
These finite checks do not replace the universal proof.

Build in a new empty directory:

    python3 reproducibility/build.py --output /tmp/ring-note-build

Prerequisites: Python 3, pdflatex, bibtex, revtex4-2 and APS bibliography styles.
No custom style, figure or external data dependencies exist. main.bbl is generated
from the provided database. Keep the logs. The builder refuses a nonempty output directory.
Environment used locally: environment.json. Third-party full papers and internal
job/audit logs are excluded from the bundle. Source references provide retrieval links.
Human scientific review and fresh release review remain necessary.
