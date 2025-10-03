#!/usr/bin/env python3
"""
GHST GUI Launcher

Direct GUI launcher for the GHST AI Coding Engine.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch GHST GUI directly."""
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        from ui_components.main import GHSTWindow

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("GHST AI Coding Engine")
        app.setApplicationVersion("0.1.0-alpha")
        app.setOrganizationName("GHST FOSS Project")
        app.setStyle('Fusion')  # Use Fusion style for consistent cross-platform look
        
        # Set high DPI support
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        print("🚀 Starting GHST AI Coding Engine GUI...")
        
        # Create main window
        window = GHSTWindow()
        window.show()
        
        print("✅ GHST GUI launched successfully!")
        print("👻 AI Expert Agents are monitoring and ready to assist.")
        print("⚙️ Ready for AI-assisted coding!")
        print("📝 Check the GUI window for the application interface")

        # Start the application event loop
        exit_code = app.exec_()
        
        print("🔚 GHST closed")
        return exit_code
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")
        return 1
    except Exception as e:
        print(f"❌ Failed to start GHST GUI: {e}")
        print("🧠 This error would be captured by the AI expert system!")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 GHST interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ GHST launcher error: {e}")
        print("🧠 This error would be captured by the AI expert system!")
        import traceback
        traceback.print_exc()
        sys.exit(1)
