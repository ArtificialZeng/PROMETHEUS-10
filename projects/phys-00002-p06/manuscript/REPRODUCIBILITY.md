# Reproducibility guide

The central result uses the exact input fixture printed in the manuscript. The
portable calculation is `manuscript/witness-data.json`; its generating implementation
is `manuscript/reproduce_witness.py`. The verifier uses only Python and mpmath. The
figure script uses Matplotlib and reads that JSON without manual transcription.

Validated write-stage environment:

- Python 3.12.14
- mpmath 1.3.0
- Matplotlib 3.11.2
- REVTeX 4.2 and TeX Live 2026

From an unpacked copy of the project or handoff bundle, regenerate the scientific
output and figure with:

```sh
PYTHONDONTWRITEBYTECODE=1 python manuscript/reproduce_witness.py
python manuscript/make_figures.py
```

The verifier should report eight `PASS` lines. It separately assembles the
ascending-energy column generator and a reversed-energy row generator, runs at 100
and 180 decimal digits, checks all four predicates, the simple slow mode, the two
amplitudes, and relative-entropy evolution, then writes the JSON record.

The portable record is deterministic and contains only scientific inputs, outputs,
scope, and checks. Internal job identifiers, runtime transcripts, evidence hashes,
and downloaded sources are intentionally omitted from the handoff data.

Build the paper from the project root with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build manuscript/main.tex
```

The accepted scope is controlled arbitrary-precision numerics. The scripts do not
provide directed-rounding interval enclosures or an exact symbolic eigensystem proof.
