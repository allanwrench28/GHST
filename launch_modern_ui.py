#!/usr/bin/env python3
"""
Launch Script for GHST Modern UI

Convenient launcher for the modernized GHST interface with proper error handling.
"""

import sys
import os

# Add the core/src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core', 'src'))

try:
    from PyQt5.QtWidgets import QApplication
    from ui_components.modern_main_window import ModernMainWindow
    
    def main():
        """Launch the modern GHST UI."""
        print("🚀 Launching GHST Modern UI...")
        print("✨ Features:")
        print("   - GitHub Dark theme with proper contrast")
        print("   - ChatGPT/Grok-style interface")
        print("   - Python syntax highlighting")
        print("   - Smooth animations (400ms fade-in)")
        print("   - Modern message bubbles")
        print("   - Production-quality code")
        print()
        
        app = QApplication(sys.argv)
        app.setApplicationName("GHST - AI Coding Engine")
        app.setOrganizationName("GHST")
        
        window = ModernMainWindow()
        window.show()
        
        print("✅ GHST Modern UI launched successfully!")
        print("💡 Tip: Check the chat interface for AI assistance")
        print()
        
        sys.exit(app.exec_())
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Error: Failed to import required modules")
    print(f"   {e}")
    print()
    print("💡 Make sure PyQt5 is installed:")
    print("   pip install PyQt5>=5.15.0")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error launching GHST Modern UI:")
    print(f"   {e}")
    sys.exit(1)
