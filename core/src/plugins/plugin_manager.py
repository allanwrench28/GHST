"""
Plugin Manager for GHST

Manages plugin discovery, loading, and lifecycle.
Modeled after the GHST Agent Manager architecture.

⚠️ DISCLAIMER: Plugin loading involves code execution - use at your own risk!
"""

import importlib
import importlib.util
import inspect
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_plugin import BasePlugin, PluginMetadata


class PluginManager:
    """Manages GHST plugins and their lifecycle."""

    def __init__(self, plugin_dirs: List[str] = None):
        """Initialize plugin manager.

        Args:
            plugin_dirs: List of directories to search for plugins
        """
        self.loaded_plugins: Dict[str, BasePlugin] = {}
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}
        self.plugin_enabled: Dict[str, bool] = {}

        # Setup logging
        self.logger = logging.getLogger('PluginManager')
        self.logger.setLevel(logging.DEBUG)

        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Default plugin directories
        if plugin_dirs is None:
            plugin_dirs = [
                str(Path(__file__).parent / "builtin"),
                str(Path(__file__).parent.parent.parent /
                    "plugins"),  # User plugins
                str(Path.home() / ".fantom" / "plugins")  # System plugins
            ]

        self.plugin_dirs = plugin_dirs

        # Create plugin directories if they don't exist
        for plugin_dir in self.plugin_dirs:
            Path(plugin_dir).mkdir(parents=True, exist_ok=True)

        self.logger.info("Plugin Manager initialized")
        self.logger.warning(
            "⚠️ Plugin system active - plugins run with system access!")

    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directories.

        Returns:
            List of plugin module names
        """
        discovered = []

        for plugin_dir in self.plugin_dirs:
            plugin_path = Path(plugin_dir)
            if not plugin_path.exists():
                continue

            # Look for Python files that might be plugins
            for py_file in plugin_path.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue  # Skip private modules

                module_name = py_file.stem
                discovered.append("{plugin_dir}:{module_name}")

            # Look for plugin packages
            for pkg_dir in plugin_path.iterdir():
                if pkg_dir.is_dir() and (pkg_dir / "__init__.py").exists():
                    discovered.append("{plugin_dir}:{pkg_dir.name}")

        self.logger.info("Discovered {len(discovered)} potential plugins")
        return discovered

    def load_plugin(self, plugin_spec: str) -> bool:
        """Load a specific plugin.

        Args:
            plugin_spec: Plugin specification in format "path:module_name"

        Returns:
            True if loaded successfully
        """
        try:
            plugin_dir, module_name = plugin_spec.split(":", 1)

            # Add plugin directory to Python path temporarily
            if plugin_dir not in sys.path:
                sys.path.insert(0, plugin_dir)

            # Also add the parent plugins directory so base_plugin can be
            # imported
            plugins_dir = str(Path(plugin_dir).parent)
            if plugins_dir not in sys.path:
                sys.path.insert(0, plugins_dir)

            try:
                # Import the module using standard importlib
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    os.path.join(plugin_dir, "{module_name}.py")
                )
                if spec is None:
                    self.logger.error("Could not load spec for {module_name}")
                    return False

                module = importlib.util.module_from_spec(spec)

                # Set up the module's globals to use our BasePlugin
                module.__dict__['BasePlugin'] = BasePlugin
                module.__dict__['PluginMetadata'] = PluginMetadata

                spec.loader.exec_module(module)

                # Find plugin classes - look for classes that inherit from our
                # BasePlugin
                plugin_classes = []
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if this is a plugin class
                    if (name.endswith('Plugin') and
                        name != 'BasePlugin' and
                            hasattr(obj, '__bases__')):

                        # Check if any of the base classes are our BasePlugin
                        for base in obj.__bases__:
                            if base is BasePlugin or (
                                hasattr(
                                    base,
                                    '__name__') and base.__name__ == 'BasePlugin'):
                                plugin_classes.append(obj)
                                break

                if not plugin_classes:
                    self.logger.warning(
                        "No plugin classes found in {module_name}")
                    return False

                # Load the first plugin class found
                plugin_class = plugin_classes[0]

                # Try to fix the inheritance by updating the base class
                if BasePlugin not in plugin_class.__bases__:
                    self.logger.debug(
                        f"Fixing inheritance for {plugin_class.__name__}")
                    # Create a new class with the correct base
                    new_class = type(
                        plugin_class.__name__, (BasePlugin,), dict(
                            plugin_class.__dict__))
                    plugin_class = new_class

                plugin_instance = plugin_class(plugin_manager=self)

                # Check compatibility
                if not plugin_instance.is_compatible():
                    self.logger.warning(
                        f"Plugin {plugin_instance.metadata.name} is not compatible")
                    return False

                # Initialize the plugin
                if plugin_instance.initialize():
                    self.loaded_plugins[plugin_instance.metadata.name] = plugin_instance
                    self.plugin_enabled[plugin_instance.metadata.name] = True

                    self.logger.info(
                        f"✅ Loaded plugin: {plugin_instance.metadata.name} v{plugin_instance.metadata.version}")

                    # Show safety warning for experimental plugins
                    if plugin_instance.metadata.experimental:
                        self.logger.warning(
                            f"⚠️ EXPERIMENTAL plugin loaded: {plugin_instance.metadata.name}")

                    return True
                else:
                    self.logger.error(
                        f"Failed to initialize plugin: {plugin_instance.metadata.name}")
                    return False

            finally:
                # Clean up paths
                if plugin_dir in sys.path:
                    sys.path.remove(plugin_dir)
                if plugins_dir in sys.path and plugins_dir != plugin_dir:
                    sys.path.remove(plugins_dir)

        except Exception as e:
            self.logger.error("Failed to load plugin {plugin_spec}: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False

    def load_all_plugins(self) -> int:
        """Load all discovered plugins.

        Returns:
            Number of plugins loaded successfully
        """
        discovered = self.discover_plugins()
        loaded_count = 0

        for plugin_spec in discovered:
            if self.load_plugin(plugin_spec):
                loaded_count += 1

        self.logger.info("Loaded {loaded_count}/{len(discovered)} plugins")
        return loaded_count

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            True if unloaded successfully
        """
        if plugin_name not in self.loaded_plugins:
            self.logger.warning("Plugin {plugin_name} is not loaded")
            return False

        try:
            plugin = self.loaded_plugins[plugin_name]
            plugin.cleanup()

            del self.loaded_plugins[plugin_name]
            del self.plugin_enabled[plugin_name]

            self.logger.info("Unloaded plugin: {plugin_name}")
            return True

        except Exception as e:
            self.logger.error("Failed to unload plugin {plugin_name}: {e}")
            return False

    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a loaded plugin."""
        if plugin_name not in self.loaded_plugins:
            return False

        self.plugin_enabled[plugin_name] = True
        self.loaded_plugins[plugin_name].active = True
        self.logger.info("Enabled plugin: {plugin_name}")
        return True

    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a loaded plugin."""
        if plugin_name not in self.loaded_plugins:
            return False

        self.plugin_enabled[plugin_name] = False
        self.loaded_plugins[plugin_name].active = False
        self.logger.info("Disabled plugin: {plugin_name}")
        return True

    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get a loaded plugin by name."""
        return self.loaded_plugins.get(plugin_name)

    def get_enabled_plugins(self) -> List[BasePlugin]:
        """Get all enabled plugins."""
        return [
            plugin for name, plugin in self.loaded_plugins.items()
            if self.plugin_enabled.get(name, False)
        ]

    def get_plugins_by_category(self, category: str) -> List[BasePlugin]:
        """Get all enabled plugins in a specific category."""
        return [
            plugin for plugin in self.get_enabled_plugins()
            if plugin.metadata.category == category
        ]

    def get_plugin_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all loaded plugins."""
        status = {}
        for name, plugin in self.loaded_plugins.items():
            status[name] = {
                **plugin.get_status(),
                'enabled': self.plugin_enabled.get(name, False)
            }
        return status

    def call_plugin_hook(self, hook_name: str, *args, **kwargs):
        """Call a specific hook on all enabled plugins.

        Args:
            hook_name: Name of the method to call
            *args, **kwargs: Arguments to pass to the hook
        """
        for plugin in self.get_enabled_plugins():
            try:
                if hasattr(plugin, hook_name):
                    method = getattr(plugin, hook_name)
                    method(*args, **kwargs)
            except Exception as e:
                self.logger.error(
                    f"Error calling {hook_name} on plugin {plugin.metadata.name}: {e}")

    def process_mesh_through_plugins(self, mesh_data: Any) -> Any:
        """Process mesh data through all enabled coding engine plugins."""
        for plugin in self.get_plugins_by_category("coding engine"):
            try:
                mesh_data = plugin.process_mesh(mesh_data) or mesh_data
            except Exception as e:
                self.logger.error(
                    f"Error processing mesh with plugin {plugin.metadata.name}: {e}")
        return mesh_data

    def process_gcode_through_plugins(
            self, gcode_lines: List[str]) -> List[str]:
        """Process G-code through all enabled coding engine plugins."""
        for plugin in self.get_plugins_by_category("coding engine"):
            try:
                gcode_lines = plugin.process_gcode(gcode_lines)
            except Exception as e:
                self.logger.error(
                    "Error processing G-code with plugin {plugin.metadata.name}: {e}")
        return gcode_lines

    def get_all_menu_actions(self) -> List[Dict[str, Any]]:
        """Get menu actions from all enabled plugins."""
        actions = []
        for plugin in self.get_enabled_plugins():
            try:
                plugin_actions = plugin.get_menu_actions()
                for action in plugin_actions:
                    action['plugin'] = plugin.metadata.name
                    actions.append(action)
            except Exception as e:
                self.logger.error(
                    f"Error getting menu actions from plugin {plugin.metadata.name}: {e}")
        return actions

    def cleanup_all_plugins(self):
        """Cleanup all loaded plugins."""
        for plugin_name in list(self.loaded_plugins.keys()):
            self.unload_plugin(plugin_name)

        self.logger.info("All plugins cleaned up")
