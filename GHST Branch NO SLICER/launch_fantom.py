#!/usr/bin/env python3
"""
FANTOM Launcher Script

Launch the FANTOM AI-driven 3D printing slicer with full
Ghost in the Machine integration and safety systems.

Usage:
    python launch_fantom.py              # Start full GUI
    python launch_fantom.py --test       # Run system tests
    python launch_fantom.py --demo       # Run demo mode
    python launch_fantom.py --console    # Console mode only

WARNING: Use at your own risk. No liability for damages.
"""

import sys
import argparse
from pathlib import Path

def show_banner():
    """Show FANTOM banner."""
    banner = """
    ======================================================
     ______ _                _                       _    
    / _____| |              | |                     | |   
   | |     | | ___   ____  _| |___      ___   _____ | | __
   | |     | |/ _ \ / ___\| __/ _ \    / _ \ / ___ \| |/ /
   | |_____| | (_) | |    | || (_) |  | (_) | |  | ||   < 
    \______|_|\___/|_|     \__\___/    \___/|_|  |_||_|\_\\
    
    AI-Driven 3D Printing Slicer with Ghosts in the Machine
    ======================================================
    
    WARNING: This software is provided "AS IS" with NO LIABILITY
    WARNING: Use experimental features at your own risk
    WARNING: The AI "Ghosts" are experimental and may cause issues
    
    By using FANTOM, you accept full responsibility for any:
    * Machine damage or malfunction
    * Print failures or material waste
    * Personal injury or property damage
    * Data loss or system instability
    
    """
    print(banner)

def launch_gui():
    """Launch the full FANTOM GUI."""
    try:
        print("Starting FANTOM Studio GUI...")
        
        # Add src to path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from PyQt5.QtWidgets import QApplication
        from slicer_ui.main import FANTOMWindow
        
        app = QApplication(sys.argv)
        app.setApplicationName("FANTOM Studio")
        
        window = FANTOMWindow()
        window.show()
        
        print("FANTOM Studio launched successfully!")
        print("Ghosts in the Machine are now monitoring...")
        
        return app.exec_()
        
    except ImportError as e:
        print(f"ERROR: Failed to import GUI components: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")
        return 1
    except Exception as e:
        print(f"ERROR: Failed to start FANTOM GUI: {e}")
        return 1

def run_tests():
    """Run FANTOM system tests."""
    try:
        print("Running FANTOM system tests...")
        
        import subprocess
        result = subprocess.run([
            sys.executable, "test_fantom.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode
        
    except Exception as e:
        print(f"ERROR: Failed to run tests: {e}")
        return 1

def run_demo():
    """Run FANTOM demo."""
    try:
        print("Running FANTOM demo...")
        
        import subprocess
        result = subprocess.run([
            sys.executable, "demo.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode
        
    except Exception as e:
        print(f"ERROR: Failed to run demo: {e}")
        return 1

def console_mode():
    """Run FANTOM in console mode."""
    print("Starting FANTOM Console Mode...")
    print("Available commands:")
    print("  help    - Show this help")
    print("  status  - Show system status")
    print("  ghosts  - Show Ghost activity")
    print("  config  - Show configuration")
    print("  exit    - Exit console")
    print()
    
    while True:
        try:
            cmd = input("fantom> ").strip().lower()
            
            if cmd == "exit":
                break
            elif cmd == "help":
                print("Available commands: help, status, ghosts, config, exit")
            elif cmd == "status":
                print("FANTOM Status: OPERATIONAL")
                print("Ghost Manager: ACTIVE")
                print("Error Handler: MONITORING")
                print("Safety Systems: ENABLED")
            elif cmd == "ghosts":
                print("Ghost Activity:")
                print("- Analysis Ghost: Monitoring codebase")
                print("- Optimization Ghost: Scanning for improvements")
                print("- Error Ghost: Watching for issues")
                print("- Research Ghost: Checking FOSS updates")
            elif cmd == "config":
                print("Configuration:")
                print("- Name: FANTOM")
                print("- Version: 0.1.0-alpha")
                print("- Theme: Material Dark")
                print("- Developer Mode: Disabled (use GUI to enable)")
                print("- Disclaimers: Required")
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            break
    
    print("Console mode ended.")
    return 0

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="FANTOM AI-Driven 3D Printing Slicer",
        epilog="WARNING: Use at your own risk. No liability for damages."
    )
    
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Run system tests"
    )
    
    parser.add_argument(
        "--demo", 
        action="store_true", 
        help="Run demonstration mode"
    )
    
    parser.add_argument(
        "--console", 
        action="store_true", 
        help="Start in console mode"
    )
    
    parser.add_argument(
        "--no-banner", 
        action="store_true", 
        help="Skip banner display"
    )
    
    args = parser.parse_args()
    
    # Show banner unless disabled
    if not args.no_banner:
        show_banner()
        
        # Get user confirmation
        response = input("Do you accept the terms and wish to continue? (y/N): ")
        if not response.lower().startswith('y'):
            print("User declined terms. Exiting.")
            return 0
    
    # Route to appropriate mode
    if args.test:
        return run_tests()
    elif args.demo:
        return run_demo()
    elif args.console:
        return console_mode()
    else:
        return launch_gui()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nFANTOM interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFANTOM launcher error: {e}")
        print("This error would be captured by the Ghost system!")
        sys.exit(1)
