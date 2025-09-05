#!/usr/bin/env python3
"""
Minimal FANTOM GUI Test

Absolute minimal GUI test to see what works.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def create_minimal_window():
    """Create and return a minimal FANTOM window."""
    from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt
    
    class SimpleFANTOMWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("FANTOM Studio - Test Mode")
            self.setGeometry(100, 100, 800, 600)
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Create layout
            layout = QVBoxLayout(central_widget)
            
            # Add labels
            title = QLabel("🚀 FANTOM Studio - Development Environment")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            status = QLabel("✅ Studio Test Interface Active!")
            status.setAlignment(Qt.AlignCenter)
            layout.addWidget(status)
            
            warning = QLabel("⚠️ This is the Studio version (no slicer UI)")
            warning.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning)
            
            ghosts = QLabel("👻 Ghosts in the Machine: ACTIVE")
            ghosts.setAlignment(Qt.AlignCenter)
            layout.addWidget(ghosts)
    
    return SimpleFANTOMWindow()

def main():
    """Main function for standalone execution."""
    print("Step 1: Starting minimal GUI test...")
    
    try:
        print("Step 2: Importing PyQt5...")
        from PyQt5.QtWidgets import QApplication
        
        print("Step 3: Creating QApplication...")
        app = QApplication(sys.argv)
        
        print("Step 4: Creating simple window...")
        window = create_minimal_window()
        
        print("Step 5: Showing window...")
        window.show()
        
        print("✅ FANTOM GUI Test Window is now visible!")
        print("👻 Simple test interface launched")
        print("🔚 Close the window to exit")
        
        # Start event loop
        exit_code = app.exec_()
        print(f"🔚 GUI closed with exit code: {exit_code}")
        return exit_code
        
    except Exception as e:
        print(f"❌ Error in GUI test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
