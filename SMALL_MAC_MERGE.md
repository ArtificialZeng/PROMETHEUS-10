# Merging the SmallMac collection

This tree is based on [`ArtificialZeng/PROMETHEUS-10`](https://github.com/ArtificialZeng/PROMETHEUS-10) commit `a2f0e6e50de892bf3544990ce41c444435edc540`. It preserves the original ten project files and the upstream root `.gitignore` byte-for-byte. The five existing root README files and `reproducibility/SHA256SUMS` are updated, a Russian root README is added, and 48 release-gated SmallMac projects are included. Six-language collection and category indexes group the additions into 21 proofs, 7 disproofs, 19 partial results and 1 computational result while preserving display numbers, batch identifiers and original project IDs. The new `projects/.gitignore` allows curated SmallMac evidence logs and frozen bibliography outputs to be tracked.

## Merge

Copy the contents of this tree over a checkout of that exact upstream commit, review the diff, then run:

```bash
python3 reproducibility/verify_small_mac.py --all
python3 reproducibility/build_small_mac_papers.py --all
python3 reproducibility/verify_package.py
```

Project IDs, original internal IDs and frozen PDF hashes are in `reproducibility/small_mac_projects.json`; the concise mapping is in `collections/small_mac/id-map.json`. Assembly provenance is in `UPSTREAM-BASE.json` and `reproducibility/assemble_small_mac_package.py`.

The package does not contain browser state, model credentials, downloaded primary-literature full texts or worker logs. It does not grant a new license or authorize external submission. Every new manuscript remains `draft_ready_author_review_required`.
