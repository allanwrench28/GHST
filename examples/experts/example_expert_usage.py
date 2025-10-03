#!/usr/bin/env python3
"""
Example: Using the GHST Expert System

This example demonstrates how to load and use experts in the GHST system.
"""

from pathlib import Path
from typing import Dict, Any


# Mock classes for demonstration (in real system, import from actual modules)
class BaseExpert:
    """Base expert class (simplified for example)."""
    
    def __init__(self, expert_dir: Path):
        self.expert_dir = expert_dir
        self.metadata = self._load_metadata()
        self.name = self.metadata.get('name', 'Unknown Expert')
        self.id = self.metadata.get('id', 'unknown')
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from YAML file."""
        import yaml
        metadata_file = self.expert_dir / 'metadata.yaml'
        if metadata_file.exists():
            with open(metadata_file) as f:
                return yaml.safe_load(f)
        return {}
    
    def analyze(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a task (to be implemented by subclasses)."""
        raise NotImplementedError
    
    def get_capabilities(self):
        """Get expert capabilities."""
        return self.metadata.get('capabilities', [])


class ExpertLoader:
    """Loads experts from filesystem."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.loaded_experts = {}
    
    def discover_experts(self):
        """Discover available experts."""
        experts = []
        for expert_dir in self.base_dir.glob('*/'):
            if (expert_dir / 'metadata.yaml').exists():
                experts.append(expert_dir.name)
        return experts
    
    def load_expert(self, expert_id: str):
        """Load an expert by ID."""
        # In real implementation, dynamically load the expert module
        print(f"Loading expert: {expert_id}")
        return None


def main():
    """Main example function."""
    print("=" * 60)
    print("GHST Expert System - Usage Example")
    print("=" * 60)
    
    # Example 1: Discovering experts
    print("\n1. Discovering Available Experts")
    print("-" * 60)
    
    experts_dir = Path('experts/core_experts')
    if not experts_dir.exists():
        experts_dir = Path('../../experts/core_experts')
    
    if experts_dir.exists():
        loader = ExpertLoader(experts_dir)
        available = loader.discover_experts()
        print(f"Found {len(available)} experts:")
        for expert_id in available:
            print(f"  - {expert_id}")
    else:
        print("Experts directory not found (this is a standalone example)")
    
    # Example 2: Using an expert (mock)
    print("\n2. Using an Expert")
    print("-" * 60)
    
    # Mock expert usage
    print("Example: Code Analysis Expert")
    print("\nTask: Analyze this code:")
    sample_code = """
def calculate_sum(a, b, c, d, e, f, g, h):
    total = 0
    total = total + a
    total = total + b
    total = total + c
    total = total + d
    total = total + e
    total = total + f
    total = total + g
    total = total + h
    return total
"""
    print(sample_code)
    
    # Simulate expert analysis result
    print("\nExpert Analysis Result:")
    result = {
        'expert_id': 'code_analysis',
        'expert_name': 'Code Analysis Expert',
        'confidence': 0.85,
        'findings': [
            {
                'category': 'complexity',
                'severity': 'medium',
                'message': 'Function has too many parameters',
                'recommendation': 'Consider using a configuration object or *args'
            },
            {
                'category': 'code_smell',
                'severity': 'low',
                'message': 'Repeated pattern detected',
                'recommendation': 'Use sum() with a list or tuple: sum([a, b, c, d, e, f, g, h])'
            }
        ],
        'requires_human_review': True
    }
    
    print(f"Expert: {result['expert_name']}")
    print(f"Confidence: {result['confidence']*100:.0f}%")
    print(f"\nFindings: {len(result['findings'])}")
    
    for i, finding in enumerate(result['findings'], 1):
        print(f"\n{i}. {finding['category'].upper()} ({finding['severity']})")
        print(f"   Issue: {finding['message']}")
        print(f"   Recommendation: {finding['recommendation']}")
    
    if result['requires_human_review']:
        print("\n⚠️  Human review required before applying changes")
    
    # Example 3: Expert capabilities
    print("\n3. Expert Capabilities")
    print("-" * 60)
    
    capabilities = [
        {
            'name': 'Static Code Analysis',
            'description': 'Analyze code structure and quality',
            'offline_capable': True
        },
        {
            'name': 'Design Pattern Recognition',
            'description': 'Identify and suggest design patterns',
            'offline_capable': True
        },
        {
            'name': 'Code Smell Detection',
            'description': 'Detect code smells and anti-patterns',
            'offline_capable': True
        }
    ]
    
    print("Code Analysis Expert Capabilities:")
    for cap in capabilities:
        offline = "✓" if cap['offline_capable'] else "✗"
        print(f"  [{offline}] {cap['name']}")
        print(f"      {cap['description']}")
    
    # Example 4: Best practices
    print("\n4. Best Practices")
    print("-" * 60)
    print("""
Best practices when using experts:

1. Always validate AI recommendations
   - Review findings before applying changes
   - Understand the reasoning behind recommendations
   - Test changes thoroughly

2. Use appropriate experts for tasks
   - Match expert specialization to your needs
   - Combine multiple experts when needed
   - Consider expert confidence scores

3. Provide good context
   - Include relevant code and context
   - Specify language and framework
   - Describe the task clearly

4. Human oversight required
   - Never auto-execute without review
   - Verify expert recommendations
   - Make final decisions yourself

5. Contribute improvements
   - Report issues with expert analysis
   - Suggest new capabilities
   - Share custom experts with community
    """)
    
    print("\n" + "=" * 60)
    print("Example Complete! 👻")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Read docs/EXPERT_SYSTEM.md for detailed documentation")
    print("2. Check experts/README.md to create custom experts")
    print("3. Review CONTRIBUTING.md to contribute")


if __name__ == '__main__':
    main()
