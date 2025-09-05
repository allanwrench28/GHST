#!/usr/bin/env python3
"""
FANTOM Studio Migration Validation Script

Validates that the migration from The_Machine was successful and
that all non-slicer functionality is operational.
"""

import sys
import os
from pathlib import Path

def validate_migration():
    """Validate the migration was successful."""
    print("🔍 FANTOM Studio Migration Validation")
    print("=" * 50)
    
    # Check core directories
    core_dirs = [
        "src/ai_collaboration",
        "src/plugins", 
        "src/ui_components",
        "src/ui_themes",
        "src/utils",
        "config",
        "docs", 
        "scripts",
        "Clockwork"
    ]
    
    print("\n📁 Checking directory structure...")
    for dir_path in core_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - MISSING")
            return False
    
    # Check key files
    key_files = [
        "demo.py",
        "demo_plugin_system.py", 
        "demo_nightly_automation.py",
        "fantom.py",
        "launcher.py",
        "setup.py",
        "requirements.txt",
        "pyproject.toml"
    ]
    
    print("\n📄 Checking key files...")
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            return False
    
    # Check that slicer files are excluded
    excluded_files = [
        "demo_slicer.py",
        "test_slicer.py",
        "src/slicer_ui"
    ]
    
    print("\n🚫 Checking slicer exclusions...")
    for file_path in excluded_files:
        if not Path(file_path).exists():
            print(f"✅ {file_path} - CORRECTLY EXCLUDED")
        else:
            print(f"❌ {file_path} - SHOULD BE EXCLUDED")
            return False
    
    # Test imports
    print("\n🔌 Testing imports...")
    
    try:
        sys.path.insert(0, str(Path("src")))
        
        from utils.config_manager import ConfigManager
        print("✅ Config Manager")
        
        from ai_collaboration.error_handler import ErrorHandler  
        print("✅ Error Handler")
        
        from plugins.plugin_manager import PluginManager
        print("✅ Plugin Manager")
        
        import demo_plugin_system
        print("✅ Plugin System Demo")
        
        print("✅ All imports successful!")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    print("\n🎉 Migration validation PASSED!")
    print("🏭 FANTOM Studio is ready for development!")
    print("👻 Ghosts in the Machine are operational!")
    
    return True

if __name__ == "__main__":
    if validate_migration():
        print("\n🚀 Run 'python demo.py' to get started!")
        sys.exit(0)
    else:
        print("\n❌ Migration validation FAILED!")
        sys.exit(1)