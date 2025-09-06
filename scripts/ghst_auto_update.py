#!/usr/bin/env python3
"""
GHST Auto-Update Script
======================

Saves checkpoint content to ghst_checkpoints/ and updates GHST_Checkpoint_Log.markdown.
"""
import os
from datetime import datetime

CHECKPOINT_DIR = "ghst_checkpoints"
LOG_FILE = os.path.join(CHECKPOINT_DIR, "GHST_Checkpoint_Log.markdown")


def save_checkpoint(content, key_points=None):
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-update%U")
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f"{timestamp}.txt")
    with open(checkpoint_file, "w", encoding="utf-8") as f:
        f.write(content)
    # Prepare log entry
    log_entry = f"\n## {
        os.path.basename(checkpoint_file)}\n- **Date**: {
        datetime.now().strftime('%B %d, %Y')}\n- **Key Points**: {
            key_points or 'Checkpoint saved.'}\n- **Goal Impact**: Automated update and logging.\n"
    # Append to log
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry)
    print(f"✅ Checkpoint saved: {checkpoint_file}")
    print(f"✅ Log updated: {LOG_FILE}")


if __name__ == "__main__":
    # Example usage
    example_content = "GHST Checkpoint Summary: Automated update test."
    example_points = "Tested auto-update script integration."
    save_checkpoint(example_content, example_points)
