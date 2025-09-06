"""
GHST Plugin System

This module provides the plugin architecture for GHST Studio, enabling
users to extend functionality through custom plugins and extensions.

⚠️ DISCLAIMER: Plugins run with system access - use at your own risk!
"""

from .base_plugin import BasePlugin
from .plugin_manager import PluginManager

__all__ = ['PluginManager', 'BasePlugin']
