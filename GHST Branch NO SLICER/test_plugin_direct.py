#!/usr/bin/env python3
"""
Simple Plugin Test

Direct test of plugin loading functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_plugin_loading():
    """Test direct plugin loading."""
    print("🔌 Direct Plugin Loading Test")
    print("=" * 40)
    
    try:
        # Import plugin manager
        from plugins.plugin_manager import PluginManager
        
        # Create plugin manager
        manager = PluginManager()
        
        # Test loading a specific plugin
        plugin_spec = f"{src_path}/plugins/builtin:print_stats"
        print(f"Loading plugin: {plugin_spec}")
        
        success = manager.load_plugin(plugin_spec)
        print(f"Load result: {success}")
        
        if success:
            plugins = manager.get_plugin_status()
            for name, status in plugins.items():
                print(f"Plugin: {name}")
                print(f"  Enabled: {status.get('enabled', False)}")
                print(f"  Category: {status.get('category', 'Unknown')}")
                print(f"  Experimental: {status.get('experimental', False)}")
        
        return success
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_plugin_loading()