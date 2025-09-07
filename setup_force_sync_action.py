import os

WORKFLOW_DIR = ".github/workflows"
WORKFLOW_FILE = "force-sync-branches.yml"
TARGET_BRANCHES = ["dev-branch", "feature-branch", "test-branch"]  # Change as needed

yaml_content = f"""name: Force Sync Branches

on:
  push:
    branches:
      - main

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main
        uses: actions/checkout@v3
        with:
          ref: main

      - name: Set up Git user
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "github-actions[bot]"

      - name: Force push to other branches
        env:
          BRANCHES: "{' '.join(TARGET_BRANCHES)}"
        run: |
          for branch in $BRANCHES; do
            git checkout $branch || git checkout -b $branch
            git reset --hard main
            git push origin $branch --force
          done
"""

def main():
    # Create directory if it doesn't exist
    os.makedirs(WORKFLOW_DIR, exist_ok=True)
    workflow_path = os.path.join(WORKFLOW_DIR, WORKFLOW_FILE)
    with open(workflow_path, "w") as f:
        f.write(yaml_content)
    print(f"Created workflow file: {workflow_path}")
    print(f"Target branches: {TARGET_BRANCHES}")

if __name__ == "__main__":
    main()