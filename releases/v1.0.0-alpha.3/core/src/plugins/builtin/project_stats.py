"""
GHST Project Statistics Plugin  
=============================

Provides project statistics and metrics for the GHST AI engine.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from base_plugin import BasePlugin, PluginMetadata
except ImportError:
    # Fallback - create minimal base classes
    class PluginMetadata:
        def __init__(self, name, version, description, author):
            self.name = name
            self.version = version
            self.description = description
            self.author = author
    
    class BasePlugin:
        def __init__(self, metadata):
            self.metadata = metadata
            self.logger = None
        
        def activate(self):
            return True
        
        def deactivate(self):
            return True


class ProjectStats(BasePlugin):
    """GHST project statistics plugin."""
    
    def __init__(self):
        metadata = PluginMetadata(
            name="Project Stats",
            version="1.0.0",
            description="Provides project statistics for GHST",
            author="GHST Expert Collective"
        )
        super().__init__(metadata)
    
    def activate(self):
        """Activate the project stats plugin."""
        if self.logger:
            self.logger.info("Project Stats activated")
        return True
    
    def deactivate(self):
        """Deactivate the project stats plugin."""
        if self.logger:
            self.logger.info("Project Stats deactivated")
        return True
    
    def get_project_stats(self, project_path: str) -> dict:
        """Get statistics for a project."""
        try:
            project_dir = Path(project_path)
            
            # Count files by type
            python_files = len(list(project_dir.rglob("*.py")))
            md_files = len(list(project_dir.rglob("*.md")))
            json_files = len(list(project_dir.rglob("*.json")))
            total_files = len(list(project_dir.rglob("*.*")))
            
            stats = {
                'total_files': total_files,
                'python_files': python_files,
                'markdown_files': md_files,
                'json_files': json_files,
                'project_path': str(project_dir),
                'analysis_timestamp': 'now'
            }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}


def create_plugin():
    """Create and return plugin instance."""
    return ProjectStats()
