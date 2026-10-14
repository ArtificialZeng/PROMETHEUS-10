# Reproducing the construction and diagnostic checks

The manuscript's result is an exact continuum argument. Its stable analytic
source is evidence/research-pass1-proof.md. This is the historical proposer
record; its original labels about pending review were preserved. Subsequent
independent scientific acceptance is recorded separately in the project.
No floating-point calculation supplies the quantified existence proof.

Always work in a **disposable copy of the selected submission files**, preserving
the evidence/ directory layout. The programs generate results beside their inputs;
running them in the original accepted project would rewrite frozen evidence.

From that disposable project root, with Python and the packages in
reproducibility/requirements.txt already available:

```sh
python3 evidence/reconstruct_a.py
python3 evidence/reconstruct_b.py
python3 evidence/compare_inputs.py
python3 evidence/research-pass1-check.py
```

The first two programs independently use input-a.json and input-b.json for the
published unit-edge pumpkin and split-tree baseline. The comparison program
uses their newly generated matching/results records to check the orientation
and convention map. It does not create either reconstruction.

The last program reads research-pass1-input.json. It checks exact radical
identities and a rational secular-pole rank, full endpoint matching at m=4,5,8,
all 300 interior edge-pair coordinate domains at m=4, and the stated high-precision
scalar and epsilon choices. It retains all edge sectors; diagnostic eigenvalue
roots, SVDs, optimization and high-precision residuals are not interval certificates.
Default sample choices are fixed in the input record; no large graph is
instantiated for the very small epsilon scalar examples.

Expected original scientific outputs are research-pass1-results.json,
research-pass1-metric-pairs.json, matching-a.json, matching-b.json,
results-a.json, results-b.json and comparison-results.json in evidence/.
Replay timestamps and environment fields can differ. Compare the substantive
values and tolerances, not byte hashes of regenerated result records.

These commands were replayed in an isolated local copy during draft preparation,
without changing accepted evidence. The actual interpreter and package versions are in
reproducibility/environment.json. The pin file records the already-installed
research environment, not a claim that packages were installed during this job.

To build the article and its authored TikZ schematic, see manuscript/BUILD.md.
No downloaded third-party paper is needed to run the diagnostic programs.
For independent primary-source reconstruction, obtain the cited papers from
their official DOI/arXiv pages; the submission selection intentionally excludes
their full PDFs and cached text.
