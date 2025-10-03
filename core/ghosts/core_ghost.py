"""
Core Ghost - General Purpose AI Assistant

The core ghost provides general-purpose AI assistance and coordinates
with specialized expert ghosts for domain-specific queries.
"""

import logging
from typing import Dict, Optional, Any
from .base_ghost import BaseGhost


class CoreGhost(BaseGhost):
    """General purpose ghost for the GHST system."""
    
    def __init__(self):
        """Initialize the core ghost."""
        super().__init__(
            ghost_id="core_ghost",
            name="Core Assistant",
            specialization="General AI Assistance"
        )
        
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        """Process a general query.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            Response from the core ghost
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        
        # TODO: Implement actual LLM-based query processing
        response = f"Core Ghost: I understand you're asking about: {query[:100]}"
        
        if context and 'loaded_expertise' in context:
            response += f"\n\nI have access to expertise in: {', '.join(context['loaded_expertise'])}"
            response += "\nI can consult with specialized expert ghosts for detailed answers."
            
        return response
        
    def get_capabilities(self) -> Dict[str, Any]:
        """Get core ghost capabilities.
        
        Returns:
            Capabilities dictionary
        """
        return {
            "type": "core",
            "specialization": self.specialization,
            "capabilities": [
                "General conversation",
                "Query routing to experts",
                "Multi-domain assistance",
                "Context management"
            ],
            "features": {
                "expert_coordination": True,
                "context_aware": True,
                "multi_language": False  # TODO: Add multi-language support
            }
        }
        
    def route_to_expert(self, query: str, 
                       available_experts: list) -> Optional[str]:
        """Route a query to the most appropriate expert.
        
        Args:
            query: User query
            available_experts: List of available expert ghost IDs
            
        Returns:
            Expert ghost ID or None
        """
        # TODO: Implement intelligent routing based on query content
        query_lower = query.lower()
        
        # Simple keyword-based routing
        routing_map = {
            "3d print": "slicer_expert",
            "web": "web_dev_expert",
            "frontend": "frontend_expert",
            "backend": "backend_expert",
            "security": "security_expert"
        }
        
        for keyword, expert in routing_map.items():
            if keyword in query_lower and expert in available_experts:
                return expert
                
        return None
