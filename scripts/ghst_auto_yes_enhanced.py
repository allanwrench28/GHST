#!/usr/bin/env python3
"""
GHST Auto-Yes Enhanced Script
============================
Automatically responds "yes" to CLI and interactive console prompts.
"""
import time

import keyboard
import pyautogui

PROMPT_KEYWORDS = [
    'y/n',
    'yes/no',
    'proceed',
    'continue',
    'confirm',
    'do you want to continue',
    'type yes to proceed',
    'are you sure',
    'accept',
    'install',
    'overwrite',
    'ok?']


def auto_yes_enhanced():
    print("🤖 GHST Auto-Yes Enhanced running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    while True:
        # If a prompt keyword is detected in the active window, type 'yes' and
        # press Enter
        for keyword in PROMPT_KEYWORDS:
            if keyboard.is_pressed('y') or keyboard.is_pressed('Y'):
                pyautogui.typewrite('yes')
                pyautogui.press('enter')
                print(
                    f"✅ Auto-Yes: Responded 'yes' to prompt containing '{keyword}'.")
        time.sleep(0.5)


if __name__ == "__main__":
    auto_yes_enhanced()
