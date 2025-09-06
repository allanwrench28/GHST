#!/usr/bin/env python3
"""
GHST Think Tank Prompt Script
============================
Prompts the user with a crucial question after 30 seconds of inactivity.
"""
import random
import time

import pyautogui

CRUCIAL_QUESTIONS = [
    "Do you want to enable advanced automation?",
    "Should we overwrite existing files if they already exist?",
    "Would you like to run a full system backup before proceeding?",
    "Do you want to allow internet access for data scrubbing?",
    "Should we apply all recommended fixes automatically?",
    "Would you like to review the generated code before installation?",
    "Do you want to save a checkpoint now?"
]

IDLE_SECONDS = 30


def prompt_crucial_question():
    print("🤖 GHST Think Tank Prompt running. Will ask a crucial question after 30s idle.")
    last_activity = time.time()
    while True:
        # Monitor for mouse or keyboard activity
        if pyautogui.position() != pyautogui.position():
            last_activity = time.time()
        # If idle for threshold, prompt user
        if time.time() - last_activity > IDLE_SECONDS:
            question = random.choice(CRUCIAL_QUESTIONS)
            print(f"\n👻 GHST Think Tank asks: {question}\n")
            last_activity = time.time()
        time.sleep(1)


if __name__ == "__main__":
    prompt_crucial_question()
