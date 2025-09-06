#!/usr/bin/env python3
"""
GHST Auto-Yes CLI Script
=======================
Automatically responds "yes" to common CLI confirmation prompts.
"""
import re
import sys
import time


def auto_yes_cli():
    prompt_patterns = [
        r"\[Y/n\]",
        r"\[y/N\]",
        r"Proceed\?",
        r"Continue\?",
        r"Confirm\?",
        r"Do you want to continue\?",
        r"Type 'yes' to proceed",
        r"Are you sure\?",
        r"Accept\?",
        r"Install\?",
        r"Overwrite\?"]
    print("🤖 GHST Auto-Yes CLI running. Will auto-confirm prompts.")
    while True:
        # Read line from stdin (simulate monitoring terminal output)
        line = sys.stdin.readline()
        if not line:
            time.sleep(0.1)
            continue
        for pattern in prompt_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                sys.stdout.write("yes\n")
                sys.stdout.flush()
                print(f"✅ Auto-Yes: Responded 'yes' to prompt: {line.strip()}")
                break


if __name__ == "__main__":
    auto_yes_cli()
