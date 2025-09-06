# GHST Auto-Continue GUI with OCR
# Automatically clicks dialog buttons using OCR (pytesseract) and pyautogui
# Requires: pip install pyautogui pytesseract pillow


import time
import pyautogui
import pytesseract


# Force pytesseract to use the correct executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BUTTON_KEYWORDS = ['OK', 'Continue', 'Yes', 'Accept', 'Close']
SCAN_INTERVAL = 2  # seconds
REGION = None  # Set to None for full screen, or (left, top, width, height)

print("🤖 GHST Auto-Continue GUI (OCR) running.")
print("Move mouse to top-left to stop.")

try:
    while True:
        # Take screenshot
        screenshot = pyautogui.screenshot(region=REGION)
        text = pytesseract.image_to_string(screenshot)
        for keyword in BUTTON_KEYWORDS:
            if keyword in text:
                print(f"🔍 Found '{keyword}' in screenshot text.")
                # Try to locate button visually
                button_location = pyautogui.locateCenterOnScreen(
                    f'{keyword}.png', confidence=0.8)
                if button_location:
                    pyautogui.click(button_location)
                    print(f"✅ Auto-Continue: Clicked '{keyword}' button.")
                else:
                    print(f"⚠️ '{keyword}' text found, but button image not found.")
        # Emergency stop: move mouse to top-left
        if pyautogui.position() == (0, 0):
            print("🛑 GHST Auto-Continue stopped by user.")
            break
        time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
    print("🛑 GHST Auto-Continue stopped by keyboard interrupt.")
