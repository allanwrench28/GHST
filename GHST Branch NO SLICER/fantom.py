#!/usr/bin/env python3
"""
FANTOM Studio Launcher

Launch the FANTOM Studio development environment with Ghost in the Machine 
integration. This version excludes slicer functionality and focuses on
the core AI collaboration framework and plugin system.

⚠️ DISCLAIMER: FANTOM is provided "as is" under the MIT license.
The developers assume NO LIABILITY for any damage, injury, or loss.
Use at your own risk.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

def show_startup_disclaimer():
    """Show the mandatory startup disclaimer."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    disclaimer = QMessageBox()
    disclaimer.setWindowTitle("⚙️ FANTOM - Important Disclaimer")
    disclaimer.setIcon(QMessageBox.Warning)
    
    disclaimer_text = """
    ⚠️ FANTOM DISCLAIMER ⚠️
    
    FANTOM is provided "AS IS" under the MIT license.
    
    The developers assume NO LIABILITY for any:
    • Machine damage or malfunction
    • Print failures or material waste  
    • Personal injury or property damage
    • Data loss or corruption
    • Experimental feature side effects
    
    By proceeding, you acknowledge:
    ✓ All use is at your own risk
    ✓ You understand experimental features may cause issues
    ✓ The AI "Ghosts in the Machine" are experimental
    ✓ You have read and accept these terms
    
    Do you accept these terms and wish to continue?
    """
    
    disclaimer.setText(disclaimer_text)
    disclaimer.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    disclaimer.setDefaultButton(QMessageBox.No)
    
    # Apply dark theme styling
    disclaimer.setStyleSheet("""
        QMessageBox {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QMessageBox QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            color: #ffffff;
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #505050;
        }
        QMessageBox QPushButton:pressed {
            background-color: #353535;
        }
    """)
    
    result = disclaimer.exec_()
    return result == QMessageBox.Yes

def main():
    """Main application entry point."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("FANTOM Studio")
    app.setApplicationVersion("0.1.0-alpha")
    app.setOrganizationName("FANTOM FOSS Project")
    
    # Set high DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Show disclaimer first
    if not show_startup_disclaimer():
        print("User declined disclaimer. Exiting FANTOM.")
        sys.exit(0)
    
    # Import and create main window after disclaimer acceptance
    try:
        # Studio version - launch demo instead of slicer UI
        print("🚀 FANTOM Studio launched successfully!")
        print("👻 Ghosts in the Machine are monitoring...")
        print("⚙️ Running Studio Demo...")
        
        # Import and run demo
        sys.path.append('.')
        import demo
        demo.main()
        
    except ImportError as e:
        QMessageBox.critical(
            None, 
            "FANTOM - Import Error", 
            f"Failed to import FANTOM modules:\n{e}\n\nPlease check your installation."
        )
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(
            None, 
            "FANTOM - Startup Error", 
            f"Failed to start FANTOM:\n{e}\n\nPlease check logs for details."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
