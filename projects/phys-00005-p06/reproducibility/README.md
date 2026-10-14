# Ten-site inverse-response filter: reproduction

The claim concerns a finite, zero-diagonal, reflection-symmetric Hermitian chain,
fixed positive couplings, time tau=2pi and every 0<x<=1/16. The exact couplings
come from the unique cancellation root in the retained radius-1e-40 box. Rounded
couplings or the exact decimal center alone do not give exact cancellations.
The uniform bound is C*x^8 with C=131072002. Conditional inverse-state error has
seventh order after normalization, and success remains probabilistic.

Use Python 3.12 and the package versions in requirements.txt. These were already
installed for the reported calculations. No software was installed by the writing
job. The elementary interval implementation is mpmath.iv; this dependency is not
proof-assistant formalization. Standard TeX Live packages, pdflatex, bibtex and
Poppler produce and render the manuscript. The environment is specified here
without requiring the original host's absolute interpreter path.

From the unpacked project root, with an interpreter containing those packages:

    python -B reproducibility/replay.py

The wrapper requires a new project-local output directory and never overwrites
the original evidence. It regenerates the retained root certificate directly
from its exact decimal center and radius, checks the preconditioner equality,
then runs the independent eigenvalue-series/propagation and symbolic/rational
checks in that directory. Root finding is not required for this replay. To use a
different fresh output directory, pass --output followed by its relative path.
For only the elementary interval check, add --certificate-only.

The root JSON includes exact binary interval endpoints, the exact decimal
preconditioner, full analytic-Jacobian enclosure, strict contraction/self-map
bounds, positive squared couplings and the nonzero linear-response interval.
The defining residue-jet equations and full remainder argument are in the paper.
The scripts use the same equations. The second representation constructs four
implicit finite-eigenvalue series and cofactor weights before comparing them
with the residue evaluator. The full propagations retain all ten eigenmodes.
Numerical scans support implementation checks; they do not prove the all-x bound.

Retained numerical comparison data are evidence/research-independent-replay.json.
The fixed-spectrum reference is numerically reconstructed at u=1/2, v=3/2;
it is not independently interval-enclosed. Its nonzero septic coefficient is
approximately -0.2639054062. The six full-response samples deliberately put the
strong-bond phase near a sine maximum. Errors, success probabilities, norm costs
and precision/representation comparisons are all recorded separately.

To regenerate the displayed exact center, preconditioner and scalar comparison
table from those retained data (this writes only the three displayed TeX inputs):

    python -B reproducibility/export_manuscript_data.py

Build with the supplied reproducibility/build.py; its destination must be new:

    python -B reproducibility/build.py --output build/reproduced

The build copies the complete manuscript inputs into an empty directory, runs
pdflatex/bibtex/pdflatex/pdflatex without shell escape, retains real logs, and
extracts PDF text. It requires no network retrieval. The selected handoff bundle
includes the own TeX/Bib, code and necessary scientific JSON, without downloaded
third-party papers, internal job logs or mutable supervisor handoffs. The original
primary papers are retrieved by their identifiers and links in manuscript/source-map.md.
Human author review, final disclosure/declarations and fresh release audits remain
necessary before any external submission.
