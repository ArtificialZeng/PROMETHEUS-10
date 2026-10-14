# Reproduction and build

This package reproduces the exact arithmetic for the two restricted Rabi results. It contains no experimental data, third-party full paper, account data or private job log.

## Compile

From the package/project root:

    mkdir -p build/local
    cd manuscript
    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build/local main.tex

TeX dependencies: standard article class, geometry, amsmath, amssymb, amsthm, booktabs, fontenc, lmodern, microtype and hyperref; BibTeX plain style. No custom style, imported figure, external TeX input or shell escape is required. Bibliography lookup requires running from manuscript.

## Exact arithmetic

The scripts write their outputs next to themselves. Preserve the delivered evidence: copy the four inputs to a new local scratch directory before running them. From the package root:

    mkdir -p build/replay
    cp evidence/research/pass2/feshbach-symbolic.py build/replay/
    cp evidence/research/pass2/check-feshbach.py build/replay/
    cp evidence/research/pass2/check-rational-functions.py build/replay/
    cp evidence/research/pass2/feshbach-bounds.json build/replay/
    python3 build/replay/feshbach-symbolic.py
    python3 build/replay/check-feshbach.py
    python3 build/replay/check-rational-functions.py

The generator needs Sympy 1.14.0 (requirements.txt). Both checkers need only Python's standard library. No installation is necessary to run the two checkers with the delivered coefficient record. They generate feshbach-replay.json and rational-replay.json in the scratch directory.

The matching checker reconstructs 73 coefficients from 34 path matchings, asserts the uniform coefficient inequalities, and tests 16 tuned energy endpoints and 12 detuning-window counts with full-operator tail bounds and 32 alternative LDL checks. The rational checker reconstructs the finite-middle and tail fractions. Point tests diagnose implementation; they do not replace the manuscript's analytic continuum, operator-domain, inertia and error proofs.

The stable full derivation is evidence/research/pass2/feshbach-derivation.md. feshbach-bounds.json records exact fractions and rational functions; feshbach-replay.json and rational-replay.json record proposer outputs. These output files may contain historical proposer-verification limitations; separate scientific review and the manuscript do not alter those records.

For full historical primary-source reconstruction and its benchmark, consult source-ledger.json and reproduction.json in the local dossier. These records and third-party retrieval archives are deliberately outside the submission supplement. The manuscript states the complete defining model and proof, and references the publicly accessible primary sources.
