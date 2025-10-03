"""
Mixture of Experts (MoE) Router

This module implements the MoE routing logic for dynamically selecting
and coordinating AI experts based on user queries and task requirements.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from .expert_metadata import ExpertMetadata, ExpertRegistry, ExpertDomain
except ImportError:
    from expert_metadata import ExpertMetadata, ExpertRegistry, ExpertDomain


@dataclass
class ExpertSelection:
    """Represents a selected expert with relevance score."""
    expert_id: str
    metadata: ExpertMetadata
    relevance_score: float
    reasoning: str = ""


class MoERouter:
    """
    Mixture of Experts Router for dynamic expert selection.
    
    The router analyzes queries and selects the most appropriate experts
    to handle specific tasks, enabling modular and domain-specific responses.
    """
    
    def __init__(self, registry: ExpertRegistry, max_experts: int = 3):
        """
        Initialize the MoE Router.
        
        Args:
            registry: ExpertRegistry containing available experts
            max_experts: Maximum number of experts to select for a query
        """
        self.registry = registry
        self.max_experts = max_experts
        self.logger = logging.getLogger('MoERouter')
        
        # Query history for learning (future enhancement)
        self.query_history: List[Dict[str, Any]] = []
    
    def route_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[ExpertSelection]:
        """
        Route a query to the most appropriate experts.
        
        Args:
            query: User query or task description
            context: Optional context information (domain hints, previous experts, etc.)
        
        Returns:
            List of ExpertSelection objects sorted by relevance
        """
        self.logger.info(f"Routing query: {query[:50]}...")
        
        # Apply domain filtering if context specifies a domain
        candidates = self._get_candidates(query, context)
        
        # Score and rank experts
        selections = self._score_experts(query, candidates, context)
        
        # Limit to max_experts
        selections = selections[:self.max_experts]
        
        # Log selections
        for selection in selections:
            self.logger.info(
                f"Selected {selection.expert_id} "
                f"(score: {selection.relevance_score:.2f})"
            )
        
        # Record in history
        self._record_query(query, selections, context)
        
        return selections
    
    def _get_candidates(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[ExpertMetadata]:
        """Get candidate experts based on query and context."""
        # If context specifies a domain, filter by that domain
        if context and 'domain' in context:
            domain = context['domain']
            if isinstance(domain, str):
                try:
                    domain = ExpertDomain(domain)
                except ValueError:
                    pass
            
            if isinstance(domain, ExpertDomain):
                return self.registry.get_by_domain(domain)
        
        # Otherwise, return all enabled experts
        return self.registry.get_enabled_experts()
    
    def _score_experts(
        self,
        query: str,
        candidates: List[ExpertMetadata],
        context: Optional[Dict[str, Any]] = None
    ) -> List[ExpertSelection]:
        """Score and rank expert candidates."""
        selections = []
        
        for expert in candidates:
            # Base score from metadata matching
            base_score = expert.matches_query(query)
            
            # Apply context modifiers
            modified_score = self._apply_context_modifiers(
                base_score, expert, query, context
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(expert, modified_score, query)
            
            # Only include experts with non-zero scores
            if modified_score > 0:
                selections.append(ExpertSelection(
                    expert_id=expert.expert_id,
                    metadata=expert,
                    relevance_score=modified_score,
                    reasoning=reasoning
                ))
        
        # Sort by score descending
        selections.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return selections
    
    def _apply_context_modifiers(
        self,
        base_score: float,
        expert: ExpertMetadata,
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> float:
        """Apply context-based score modifiers."""
        score = base_score
        
        if not context:
            return score
        
        # Boost score if expert was successful in previous queries
        if 'preferred_experts' in context:
            if expert.expert_id in context['preferred_experts']:
                score = min(score + 0.2, 1.0)
        
        # Boost score if query is in expert's primary domain
        if 'primary_domain' in context:
            if context['primary_domain'] == expert.domain:
                score = min(score + 0.15, 1.0)
        
        # Apply user preferences
        if 'user_preferences' in context:
            prefs = context['user_preferences']
            if expert.expert_id in prefs.get('favorite_experts', []):
                score = min(score + 0.1, 1.0)
            if expert.domain in prefs.get('disabled_domains', []):
                score = 0.0
        
        return score
    
    def _generate_reasoning(
        self,
        expert: ExpertMetadata,
        score: float,
        query: str
    ) -> str:
        """Generate human-readable reasoning for expert selection."""
        reasons = []
        
        if score >= 0.7:
            reasons.append("High relevance match")
        elif score >= 0.4:
            reasons.append("Moderate relevance match")
        elif score > 0:
            reasons.append("Low relevance match")
        
        # Check specific matches
        query_lower = query.lower()
        matching_keywords = [kw for kw in expert.keywords if kw.lower() in query_lower]
        if matching_keywords:
            reasons.append(f"Matches keywords: {', '.join(matching_keywords[:3])}")
        
        if expert.expertise.lower() in query_lower:
            reasons.append(f"Expertise in {expert.expertise}")
        
        return "; ".join(reasons) if reasons else "Generic match"
    
    def _record_query(
        self,
        query: str,
        selections: List[ExpertSelection],
        context: Optional[Dict[str, Any]]
    ) -> None:
        """Record query for history and potential learning."""
        record = {
            'query': query,
            'selected_experts': [s.expert_id for s in selections],
            'scores': {s.expert_id: s.relevance_score for s in selections},
            'context': context
        }
        self.query_history.append(record)
        
        # Keep history size manageable
        if len(self.query_history) > 100:
            self.query_history = self.query_history[-50:]
    
    def get_expert_by_domain(self, domain: ExpertDomain) -> List[ExpertSelection]:
        """Get all experts for a specific domain."""
        experts = self.registry.get_by_domain(domain)
        return [
            ExpertSelection(
                expert_id=exp.expert_id,
                metadata=exp,
                relevance_score=1.0,
                reasoning=f"Domain expert: {domain.value}"
            )
            for exp in experts
        ]
    
    def get_expert_by_id(self, expert_id: str) -> Optional[ExpertSelection]:
        """Get a specific expert by ID."""
        metadata = self.registry.get_expert(expert_id)
        if metadata and metadata.enabled:
            return ExpertSelection(
                expert_id=expert_id,
                metadata=metadata,
                relevance_score=1.0,
                reasoning="Direct selection"
            )
        return None
    
    def suggest_experts_for_task(self, task_description: str) -> List[ExpertSelection]:
        """
        Suggest experts for a task based on description analysis.
        
        This is a higher-level method that can perform more sophisticated
        analysis of the task requirements.
        """
        # Extract task type hints
        context = self._analyze_task_description(task_description)
        
        # Route based on analysis
        return self.route_query(task_description, context)
    
    def _analyze_task_description(self, description: str) -> Dict[str, Any]:
        """Analyze task description to extract hints for routing."""
        context = {}
        desc_lower = description.lower()
        
        # Detect domain hints
        domain_keywords = {
            ExpertDomain.MUSIC_THEORY: ['music', 'audio', 'sound', 'melody', 'harmony'],
            ExpertDomain.THREE_D_PRINTING: ['3d print', 'mesh', 'model', 'stl', 'gcode'],
            ExpertDomain.UI_UX_DESIGN: ['ui', 'ux', 'design', 'interface', 'user experience'],
            ExpertDomain.ENGINEERING: ['engineering', 'physics', 'mechanical', 'materials'],
            ExpertDomain.MATHEMATICS: ['math', 'algorithm', 'calculation', 'optimization'],
            ExpertDomain.SECURITY: ['security', 'vulnerability', 'safe', 'protection'],
            ExpertDomain.PERFORMANCE: ['performance', 'speed', 'optimize', 'efficient'],
        }
        
        for domain, keywords in domain_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                context['primary_domain'] = domain
                break
        
        # Detect task complexity
        complexity_keywords = {
            'high': ['complex', 'advanced', 'sophisticated', 'intricate'],
            'medium': ['moderate', 'standard', 'typical'],
            'low': ['simple', 'basic', 'straightforward']
        }
        
        for level, keywords in complexity_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                context['complexity'] = level
                break
        
        return context
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get router statistics and insights."""
        total_queries = len(self.query_history)
        
        if total_queries == 0:
            return {
                'total_queries': 0,
                'most_used_experts': [],
                'average_experts_per_query': 0
            }
        
        # Count expert usage
        expert_usage = {}
        for record in self.query_history:
            for expert_id in record['selected_experts']:
                expert_usage[expert_id] = expert_usage.get(expert_id, 0) + 1
        
        # Sort by usage
        most_used = sorted(
            expert_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Calculate average experts per query
        total_experts = sum(len(r['selected_experts']) for r in self.query_history)
        avg_experts = total_experts / total_queries if total_queries > 0 else 0
        
        return {
            'total_queries': total_queries,
            'most_used_experts': [
                {'expert_id': eid, 'count': count}
                for eid, count in most_used
            ],
            'average_experts_per_query': round(avg_experts, 2),
            'total_registered_experts': len(self.registry.experts),
            'enabled_experts': len(self.registry.get_enabled_experts())
        }
