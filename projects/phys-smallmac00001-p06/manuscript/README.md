# Local manuscript sources

This is the local author-review draft of *A missing spectral arc at finite cycle
affinity in four-state Markov generators*. It contains one accepted analytic
contribution: the existential missing arc at B = log(3)/2. The proof is in
main.tex, including its uniform remainder and all-support compactness argument.
The bibliography contains four primary works actually consulted. No external
figure files or downloaded journal styles are required.

From the project root (or the root of the eventual source handoff), build with:

```sh
python3 manuscript/build.py --output-dir build/local-clean
```

The chosen output directory must be new or empty. The builder stages identical
copies of main.tex and references.bib and runs latexmk with pdfLaTeX, BibTeX,
and the standard TeX packages named in main.tex. It writes main.pdf, main.log,
main.bbl, main.blg, main.fls, build-console.log, and build-record.json there.
For another clean build, choose a different new output directory. No software
installation is performed by this script.

Exact arithmetic checks are documented in repro/README.md. Source locations
and the link to accepted evidence are in source-map.md. Author identity,
policy decisions, scientific caveats, and the pending human review are in
../AUTHOR_HANDOFF.md. This draft has not been externally submitted.
