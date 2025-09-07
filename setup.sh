#!/usr/bin/env bash
set -euo pipefail

echo "Bootstrapping GHST browser tooling..."

# Make sure we're running from the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Install nvm and Node 18 if node is missing
if ! command -v node >/dev/null 2>&1; then
  echo "Node not found. Installing via nvm..."
  if [ ! -d "$HOME/.nvm" ]; then
    curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \ . "$NVM_DIR/nvm.sh"
  else
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \ . "$NVM_DIR/nvm.sh"
  fi
  nvm install 18
fi

# Ensure npm is available
if ! command -v npm >/dev/null 2>&1; then
  echo "npm still not available. Aborting."
  exit 1
fi

# Install node deps
echo "Installing npm dependencies..."
npm install

# Install Playwright browsers and OS deps
echo "Installing Playwright browsers (this may require sudo for system dependencies)..."
# Use --with-deps on linux to attempt system deps install where supported
npx playwright install --with-deps || npx playwright install

# Make scripts executable
chmod +x setup.sh

cat <<'EOF'
Bootstrapping complete.
To run a quick fetch of a page with Playwright:
  TARGET_URL='https://example.com' npm run fetch

If you want to run the workflow locally (simulate):
  ./setup.sh
EOF

exit 0
