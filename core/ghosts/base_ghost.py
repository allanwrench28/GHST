"""
Base Ghost Class for GHST System

Abstract base class for all ghost personalities. Ghosts are AI entities
that provide specialized expertise and can collaborate with each other.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any


class BaseGhost(ABC):
    """Abstract base class for all GHST ghost personalities."""
    
    def __init__(self, ghost_id: str, name: str, specialization: str):
        """Initialize a ghost.
        
        Args:
            ghost_id: Unique identifier for this ghost
            name: Display name of the ghost
            specialization: Area of expertise
        """
        self.ghost_id = ghost_id
        self.name = name
        self.specialization = specialization
        self.logger = logging.getLogger(f"Ghost.{ghost_id}")
        self.active = True
        
        self.logger.info(f"👻 Ghost initialized: {name} ({specialization})")
        
    @abstractmethod
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        """Process a query with this ghost's expertise.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            Ghost's response
        """
        pass
        
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities of this ghost.
        
        Returns:
            Dictionary describing ghost's capabilities
        """
        pass
        
    def activate(self):
        """Activate this ghost."""
        self.active = True
        self.logger.info(f"✨ Ghost activated: {self.name}")
        
    def deactivate(self):
        """Deactivate this ghost."""
        self.active = False
        self.logger.info(f"💤 Ghost deactivated: {self.name}")
        
    def is_active(self) -> bool:
        """Check if ghost is active.
        
        Returns:
            True if active
        """
        return self.active
        
    def get_info(self) -> Dict[str, Any]:
        """Get information about this ghost.
        
        Returns:
            Dictionary with ghost information
        """
        return {
            "ghost_id": self.ghost_id,
            "name": self.name,
            "specialization": self.specialization,
            "active": self.active
        }
        
    def __repr__(self) -> str:
        """String representation of ghost."""
        return f"Ghost({self.name}, {self.specialization})"
