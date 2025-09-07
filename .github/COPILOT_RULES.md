````markdown
```markdown
# Copilot & Automation Guidance for this repository

Purpose
- Give a clear, human-readable set of principles for Copilot, bots, and contributors to follow so automated suggestions and changes align with the intent you express in the terminal, commits, and PRs.

Core principles
- Respect explicit intent: Prefer explicit instructions from the repo owner (terminal commands, commit messages, PR descriptions, labels) over inferred intents.
- Ask when unsure: If intent is ambiguous, require a clarifying question or a draft PR rather than making potentially destructive changes.
- Non-destructive by default: Any automation that deletes, rewrites, or moves content must offer a dry-run, show the planned changes, and require explicit approval before making irreversible changes.
- Preserve history: Avoid rewriting published history (force-push to shared branches) unless a human explicitly requests it.
- Safety exclusions: Never touch `.git`, `.github`, sensitive config files, or any paths listed in an explicit EXCLUDE block in repo docs.
- Minimal changes: Prefer small, incremental changes with clear commit messages that explain why the change matches the stated intent.
- Preserve developer conventions: Honor repository coding conventions, linters, formatting, and existing CI checks.
- Transparent actions: Automation must leave an audit trail (commit, PR, issue, or comment) that clearly states what was done and why.

How to signal intent to automation
- Put explicit instructions in the command you run in the terminal and in your commit/PR message.
- Use labels like `copilot:auto-allow` or `copilot:dry-run-ok` on PRs to permit different behaviors.
- Use a short YAML header in PR body for richer controls (example below).

Example PR YAML header (optional)
---
copilot:
  allow_delete: false       # true to allow automated deletions
  dry_run: true             # true to require dry-run output before action
  scope: "src/**"         # glob restricting automation's scope
---

Enforcement and human review
- This document is guidance. If you want enforcement, add a simple CI/Action that posts this doc and requires human confirmation for destructive changes.

Feedback & updates
- Treat this file as part of the repo's governance. Edit it if your preferences change.
````