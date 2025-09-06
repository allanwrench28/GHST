#!/usr/bin/env python3
"""
🚀 GHST Launcher - AI Coding Engine
===================================

Simple launcher for the GHST AI coding engine with expert AI agents
for coding, debugging, and problem solving.

Created by: The GHST Expert Collective
Version: 0.1.0-alpha - AI Coding Engine Edition
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import GHST components
try:
    from src.syntax_supervisors import SyntaxSupervisorManager
    SYNTAX_SUPERVISORS_AVAILABLE = True
except ImportError:
    SYNTAX_SUPERVISORS_AVAILABLE = False
    print("⚠️ Syntax Supervisors not available")


def launch_ghst():
    """Launch the GHST AI coding engine."""
    print("🚀 Starting GHST - Open Source AI Coding Engine")
    print("=" * 60)
    print()
    
    print("🧠 AI EXPERT COLLECTIVE STATUS")
    print("✅ Human oversight enabled")
    print("✅ Transparency enforced")
    print("✅ Human authority maintained")
    print("✅ Expert agents ready")
    print()
    
    print("�‍💻 AI EXPERT AGENTS ONLINE")
    print("� Code Analysis & Debugging specialists ready")
    print("�️ Problem Solving & Optimization ready")
    print("📚 Documentation & Testing ready")
    print("🔧 Plugin System & Configuration ready")
    print("🎨 UI Components & Themes ready")
    print("⚡ Performance & Security ready")
    print("🤖 AI Collaboration Framework active")
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
        print("🔄 Loading AI expert collective...")
        from src.ai_collaboration.expert_manager import ExpertManager
        expert_manager = ExpertManager()
        print("✅ AI expert collective initialized")
        
        print("🔄 Loading configuration...")
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        print("✅ Configuration loaded")
        
        # Initialize Syntax Supervisors
        if SYNTAX_SUPERVISORS_AVAILABLE:
            print("🔄 Starting Syntax Supervisors...")
            ss_manager = SyntaxSupervisorManager(str(project_root))
            ss_manager.start_monitoring()
            print("✅ Syntax Supervisors active - monitoring in background")
        else:
            print("⚠️ Syntax Supervisors unavailable")
        
        print("🔄 Starting GUI...")
        from src.ui_components.main import GHSTWindow
        
        # Initialize PyQt5 application
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            print("❌ PyQt5 not found. Installing...")
            os.system("pip install PyQt5")
            from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("GHST")
        app.setApplicationVersion("0.1.0-alpha")
        
        # Create main window
        main_window = GHSTWindow()
        main_window.expert_manager = expert_manager
        main_window.config_manager = config_manager
        main_window.show()
        
        print("✅ GHST GUI launched successfully!")
        print()
        print("🎯 Ready for AI-assisted coding and problem solving!")
        print("💬 Use the interface to interact with expert AI agents")
        print("⚖️ Remember: You have final authority over all decisions")
        print()
        
        # Run the application
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Attempting to install missing dependencies...")
        
        dependencies = [
            "PyQt5",
            "PyYAML",
            "numpy"
        ]
        
        for dep in dependencies:
            print(f"📦 Installing {dep}...")
            os.system(f"pip install {dep}")
        
        print("✅ Dependencies installed. Please restart the launcher.")
        
    except Exception as e:
        print(f"❌ Error launching GHST: {e}")
        print("🔍 Please check the error above and try again.")
        print("📧 Report issues to the development team.")


def show_help():
    """Show help information."""
    print("🚀 GHST Launcher Help")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python launcher.py        - Launch GHST")
    print("  python launcher.py help   - Show this help")
    print()
    print("Features:")
    print("• AI expert collective for coding assistance")
    print("• Plugin system for extensibility")
    print("• YAML-based configuration management")
    print("• Modern UI components and themes")
    print("• Developer tools and automation")
    print()
    print("Ethics:")
    print("• Human-centered design principles")
    print("• Transparent AI operations")
    print("• Human oversight and control")
    print("• Open source collaboration")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        show_help()
    else:
        launch_ghst()


if __name__ == "__main__":
    main()
