"""
Memory System for GHST LLM

Handles fragmented data storage and retrieval for expertise knowledge.
Implements efficient storage and search of domain-specific information.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any


class MemorySystem:
    """Fragmented memory storage and retrieval system."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize memory system.
        
        Args:
            storage_path: Path to memory storage directory
        """
        self.storage_path = storage_path or Path("data/plugin_cache")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.memory_index = {}
        
        self.logger.info("🧠 Memory System initialized")
        
    def store_fragment(self, plugin_name: str, fragment_id: str, 
                      data: Dict[str, Any]) -> bool:
        """Store a knowledge fragment.
        
        Args:
            plugin_name: Name of the expertise plugin
            fragment_id: Unique identifier for this fragment
            data: Fragment data to store
            
        Returns:
            True if stored successfully
        """
        plugin_path = self.storage_path / plugin_name
        plugin_path.mkdir(exist_ok=True)
        
        fragment_file = plugin_path / f"{fragment_id}.json"
        try:
            with open(fragment_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Update index
            if plugin_name not in self.memory_index:
                self.memory_index[plugin_name] = []
            self.memory_index[plugin_name].append(fragment_id)
            
            self.logger.debug(f"Stored fragment: {plugin_name}/{fragment_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to store fragment: {e}")
            return False
            
    def retrieve_fragment(self, plugin_name: str, 
                         fragment_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a knowledge fragment.
        
        Args:
            plugin_name: Name of the expertise plugin
            fragment_id: Fragment identifier
            
        Returns:
            Fragment data or None if not found
        """
        fragment_file = self.storage_path / plugin_name / f"{fragment_id}.json"
        try:
            if fragment_file.exists():
                with open(fragment_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to retrieve fragment: {e}")
        return None
        
    def search_fragments(self, plugin_name: str, 
                        query: str) -> List[Dict[str, Any]]:
        """Search for relevant fragments.
        
        Args:
            plugin_name: Name of the expertise plugin
            query: Search query
            
        Returns:
            List of relevant fragments
        """
        # TODO: Implement semantic search
        results = []
        if plugin_name in self.memory_index:
            for fragment_id in self.memory_index[plugin_name]:
                fragment = self.retrieve_fragment(plugin_name, fragment_id)
                if fragment:
                    # Simple keyword search for now
                    if query.lower() in str(fragment).lower():
                        results.append(fragment)
        return results
        
    def delete_plugin_memory(self, plugin_name: str) -> bool:
        """Delete all memory fragments for a plugin.
        
        Args:
            plugin_name: Name of the expertise plugin
            
        Returns:
            True if deleted successfully
        """
        plugin_path = self.storage_path / plugin_name
        try:
            if plugin_path.exists():
                import shutil
                shutil.rmtree(plugin_path)
            
            if plugin_name in self.memory_index:
                del self.memory_index[plugin_name]
                
            self.logger.info(f"Deleted memory for plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete plugin memory: {e}")
            return False
            
    def get_plugin_stats(self, plugin_name: str) -> Dict[str, int]:
        """Get statistics for a plugin's memory.
        
        Args:
            plugin_name: Name of the expertise plugin
            
        Returns:
            Dictionary with fragment count and size
        """
        stats = {"fragment_count": 0, "total_size_bytes": 0}
        
        if plugin_name in self.memory_index:
            stats["fragment_count"] = len(self.memory_index[plugin_name])
            
        plugin_path = self.storage_path / plugin_name
        if plugin_path.exists():
            stats["total_size_bytes"] = sum(
                f.stat().st_size for f in plugin_path.glob("*.json")
            )
            
        return stats
