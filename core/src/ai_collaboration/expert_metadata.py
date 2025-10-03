"""
Expert Metadata System for Mixture of Experts (MoE)

This module defines the metadata structure for AI experts and provides
utilities for managing expert information, specializations, and domains.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
from pathlib import Path
import json


class ExpertDomain(Enum):
    """Enum defining expert domains for organization."""
    CORE = "core"
    MUSIC_THEORY = "music_theory"
    THREE_D_PRINTING = "3d_printing"
    UI_UX_DESIGN = "ui_ux_design"
    ENGINEERING = "engineering"
    MATHEMATICS = "mathematics"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    AI_ML = "ai_ml"
    DATA_SCIENCE = "data_science"
    ETHICS = "ethics"
    RESEARCH = "research"


@dataclass
class ExpertMetadata:
    """Metadata for an AI expert in the MoE system."""
    
    expert_id: str
    name: str
    domain: ExpertDomain
    expertise: str
    specialization: str
    keywords: List[str] = field(default_factory=list)
    enabled: bool = True
    version: str = "1.0.0"
    description: str = ""
    fragments_path: Optional[Path] = None
    model_path: Optional[Path] = None
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert metadata to dictionary."""
        return {
            'expert_id': self.expert_id,
            'name': self.name,
            'domain': self.domain.value,
            'expertise': self.expertise,
            'specialization': self.specialization,
            'keywords': self.keywords,
            'enabled': self.enabled,
            'version': self.version,
            'description': self.description,
            'fragments_path': str(self.fragments_path) if self.fragments_path else None,
            'model_path': str(self.model_path) if self.model_path else None,
            'dependencies': self.dependencies
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExpertMetadata':
        """Create metadata from dictionary."""
        data = data.copy()
        data['domain'] = ExpertDomain(data['domain'])
        if data.get('fragments_path'):
            data['fragments_path'] = Path(data['fragments_path'])
        if data.get('model_path'):
            data['model_path'] = Path(data['model_path'])
        return cls(**data)
    
    def matches_query(self, query: str) -> float:
        """Calculate relevance score for a query (0.0 to 1.0)."""
        query_lower = query.lower()
        score = 0.0
        
        # Check keywords
        keyword_matches = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        if keyword_matches > 0:
            score += min(keyword_matches * 0.2, 0.6)
        
        # Check expertise
        if self.expertise.lower() in query_lower:
            score += 0.3
        
        # Check specialization
        if self.specialization.lower() in query_lower:
            score += 0.2
        
        # Check domain
        if self.domain.value.replace('_', ' ') in query_lower:
            score += 0.1
        
        return min(score, 1.0)


class ExpertRegistry:
    """Registry for managing expert metadata."""
    
    def __init__(self):
        self.experts: Dict[str, ExpertMetadata] = {}
        self.domains: Dict[ExpertDomain, List[str]] = {}
    
    def register(self, metadata: ExpertMetadata) -> None:
        """Register an expert in the registry."""
        self.experts[metadata.expert_id] = metadata
        
        # Add to domain index
        if metadata.domain not in self.domains:
            self.domains[metadata.domain] = []
        if metadata.expert_id not in self.domains[metadata.domain]:
            self.domains[metadata.domain].append(metadata.expert_id)
    
    def unregister(self, expert_id: str) -> None:
        """Unregister an expert from the registry."""
        if expert_id in self.experts:
            metadata = self.experts[expert_id]
            del self.experts[expert_id]
            
            # Remove from domain index
            if metadata.domain in self.domains:
                if expert_id in self.domains[metadata.domain]:
                    self.domains[metadata.domain].remove(expert_id)
    
    def get_expert(self, expert_id: str) -> Optional[ExpertMetadata]:
        """Get expert metadata by ID."""
        return self.experts.get(expert_id)
    
    def get_by_domain(self, domain: ExpertDomain) -> List[ExpertMetadata]:
        """Get all experts in a specific domain."""
        expert_ids = self.domains.get(domain, [])
        return [self.experts[eid] for eid in expert_ids if eid in self.experts]
    
    def get_enabled_experts(self) -> List[ExpertMetadata]:
        """Get all enabled experts."""
        return [exp for exp in self.experts.values() if exp.enabled]
    
    def search_experts(self, query: str, threshold: float = 0.1) -> List[tuple[ExpertMetadata, float]]:
        """Search for experts matching a query with relevance scores."""
        results = []
        for expert in self.get_enabled_experts():
            score = expert.matches_query(query)
            if score >= threshold:
                results.append((expert, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def save_to_file(self, filepath: Path) -> None:
        """Save registry to JSON file."""
        data = {
            'experts': {eid: exp.to_dict() for eid, exp in self.experts.items()}
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: Path) -> None:
        """Load registry from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for expert_id, expert_data in data.get('experts', {}).items():
            metadata = ExpertMetadata.from_dict(expert_data)
            self.register(metadata)


# Predefined expert metadata for existing experts
CORE_EXPERTS = {
    'analysis_ghost': ExpertMetadata(
        expert_id='analysis_ghost',
        name='Analysis Ghost',
        domain=ExpertDomain.CORE,
        expertise='Code analysis and quality assessment',
        specialization='Mesh and model quality analysis',
        keywords=['analysis', 'mesh', 'model', 'quality', 'validation'],
        description='Specialized in analyzing mesh and model quality'
    ),
    'optimization_ghost': ExpertMetadata(
        expert_id='optimization_ghost',
        name='Optimization Ghost',
        domain=ExpertDomain.CORE,
        expertise='Algorithm optimization',
        specialization='Slicing algorithm optimization',
        keywords=['optimization', 'performance', 'slicing', 'algorithm'],
        description='Specialized in optimizing slicing algorithms'
    ),
    'error_ghost': ExpertMetadata(
        expert_id='error_ghost',
        name='Error Ghost',
        domain=ExpertDomain.CORE,
        expertise='Error detection and correction',
        specialization='Error handling and debugging',
        keywords=['error', 'exception', 'debug', 'troubleshooting'],
        description='Specialized in error detection and correction'
    ),
    'research_ghost': ExpertMetadata(
        expert_id='research_ghost',
        name='Research Ghost',
        domain=ExpertDomain.RESEARCH,
        expertise='Research and innovation',
        specialization='FOSS solutions and best practices',
        keywords=['research', 'foss', 'innovation', 'solutions'],
        description='Specialized in researching FOSS solutions and innovations'
    ),
}

ENGINEERING_EXPERTS = {
    'physics_ghost': ExpertMetadata(
        expert_id='physics_ghost',
        name='Physics Ghost',
        domain=ExpertDomain.ENGINEERING,
        expertise='Mechanical engineering and fluid dynamics',
        specialization='Thermodynamics and material behavior',
        keywords=['physics', 'mechanics', 'thermodynamics', 'fluid dynamics'],
        description='PhD-level specialist in mechanical engineering'
    ),
    'materials_ghost': ExpertMetadata(
        expert_id='materials_ghost',
        name='Materials Ghost',
        domain=ExpertDomain.ENGINEERING,
        expertise='Polymer science and material properties',
        specialization='Material chemistry and behavior',
        keywords=['materials', 'polymer', 'chemistry', 'properties'],
        description='PhD-level specialist in polymer science'
    ),
    'mathematics_ghost': ExpertMetadata(
        expert_id='mathematics_ghost',
        name='Mathematics Ghost',
        domain=ExpertDomain.MATHEMATICS,
        expertise='Computational geometry and algorithms',
        specialization='Mathematical optimization',
        keywords=['mathematics', 'geometry', 'algorithms', 'optimization'],
        description='PhD-level specialist in computational mathematics'
    ),
}

UIUX_EXPERTS = {
    'colorscience_ghost': ExpertMetadata(
        expert_id='colorscience_ghost',
        name='Color Science Ghost',
        domain=ExpertDomain.UI_UX_DESIGN,
        expertise='Color theory and color science',
        specialization='Color harmony and perception',
        keywords=['color', 'design', 'visual', 'aesthetics'],
        description='PhD-level specialist in color science'
    ),
    'typography_ghost': ExpertMetadata(
        expert_id='typography_ghost',
        name='Typography Ghost',
        domain=ExpertDomain.UI_UX_DESIGN,
        expertise='Typography and font design',
        specialization='Type systems and readability',
        keywords=['typography', 'fonts', 'text', 'readability'],
        description='PhD-level specialist in typography'
    ),
    'uxdesign_ghost': ExpertMetadata(
        expert_id='uxdesign_ghost',
        name='UX Design Ghost',
        domain=ExpertDomain.UI_UX_DESIGN,
        expertise='User experience design',
        specialization='Interface design and usability',
        keywords=['ux', 'ui', 'design', 'usability', 'interface'],
        description='PhD-level specialist in UX design'
    ),
}

SECURITY_EXPERTS = {
    'security_ghost': ExpertMetadata(
        expert_id='security_ghost',
        name='Security Ghost',
        domain=ExpertDomain.SECURITY,
        expertise='Security analysis and vulnerability assessment',
        specialization='Code security and best practices',
        keywords=['security', 'vulnerability', 'safety', 'protection'],
        description='Specialist in code security'
    ),
    'ethics_ghost': ExpertMetadata(
        expert_id='ethics_ghost',
        name='Ethics Ghost',
        domain=ExpertDomain.ETHICS,
        expertise='AI ethics and responsible development',
        specialization='Ethical AI practices',
        keywords=['ethics', 'responsible', 'bias', 'fairness', 'transparency'],
        description='Non-biased ethics specialist'
    ),
}


def create_default_registry() -> ExpertRegistry:
    """Create and populate a registry with default experts."""
    registry = ExpertRegistry()
    
    # Register all predefined experts
    for expert_metadata in CORE_EXPERTS.values():
        registry.register(expert_metadata)
    
    for expert_metadata in ENGINEERING_EXPERTS.values():
        registry.register(expert_metadata)
    
    for expert_metadata in UIUX_EXPERTS.values():
        registry.register(expert_metadata)
    
    for expert_metadata in SECURITY_EXPERTS.values():
        registry.register(expert_metadata)
    
    return registry
