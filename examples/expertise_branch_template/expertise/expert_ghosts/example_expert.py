"""
Example Expert Ghost

Template for creating expert ghosts in expertise branches.
Copy and customize this for your domain.
"""

import sys
from pathlib import Path

# Add core to path for imports
core_path = Path(__file__).parent.parent.parent.parent.parent / "core"
sys.path.insert(0, str(core_path))

from ghosts.base_ghost import BaseGhost
from typing import Dict, Optional, Any


class ExampleExpertGhost(BaseGhost):
    """Example expert ghost for demonstration purposes."""
    
    def __init__(self):
        """Initialize the example expert ghost."""
        super().__init__(
            ghost_id="example_expert",
            name="Example Expert",
            specialization="Example Domain Expertise"
        )
        
        # Initialize domain-specific knowledge
        self.knowledge_base = {
            "basics": "Basic concepts...",
            "advanced": "Advanced techniques...",
            "troubleshooting": "Common issues..."
        }
        
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        """Process a domain-specific query.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            Expert response
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        
        # Analyze query to determine topic
        query_lower = query.lower()
        
        if "basic" in query_lower or "beginner" in query_lower:
            return self._handle_basic_query(query)
        elif "advanced" in query_lower or "expert" in query_lower:
            return self._handle_advanced_query(query)
        elif "problem" in query_lower or "error" in query_lower:
            return self._handle_troubleshooting_query(query)
        else:
            return self._handle_general_query(query)
            
    def _handle_basic_query(self, query: str) -> str:
        """Handle beginner-level questions."""
        return f"🎓 **Example Expert**: For basic questions like '{query[:50]}...', here's what you need to know:\n\n{self.knowledge_base['basics']}"
        
    def _handle_advanced_query(self, query: str) -> str:
        """Handle advanced questions."""
        return f"🔬 **Example Expert**: For advanced topics like '{query[:50]}...', I recommend:\n\n{self.knowledge_base['advanced']}"
        
    def _handle_troubleshooting_query(self, query: str) -> str:
        """Handle troubleshooting questions."""
        return f"🔧 **Example Expert**: For troubleshooting '{query[:50]}...', try these solutions:\n\n{self.knowledge_base['troubleshooting']}"
        
    def _handle_general_query(self, query: str) -> str:
        """Handle general questions."""
        return f"💡 **Example Expert**: I can help with:\n- Basic concepts\n- Advanced techniques\n- Troubleshooting\n\nYour question: '{query[:50]}...'\n\nCould you be more specific?"
        
    def get_capabilities(self) -> Dict[str, Any]:
        """Get expert capabilities.
        
        Returns:
            Capabilities dictionary
        """
        return {
            "type": "expert",
            "domain": "example_domain",
            "specialization": self.specialization,
            "capabilities": [
                "Basic concept explanation",
                "Advanced technique guidance",
                "Problem troubleshooting",
                "Best practices recommendations"
            ],
            "features": {
                "context_aware": True,
                "code_generation": False,
                "real_time_data": False,
                "multi_language": False
            },
            "knowledge_areas": [
                "Fundamentals",
                "Advanced concepts",
                "Troubleshooting",
                "Best practices"
            ]
        }
        
    def search_knowledge(self, query: str) -> list:
        """Search the expert's knowledge base.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant knowledge fragments
        """
        # TODO: Implement actual knowledge fragment search
        results = []
        for category, content in self.knowledge_base.items():
            if query.lower() in content.lower():
                results.append({
                    "category": category,
                    "content": content,
                    "relevance": 0.8
                })
        return results


# For testing
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    ghost = ExampleExpertGhost()
    print(f"\n{ghost}")
    print(f"\nCapabilities: {ghost.get_capabilities()}")
    
    # Test queries
    test_queries = [
        "How do I get started with basics?",
        "What are some advanced techniques?",
        "I'm having a problem with something"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        response = ghost.process_query(query)
        print(response)
