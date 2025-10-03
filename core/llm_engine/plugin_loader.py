"""
Plugin Loader for GHST Expertise Branches

Dynamically loads and manages expertise branch plugins. Each branch
provides specialized domain knowledge and expert ghosts.
"""

import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any


class PluginLoader:
    """Dynamic loader for expertise branch plugins."""
    
    def __init__(self, plugin_cache_path: Optional[Path] = None):
        """Initialize plugin loader.
        
        Args:
            plugin_cache_path: Path to cached expertise plugins
        """
        self.plugin_cache_path = plugin_cache_path or Path("data/plugin_cache")
        self.plugin_cache_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.loaded_plugins = {}
        
        self.logger.info("🔌 Plugin Loader initialized")
        
    def discover_available_plugins(self) -> List[str]:
        """Discover available expertise branch plugins.
        
        Returns:
            List of available plugin names
        """
        # TODO: Scan repository branches for expertise plugins
        available = []
        
        # Check cache directory
        for plugin_dir in self.plugin_cache_path.iterdir():
            if plugin_dir.is_dir() and (plugin_dir / "manifest.yaml").exists():
                available.append(plugin_dir.name)
                
        self.logger.info(f"Discovered {len(available)} plugins")
        return available
        
    def load_plugin(self, plugin_name: str, 
                   plugin_path: Optional[Path] = None) -> bool:
        """Load an expertise branch plugin.
        
        Args:
            plugin_name: Name of the plugin to load
            plugin_path: Optional path to plugin (uses cache if not provided)
            
        Returns:
            True if loaded successfully
        """
        if plugin_name in self.loaded_plugins:
            self.logger.warning(f"Plugin already loaded: {plugin_name}")
            return True
            
        if plugin_path is None:
            plugin_path = self.plugin_cache_path / plugin_name
            
        if not plugin_path.exists():
            self.logger.error(f"Plugin path not found: {plugin_path}")
            return False
            
        try:
            # Load plugin manifest
            manifest = self._load_manifest(plugin_path)
            if not manifest:
                return False
                
            # Load expert ghosts
            experts = self._load_expert_ghosts(plugin_path)
            
            # Load knowledge fragments
            knowledge = self._load_knowledge_fragments(plugin_path)
            
            self.loaded_plugins[plugin_name] = {
                "manifest": manifest,
                "experts": experts,
                "knowledge": knowledge,
                "path": plugin_path
            }
            
            self.logger.info(f"✅ Loaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
            
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload an expertise branch plugin.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if unloaded successfully
        """
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        return False
        
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a loaded plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin info dictionary or None
        """
        return self.loaded_plugins.get(plugin_name)
        
    def list_loaded_plugins(self) -> List[str]:
        """Get list of currently loaded plugins.
        
        Returns:
            List of loaded plugin names
        """
        return list(self.loaded_plugins.keys())
        
    def _load_manifest(self, plugin_path: Path) -> Optional[Dict[str, Any]]:
        """Load plugin manifest file.
        
        Args:
            plugin_path: Path to plugin directory
            
        Returns:
            Manifest dictionary or None
        """
        manifest_file = plugin_path / "manifest.yaml"
        if manifest_file.exists():
            try:
                import yaml
                with open(manifest_file, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                self.logger.error(f"Failed to load manifest: {e}")
        return None
        
    def _load_expert_ghosts(self, plugin_path: Path) -> List[str]:
        """Load expert ghost modules from plugin.
        
        Args:
            plugin_path: Path to plugin directory
            
        Returns:
            List of loaded expert ghost names
        """
        # TODO: Implement ghost module loading
        experts_path = plugin_path / "expertise" / "expert_ghosts"
        experts = []
        
        if experts_path.exists():
            for ghost_file in experts_path.glob("*.py"):
                if not ghost_file.name.startswith("_"):
                    experts.append(ghost_file.stem)
                    
        return experts
        
    def _load_knowledge_fragments(self, plugin_path: Path) -> Dict[str, int]:
        """Load knowledge fragments from plugin.
        
        Args:
            plugin_path: Path to plugin directory
            
        Returns:
            Dictionary with fragment category counts
        """
        # TODO: Implement knowledge fragment loading
        knowledge_path = plugin_path / "expertise" / "knowledge_fragments"
        fragments = {}
        
        if knowledge_path.exists():
            for category_dir in knowledge_path.iterdir():
                if category_dir.is_dir():
                    count = len(list(category_dir.glob("*.json")))
                    fragments[category_dir.name] = count
                    
        return fragments
