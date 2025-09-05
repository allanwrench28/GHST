#!/usr/bin/env python3
"""
FANTOM GUI Test Launcher

Launches GUI with minimal disclaimers for testing purposes.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch GUI for testing."""
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        # Create application first
        app = QApplication(sys.argv)
        app.setApplicationName("FANTOM Studio")
        app.setApplicationVersion("0.1.0-alpha")
        
        print("🚀 Starting FANTOM Studio GUI (Test Mode)...")
        
        # Import and create window after app creation
        # Studio version - use minimal GUI test instead of slicer UI
        from minimal_gui_test import create_minimal_window
        
        # Create minimal test window
        window = create_minimal_window()
        window.show()
        
        print("✅ FANTOM Studio minimal GUI is now visible!")
        print("👻 Ghosts in the Machine are monitoring...")
        print("⚙️ Studio version - no slicer UI included!")
        print("🔚 Close the GUI window to exit")
        
        # Start the application event loop
        exit_code = app.exec_()
        
        print("🔚 FANTOM Studio closed")
        return exit_code
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("Please ensure PyQt5 is installed")
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
        sys.exit(1)
