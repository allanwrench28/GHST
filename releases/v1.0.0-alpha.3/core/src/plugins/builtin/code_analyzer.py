"""
GHST Code Analysis Plugin
========================

Analyzes code quality and provides suggestions for the GHST AI engine.
"""

import sys
import os
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


class CodeAnalyzer(BasePlugin):
    """GHST code analysis plugin."""
    
    def __init__(self):
        metadata = PluginMetadata(
            name="Code Analyzer",
            version="1.0.0",
            description="Analyzes code quality for GHST AI engine",
            author="GHST Expert Collective"
        )
        super().__init__(metadata)
    
    def activate(self):
        """Activate the code analyzer."""
        if self.logger:
            self.logger.info("Code Analyzer activated")
        return True
    
    def deactivate(self):
        """Deactivate the code analyzer."""
        if self.logger:
            self.logger.info("Code Analyzer deactivated")
        return True
    
    def analyze_code(self, code_content: str) -> dict:
        """Analyze code and return quality metrics."""
        lines = code_content.split('\n')
        
        analysis = {
            'total_lines': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'quality_score': 85,  # Placeholder
            'suggestions': [
                "Consider adding more comments",
                "Code structure looks good"
            ]
        }
        
        return analysis


def create_plugin():
    """Create and return plugin instance."""
    return CodeAnalyzer()
