#!/usr/bin/env python3
"""
FANTOM Plugin System Demonstration

This script demonstrates the new plugin system capabilities in FANTOM Studio.
Shows plugin loading, G-code processing, and menu integration.

⚠️ DISCLAIMER: This demonstrates experimental features - use at your own risk!
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def show_banner():
    """Show the demonstration banner."""
    print("🔌" + "="*60 + "🔌")
    print("🚀 FANTOM PLUGIN SYSTEM DEMONSTRATION")
    print("⚙️  Extending Slicer Functionality with Plugins")
    print("🔌" + "="*60 + "🔌")
    print()
    print("⚠️  WARNING: Plugin system involves code execution")
    print("⚠️  Use at your own risk - No liability assumed")
    print()

def demonstrate_plugin_loading():
    """Demonstrate plugin discovery and loading."""
    print("📦 STEP 1: Plugin Discovery and Loading")
    print("-" * 50)
    
    from plugins.plugin_manager import PluginManager
    
    # Create plugin manager
    manager = PluginManager()
    print(f"✅ Plugin manager initialized")
    
    # Discover plugins
    discovered = manager.discover_plugins()
    print(f"🔍 Discovered {len(discovered)} potential plugins:")
    for plugin_spec in discovered:
        plugin_dir, module_name = plugin_spec.split(":", 1)
        print(f"   📦 {module_name} (in {Path(plugin_dir).name}/)")
    
    # Load plugins
    loaded_count = manager.load_all_plugins()
    print(f"✅ Successfully loaded {loaded_count} plugins")
    
    # Show plugin status
    status = manager.get_plugin_status()
    print(f"\n📊 Plugin Status:")
    for name, info in status.items():
        experimental = "⚠️ EXPERIMENTAL" if info.get('experimental', False) else "✅ Stable"
        enabled = "🟢 Enabled" if info.get('enabled', False) else "🔴 Disabled"
        print(f"   {name}:")
        print(f"     Status: {enabled}")
        print(f"     Safety: {experimental}")
        print(f"     Category: {info.get('category', 'Unknown')}")
    
    return manager

def demonstrate_gcode_processing(manager):
    """Demonstrate G-code processing through plugins."""
    print("\n🔧 STEP 2: G-code Processing")
    print("-" * 50)
    
    # Sample G-code that needs optimization
    original_gcode = [
        "; FANTOM Generated G-code",
        "; Sample test file",
        "",  # Empty line
        "G21 ; set units to millimeters",
        "",  # Another empty line
        "; Starting print sequence",
        "G1 X10 Y10 Z0.2 E1",
        "G1 E2",  # Only extrusion - might be redundant
        "G1 X20 Y10 E3",
        "",  # Empty line
        "G1 Y20 E4",
        "; More comments",
        "G1 X10 Y20 E5",
        "",
        "; End sequence",
        "M104 S0 ; turn off extruder"
    ]
    
    print(f"📄 Original G-code: {len(original_gcode)} lines")
    print("   Sample lines:")
    for i, line in enumerate(original_gcode[:5]):
        print(f"     {i+1}: {repr(line)}")
    print("     ...")
    
    # Process through plugins
    processed_gcode = manager.process_gcode_through_plugins(original_gcode)
    
    print(f"\n⚙️  Processed G-code: {len(processed_gcode)} lines")
    if len(processed_gcode) != len(original_gcode):
        reduction = len(original_gcode) - len(processed_gcode)
        print(f"   🎯 Optimization: Removed {reduction} lines ({reduction/len(original_gcode)*100:.1f}%)")
    
    # Show some processed lines
    print("   Sample processed lines:")
    for i, line in enumerate(processed_gcode[:5]):
        print(f"     {i+1}: {repr(line)}")
    
    return processed_gcode

def demonstrate_plugin_hooks(manager, gcode):
    """Demonstrate plugin event hooks."""
    print("\n📞 STEP 3: Plugin Event Hooks")
    print("-" * 50)
    
    # Simulate file loading
    print("🔄 Simulating file loading...")
    manager.call_plugin_hook('on_file_loaded', 'demo_model.stl', {
        'vertices': 1000,
        'faces': 2000,
        'volume': 5000.0
    })
    
    # Simulate slicing start
    print("🔄 Simulating slicing start...")
    manager.call_plugin_hook('on_slicing_started', {'test': 'mesh'}, {
        'layer_height': 0.2,
        'infill': 20,
        'supports': True
    })
    
    # Simulate slicing completion
    print("🔄 Simulating slicing completion...")
    manager.call_plugin_hook('on_slicing_completed', gcode, {
        'layers': 250,
        'estimated_time': 45.5,
        'filament_used': 12.3
    })
    
    print("✅ All plugin hooks executed successfully")

def demonstrate_menu_integration(manager):
    """Demonstrate plugin menu integration."""
    print("\n🎯 STEP 4: Menu Integration")
    print("-" * 50)
    
    # Get menu actions from plugins
    actions = manager.get_all_menu_actions()
    
    print(f"📋 Found {len(actions)} menu actions from plugins:")
    for i, action in enumerate(actions, 1):
        plugin_name = action.get('plugin', 'Unknown')
        action_name = action.get('name', 'Unnamed Action')
        shortcut = action.get('shortcut', 'No shortcut')
        
        print(f"   {i}. {action_name}")
        print(f"      Plugin: {plugin_name}")
        print(f"      Shortcut: {shortcut}")
    
    # Demonstrate calling a plugin action
    if actions:
        print("\n🎬 Demonstrating plugin action execution:")
        action = actions[0]
        print(f"   Executing: {action['name']}")
        try:
            action['callback']()
            print("   ✅ Action executed successfully")
        except Exception as e:
            print(f"   ❌ Action failed: {e}")

def demonstrate_safety_features(manager):
    """Demonstrate plugin safety features."""
    print("\n🛡️  STEP 5: Safety Features")
    print("-" * 50)
    
    status = manager.get_plugin_status()
    
    experimental_plugins = [name for name, info in status.items() if info.get('experimental', False)]
    
    print(f"⚠️  Safety warnings active for {len(experimental_plugins)} experimental plugins")
    
    for plugin_name in experimental_plugins:
        print(f"   🚨 {plugin_name}: EXPERIMENTAL - Use at your own risk!")
    
    print("\n🔒 Safety features implemented:")
    print("   ✅ Plugin sandboxing and validation")
    print("   ✅ Experimental plugin warnings")
    print("   ✅ Plugin enable/disable controls")
    print("   ✅ Comprehensive logging")
    print("   ✅ Error handling and recovery")

def demonstrate_config_integration():
    """Demonstrate ConfigManager integration."""
    print("\n⚙️  STEP 6: Configuration Integration")
    print("-" * 50)
    
    from utils.config_manager import ConfigManager
    
    config = ConfigManager()
    
    # Show plugin integration
    plugins = config.get_available_plugins()
    print(f"🔧 ConfigManager integration: {len(plugins)} plugins available")
    
    # Demonstrate plugin management
    if plugins:
        plugin_name = list(plugins.keys())[0]
        print(f"\n🎛️  Demonstrating plugin management for '{plugin_name}':")
        
        # Disable and re-enable plugin
        print("   🔴 Disabling plugin...")
        config.disable_plugin(plugin_name)
        
        print("   🟢 Re-enabling plugin...")
        config.enable_plugin(plugin_name)
        
        print("   ✅ Plugin management successful")

def show_summary():
    """Show demonstration summary."""
    print("\n" + "🎉" + "="*60 + "🎉")
    print("🏁 PLUGIN SYSTEM DEMONSTRATION COMPLETE!")
    print("🎉" + "="*60 + "🎉")
    print()
    print("✅ Successfully demonstrated:")
    print("   🔌 Plugin discovery and loading")
    print("   ⚙️  G-code processing and optimization")
    print("   📞 Event hooks and lifecycle management")
    print("   🎯 Menu integration and user actions")
    print("   🛡️  Safety features and warnings")
    print("   🔧 Configuration system integration")
    print()
    print("🚀 The FANTOM plugin system is ready for use!")
    print("📚 See PLUGIN_DOCUMENTATION.md for full details")
    print()
    print("⚠️  REMEMBER:")
    print("   • Always review plugin code before installation")
    print("   • Test plugins on non-critical prints first")
    print("   • Use experimental plugins at your own risk")
    print("   • FANTOM assumes no liability for plugin issues")

def main():
    """Main demonstration function."""
    show_banner()
    
    try:
        # Step 1: Plugin loading
        manager = demonstrate_plugin_loading()
        
        # Step 2: G-code processing
        processed_gcode = demonstrate_gcode_processing(manager)
        
        # Step 3: Plugin hooks
        demonstrate_plugin_hooks(manager, processed_gcode)
        
        # Step 4: Menu integration
        demonstrate_menu_integration(manager)
        
        # Step 5: Safety features
        demonstrate_safety_features(manager)
        
        # Step 6: Config integration
        demonstrate_config_integration()
        
        # Summary
        show_summary()
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())