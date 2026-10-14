# Subsequent big_mac results

This synchronization adds **35** locally qualified manuscript packages after the original ten: **9 proofs, 8 disproofs and 18 partial-result notes**. No new computational-only or conjecture-only PDF is added in this wave. Exact original-question status is retained; a useful partial theorem is not reclassified as a solution of the general original question.

Each `projects/phys-…` directory contains an unchanged `paper.pdf`, release-selected TeX/Bib, code and necessary data, the author handoff and the replay guide. The original package's `main.pdf` is renamed `paper.pdf` for the upstream layout. `PACKAGE-PROVENANCE.json` records the original release/bundle/PDF hashes, that rename, and any copied machine-path substitution. Original research projects, worker histories and source statements are not modified by this export.

`SOURCE-BUNDLE-CONTENTS.json` preserves the original selected-file inventory; it does not describe the renamed or normalized public derivative. `ARTIFACTS.sha256` inventories the actual public project. The global [portfolio verifier](verify_portfolio.py) checks each public PDF, code/guide existence, project inventory and canonical classification.

## Inspect and reproduce

From the repository root:

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Each scientific replay has its own dependencies and exact command in the linked guide. Use an isolated writable copy of the project: some original diagnostic programs regenerate JSON or figures. Do not interpret an old cache, a zero process exit or the package hashes as independent scientific proof. No AI account is needed to reproduce the supplied calculations.

Examples, run from a scratch copy of the corresponding project:

```bash
# Landau: exact symbolic coefficient and normalization checks
python3 repro/run_beam_checks.py --output-dir checks-new

# Fixed coherent conductor: exact resummation of the exported partition
python3 -B reproducibility/check_certificate.py

# Three-mode fermionic channel: exact entropy-Hessian supplement
python3 supplement/run_checks.py --output-dir replay-output
```

The examples belong to `phys-00040-p01`, `phys-00030-p01` and `phys-00037-p01`, respectively. They are not interchangeable commands or a complete universal runner. Scientific limits and optional longer reconstructions are documented in each guide.

No primary-paper PDFs, browser conversations, credentials, terminal research logs, research supervisor, or news submission manuscript are added to this repository. The numerical certificate data needed for replay are included. Human scientific, novelty, rights and authorship review remains required before treating any draft as a final scholarly publication.
