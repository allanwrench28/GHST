#!/usr/bin/env python3
"""
FANTOM GUI Only Launcher

Direct GUI launcher without terminal disclaimers for testing.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch GUI directly."""
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        from PyQt5.QtCore import Qt
        from slicer_ui.main import FANTOMWindow
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("FANTOM Studio")
        app.setApplicationVersion("0.1.0-alpha")
        app.setOrganizationName("FANTOM FOSS Project")
        
        # Set high DPI support
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        print("🚀 Starting FANTOM Studio GUI...")
        print("📋 Disclaimer will be shown in GUI window")
        
        # Create main window (it will show its own disclaimer)
        window = FANTOMWindow()
        window.show()
        
        print("✅ FANTOM Studio GUI launched successfully!")
        print("👻 Ghosts in the Machine are monitoring...")
        print("⚙️ Ready for AI-driven slicing!")
        print("📝 Check the GUI window for the application interface")
        
        # Start the application event loop
        exit_code = app.exec_()
        
        print("🔚 FANTOM Studio closed")
        return exit_code
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")
        return 1
    except Exception as e:
        print(f"❌ Failed to start FANTOM GUI: {e}")
        print("👻 This error would be captured by the Ghost system!")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 FANTOM interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ FANTOM launcher error: {e}")
        print("👻 This error would be captured by the Ghost system!")
        sys.exit(1)
