# Reproducing the product-profile narrow-beam note

The current manuscript concerns a fixed finite separated product-profile beam configuration for the three-dimensional homogeneous Landau equation with kernel a(z)=(|z|^2 I-zz^T)/2. It proves a small-p expansion of the actual initial right entropy-production derivative and a strict negative leading bound. Universal and all-time monotonicity remain unresolved.

## Exact replay

The two portable programs need Python and SymPy 1.14.0, recorded in repro/beam-requirements.txt. They were actually exercised with Python 3.12.14 and SymPy 1.14.0. No numerical quadrature, network access, experimental dataset or downloaded paper is needed. From the project or extracted bundle root:

    python3 repro/run_beam_checks.py --output-dir checks-new

Use a fresh output directory. The command writes the two exact JSON outputs, command logs and receipt there, and compares all fields to the supplied exact reference outputs. It never rewrites the reference files or manuscript. No automatic dependency installation occurs.

beam_pair_check.py starts from the leading two-particle quadratic kernel. Explicit product-profile moment identities reconstruct the partner averages and the local row. It checks the difference B_j*Ibar-6*I_j, its weighted cancellation, the Gaussian specialization, the longitudinal square completion and the nonsharp sign constants. expected-beam-pair.json is the actual normalized frozen calculation output.

beam_scaling_check.py constructs the full scaled diffusion and collision matrices, verifies degree two in p and hence degree at most four in the scaled pair integrand, and checks exact means and normalization for polynomial-Gaussian diagnostic profiles. expected-beam-scaling.json is the corresponding actual normalized frozen output. Those optional profile controls and floating discovery scans are not used to prove the sign.

These programs check exact algebra. The integrations by parts, finite-moment hypotheses, posterior overlap/tail bounds, and actual-flow differentiability require the analytic arguments in the manuscript. Symbolic agreement does not replace human mathematical review.

## Manuscript build

From the project or bundle root, with TeX Live, BibTeX and latexmk:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder -outdir=build-new manuscript/main.tex

The bibliography path is relative to that root. All TeX inputs are manuscript/main.tex and manuscript/references.bib; there are no figures or custom style files. Standard installed TeX packages and fonts are external environment dependencies. No shell escape is used.

## Scope of the supplement

The explicitly selected files contain original TeX/BibTeX, the author handoff/source map, these instructions, original portable code and exact calculated reference outputs. Downloaded third-party papers, raw web captures, job/audit logs and mutable handoffs are excluded. Older Gaussian/fixed-standardized-shape scripts may remain in the local historical project but are not required by or selected for this note. Human authorship and submission-rights approval remain pending.
