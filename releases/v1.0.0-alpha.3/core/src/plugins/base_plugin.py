"""
Base Plugin Interface for GHST

Defines the core interface that all GHST plugins must implement.
Modeled after the GHST Agent system architecture for consistency.

⚠️ DISCLAIMER: Plugin execution involves system access - use at your own risk!
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from dataclasses import dataclass

@dataclass
class PluginMetadata:
    """Plugin metadata structure."""
    name: str
    version: str
    author: str
    description: str
    category: str  # "coding engine", "ui", "analysis", "export", "import", "utility"
    requires_gui: bool = False
    experimental: bool = False
    safety_notes: List[str] = None

    def __post_init__(self):
        if self.safety_notes is None:
            self.safety_notes = []

class BasePlugin(ABC):
    """Base class for all GHST plugins."""

    def __init__(self, plugin_manager=None):
        """Initialize plugin with reference to plugin manager."""
        self.plugin_manager = plugin_manager
        self.active = False
        self.logger = logging.getLogger(f'Plugin.{self.__class__.__name__}')
        self._config = {}

        # Initialize metadata
        self.metadata = self.get_metadata()

        # Safety check for experimental plugins
        if self.metadata.experimental:
            self.logger.warning(
                f"⚠️ EXPERIMENTAL plugin '{self.metadata.name}' loaded - Use at your own risk!")

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin. Return True if successful."""

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up plugin resources. Return True if successful."""

    def is_compatible(self) -> bool:
        """Check if plugin is compatible with current system."""
        # Default implementation - can be overridden
        return True

    def get_config(self) -> Dict[str, Any]:
        """Get plugin configuration."""
        return self._config.copy()

    def set_config(self, config: Dict[str, Any]) -> bool:
        """Set plugin configuration. Return True if valid."""
        try:
            # Validate configuration if needed
            if self.validate_config(config):
                self._config.update(config)
                return True
            return False
        except Exception as e:
            self.logger.error("Failed to set config: {e}")
            return False

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration. Override in subclasses."""
        return True

    def get_menu_actions(self) -> List[Dict[str, Any]]:
        """Return list of menu actions this plugin provides.

        Returns:
            List of dictionaries with keys: 'name', 'callback', 'shortcut' (optional)
        """
        return []

    def get_toolbar_actions(self) -> List[Dict[str, Any]]:
        """Return list of toolbar actions this plugin provides.

        Returns:
            List of dictionaries with keys: 'name', 'icon', 'callback', 'tooltip' (optional)
        """
        return []

    def process_mesh(self, mesh_data: Any) -> Optional[Any]:
        """Process mesh data. Override if plugin modifies meshes."""
        return mesh_data

    def process_gcode(self, gcode_lines: List[str]) -> List[str]:
        """Process G-code. Override if plugin modifies G-code."""
        return gcode_lines

    def on_slicing_started(self, mesh_data: Any, config: Dict[str, Any]):
        """Called when slicing starts."""

    def on_slicing_completed(
            self, gcode_lines: List[str], stats: Dict[str, Any]):
        """Called when slicing completes."""

    def on_file_loaded(self, file_path: str, mesh_data: Any):
        """Called when a file is loaded."""

    def get_status(self) -> Dict[str, Any]:
        """Get plugin status information."""
        return {
            'name': self.metadata.name,
            'active': self.active,
            'experimental': self.metadata.experimental,
            'category': self.metadata.category
        }
