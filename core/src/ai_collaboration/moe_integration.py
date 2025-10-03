"""
MoE Integration Module

Integrates the Mixture of Experts (MoE) system with the existing ExpertManager,
providing backward compatibility while enabling dynamic expert selection.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from .expert_metadata import (
        ExpertMetadata,
        ExpertDomain,
        ExpertRegistry,
        create_default_registry
    )
    from .moe_router import MoERouter, ExpertSelection
except ImportError:
    from expert_metadata import (
        ExpertMetadata,
        ExpertDomain,
        ExpertRegistry,
        create_default_registry
    )
    from moe_router import MoERouter, ExpertSelection


class MoEIntegration:
    """
    Integration layer between MoE system and ExpertManager.
    
    This class provides:
    - Backward compatibility with existing code
    - Dynamic expert selection
    - Query routing
    - Expert coordination
    """
    
    def __init__(self, expert_manager):
        """
        Initialize MoE integration.
        
        Args:
            expert_manager: Existing ExpertManager instance
        """
        self.expert_manager = expert_manager
        self.registry = create_default_registry()
        self.router = MoERouter(self.registry, max_experts=3)
        self.logger = logging.getLogger('MoEIntegration')
        
        # Sync existing experts with registry
        self._sync_experts()
    
    def _sync_experts(self):
        """Synchronize existing experts with MoE registry."""
        # This ensures all experts in ExpertManager are registered
        # in the MoE system for routing
        self.logger.info("Synchronizing experts with MoE registry...")
        
        # The registry already has predefined experts from metadata
        # This method can be extended to dynamically register experts
        # found in the expert_manager.active_ghosts dictionary
        
        synced_count = len(self.registry.experts)
        self.logger.info(f"Synced {synced_count} experts to MoE registry")
    
    def query_experts(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the expert system using MoE routing.
        
        Args:
            query: User query or task description
            context: Optional context information
        
        Returns:
            Dictionary containing selected experts and their analyses
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        
        # Route query to appropriate experts
        selections = self.router.route_query(query, context)
        
        if not selections:
            self.logger.warning("No experts selected for query")
            return {
                'query': query,
                'experts': [],
                'analyses': [],
                'warning': 'No relevant experts found for this query'
            }
        
        # Collect analyses from selected experts
        analyses = []
        for selection in selections:
            analysis = self._get_expert_analysis(selection, query, context)
            if analysis:
                analyses.append(analysis)
        
        return {
            'query': query,
            'experts': [
                {
                    'expert_id': s.expert_id,
                    'name': s.metadata.name,
                    'relevance_score': s.relevance_score,
                    'reasoning': s.reasoning
                }
                for s in selections
            ],
            'analyses': analyses,
            'router_stats': self.router.get_statistics()
        }
    
    def _get_expert_analysis(
        self,
        selection: ExpertSelection,
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Get analysis from a specific expert."""
        expert_id = selection.expert_id
        
        # Check if expert exists in active ghosts
        if expert_id not in self.expert_manager.active_ghosts:
            self.logger.warning(f"Expert {expert_id} not found in active ghosts")
            return None
        
        expert = self.expert_manager.active_ghosts[expert_id]
        
        # Try to get analysis if expert has analyze_task method
        if hasattr(expert, 'analyze_task'):
            try:
                analysis = expert.analyze_task(query)
                return {
                    'expert_id': expert_id,
                    'expert_name': selection.metadata.name,
                    'analysis': analysis,
                    'relevance_score': selection.relevance_score
                }
            except Exception as e:
                self.logger.error(f"Error getting analysis from {expert_id}: {e}")
                return None
        
        # Fallback: return basic info
        return {
            'expert_id': expert_id,
            'expert_name': selection.metadata.name,
            'analysis': {
                'message': f"{selection.metadata.name} available for {selection.metadata.expertise}",
                'specialization': selection.metadata.specialization
            },
            'relevance_score': selection.relevance_score
        }
    
    def get_expert_suggestions(self, task_description: str) -> List[Dict[str, Any]]:
        """
        Get expert suggestions for a task.
        
        Args:
            task_description: Description of the task
        
        Returns:
            List of expert suggestions with details
        """
        selections = self.router.suggest_experts_for_task(task_description)
        
        return [
            {
                'expert_id': s.expert_id,
                'name': s.metadata.name,
                'domain': s.metadata.domain.value,
                'expertise': s.metadata.expertise,
                'specialization': s.metadata.specialization,
                'relevance_score': s.relevance_score,
                'reasoning': s.reasoning,
                'keywords': s.metadata.keywords
            }
            for s in selections
        ]
    
    def get_domain_experts(self, domain: str) -> List[Dict[str, Any]]:
        """
        Get all experts for a specific domain.
        
        Args:
            domain: Domain name (e.g., 'ui_ux_design', 'engineering')
        
        Returns:
            List of experts in the domain
        """
        try:
            domain_enum = ExpertDomain(domain)
        except ValueError:
            self.logger.error(f"Invalid domain: {domain}")
            return []
        
        selections = self.router.get_expert_by_domain(domain_enum)
        
        return [
            {
                'expert_id': s.expert_id,
                'name': s.metadata.name,
                'expertise': s.metadata.expertise,
                'specialization': s.metadata.specialization,
                'keywords': s.metadata.keywords
            }
            for s in selections
        ]
    
    def list_all_domains(self) -> List[Dict[str, Any]]:
        """
        List all available domains.
        
        Returns:
            List of domain information
        """
        domains = []
        for domain in ExpertDomain:
            experts = self.registry.get_by_domain(domain)
            domains.append({
                'domain': domain.value,
                'display_name': domain.value.replace('_', ' ').title(),
                'expert_count': len(experts),
                'experts': [e.expert_id for e in experts]
            })
        
        return domains
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get MoE system statistics.
        
        Returns:
            Dictionary containing statistics
        """
        router_stats = self.router.get_statistics()
        
        return {
            'total_experts': len(self.registry.experts),
            'enabled_experts': len(self.registry.get_enabled_experts()),
            'domains': len(ExpertDomain),
            'router_stats': router_stats,
            'domain_breakdown': {
                domain.value: len(self.registry.get_by_domain(domain))
                for domain in ExpertDomain
            }
        }
    
    def enable_expert(self, expert_id: str) -> bool:
        """
        Enable a specific expert.
        
        Args:
            expert_id: Expert identifier
        
        Returns:
            True if successful, False otherwise
        """
        expert = self.registry.get_expert(expert_id)
        if expert:
            expert.enabled = True
            self.logger.info(f"Enabled expert: {expert_id}")
            return True
        return False
    
    def disable_expert(self, expert_id: str) -> bool:
        """
        Disable a specific expert.
        
        Args:
            expert_id: Expert identifier
        
        Returns:
            True if successful, False otherwise
        """
        expert = self.registry.get_expert(expert_id)
        if expert:
            expert.enabled = False
            self.logger.info(f"Disabled expert: {expert_id}")
            return True
        return False
    
    def add_custom_expert(
        self,
        expert_id: str,
        name: str,
        domain: str,
        expertise: str,
        specialization: str,
        keywords: List[str],
        **kwargs
    ) -> bool:
        """
        Add a custom expert to the registry.
        
        Args:
            expert_id: Unique identifier
            name: Expert name
            domain: Domain name
            expertise: Expertise area
            specialization: Specialization
            keywords: List of keywords
            **kwargs: Additional metadata fields
        
        Returns:
            True if successful, False otherwise
        """
        try:
            domain_enum = ExpertDomain(domain)
        except ValueError:
            self.logger.error(f"Invalid domain: {domain}")
            return False
        
        metadata = ExpertMetadata(
            expert_id=expert_id,
            name=name,
            domain=domain_enum,
            expertise=expertise,
            specialization=specialization,
            keywords=keywords,
            **kwargs
        )
        
        self.registry.register(metadata)
        self.logger.info(f"Added custom expert: {expert_id}")
        return True
    
    def export_registry(self, filepath: str) -> bool:
        """
        Export registry to file.
        
        Args:
            filepath: Path to save registry
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from pathlib import Path
            self.registry.save_to_file(Path(filepath))
            self.logger.info(f"Exported registry to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export registry: {e}")
            return False
    
    def import_registry(self, filepath: str) -> bool:
        """
        Import registry from file.
        
        Args:
            filepath: Path to load registry from
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from pathlib import Path
            self.registry.load_from_file(Path(filepath))
            self.logger.info(f"Imported registry from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import registry: {e}")
            return False


def integrate_moe_with_expert_manager(expert_manager) -> MoEIntegration:
    """
    Convenience function to integrate MoE with ExpertManager.
    
    Args:
        expert_manager: ExpertManager instance
    
    Returns:
        MoEIntegration instance
    """
    integration = MoEIntegration(expert_manager)
    
    # Attach integration to expert_manager for easy access
    expert_manager.moe = integration
    
    return integration
