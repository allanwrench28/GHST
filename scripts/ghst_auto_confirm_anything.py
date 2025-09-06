#!/usr/bin/env python3
"""
GHST Universal Auto-Confirm Script
=================================
Aggressively clicks and types confirmation responses at all likely locations.
"""
import time

import pyautogui

LIKELY_LOCATIONS = [
    lambda w, h: (w // 2, h // 2),      # Center
    lambda w, h: (w - 100, h - 50),     # Bottom right
    lambda w, h: (100, h - 50),         # Bottom left
    lambda w, h: (w // 2, h - 50),      # Bottom center
    lambda w, h: (w - 100, h // 2),     # Right center
    lambda w, h: (100, h // 2),         # Left center
    lambda w, h: (w // 2, 100),         # Top center
    lambda w, h: (w - 100, 100),        # Top right
    lambda w, h: (100, 100),            # Top left
]

RESPONSES = ['yes', 'ok', 'continue', 'proceed', 'accept']


def auto_confirm_anything():
    print("🤖 GHST Universal Auto-Confirm running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    screen_width, screen_height = pyautogui.size()
    while True:
        # Click all likely button locations
        for loc_fn in LIKELY_LOCATIONS:
            x, y = loc_fn(screen_width, screen_height)
            pyautogui.click(x, y)
            print(f"✅ Clicked likely button location ({x}, {y}).")
            time.sleep(0.5)
        # Type all common confirmation responses
        for resp in RESPONSES:
            pyautogui.typewrite(resp)
            pyautogui.press('enter')
            print(f"✅ Typed '{resp}' and pressed Enter.")
            time.sleep(0.5)
        time.sleep(2)


if __name__ == "__main__":
    auto_confirm_anything()
