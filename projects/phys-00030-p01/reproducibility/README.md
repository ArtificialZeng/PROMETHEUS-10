# Fixed finite-conductor reproduction

This is a local draft supplement. It makes no claim of author approval, external peer review or public data deposition. The sample and exported partition are fixed. It does not certify the original ABS helper for new parameters or grids.

Run from the project/package root with Python 3.12 and the versions in requirements.txt. The installed research interpreter used here is `python3`. This absolute path identifies the actual local environment; another installation with the same documented dependencies can use `python`. Nothing is installed by these instructions.

Always use an isolated writable scratch copy of the selected handoff files. The original scientific evidence is frozen; some historical generation scripts overwrite their own result JSON files. The portable check scripts below write only reproducibility/run-output and leave the frozen input files intact. Output JSON status and complete counts must be inspected, not merely process exit codes.

## Fast complete-partition resummation

```sh
python -B reproducibility/check_certificate.py
```

This imports no physical/scattering code. It verifies all exact consecutive dyadic endpoints, every positive width, the exact total width 24576, the count 26275, the count 727 of physical denominator fallbacks, exact-rational exported integral sums and directed 100-digit tail bounds. It writes reproducibility/run-output/certificate-check.json. A successful resummation verifies bookkeeping and the displayed margin conditional on each full-panel range being valid. The range proof also requires the arithmetic derivation and the complete remainder check.

## Arithmetic defect and its fixed-certificate closure

```sh
python -B reproducibility/check_coefficient_magnitudes.py
python -B reproducibility/check_remainders.py
```

The first deliberately reproduces the real defect: 44 failures to enclose initial 250-digit intervals and 42 strict exact-coefficient magnitude underestimates. Its failed_outward_bound status is expected and must not be concealed. The second independently reconstructs directed 500-digit coefficient bounds and tests the actual 85-digit remainder upper endpoint for both polynomials at every final panel. Completion requires status pass_actual_remainders_enclosed, completed_panels=26275, checks=52550 and no violations. The historical actual run completed in about 78 seconds on the recorded machine. Its code has a 240-second ceiling; an incomplete run establishes no remainder claim.

Exact substantive copies of the original defect/closure records and logs are in records/. copy-provenance.json binds those byte-identical copies to the untouched accepted audit records. The portable scripts redirect output paths. physical_replay.py additionally removes workflow-only snapshot-binding/scanning and renames completion metadata to completed_reproducibility_replay; it preserves all physical and arithmetic calculations. Those adaptation details are recorded explicitly.

## Independent physical and baseline replay

```sh
python -B reproducibility/physical_replay.py
```

This consumes the exported final partition for exact sums, panel comparisons and a disclosed quadrature grid. It imports no discovery solver or cached scattering values. It independently builds the outgoing boundary/forward branch/core resolvent, explicit Slater events and original counting determinant, checks the reciprocal boxcar limit, and performs five separate dense 387-site solves. Its quadrature orders are diagnostics, not the integral error proof. Outputs are in reproducibility/run-output. The retained historical replay and serialization-failure logs are in records/; the first failure was a NumPy-boolean JSON conversion after scientific calculations and was not suppressed.

The alternative outgoing-Bloch/backward-sector implementation is evidence/research/r3-independent-check.py. Its point checks use 320 digits; only the comparison imports the range kernel. Its first lower-precision failure and diagnosis are included. To inspect the original exact-fraction checker without overwriting frozen files:

```sh
python -B evidence/research/r3-independent-check.py --certificate evidence/research/r3-interval-refine.json --partition-only --output reproducibility/run-output/original-partition-check.json
```

## Recompute the original full-range integration

The defining model is evidence/research/r1-tightbinding-model.md and r1-proposed-witness.json. The finite determinant identities are r2-enclosure-derivation.md. The refined certificate consumes the completed parent certificate; both are included. In a scratch copy only, these are the historical commands:

```sh
python -B -u evidence/research/r3-interval-enclosure.py --seconds 1000 --target-width 0.012 --output evidence/research/r3-interval-enclosure.json
python -B -u evidence/research/r3-interval-refine.py --seconds 300 --target-width 0.0048
python -B reproducibility/check_certificate.py
python -B reproducibility/check_remainders.py
```

Panel selection near a time ceiling can depend on machine speed. Replacing the fixed certificate by another partition requires a new complete remainder check and integral validation; completion or arithmetic properties of the retained partition cannot be transferred automatically. A partial/time-ceiling status is not a certificate. The retained complete JSON data are the accepted fixed partition for the manuscript.

## Proof, units and source map

The central accepted argument is evidence/research/r3-counterexample.md, read together with the stronger fixed-certificate correction in records/analytic-reconstruction.md. The latter supersedes the original prose's false blanket outwardness statement. The exact constant proof is r1-exact-psi-control.md, and the fixed-current Fenchel identity is r1-legendre-cycle-derivation.md. Physical admissibility is r3-physical-admissibility.md. Rates use epsilon/h, entropy rates k_B epsilon/h, with epsilon=k_B T_ref, T_ref>0. All three fixed Fermi reservoirs and the full actual lead band enter the calculation.

The bibliography cites the final JPA paper (DOI 10.1088/1751-8121/ae0ede), the PRL paper (DOI 10.1103/6nww-8wcp; arXiv:2502.07917v2) and Tesser--Splettstoesser (arXiv:2607.06190v1). Original third-party full papers and raw retrieval caches are not distributed in the submission supplement. They remain in the private source dossier. Scientific formulas are explicitly reproduced with attribution; no third-party figure is reused.

## Manuscript build

From manuscript/ in a scratch copy:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder -outdir=../build/clean main.tex
```

The only authored TeX dependency is main.tex; its bibliography is references.bib. Standard installed TeX packages are not redistributed. The fresh release role must separately audit citations, the actual clean build and every rendered page before a local validated release. Human critical review and confirmation of the supplied author details and AI disclosures remain required.
