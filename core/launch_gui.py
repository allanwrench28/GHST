#!/usr/bin/env python3
"""
GHST GUI Launcher

Direct GUI launcher for the GHST AI coding engine.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Launch GUI directly."""
    try:
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication
        from src.ui_components.main import GHSTWindow

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("GHST")
        app.setApplicationVersion("0.1.0-alpha")
        app.setOrganizationName("GHST Open Source Project")

        # Set high DPI support
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        print("🚀 Starting GHST AI Coding Engine GUI...")
        print("📋 Loading expert AI agents...")

        # Create main window
        window = GHSTWindow()
        window.show()

        print("✅ GHST GUI launched successfully!")
        print("🧠 AI expert collective is monitoring...")
        print("⚙️ Ready for AI-assisted coding!")
        print("📝 Check the GUI window for the application interface")
        print("👥 Council status: All agents are monitoring and ready to assist.")

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
        sys.exit(1)
