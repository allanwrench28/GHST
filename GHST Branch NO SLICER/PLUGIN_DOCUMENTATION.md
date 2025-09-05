# FANTOM Plugin System Documentation

## Overview

FANTOM Studio now includes a comprehensive plugin system that allows users to extend the slicer's functionality with custom plugins and extensions. The plugin architecture is modeled after the existing Ghost system for consistency and ease of use.

## ⚠️ Safety Warning

**IMPORTANT**: Plugins run with system access and can execute arbitrary code. Always review plugin code before installation and use plugins at your own risk. FANTOM assumes no liability for plugin-related issues.

## Plugin Architecture

### Base Plugin Interface

All plugins must inherit from `BasePlugin` and implement the required methods:

```python
from plugins.base_plugin import BasePlugin, PluginMetadata

class MyPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="My Plugin",
            version="1.0.0",
            author="Your Name",
            description="Description of what the plugin does",
            category="slicer",  # or "ui", "analysis", "export", "import", "utility"
            experimental=False,
            safety_notes=["Any safety warnings"]
        )
    
    def initialize(self) -> bool:
        # Plugin initialization code
        return True
    
    def cleanup(self) -> bool:
        # Plugin cleanup code
        return True
```

### Plugin Categories

- **slicer**: Plugins that modify slicing behavior or G-code
- **ui**: Plugins that add UI elements or modify the interface
- **analysis**: Plugins that analyze models or G-code
- **export**: Plugins that provide additional export formats
- **import**: Plugins that provide additional import formats
- **utility**: General utility plugins

### Plugin Hooks

Plugins can respond to various events in the slicing process:

- `on_file_loaded(file_path, mesh_data)`: Called when a file is loaded
- `on_slicing_started(mesh_data, config)`: Called when slicing begins
- `on_slicing_completed(gcode_lines, stats)`: Called when slicing completes
- `process_mesh(mesh_data)`: Process/modify mesh data
- `process_gcode(gcode_lines)`: Process/modify G-code
- `get_menu_actions()`: Provide menu items
- `get_toolbar_actions()`: Provide toolbar buttons

## Built-in Plugins

### Print Statistics Plugin
- **Category**: analysis
- **Description**: Calculates detailed print statistics including time, material usage, and cost estimates
- **Features**:
  - Estimates print time and material usage
  - Calculates material costs
  - Provides detailed statistics dialog

### G-code Optimizer Plugin (EXPERIMENTAL)
- **Category**: slicer
- **Description**: Optimizes G-code for better print quality and reduced print time
- **Features**:
  - Removes empty lines and unnecessary comments
  - Eliminates redundant moves
  - Adds optimization metadata
- **Warning**: This is experimental and may affect print quality

## Plugin Installation

### Built-in Plugin Directory
Built-in plugins are located in: `src/plugins/builtin/`

### User Plugin Directories
User plugins can be placed in:
- `plugins/` (project directory)
- `~/.fantom/plugins/` (user home directory)

### Plugin File Structure
Each plugin should be a Python file (.py) containing a class that inherits from `BasePlugin`.

Example plugin file (`my_plugin.py`):
```python
from plugins.base_plugin import BasePlugin, PluginMetadata

class MyCustomPlugin(BasePlugin):
    def get_metadata(self):
        return PluginMetadata(
            name="My Custom Plugin",
            version="1.0.0",
            author="Your Name",
            description="Custom functionality",
            category="utility"
        )
    
    def initialize(self):
        self.logger.info("My custom plugin initialized")
        return True
    
    def cleanup(self):
        self.logger.info("My custom plugin cleaned up")
        return True
```

## Using Plugins

### Via GUI
1. Open FANTOM Studio
2. Go to **Plugins** menu
3. Click **Plugin Manager** to see available plugins
4. Use **Refresh** to reload plugins after installation

### Plugin Status Display
The main interface shows plugin status in the "Plugin System" card:
- Number of enabled/total plugins
- Plugin management buttons
- Quick refresh functionality

