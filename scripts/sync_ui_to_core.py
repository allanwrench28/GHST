import shutil
import os
from datetime import datetime

# Paths to UI branch and main core UI components
UI_BRANCH_PATH = os.path.join('GHST Branch NO SLICER', 'src', 'ui_components')
MAIN_CORE_PATH = os.path.join('src', 'ui_components')

COUNCIL_LOG_PATH = os.path.join('GHST Branch NO SLICER', 'ghst_checkpoints', 'council_ui_sync_log.txt')

# List of UI files to sync (add more as needed)
UI_FILES = [
    'speedbuild_slider.py',
    # Add other UI files here
]


def sync_ui_files():
    council_messages = []
    ml_issues = []
    for filename in UI_FILES:
        src = os.path.join(UI_BRANCH_PATH, filename)
        dst = os.path.join(MAIN_CORE_PATH, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            council_messages.append(f"Council: Synced {filename} from UI branch to main core at {datetime.now().isoformat()}.")
        else:
            msg = f"Council: {filename} not found in UI branch, skipped. [ML: Branch divergence, manual review needed]"
            council_messages.append(msg)
            ml_issues.append(msg)
    # Log council feedback
    with open(COUNCIL_LOG_PATH, 'a') as log:
        for msg in council_messages:
            log.write(msg + '\n')
        if ml_issues:
            log.write("\n--- ML RELEVANT ISSUES ---\n")
            for issue in ml_issues:
                log.write(issue + '\n')
    print('\n'.join(council_messages))
    if ml_issues:
        print("\n--- ML RELEVANT ISSUES ---")
        for issue in ml_issues:
            print(issue)

if __name__ == '__main__':
    sync_ui_files()
    print("Council: UI sync complete. Main core is up to date.")
