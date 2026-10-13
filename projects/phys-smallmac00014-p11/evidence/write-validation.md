# Write-role validation

Checked 2026-09-13 UTC.

- The dispatch deadline is `2026-09-13T21:25:50.413328+00:00`; this write
  pass ran before that deadline.
- `command -v python3`, `PHYSICS_PYTHON`, and `sys.executable` all resolved to
  `python3`. The runtime was
  Python 3.12.14, NumPy 2.3.5, and SciPy 1.18.1.
- `release_gate.py check-science` returned `ok:true` for accepted snapshot
  `d999590dfa473e6360fb325cc50bfe2aebaa625c99b7acff4f10a70d4549ffd7`.
- A fresh write-role run of `python3 code/takagi_commuting_frame.py` exited
  zero. It reproduced the manuscript table: generic-triple residual
  `1.639e-15`, Takagi residual `1.364e-15`, determinant residual `4.441e-16`,
  commutator residual `1.316e-16`, `n=1,...,7` score residual `1.554e-15`,
  and explicit three-use residual `3.331e-15`.
- A fresh write-role run of `python3 code/reproduce.py` exited zero and ended
  `STATUS PASS`; its largest published-baseline residual was `1.887e-15`.
- The manuscript was built from a cleaned directory with TeX Live 2026 and
  `latexmk` 4.88. The final `build/main.log` has no warning, overfull,
  underfull, undefined-reference, or undefined-citation diagnostic.
- `build/main.pdf` has eight A4 pages and extractable text. All eight pages
  were rendered to PNG at 144 dpi and visually inspected; no clipping,
  overlap, missing glyph, broken equation, unreadable table, or malformed
  reference was observed.
- The paper contains only the accepted central claim. It adds no unaudited
  theorem, experiment, or physical regime. Venue fit and AI-policy limits are
  recorded in `venue/aims-and-policy.md`.

Remaining obstacle: human scientific verification, priority review, author
details, funding/interest declarations, and a policy-compatible final AI
disclosure are mandatory before any submission. This is not a failed
scientific audit; it is the explicit author-review boundary of the local
draft.

