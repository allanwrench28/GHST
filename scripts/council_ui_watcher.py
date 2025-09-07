import time
import os
import sys
from scripts.sync_ui_to_core import sync_ui_files
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

UI_BRANCH_PATH = os.path.join('GHST Branch NO SLICER', 'src', 'ui_components')
WATCHED_EXTENSIONS = ['.py', '.ui', '.qss']  # Add more as needed

class UIChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if any(event.src_path.endswith(ext) for ext in WATCHED_EXTENSIONS):
            print(f"Council: Detected UI branch change in {event.src_path}. Triggering sync...")
            sync_ui_files()

if __name__ == '__main__':
    event_handler = UIChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, UI_BRANCH_PATH, recursive=True)
    print("Council: UI watcher started. Monitoring for changes...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Council: UI watcher stopped.")
