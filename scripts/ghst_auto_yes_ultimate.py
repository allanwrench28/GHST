#!/usr/bin/env python3
"""
GHST Ultimate Auto-Yes Script
============================
Scans the screen for confirmation prompts and auto-types or clicks "Yes".
"""
import time

import pyautogui
import pytesseract  # pip install pytesseract
from PIL import ImageGrab

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
    'ok?'
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
BUTTON_KEYWORDS = ['yes', 'ok', 'accept', 'continue', 'proceed']


def scan_and_confirm():
    print("🤖 GHST Ultimate Auto-Yes running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    while True:
        img = ImageGrab.grab()
        text = pytesseract.image_to_string(img).lower()
        # Auto-type 'yes' for text prompts
        for keyword in PROMPT_KEYWORDS:
            if keyword in text:
                pyautogui.typewrite('yes')
                pyautogui.press('enter')
                print(
                    f"✅ Ultimate Auto-Yes: Typed 'yes' for prompt containing '{keyword}'.")
                time.sleep(2)

        # Auto-click 'Yes' buttons by searching for button text
        for button in BUTTON_KEYWORDS:
            if button in text:
                # Try clicking center of screen (common for dialogs)
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width // 2, screen_height // 2)
                print(
                    f"✅ Ultimate Auto-Yes: Clicked center for button '{button}'.")
                time.sleep(2)

        time.sleep(1)


if __name__ == "__main__":

    if __name__ == "__main__":
        scan_and_confirm()
