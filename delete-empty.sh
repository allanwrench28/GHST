#!/usr/bin/env bash
# Delete empty regular files and empty directories under a root (default: .)
# - Deletes empty files
# - Removes empty directories (only if empty)
# Usage: ./delete-empty.sh [-n] [-r ROOT] [-h]
#   -n        dry-run (show what would happen)
#   -r ROOT   root directory to search (default: .)
#   -h        show this help
set -euo pipefail

DRYRUN=false
ROOT="."

print_usage() {
  cat <<EOF
Usage: $0 [-n] [-r ROOT]
  -n        dry-run (show what would happen)
  -r ROOT   root directory to search (default: .)
  -h        show this help

This script will:
  - Find and delete empty regular files (size 0).
  - Find and remove empty directories (only if empty).
Safety:
  - Will NOT touch .git or .github directories.
  - Will NOT remove the ROOT directory itself.
  - Refuses to run if ROOT resolves to "/" for safety.
EOF
}

while getopts ":nr:h" opt; do
  case $opt in
    n) DRYRUN=true ;;  
    r) ROOT="$OPTARG" ;;  
    h) print_usage; exit 0 ;;  
    \?) echo "Invalid option -$OPTARG" >&2; print_usage; exit 1 ;;  
  esac
done

# Resolve absolute path for ROOT
if command -v realpath >/dev/null 2>&1; then
  ROOT_ABS=$(realpath "$ROOT")
else
  ROOT_ABS=$(python3 - <<PY
import os,sys
print(os.path.abspath(sys.argv[1]))
PY
"$ROOT")
fi

echo "Root: $ROOT_ABS"
$DRYRUN && echo "Dry-run: ON"

# Safety checks
if [ "$ROOT_ABS" = "/" ]; then
  echo "Refusing to operate at root '/' for safety." >&2;
  exit 1
fi

# Exclude patterns (absolute path prefixes)
EXCLUDE_PATHS=("$ROOT_ABS/.git" "$ROOT_ABS/.git/*" "$ROOT_ABS/.github" "$ROOT_ABS/.github/*")

# 1) Find empty regular files
echo "Searching for empty files..."
if $DRYRUN; then
  find "$ROOT_ABS" -type f -empty \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -print0 | xargs -0 -I{} bash -c 'echo "Would delete file: {}"'
else
  files_deleted=0
  while IFS= read -r -d '' f; do
    rm -f -- "$f" && {
      echo "Deleted file: $f"
      files_deleted=$((files_deleted+1))
    } || {
      echo "Failed to delete file: $f" >&2
    }
  done < <(find "$ROOT_ABS" -type f -empty \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) -print0)
  echo "Deleted $files_deleted empty files."
fi

# 2) Find and remove empty directories (deepest first)
echo "Searching for empty directories..."
if $DRYRUN; then
  find "$ROOT_ABS" -type d \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -not -Path "$ROOT_ABS" -empty -print0 | xargs -0 -I{} bash -c 'echo "Would remove empty dir: {}"'
else
  mapfile -d '' dirs < <(find "$ROOT_ABS" -type d \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -not -path "$ROOT_ABS" -empty -print0 || true)

  if [ "");  # Find empty regular files
  echo "Searching for empty files..."
if $DRYRUN; then
  find "$ROOT_ABS" -type f -empty \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -print0 | xargs -0 -I{} bash -c 'echo "Would delete file: {}"'
else
  files_deleted=0
  while IFS= read -r -d '' f; do
    rm -f -- "$f" && {
      echo "Deleted file: $f"
      files_deleted=$((files_deleted+1))
    } || {
      echo "Failed to delete file: $f" >&2
    }
  done < <(find "$ROOT_ABS" -type f -empty \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) -print0)
  echo "Deleted $files_deleted empty files."
fi

# 2) Find and remove empty directories (deepest first)
echo "Searching for empty directories..."
if $DRYRUN; then
  find "$ROOT_ABS" -type d \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -not -Path "$ROOT_ABS" -empty -print0 | xargs -0 -I{} bash -c 'echo "Would remove empty dir: {}"'
else
  mapfile -d '' dirs < <(find "$ROOT_ABS" -type d \
    $(for p in "${EXCLUDE_PATHS[@]}"; do printf ' -not -path %q' "$p"; done) \
    -not -path "$ROOT_ABS" -empty -print0 || true)

  if [ "${#dirs[@]}" -eq 0 ]; then
    echo "No empty directories found."
  else
    IFS=$'\n' sorted_dirs=($(for d in "${dirs[@]}"; do echo "$d"; done | awk '{ print length, $0 }' | sort -rn | cut -d" " -f2-))
    dirs_removed=0
    for d in "${sorted_dirs[@]}"; do
      [ -z "$d" ] && continue
      if rmdir -- "$d" 2>/dev/null; then
        echo "Removed empty dir: $d"
        dirs_removed=$((dirs_removed+1))
      else
        echo "Skipped (not empty now): $d"
      fi
    done
    echo "Removed $dirs_removed empty directories."
  fi
fi

echo "Done."