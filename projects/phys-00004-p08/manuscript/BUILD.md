# Build this local draft

Run from the extracted project root:

```sh
python3 manuscript/build.py --output build/local-clean
```

The chosen directory must be new or empty. The script never removes an older
build and retains the actual latexmk command output, compiler log, BibTeX output,
and recorder file. It requires Python 3, a TeX installation with latexmk,
pdfLaTeX, BibTeX, and the standard packages imported by main.tex.
No downloads, custom journal class, shell escape, or external figure program are used.

The complete manuscript compilation inputs are main.tex, references.bib,
and graph-figure.tex in this directory. The schematic is authored TikZ code
and is compiled with the text. The supporting manifest and handoff files
are dossier inputs rather than TeX imports.

The local author's draft is conventional article-format TeX, not an assertion
that a journal has approved its template or accepted the article.
Fresh citation, build, and every-page visual release review remain required.
