# Force Sync Branches GitHub Action

This repo includes a GitHub Action that force-pushes the contents of `main` to specific branches (`dev-branch`, `feature-branch`, `test-branch`) every time you push to `main`.

## How it Works
- On every push to `main`, the workflow force-pushes the latest state of `main` to your target branches.
- You can change the branch names in `.github/workflows/force-sync-branches.yml` as needed.

## Setup Instructions
1. All files/scripts are already included (see below).
2. To add/remove branches, edit the `BRANCHES` line in `.github/workflows/force-sync-branches.yml`.

## Included Scripts
- `.github/workflows/force-sync-branches.yml`: The workflow file that automates syncing.
- `setup_force_sync_action.py`: Script to auto-generate the workflow file if needed (already in the repo).

## Usage
No manual setup needed. Just push commits to `main` and the target branches will be force-updated automatically.
