"""
Context Manager for GHST LLM System

Manages context windows, expertise plugin contexts, and conversation history
for efficient LLM inference with loaded expertise.
"""

import logging
from typing import Dict, List, Optional, Any


class ContextManager:
    """Manages LLM context windows and expertise integration."""
    
    def __init__(self, max_context_size: int = 4096):
        """Initialize context manager.
        
        Args:
            max_context_size: Maximum context window size
        """
        self.max_context_size = max_context_size
        self.logger = logging.getLogger(__name__)
        self.context_stack = []
        self.expertise_contexts = {}
        
        self.logger.info("📚 Context Manager initialized")
        
    def push_context(self, context: Dict[str, Any]) -> bool:
        """Push a new context onto the stack.
        
        Args:
            context: Context dictionary to push
            
        Returns:
            True if pushed successfully
        """
        # TODO: Implement context size management
        self.context_stack.append(context)
        return True
        
    def pop_context(self) -> Optional[Dict[str, Any]]:
        """Pop the most recent context from the stack.
        
        Returns:
            Popped context or None
        """
        if self.context_stack:
            return self.context_stack.pop()
        return None
        
    def add_expertise_context(self, plugin_name: str, context_data: Dict) -> bool:
        """Add expertise-specific context for a loaded plugin.
        
        Args:
            plugin_name: Name of the expertise plugin
            context_data: Context data from the plugin
            
        Returns:
            True if added successfully
        """
        self.expertise_contexts[plugin_name] = context_data
        self.logger.info(f"Added expertise context: {plugin_name}")
        return True
        
    def remove_expertise_context(self, plugin_name: str) -> bool:
        """Remove expertise context when plugin is unloaded.
        
        Args:
            plugin_name: Name of the expertise plugin
            
        Returns:
            True if removed successfully
        """
        if plugin_name in self.expertise_contexts:
            del self.expertise_contexts[plugin_name]
            self.logger.info(f"Removed expertise context: {plugin_name}")
            return True
        return False
        
    def get_combined_context(self) -> str:
        """Build combined context from stack and expertise plugins.
        
        Returns:
            Combined context string for LLM
        """
        # TODO: Implement smart context combination and truncation
        context_parts = []
        
        # Add expertise contexts
        for plugin_name, context in self.expertise_contexts.items():
            context_parts.append(f"[Expertise: {plugin_name}]")
            
        # Add conversation context
        for ctx in self.context_stack[-5:]:  # Last 5 context entries
            if 'text' in ctx:
                context_parts.append(ctx['text'])
                
        return "\n".join(context_parts)
        
    def clear_context(self):
        """Clear all context."""
        self.context_stack.clear()
        self.expertise_contexts.clear()
        self.logger.info("🧹 Context cleared")
