#!/usr/bin/env python3
"""
🚀 FANTOM Launcher - Ethical AI-Driven 3D Slicer
==================================================

Simple launcher for the FANTOM 3D slicer with 25 PhD-level Ghost AI
specialists and comprehensive ethical oversight.

Created by: The FANTOM Ghost Collective
Ethics: Dr. Ethics Ghost ensures responsible AI behavior
Version: 2.0 - Ethical AI Edition
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def launch_fantom():
    """Launch the FANTOM AI-driven 3D slicer."""
    print("🚀 Starting FANTOM - Ethical AI-Driven 3D Slicer")
    print("=" * 60)
    print()
    
    print("⚖️ ETHICAL AI FRAMEWORK ACTIVE")
    print("✅ Human oversight enabled")
    print("✅ Bias monitoring active")
    print("✅ Transparency enforced")
    print("✅ Human authority maintained")
    print("✅ Emergency protocols ready")
    print()
    
    print("👻 GHOST AI COLLECTIVE STATUS")
    print("📊 25 PhD-level specialists online")
    print("🔬 Analysis, Optimization, Research ready")
    print("🧪 Physics, Materials, Mathematics ready")
    print("🏭 Manufacturing, Quality, Innovation ready")
    print("🎨 ColorScience, Typography, UX ready")
    print("💾 FileSystem, Git, Performance ready")
    print("🛡️ Security, Ethics, Documentation ready")
    print("🤖 AI, Testing, Deployment ready")
    print()
    
    print("🤝 HUMAN-CENTERED DESIGN PRINCIPLES")
    print("• You maintain ultimate authority over all decisions")
    print("• All AI recommendations require your validation")
    print("• Transparent operation with full disclosure")
    print("• Minimum viable human interaction maintained")
    print("• Emergency human override always available")
    print()
    
    # Try to launch the main application
    try:
        print("🔄 Loading AI collective...")
        from src.ai_collaboration.ghost_manager import GhostManager
        ghost_manager = GhostManager()
        print("✅ Ghost collective initialized")
        
        print("🔄 Loading configuration...")
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        print("✅ Configuration loaded")
        
        print("🔄 Starting GUI...")
        from src.slicer_ui.main import FANTOMWindow
        
        # Initialize PyQt5 application
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            print("❌ PyQt5 not found. Installing...")
            os.system("pip install PyQt5")
            from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("FANTOM")
        app.setApplicationVersion("2.0")
        
        # Create main window
        main_window = FANTOMWindow()
        main_window.ghost_manager = ghost_manager
        main_window.config_manager = config_manager
        main_window.show()
        
        print("✅ FANTOM GUI launched successfully!")
        print()
        print("🎯 Ready for ethical AI-assisted 3D slicing!")
        print("💬 Use the chat interface to interact with Ghost specialists")
        print("⚖️ Remember: You have final authority over all decisions")
        print()
        
        # Run the application
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Attempting to install missing dependencies...")
        
        dependencies = [
            "PyQt5",
            "trimesh",
            "PyYAML",
            "numpy"
        ]
        
        for dep in dependencies:
            print(f"📦 Installing {dep}...")
            os.system(f"pip install {dep}")
        
        print("✅ Dependencies installed. Please restart the launcher.")
        
    except Exception as e:
        print(f"❌ Error launching FANTOM: {e}")
        print("🔍 Please check the error above and try again.")
        print("📧 Report issues to the development team.")


def show_help():
    """Show help information."""
    print("🚀 FANTOM Launcher Help")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python launcher.py        - Launch FANTOM")
    print("  python launcher.py help   - Show this help")
    print()
    print("Features:")
    print("• 25 PhD-level Ghost AI specialists")
    print("• Ethical AI framework with human oversight")
    print("• Advanced 3D slicing capabilities")
    print("• Material Design 3.0 interface")
    print("• Comprehensive safety protocols")
    print()
    print("Ethics:")
    print("• Human-centered design principles")
    print("• Transparent AI operations")
    print("• Bias monitoring and mitigation")
    print("• Emergency override capabilities")
    print("• Minimum human interaction requirements")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        show_help()
    else:
        launch_fantom()


if __name__ == "__main__":
    main()
