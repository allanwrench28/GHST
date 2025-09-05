#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FANTOM Demo Script

Demonstrates the key features of FANTOM:
- Ghost in the Machine AI system
- Developer mode with disclaimers
- Error handling and PR submission
- FOSS-driven innovation

WARNING: This is a demonstration - use at your own risk!
"""

import sys
import time
import random
from pathlib import Path

# Set UTF-8 encoding for Windows
import os
if os.name == 'nt':  # Windows
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from ai_collaboration.ghost_manager import GhostManager
    from ai_collaboration.error_handler import ErrorHandler
    from utils.config_manager import ConfigManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed.")
    sys.exit(1)

def demo_disclaimer():
    """Show demo disclaimer."""
    print("=" + "="*60 + "=")
    print("            FANTOM DEMO - DISCLAIMER")
    print("=" + "="*60 + "=")
    print()
    print("WARNING: This demonstration shows FANTOM's AI capabilities")
    print("WARNING: All features are experimental and use is at your own risk")
    print("WARNING: The 'Ghosts in the Machine' are AI entities that:")
    print("   * Monitor for errors and issues")
    print("   * Research FOSS solutions via internet")
    print("   * Submit pull requests for improvements")
    print("   * Operate with repository admin access")
    print()
    print("GHOSTS ASSUME NO LIABILITY for any damages")
    print("DENY: Use experimental features at your own risk")
    print()
    response = input("Continue with demo? (y/N): ").lower().strip()
    return response in ['y', 'yes']

def simulate_ghost_activity():
    """Simulate Ghost in the Machine activity."""
    activities = [
        "SCAN: Scanning codebase for optimization opportunities...",
        "WEB: Researching FOSS slicing algorithms on GitHub...",
        "AI: Analyzing print failure patterns...",
        "OPT: Optimizing toolpath generation...",
        "FIX: Detecting potential memory leaks...",
        "DATA: Processing material compatibility data...",
        "CALIB: Calibrating AI models with new data...",
        "PR: Submitting pull request for bug fix..."
    ]
    
    for i in range(8):
        activity = random.choice(activities)
        print(f"Ghost #{i+1}: {activity}")
        time.sleep(0.5)
    
    print("\nSUCCESS: Ghost collective analysis complete!")

def simulate_error_handling():
    """Simulate error detection and AI-driven fixing."""
    print("\n🚨 Simulating error detection...")
    
    # Simulate different types of errors
    errors = [
        {"code": "MESH_001", "type": "mesh_error", "desc": "Non-manifold geometry detected"},
        {"code": "SLICE_002", "type": "slicing_error", "desc": "Layer height incompatible with nozzle"},
        {"code": "IO_003", "type": "io_error", "desc": "STL file corrupted or invalid"},
    ]
    
    for error in errors:
        print(f"❌ Error {error['code']}: {error['desc']}")
        print(f"🤖 Ghost analyzing error type: {error['type']}")
        print("🌐 Searching FOSS repositories for solutions...")
        print("📝 Generating fix proposal...")
        print("🔄 Preparing pull request with disclaimer...")
        print("✅ Error handled by Ghost collective\n")
        time.sleep(1)

def demo_developer_mode():
    """Demonstrate developer mode activation."""
    print("\n🔓 DEVELOPER MODE DEMONSTRATION")
    print("="*50)
    print("⚠️  WARNING: Enabling experimental features!")
    print("⚠️  Features may cause:")
    print("   • Machine damage or malfunction")
    print("   • Unexpected behavior")
    print("   • Print failures")
    print("   • System instability")
    print()
    print("🚫 FANTOM ASSUMES NO LIABILITY")
    print("👤 Use at your own risk!")
    print()
    
    response = input("Enable developer mode? (y/N): ").lower().strip()
    if response in ['y', 'yes']:
        print("\n🔥 Developer mode ENABLED!")
        print("🚀 Experimental features unlocked:")
        print("   ✓ Non-planar slicing")
        print("   ✓ Advanced AI optimization")
        print("   ✓ Experimental toolpaths")
        print("   ✓ Beta Ghost features")
        return True
    else:
        print("\n🔒 Developer mode disabled - staying safe!")
        return False

def main():
    """Main demo function."""
    print("🚀 Starting FANTOM Demo...")
    print()
    
    # Show disclaimer
    if not demo_disclaimer():
        print("Demo cancelled by user.")
        return
    
    print("\n" + "="*60)
    print("            FANTOM SYSTEM INITIALIZATION")
    print("="*60)
    
    # Initialize components
    print("⚙️  Initializing Ghost Manager...")
    ghost_manager = GhostManager()
    
    print("🛡️  Initializing Error Handler...")
    error_handler = ErrorHandler(ghost_manager)
    
    print("⚙️  Loading configuration...")
    config_manager = ConfigManager()
    
    print("✅ FANTOM systems online!")
    
    # Simulate ghost activity
    print("\n" + "="*60)
    print("            GHOST IN THE MACHINE ACTIVITY")
    print("="*60)
    simulate_ghost_activity()
    
    # Demonstrate error handling
    print("\n" + "="*60)
    print("            AI ERROR HANDLING SYSTEM")
    print("="*60)
    simulate_error_handling()
    
    # Developer mode demo
    print("\n" + "="*60)
    print("            DEVELOPER MODE SYSTEM")
    print("="*60)
    dev_mode = demo_developer_mode()
    
    # Final summary
    print("\n" + "="*60)
    print("            FANTOM DEMO COMPLETE")
    print("="*60)
    print("🎉 FANTOM demonstration finished!")
    print()
    print("Key features demonstrated:")
    print("✓ Ghost in the Machine AI collective")
    print("✓ Error detection and AI-driven fixing")
    print("✓ Safety disclaimers and risk warnings")
    print("✓ Developer mode with experimental features")
    print("✓ FOSS-driven collaborative development")
    print()
    if dev_mode:
        print("⚠️  Remember: Developer mode enabled - use with caution!")
    print("🚫 All usage is at your own risk!")
    print()
    print("🌟 Ready to revolutionize 3D printing with AI! ⚙️")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This is exactly the kind of error the Ghosts would fix! 👻")
