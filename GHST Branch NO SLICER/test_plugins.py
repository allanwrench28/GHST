#!/usr/bin/env python3
"""
Test the FANTOM Plugin System

Tests plugin loading, configuration, and basic functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_plugin_system():
    """Test the plugin system functionality."""
    print("🔌 FANTOM Plugin System Test")
    print("=" * 50)
    
    try:
        from plugins.plugin_manager import PluginManager
        from plugins.base_plugin import BasePlugin, PluginMetadata
        
        print("✅ Plugin system imports successful")
        
        # Test plugin manager initialization
        plugin_manager = PluginManager()
        print(f"✅ Plugin manager initialized")
        
        # Test plugin discovery
        discovered = plugin_manager.discover_plugins()
        print(f"✅ Discovered {len(discovered)} potential plugins")
        
        for plugin_spec in discovered:
            print(f"   📦 {plugin_spec}")
        
        # Test plugin loading
        loaded_count = plugin_manager.load_all_plugins()
        print(f"✅ Loaded {loaded_count} plugins successfully")
        
        # Test plugin status
        status = plugin_manager.get_plugin_status()
        print(f"✅ Plugin status retrieved for {len(status)} plugins")
        
        for name, plugin_status in status.items():
            print(f"   🔌 {name}: {'Enabled' if plugin_status.get('enabled', False) else 'Disabled'}")
            if plugin_status.get('experimental', False):
                print(f"      ⚠️ EXPERIMENTAL")
        
        # Test plugin hooks
        print("\n📞 Testing Plugin Hooks:")
        plugin_manager.call_plugin_hook('on_file_loaded', 'test.stl', {'test': 'data'})
        plugin_manager.call_plugin_hook('on_slicing_started', {'test': 'mesh'}, {'test': 'config'})
        
        # Test G-code processing
        test_gcode = [
            "; Test G-code",
            "G1 X10 Y10 Z0.2",
            "G1 X20 Y10 E1"
        ]
        
        processed_gcode = plugin_manager.process_gcode_through_plugins(test_gcode)
        print(f"✅ G-code processed: {len(test_gcode)} -> {len(processed_gcode)} lines")
        
        plugin_manager.call_plugin_hook('on_slicing_completed', processed_gcode, {'layers': 10})
        
        # Test menu actions
        menu_actions = plugin_manager.get_all_menu_actions()
        print(f"✅ Found {len(menu_actions)} menu actions from plugins")
        
        for action in menu_actions:
            print(f"   📋 {action['name']} (from {action['plugin']})")
        
        # Test cleanup
        plugin_manager.cleanup_all_plugins()
        print("✅ Plugin cleanup completed")
        
        print("\n" + "=" * 50)
        print("🎉 Plugin system test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Plugin system test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_manager_integration():
    """Test ConfigManager integration with plugin system."""
    print("\n🔧 Testing ConfigManager Integration")
    print("=" * 50)
    
    try:
        from utils.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        print("✅ ConfigManager initialized")
        
        # Test plugin manager access
        plugin_manager = config_manager.get_plugin_manager()
        if plugin_manager:
            print("✅ Plugin manager accessible from ConfigManager")
            
            # Test plugin status
            plugins = config_manager.get_available_plugins()
            print(f"✅ Available plugins: {len(plugins)}")
            
            # Test plugin menu actions
            actions = config_manager.get_plugin_menu_actions()
            print(f"✅ Menu actions: {len(actions)}")
            
        else:
            print("⚠️ Plugin manager not available in ConfigManager")
        
        print("✅ ConfigManager integration test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ConfigManager integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all plugin system tests."""
    print("🚀 Starting FANTOM Plugin System Tests")
    print("⚠️ This tests the plugin architecture and built-in plugins")
    print()
    
    success = True
    
    # Test plugin system
    if not test_plugin_system():
        success = False
    
    # Test config manager integration
    if not test_config_manager_integration():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Plugin system is working correctly")
        print("⚠️ Remember: Use plugins at your own risk!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️ Plugin system may have issues")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())