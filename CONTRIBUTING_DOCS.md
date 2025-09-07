# Contributing to docs/external_docs

Purpose
This document explains how to add documents to docs/external_docs safely and consistently.

Before adding
- Check copyright and licensing. Do not add copyrighted books unless you own the rights or have permission.
- Remove or redact any PII or secrets.
- Prefer summaries (.md) over full books when possible.

File naming conventions
- Use lowercase with hyphens: source-topic-short.pdf
- Example: "oreilly-rust-systems-programming-2021.pdf"

Metadata
- Add or update docs/external_docs/template-metadata.yaml with a new entry for each file.
- Required metadata keys: title, filename, author, license, tags, summary, added_by, added_on.

Large files
- For files > 5 MB, use Git LFS. Steps:
  1. git lfs install
  2. git lfs track "docs/external_docs/*.pdf"
  3. git add .gitattributes
  4. git add <your files> && git commit

Privacy & licensing checklist
- Confirm you may add the document.
- If unsure, add only a short summary (.md) and a link to the original source.

Review & QA
- Add a short summary file when adding a large doc, e.g. filename-summary.md with key sections and page references.
- Optionally add tags in metadata to help searching.

Contact
If you have questions about licensing or suitability, open an issue in the repo and tag @allanwrench28.