### Via Configuration
Plugins can be enabled/disabled through the ConfigManager:
```python
config_manager.enable_plugin("Plugin Name")
config_manager.disable_plugin("Plugin Name")
```

## Creating Custom Plugins

### Step 1: Create Plugin File
Create a new `.py` file in one of the plugin directories.

### Step 2: Implement BasePlugin
```python
from plugins.base_plugin import BasePlugin, PluginMetadata
from typing import Dict, Any, List

class MySlicerPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="My Slicer Plugin",
            version="1.0.0",
            author="Your Name",
            description="Custom slicer functionality",
            category="slicer",
            experimental=True,
            safety_notes=[
                "This plugin modifies G-code",
                "Test thoroughly before use"
            ]
        )
    
    def initialize(self) -> bool:
        self.logger.info("My slicer plugin initialized")
        return True
    
    def cleanup(self) -> bool:
        return True
    
    def process_gcode(self, gcode_lines: List[str]) -> List[str]:
        # Custom G-code processing
        processed = []
        for line in gcode_lines:
            # Your custom logic here
            processed.append(line)
        return processed
    
    def get_menu_actions(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': 'My Custom Action',
                'callback': self.my_action,
                'shortcut': 'Ctrl+Alt+M'
            }
        ]
    
    def my_action(self):
        print("Custom action executed!")
```

### Step 3: Refresh Plugins
Use the "Refresh" button in the Plugin System card or restart FANTOM.

## Plugin Configuration

Plugins can store and retrieve configuration:
```python
def initialize(self):
    # Set default config
    self.set_config({
        'enabled': True,
        'setting1': 'value1'
    })
    return True

def get_current_setting(self):
    config = self.get_config()
    return config.get('setting1', 'default')
```

## Security Considerations

### Plugin Safety
- Always review plugin source code before installation
- Only install plugins from trusted sources
- Be especially careful with experimental plugins
- Plugins marked as experimental include additional safety warnings

### Permissions
- Plugins run with the same permissions as FANTOM
- Plugins can access the file system and network
- Plugins can modify G-code and affect print output

### Best Practices
- Test plugins on non-critical prints first
- Keep backups of important G-code files
- Monitor plugin behavior during operation
- Remove unused plugins to reduce attack surface

## Troubleshooting

### Plugin Not Loading
1. Check that the plugin file is in a valid plugin directory
2. Verify the plugin inherits from `BasePlugin`
3. Check the FANTOM logs for error messages
4. Ensure the plugin's `initialize()` method returns `True`

### Plugin Errors
1. Check the console output for error messages
2. Verify plugin dependencies are installed
3. Check that plugin methods are properly implemented
4. Use the Plugin Manager to see plugin status

### Performance Issues
1. Disable experimental plugins if experiencing slowdowns
2. Check plugin G-code processing efficiency
3. Monitor memory usage with complex plugins
4. Consider plugin initialization time

## API Reference

### BasePlugin Methods
- `get_metadata()`: Returns plugin metadata
- `initialize()`: Initialize the plugin
- `cleanup()`: Clean up plugin resources
- `is_compatible()`: Check plugin compatibility
- `get_config()` / `set_config()`: Plugin configuration
- `validate_config()`: Validate configuration
- `get_status()`: Get plugin status

### Plugin Hooks
- `on_file_loaded(file_path, mesh_data)`
- `on_slicing_started(mesh_data, config)`
- `on_slicing_completed(gcode_lines, stats)`
- `process_mesh(mesh_data)`
- `process_gcode(gcode_lines)`

### UI Integration
- `get_menu_actions()`: Add menu items
- `get_toolbar_actions()`: Add toolbar buttons

## Examples

See the built-in plugins in `src/plugins/builtin/` for working examples:
- `print_stats.py`: Analysis plugin example
- `gcode_optimizer.py`: Slicer plugin example

## Support

For plugin development support:
- Check the FANTOM GitHub repository
- Review built-in plugin source code
- Join the FANTOM community discussions

Remember: Use plugins at your own risk and always verify G-code before printing!