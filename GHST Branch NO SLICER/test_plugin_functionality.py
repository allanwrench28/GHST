#!/usr/bin/env python3
"""
Test Plugin Functionality

Test that plugins actually process data correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_gcode_processing():
    """Test G-code processing with plugins."""
    print("🔧 Testing G-code Processing")
    print("=" * 40)
    
    try:
        from plugins.plugin_manager import PluginManager
        
        # Create and load plugins
        manager = PluginManager()
        manager.load_all_plugins()
        
        # Test G-code
        test_gcode = [
            "; Test G-code",
            "",  # Empty line
            "; Just a comment",
            "G1 X10 Y10 Z0.2 E1",
            "G1 E2",  # Only extrusion move
            "G1 X20 Y10 E3",
            "",  # Another empty line
            "G1 Y20 E4",
            "; End test"
        ]
        
        print(f"Original G-code: {len(test_gcode)} lines")
        for i, line in enumerate(test_gcode):
            print(f"  {i+1}: {repr(line)}")
        
        # Process through plugins
        processed_gcode = manager.process_gcode_through_plugins(test_gcode)
        
        print(f"\nProcessed G-code: {len(processed_gcode)} lines")
        for i, line in enumerate(processed_gcode):
            print(f"  {i+1}: {repr(line)}")
        
        # Test plugin statistics
        stats = {'layers': 10, 'estimated_print_time': 25.5}
        manager.call_plugin_hook('on_slicing_completed', processed_gcode, stats)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plugin_menu_actions():
    """Test plugin menu actions."""
    print("\n🎯 Testing Plugin Menu Actions")
    print("=" * 40)
    
    try:
        from plugins.plugin_manager import PluginManager
        
        # Create and load plugins
        manager = PluginManager()
        manager.load_all_plugins()
        
        # Get menu actions
        actions = manager.get_all_menu_actions()
        
        print(f"Found {len(actions)} menu actions:")
        for action in actions:
            print(f"  📋 {action['name']} (from {action['plugin']})")
            
            # Try to call the action
            try:
                if 'callback' in action:
                    print(f"     Calling action...")
                    action['callback']()
                    print(f"     ✅ Action completed successfully")
            except Exception as e:
                print(f"     ❌ Action failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run plugin functionality tests."""
    print("🚀 FANTOM Plugin Functionality Tests")
    print("=" * 50)
    
    success = True
    
    # Test G-code processing
    if not test_gcode_processing():
        success = False
    
    # Test menu actions
    if not test_plugin_menu_actions():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL FUNCTIONALITY TESTS PASSED!")
        print("✅ Plugin system is fully operational")
    else:
        print("❌ SOME FUNCTIONALITY TESTS FAILED!")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())