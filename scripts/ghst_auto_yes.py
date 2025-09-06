#!/usr/bin/env python3
"""
GHST Auto-Yes Script
===================
Automatically responds "yes" to prompts and dialogs.
"""
import time

import keyboard
import pyautogui


def auto_yes_loop():
    print("🤖 GHST Auto-Yes running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    while True:
        # Simulate typing "yes" and pressing Enter if Y/N prompt detected
        if keyboard.is_pressed('y') or keyboard.is_pressed('Y'):
            pyautogui.typewrite('yes')
            pyautogui.press('enter')
            print("✅ Auto-Yes: Responded 'yes' to prompt.")
        time.sleep(0.5)


if __name__ == "__main__":
    auto_yes_loop()
