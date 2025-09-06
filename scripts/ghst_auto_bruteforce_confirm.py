#!/usr/bin/env python3
"""
GHST Brute-Force Auto-Confirm Script
===================================
Cycles through keypresses, types confirmation words, and clicks all likely locations.
"""
import time

import pyautogui

KEYS = ['enter', 'space', 'tab', 'right', 'left', 'up', 'down']
RESPONSES = ['yes', 'ok', 'continue', 'proceed', 'accept']
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


def brute_force_confirm():
    print("🤖 GHST Brute-Force Auto-Confirm running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    screen_width, screen_height = pyautogui.size()
    while True:
        # Press all keys
        for key in KEYS:
            pyautogui.press(key)
            print(f"✅ Pressed key: {key}")
            time.sleep(0.2)
        # Type all responses
        for resp in RESPONSES:
            pyautogui.typewrite(resp)
            pyautogui.press('enter')
            print(f"✅ Typed '{resp}' and pressed Enter.")
            time.sleep(0.2)
        # Click all likely locations
        for loc_fn in LIKELY_LOCATIONS:
            x, y = loc_fn(screen_width, screen_height)
            pyautogui.click(x, y)
            print(f"✅ Clicked likely button location ({x}, {y}).")
            time.sleep(0.2)
        time.sleep(1)


if __name__ == "__main__":
    brute_force_confirm()
