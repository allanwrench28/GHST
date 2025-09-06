#!/usr/bin/env python3
"""
GHST OCR Auto-Continue Script
============================
Scans the screen for confirmation prompts and auto-responds "yes".
"""
import time

import pyautogui
import pytesseract
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
    'ok?']


def scan_and_confirm():
    print("🤖 GHST OCR Auto-Continue running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    while True:
        img = ImageGrab.grab()
        text = pytesseract.image_to_string(img).lower()
        for keyword in PROMPT_KEYWORDS:
            if keyword in text:
                pyautogui.typewrite('yes')
                pyautogui.press('enter')
                print(
                    f"✅ OCR Auto-Continue: Responded 'yes' to prompt containing '{keyword}'.")
                time.sleep(2)
        time.sleep(1)


if __name__ == "__main__":
    scan_and_confirm()
