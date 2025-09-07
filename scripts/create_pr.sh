#!/usr/bin/env bash
set -euo pipefail

# create_pr.sh — create a branch, commit specified files, push, and open a GitHub PR via the gh CLI
# Usage:
#   scripts/create_pr.sh -b my-branch -t "My PR title" -m "My PR body" -- files...
# If no files are provided, all changes in the repo are staged.

show_help() {
  cat <<'EOF'
Usage: $0 [-b branch] [-t title] [-m message] [-- base_branch] [-- files...]

Options:
  -b BRANCH    Branch name to create (default: pr/<timestamp>)
  -t TITLE     Pull request title (default: "Automated PR: <branch>")
  -m MESSAGE   Pull request body/message
  --base BASE  Base branch to open PR against (default: main)
  --dry-run    Show commands but don't run network operations
  -h           Show this help

Examples:
  scripts/create_pr.sh -b add-ink-tui -t "Add Ink TUI" -m "Adds an Ink-based TUI to control the internet toggle" -- scripts/tui_toggle_ink.js requirements-ink.txt README_INK.md
EOF
}

BRANCH=""
TITLE=""
BODY=""
BASE="main"
DRY_RUN=0
FILES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -b) BRANCH="$2"; shift 2;;
    -t) TITLE="$2"; shift 2;;
    -m) BODY="$2"; shift 2;;
    --base) BASE="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    -h) show_help; exit 0;;
    --) shift; FILES=("$@"); break;;
    --*) echo "Unknown option: $1"; show_help; exit 2;;
    *) FILES+=("$1"); shift;;
  esac
done

if [[ -z "$BRANCH" ]]; then
  BRANCH="pr/$(date -u +%Y%m%dT%H%M%SZ)"
fi
if [[ -z "$TITLE" ]]; then
  TITLE="Automated PR: $BRANCH"
fi
if [[ -z "$BODY" ]]; then
  BODY="$TITLE"
fi

# Ensure we're in a git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not in a git repository. Run this from your repository root." >&2
  exit 2
fi

# Check gh CLI
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install GitHub CLI (https://cli.github.com/) and authenticate (gh auth login)." >&2
  exit 2
fi

# Dry run helper
run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "+ $*"
  else
    echo "+ $*"; eval "$@"
  fi
}

# Create branch from current HEAD
run_cmd git checkout -b "$BRANCH"

# Stage files
if [[ ${#FILES[@]} -eq 0 ]]; then
  run_cmd git add -A
else
  for f in "${FILES[@]}"; do
    run_cmd git add -- "$f"
  done
fi

# Commit
run_cmd git commit -m "$TITLE" || echo "No changes to commit or commit failed."

# Push branch
run_cmd git push -u origin "$BRANCH"

# Create PR via gh
PR_URL_CMD="gh pr create --title \"$TITLE\" --body \"$BODY\" --base \"$BASE\" --head \"$BRANCH\" --assignee @me --label copilot:auto-allow"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "+ $PR_URL_CMD"
else
  echo "+ $PR_URL_CMD"
  PR_URL=$(eval "$PR_URL_CMD" --web 2>/dev/null || true)
  # gh pr create may output web URL or open browser. Try to capture URL
  if [[ -z "$PR_URL" ]]; then
    # try to get created PR URL via gh api
    PR_URL=$(gh pr view --json url --jq .url 2>/dev/null || true)
  fi
  echo "Pull request created: "+{PR_URL:-(unknown)}
fi

# Checkout back to base if desired
# run_cmd git checkout "$BASE"

echo "Done."