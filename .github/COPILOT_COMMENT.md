<!-- This file is used by the Copilot Guidance workflow to post a checklist on new pull requests -->

Please review the Copilot & Automation Guidance for this repository: [.github/COPILOT_RULES.md](./.github/COPILOT_RULES.md)

Before merging, confirm:
- [ ] The PR follows explicit intent from the author (terminal commands / PR description).
- [ ] Any destructive actions (delete/rename/move) were previewed with a dry-run and approved.
- [ ] Sensitive files and .git/.github were not modified by automation unless explicitly allowed.
- [ ] Commit messages explain why changes match the expressed intent.

If you want automation to proceed without human approval, add one of the following labels:
- `copilot:auto-allow` — allow non-destructive automation.
- `copilot:allow-destructive` — allow destructive changes (use with caution).

If the PR author believes Copilot should act differently, update the PR body with a `copilot:` YAML header (see .github/COPILOT_RULES.md).