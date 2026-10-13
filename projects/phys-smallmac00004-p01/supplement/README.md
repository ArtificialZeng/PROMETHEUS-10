# Reproducing the dephrasure interval result

The accompanying article proves only p in [27/250,221/2000], q=3p,
for arbitrary finite ensembles of qubit states, with the full environment.
The interval endpoints are exact rational numbers. Entropies are in bits.
No claim is made about the rest of the original interval or regularized capacity.

## Environment and clean execution

The recorded environment is Python 3.12.14, python-flint 0.9.0,
NumPy 2.3.5, SymPy 1.14.0, and mpmath 1.3.0 on macOS.
`requirements.txt` records these versions; no script installs anything.
The interval programs need only python-flint and the standard library.
The Stinespring reconstruction also needs NumPy, SymPy, and mpmath.
`resource` is a Unix standard-library module, so native Windows requires
a compatible Unix environment or an explicit portability adaptation.

From the root of this project or extracted author bundle, with an environment
that already supplies the above packages, run:

```sh
python3 supplement/run_replay.py --output replay-new
python3 supplement/make_tables.py
python3 manuscript/build.py --output build-new
```

The replay/build destinations must not already exist and must lie inside the
project/archive root. This prevents regeneration from overwriting accepted
scientific evidence. The replay invokes the ordinary Python programs sequentially
in the foreground; it performs no model calls or network access. Per-program
timeouts stop incomplete checks and never produce a pass for them.

The PDF build needs the existing `pdflatex`, `bibtex`, REVTeX 4.2, and standard
LaTeX packages listed in `manuscript/main.tex`. It uses shell escape disabled,
runs BibTeX, and resolves references through two subsequent LaTeX passes.
Full output is retained in `build-new/build.log` and `build-new/main.log`.

## What each program establishes

- `code/uniform_certificate.py`: outward-rounded 192/256-bit Arb tests of
  the seven sufficient conditions, on exact rational uniform partitions.
  Default 192-bit counts are 100 x 500 exterior boxes and 100 x 1000 compact
  derivative boxes plus five sets of 100 parameter boxes: 150500 total.
  The 256-bit replay uses 160 x 700 and 160 x 1400 plus 5 x 160: 336800 total.
- `code/adaptive_certificate.py`: a separately implemented 256-bit check,
  partitioning z rather than z squared and using cancelled entropy differences.
  Its 2500 accepted leaf boxes cover the exact rational domains. It shares Arb
  and the analytic sufficient conditions with the uniform implementation.
- `code/stinespring_checks.py`: exact symbolic reconstruction of the receiver
  and full environment, spectra, finite floating-point Holevo diagnostics,
  globally enclosed scalar coding values, and the positive slack of the prior
  max-minus-min bound at p=0.11.
- `make_tables.py`: creates the two TeX tables from `data/`, checks the downward
  rounding of certificate margins, and checks that both radius and rate enclosures lie within
  5e-13 of the displayed table centers. It is a presentation step, not a proof search.

The three calculation programs are byte-identical copies of the versions used
in the accepted research/replay record. Their historical metadata remains in
the source for traceability; it is not an assertion of a new reviewer identity.
The table data are aggregate result fields extracted from those records, excluding
private conversations and process logs. `run_replay.py` writes only into its new
output folder. The embedded programs' `audit/` output path is inside that folder,
not the project's accepted `audit/` directory.

## Error control and limitations

The proof is the analytic argument in the article plus strict interval signs
over a continuous covering. It uses the exact limits H(1)=0 and L(0)=1 and an
analytic bound for z approaching 1; there is no entropy cutoff in the theorem.
The Stinespring floating diagnostics explicitly tolerate errors of 2e-12 bits
and clamp radii within 1e-14 of the pure-state endpoint; these diagnostics do not
establish the theorem. Finite random ensembles are not a universal optimization.
The scalar root enclosures use a monotonicity argument proved in the article.

Both interval implementations share the Arb arithmetic library. This is neither
a formal proof-assistant certificate nor independent validation of Arb itself.
The original full-plot vertex comparison failed its 2e-5-bit tolerance, with
a largest discrepancy about 4.82e-5 bits. Its status is preserved in the local
dossier. Neither this plot comparison nor any fitted optimizer enters the proof.
Independent human review and final publication-policy decisions remain pending.

## Rights and sharing scope

This author bundle contains project-generated manuscript source, table source,
calculation programs, and aggregate numerical outputs. It does not contain
downloaded papers, browser conversations, credentials, or private job logs.
Third-party software is referenced as a dependency and is not redistributed.
No license for the author's work is asserted without the author's decision.
Primary papers remain accessible through the bibliography's DOI/arXiv links.
