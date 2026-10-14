# Exact five-state certificate replay

The mathematical argument is self-contained in manuscript/main.tex.
This package supplies supplementary exact symbolic and finite-point checks.
Requires Python 3 and SymPy 1.14.0. No SDP solver or floating-point fit is used.

From the package root:

    python3 evidence/verify-five-state-certificate.py

The script prints exact identity checks, verifies the full five projector
constraints at three rational values of p, and writes
evidence/five-state-exact-checks.json. The recorded proposer stdout is
evidence/five-state-verification.log. Replay in a writable copy: do not overwrite
the original reviewed dossier's bound evidence files. Finite samples do not
prove the interval; the analytic Schur bounds in the manuscript do.

To build the article, from manuscript/:

    pdflatex -halt-on-error main.tex
    bibtex main
    pdflatex -halt-on-error main.tex
    pdflatex -halt-on-error main.tex

Standard TeX packages only; no downloaded class, figure, or private data.
The source package intentionally excludes third-party full papers and raw
research/audit transcripts. References identify the primary sources.

Packaging correction (2026-10-12): source.md is a required runtime input for
the provenance hash and must be shipped alongside this directory. The earlier
archive omitted it and failed after completing the mathematical checks.
A fresh release must replay the corrected extracted archive to exit zero.
