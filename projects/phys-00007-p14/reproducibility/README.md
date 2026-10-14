# Reproduce the local draft

The result is analytic. Equations in manuscript/main.tex reproduce the accepted derivation in evidence/joint-tail-proof.md. The scientific dossier and audit remain local and are not part of the public supplement.

From the project root:

    python3 evidence/check_joint_tail.py

This existing diagnostic overwrites evidence/joint-tail-check.log and must NOT be run in an accepted frozen project. For safe repetition, copy evidence/check_joint_tail.py into a separate scratch directory first, then run the copied script there. It needs only Python's standard library and writes joint-tail-check.log next to itself. The submission bundle includes the script, not frozen scientific logs. Its floating-point mesh checks are not interval certificates.

The quoted coefficient at T=r=1,a=0 follows directly from the displayed expressions labeled eq:zero and eq:I in the TeX source. No numeric table or figure is used as proof.

Build from a clean directory inside the project:

    mkdir -p build
    cd manuscript
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build main.tex
    cd ../build
    BIBINPUTS=../manuscript: bibtex main
    cd ../manuscript
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build main.tex
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build main.tex

Only main.tex and references.bib are authored PDF dependencies; packages and the plain bibliography style are system TeX resources. Compiler products and third-party primary papers are excluded from submission_files.
