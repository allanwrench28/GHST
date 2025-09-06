#!/usr/bin/env python3
"""
GHST Think Tank Debate Prompt Script
===================================
Simulates a council debate and asks the most pertinent question after 30s idle.
"""
import random
import time

COUNCIL_DEBATE = [
    ("Dr. Fixer", "We need to know if you want auto-fixes enabled!"),
    ("Prof. Backup", "Backup is more important before any changes!"),
    ("Dr. UI", "Should we simplify the interface even more?"),
    ("Prof. Ethics", "Do you want to review code for compliance?"),
    ("Dr. Speed", "Should we optimize for speed or safety?"),
    ("Prof. Internet", "Is it okay to use online data for suggestions?"),
]

PERTINENT_QUESTIONS = [
    "Enable auto-fixes?",
    "Run backup before changes?",
    "Simplify interface more?",
    "Review code for compliance?",
    "Optimize for speed or safety?",
    "Allow internet data for suggestions?",
]

IDLE_SECONDS = 30


def prompt_debate_question():
    print("🤖 GHST Think Tank Debate running. Will ask the most crucial question after 30s idle.")
    last_activity = time.time()
    while True:
        # Simulate idle detection (replace with real activity check if needed)
        if time.time() - last_activity > IDLE_SECONDS:
            # Simulate council debate
            print("\n👻 GHST Council begins debate:")
            debaters = random.sample(COUNCIL_DEBATE, 3)
            for name, line in debaters:
                print(f"{name}: {line}")
            # Present the most pertinent question
            question = random.choice(PERTINENT_QUESTIONS)
            print(f"\n👻 GHST asks: {question}\n")
            last_activity = time.time()
        time.sleep(1)


if __name__ == "__main__":
    prompt_debate_question()
