# Computational environment and bounds

The strict replay uses Python 3.9+ standard-library `fractions`, `decimal`,
integer arithmetic and ordinary containers. There are no package requirements.
The complex module contains an optional high-precision discovery entry point
that imports mpmath only when run directly; the certificate imports its
coefficient functions and does not execute that optional discovery path.

The complex certificate uses a fixed 384-bit binary grid. The independent
scalar certificate uses 90 significant decimal digits with separate directed
rounding contexts. Exact calibrations use Fraction. A lost denominator sign,
failed inclusion, failed rank/sign test, or nonzero exact baseline residual
causes failure; no numerical tolerance is promoted to proof.

The replay driver gives each sequential certificate subprocess a 120-second
timeout. A timeout is a failed replay, not a scientific conclusion. No background
worker, model process or multi-core parallel algorithm is required. Runtime and
process memory are measured by each program. The `peak_rss_bytes_macos` field is
in bytes on macOS; on other platforms `resource.ru_maxrss` may have other units,
so it must not be interpreted as bytes without a platform conversion.

The manuscript is built with installed pdfLaTeX, BibTeX, standard article,
Latin Modern, AMS packages, geometry, microtype, natbib and hyperref. No custom
font or external figure is needed. The build script copies the two authored
sources to a new empty local directory before compiling them. Actual versions
and replay output are recorded separately in the local author dossier.
