# Scope of the proposed local handoff bundle

The explicit submission_files list in publication.json was reviewed during
writing on 2026-09-12. It includes only the following material:

- Authored manuscript TeX and bibliographic metadata, the build helper, and
  the generated scientific figure with its own data and generation script.
- The author's handoff, the evidence/source map and copy-provenance map.
- The project-generated independent checker, the isolated replay wrapper,
  environment/requirements and reproduction instructions.
- Two project-generated dyadic witnesses and five project-generated reference
  calculation records copied without alteration from the actual accepted audit.
- This scope statement.

The checker is project-authored scientific code. NumPy, SciPy, SymPy,
python-flint/Arb, Matplotlib and TeX packages are referenced dependencies;
their software distributions are not included. The figure plots the
project's own calculated bounds. Bibliographic entries contain source
metadata and links, not reproduced third-party figures or article text.
Historical calculation records retain their real provenance identities
and filenames; they contain own numerical/algebraic data rather than
private human referee reports or model dialogues.

Excluded from submission_files: the literature cache and downloaded
third-party papers, raw web retrievals, venue-policy captures, jobs/,
audit/, release/, private transcripts, worker event/usage logs, build
scratch files, credentials and account information. Some excluded source
verification records are bound in the local publication source snapshot
for review; binding does not grant redistribution permission.

The checked selection supports a local handoff. No redistribution licence
has been assigned, author rights declaration signed, or external
distribution performed. The author retains responsibility for final rights,
policy and disclosure decisions. The fresh release role must recheck this
scope against its actual archive selection before creating the final local
bundle.
