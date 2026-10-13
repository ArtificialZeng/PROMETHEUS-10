# SmallMac manuscript build validation

Validated `48` release-selected manuscript source trees in disposable copies. All `48` builds produced parseable PDFs with clean final logs. The archived `paper.pdf` files were not overwritten.

## Final checks

- PDF build and `pdfinfo`: 48/48
- Undefined citations: 0
- Undefined references: 0
- LaTeX errors: 0
- Missing-character warnings: 0
- Overfull boxes: 0
- Preferred `manuscript/` working directory: 41 projects
- Project-root fallback required by source-relative assets: 7 projects

## Replay

```bash
python3 reproducibility/build_small_mac_papers.py --all --timeout 240 --output-dir <external-output-dir>
```

The builder accepts a project only when `latexmk` exits successfully, a PDF exists, and the final `main.log` contains no unresolved citation or reference. Per-project commands, output hashes, page counts and log hashes are recorded in [`SMALL_MAC_BUILD_VALIDATION.json`](SMALL_MAC_BUILD_VALIDATION.json). Scientific-code replay remains project-specific and is indexed in [`SMALL_MAC.md`](SMALL_MAC.md).

These checks establish package integrity and local rebuildability. They are not external peer review or human author approval.
