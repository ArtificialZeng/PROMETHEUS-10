# Reproduction of the local draft

The manuscript's theorem is proved analytically in manuscript/main.tex. Stable scientific proof: evidence/monotonicity-proof.md. Numerical work is supplementary, not interval certification. Basis |00>,|01>,|10>,|11>; entropy bits; only positive input/output measured-marginal gaps are admissible.

Build from the project or extracted submission root with existing TeX Live and latexmk:

    mkdir -p build
    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build manuscript/main.tex

Run numerical replay in an ISOLATED scratch copy: the original scripts write outputs beside themselves and must never overwrite accepted evidence. The following creates a disposable working tree, copies source.md solely for the script's provenance hash, and writes outputs only there:

    mkdir -p build/replay/evidence
    cp source.md build/replay/source.md
    cp evidence/reconstruct_a.py evidence/reconstruct_b.py evidence/research-check.py evidence/research-precision.py build/replay/evidence/
    cd build/replay
    python evidence/research-check.py > research-check.log 2>&1
    python evidence/research-precision.py > research-precision.log 2>&1

Use Python with NumPy, SymPy and mpmath as recorded in requirements.txt and environment.json. Expected scan: 6000 cases with seed 20261012051, including 3000 small-positive-gap inputs. The floating-point output can vary by platform; all gains are nonpositive within observed conditioning error. Expected maximum recorded gain approximately -2.91824e-11 bits, not a certified bound. Direct spectral and Pauli-tensor channel implementations are compared. High-precision replay selects distinct cases at 50/80 decimal digits and compares gains; this is precision agreement, not a rigorous enclosure. The accepted proof has no numerical gap cutoff. Legacy helper routines have numerical cutoffs; they are not theorem hypotheses.

Saved research-inputs.npz, research-scan.json and research-precision.json permit inspection of the accepted proposer run without regenerating it. They are own generated synthetic data, not experimental data or copied primary-paper tables. Independent referee replay remains in the private project audit dossier and is not bundled as a claimed peer review.

The submission file list deliberately excludes downloaded third-party full papers, raw web/policy responses, supervisor inputs, mutable checkpoints, state files, workflow logs and audit/release directories. The author must obtain primary papers by their cited DOI/arXiv identifiers. No external repository or distribution is performed by this writing job.
