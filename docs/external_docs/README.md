# docs/external_docs

Purpose
This folder is a place to drop auxiliary documents (books, cheat-sheets, debugging notes, specs, PDFs, markdown, text files) that augment the repository and help models or humans when working on the project.

Recommended structure
- docs/external_docs/
  - <source>-<topic>-<short>.pdf      (e.g. "rust-syntax-cheatsheet.pdf")
  - <title>.md                        (notes, summaries, short guides)
  - attachments/                      (optional subfolder for large binaries)
  - template-metadata.yaml            (metadata for each document)

Naming guidance
- Use lowercase, hyphen-separated names.
- Include a short topic and source if known, e.g. "oreilly-rust-book-2020.pdf".
- Avoid special characters and spaces.

Metadata
Each document should have a corresponding entry in template-metadata.yaml or an adjacent .yaml/.json file with these recommended keys:
- title:
- filename:
- author:
- source:
- license:
- tags: [tag1, tag2]
- summary:
- added_by:
- added_on:
- notes:

Large files & Git LFS
- If you plan to add many PDFs or large binaries, enable Git LFS and track patterns (see .gitattributes).
- Do NOT add copyrighted materials without the right to store/share them.

Privacy & security
- Do not add secrets, private keys, credentials, or PII.
- For sensitive internal docs, prefer an internal encrypted store rather than adding to the repo.

How models should use these files
- Prefer structured metadata (template-metadata.yaml) to locate relevant docs quickly.
- Prefer summary/README and lightweight notes (.md) for fast ingestion.
