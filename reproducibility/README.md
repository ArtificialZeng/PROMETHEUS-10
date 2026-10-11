# Reproduction guide

This directory contains portable replay/build entry points and compact validation records. The project directories hold the actual scientific code, data, TeX/Bib, figures and unchanged archived paper PDFs. There is no research orchestrator, browser controller, API credential or news article in this repository.

## Environment

Use Python 3.12 and a virtual environment. `requirements.txt` records the versions used in this replay; installing packages requires access to a package index. The exact qutrit counterexample uses only the standard library. The interval qubit project needs **python-flint 0.9.0** (import name `flint`), which replaces the original workstation-specific library path.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --list
python reproducibility/reproduce.py --project phys-00004-p02
python reproducibility/reproduce.py --all
```

The runner creates a timestamped directory under `reproduction-runs/`, copies projects into it and captures each command's output. Failed steps stop that project; the runner continues with other projects and returns nonzero if any step fails. Default timeout is 900 seconds **per command**; change it with `--timeout`. Read the scientific checks and generated JSON, not just exit codes. `--list` shows every command. No model inference is necessary to replay these results.

The phase-ordering, exact arithmetic and interval tests are narrow checks of manuscript claims. Floating-point and high-precision probes are not general proofs. This package is not a substitute for reading the mathematical arguments.

## Rebuilding PDFs

An installed TeX distribution with `latexmk`, BibTeX and the manuscript classes (including `revtex4-2`) is required. The script does not install system components or overwrite archived PDFs.

```bash
python reproducibility/build_papers.py --all
python reproducibility/build_papers.py --project phys-00004-p02
```

The script selects the correct working directory for each manuscript's bibliography and graphics paths. Fresh PDFs appear under the timestamped copy's `rebuild/` directory (inside `manuscript/` for some projects). Builds are not claimed to be byte-identical across TeX versions. They do not supersede the archived PDFs or their historical review state.

## Package changes and integrity

- Original `paper.pdf` bytes are unchanged, checked against the local historical PDFs. Their hashes and the historical bundle exception are in `projects.json`.
- Two interval-code imports were made portable by removing the original absolute `sys.path` insertion. Scientific formulas were not edited.
- Machine-specific paths were normalized or redacted in a few copied support documents/JSON files. Those derivative files are not claimed to have unchanged historical hashes. See `portability-changes.json`.
- The four-measurement source file `projects/phys-00002-p02/source.md` was added because its verifier binds the immutable source hash. The omission was detected by a failed fresh replay and repaired without changing the verifier or expected hash.
- The Sibuya legacy instructions omitted required `--output` arguments. Use the corrected commands in the runner and the revised local reproduction note.
- Logs from the original research, browser conversations, queue control files and third-party paper PDFs are excluded. Supplied JSON evidence is retained where needed to understand and reproduce the research.
- `SHA256SUMS` inventories public package files (excluding itself). On macOS use `shasum -a 256 -c reproducibility/SHA256SUMS` from the repository root.

## Scientific release status

All manuscripts still require final author review. Seven have historical original-problem resolution records; the other three retain unresolved scope. `phys-00007-p01` remains an archived draft with a failed historical evidence/manuscript binding gate. This packaging exercise does not reset that result or inherit it as a new acceptance.

No extra reuse license is granted by the act of packaging. See the main README's attribution and rights note.
