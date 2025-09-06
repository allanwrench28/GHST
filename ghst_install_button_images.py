# GHST Button Image Installer
# Copies all button images (e.g., OK.png, Continue.png) from a source folder into the repo's button_images/ directory.
# Usage: python ghst_install_button_images.py <source_folder>

import os
import shutil
import sys

TARGET_DIR = os.path.join(os.path.dirname(__file__), 'button_images')
BUTTON_NAMES = ['OK.png', 'Continue.png', 'Yes.png', 'Accept.png', 'Close.png']

if len(sys.argv) < 2:
    print("Usage: python ghst_install_button_images.py <source_folder>")
    sys.exit(1)

source_folder = sys.argv[1]
if not os.path.isdir(source_folder):
    print(f"Source folder '{source_folder}' does not exist.")
    sys.exit(1)

os.makedirs(TARGET_DIR, exist_ok=True)

for name in BUTTON_NAMES:
    src = os.path.join(source_folder, name)
    dst = os.path.join(TARGET_DIR, name)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        print(f"✅ Installed {name} to {TARGET_DIR}")
    else:
        print(f"⚠️ {name} not found in source folder.")

print("🎉 Button image installation complete.")
