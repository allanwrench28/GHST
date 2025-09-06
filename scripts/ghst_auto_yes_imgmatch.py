#!/usr/bin/env python3
"""
GHST Auto-Yes Image-Match Script
===============================
Scans the screen for 'Yes'/'OK' buttons using image matching and clicks them.
"""
import time

import pyautogui
from PIL import Image

# You must provide reference images for 'Yes' and 'OK' buttons (PNG, cropped)
BUTTON_IMAGES = [
    'yes_button.png',
    'ok_button.png'
]

LIKELY_LOCATIONS = [
    lambda w, h: (w // 2, h // 2),  # Center
    lambda w, h: (w - 100, h - 50),  # Bottom right
    lambda w, h: (100, h - 50),     # Bottom left
    lambda w, h: (w // 2, h - 50),  # Bottom center
    lambda w, h: (w - 100, h // 2),  # Right center
]


def find_and_click_buttons():
    print("🤖 GHST Auto-Yes Image-Match running. Move mouse to top-left to stop.")
    pyautogui.FAILSAFE = True
    screen_width, screen_height = pyautogui.size()
    while True:
        screenshot = pyautogui.screenshot()
        for img_path in BUTTON_IMAGES:
            try:
                button_img = Image.open(img_path)
                loc = pyautogui.locateCenterOnScreen(
                    button_img, confidence=0.8)
                if loc:
                    pyautogui.click(loc)
                    print(
                        f"✅ Image-Match: Clicked button at {loc} from {img_path}.")
                    time.sleep(2)
            except Exception as e:
                pass
        # Fallback: click all likely locations
        for loc_fn in LIKELY_LOCATIONS:
            x, y = loc_fn(screen_width, screen_height)
            pyautogui.click(x, y)
            print(f"✅ Fallback: Clicked likely button location ({x}, {y}).")
            time.sleep(1)
        time.sleep(2)


if __name__ == "__main__":
    find_and_click_buttons()
