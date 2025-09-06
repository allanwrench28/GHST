# GHST Auto-Continue for GUI Dialogs
# Automatically clicks 'OK' or 'Continue' buttons in PyQt5 dialogs using pyautogui
# Requires: pip install pyautogui

import time
import pyautogui

BUTTON_KEYWORDS = ['OK', 'Continue', 'Yes', 'Accept', 'Close']
SCAN_INTERVAL = 2  # seconds

print("🤖 GHST Auto-Continue GUI running. Move mouse to top-left to stop.")

try:
    while True:
        # Screenshot and locate buttons by text
        for keyword in BUTTON_KEYWORDS:
            try:
                # Locate button by text (OCR)
                button_location = pyautogui.locateOnScreen(f'{keyword}.png', confidence=0.8)
                if button_location:
                    pyautogui.click(button_location)
                    print(f"✅ Auto-Continue: Clicked '{keyword}' button.")
            except Exception:
                pass
        # Emergency stop: move mouse to top-left
        if pyautogui.position() == (0, 0):
            print("🛑 GHST Auto-Continue stopped by user.")
            break
        time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
    print("🛑 GHST Auto-Continue stopped by keyboard interrupt.")
