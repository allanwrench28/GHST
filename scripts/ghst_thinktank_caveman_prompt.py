#!/usr/bin/env python3
"""
GHST Caveman Think Tank Prompt Script
====================================
Prompts the user with short, easy questions and 2-5 dynamic options after 30s idle.
"""
import random
import time

CAVEMAN_PROMPTS = [
    ("Save now?", ["Yes", "No", "Later", "Show details"]),
    ("Auto-fix everything?", ["Yes", "No", "Review", "Skip", "Explain"]),
    ("Overwrite old files?", ["Yes", "No", "Backup first", "Ask me next time"]),
    ("Run backup?", ["Yes", "No", "Only important", "Show log"]),
    ("Use internet?", ["Yes", "No", "Ask me", "Offline mode"]),
    ("Apply all fixes?", ["Yes", "No", "Review", "Skip"]),
    ("Review code?", ["Yes", "No", "Show changes", "Trust AI"]),
    ("Continue?", ["Yes", "No", "Pause", "Show plan"]),
]

IDLE_SECONDS = 30


def prompt_caveman_question():
    print("🤖 GHST Caveman Think Tank Prompt running. Will ask a short question after 30s idle.")
    last_activity = time.time()
    while True:
        # Simulate idle detection (replace with real activity check if needed)
        if time.time() - last_activity > IDLE_SECONDS:
            question, options = random.choice(CAVEMAN_PROMPTS)
            print(f"\n👻 GHST asks: {question}")
            print("Options:", " | ".join(f"[{opt}]" for opt in options))
            last_activity = time.time()
        time.sleep(1)


if __name__ == "__main__":
    prompt_caveman_question()
