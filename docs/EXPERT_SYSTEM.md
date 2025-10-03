# GHST Expert System Documentation

## Overview

The GHST Expert System is a modular, extensible framework for domain-specific AI assistance. Each expert is self-contained with its own metadata, tools, and knowledge fragments.

## Architecture

### Component Structure

```
experts/
├── core_experts/           # Built-in system experts
│   ├── code_analysis/
│   │   ├── expert.py          # Expert implementation
│   │   ├── metadata.yaml      # Expert configuration
│   │   ├── fragments/         # Knowledge fragments
│   │   └── __init__.py
│   ├── debugging/
│   ├── problem_solving/
│   └── ...
├── custom/                 # User-created experts
│   └── my_expert/
└── README.md
```

## Expert Metadata Schema

### metadata.yaml

```yaml
# Expert Identity
name: "Code Analysis Expert"
id: "code_analysis"
version: "1.0.0"
author: "GHST Team"
created: "2024-01-01"
updated: "2024-01-15"

# Expertise Definition
specialization: "Code quality analysis, design patterns, best practices"
expertise_level: "PhD"
domain: "Software Engineering"
sub_domains:
  - "Static Analysis"
  - "Design Patterns"
  - "Code Quality"

# Capabilities
capabilities:
  - name: "Static Code Analysis"
    description: "Analyze code structure and quality"
    offline_capable: true
  - name: "Design Pattern Recognition"
    description: "Identify and suggest design patterns"
    offline_capable: true
  - name: "Code Smell Detection"
    description: "Detect code smells and anti-patterns"
    offline_capable: true

# Tools and Dependencies
tools:
  - "ast_analyzer"
  - "complexity_calculator"
  - "style_checker"

dependencies:
  python: ">=3.8"
  packages:
    - "ast"
    - "inspect"
  optional:
    - "pylint"
    - "radon"

# Operational Settings
offline_capable: true
requires_internet: false
cache_enabled: true
max_concurrent_tasks: 5
timeout_seconds: 30

# Safety and Ethics
safety:
  require_approval: true
  validation_level: "standard"  # minimal, standard, strict
  auto_execute: false
  experimental: false

# Performance
performance:
  priority: "normal"  # low, normal, high
  resource_intensive: false
  estimated_response_time: "1-5 seconds"

# Integration
interfaces:
  - "cli"
  - "api"
  - "gui"

output_formats:
  - "json"
  - "yaml"
  - "text"
```

## Expert Implementation

### Base Expert Class

```python
"""
Base Expert Class

All experts must inherit from BaseExpert and implement required methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml


class BaseExpert(ABC):
    """Base class for all GHST experts."""
    
    def __init__(self, expert_dir: Path):
        """
        Initialize expert.
        
        Args:
            expert_dir: Path to expert directory
        """
        self.expert_dir = expert_dir
        self.metadata = self._load_metadata()
        self.name = self.metadata.get('name', 'Unknown')
        self.id = self.metadata.get('id', 'unknown')
        self.fragments_dir = expert_dir / 'fragments'
        self.cache = {}
        
    def _load_metadata(self) -> Dict[str, Any]:
        """Load expert metadata from YAML file."""
        metadata_file = self.expert_dir / 'metadata.yaml'
        if metadata_file.exists():
            with open(metadata_file) as f:
                return yaml.safe_load(f)
        return {}
    
    @abstractmethod
    def analyze(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a task and provide expert recommendations.
        
        Args:
            task: Task description and context
            
        Returns:
            Analysis results with recommendations
            
        Example:
            >>> expert.analyze({
            ...     'type': 'code_review',
            ...     'code': 'def hello(): print("world")',
            ...     'context': {'language': 'python'}
            ... })
            {
                'expert_id': 'code_analysis',
                'findings': [...],
                'confidence': 0.85,
                'requires_human_review': True
            }
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[Dict[str, Any]]:
        """
        Return list of expert capabilities.
        
        Returns:
            List of capability dictionaries
        """
        pass
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate expert output before returning.
        
        Args:
            output: Expert output to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['expert_id', 'confidence', 'requires_human_review']
        return all(field in output for field in required_fields)
    
    def load_fragment(self, fragment_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a knowledge fragment.
        
        Args:
            fragment_name: Name of fragment to load
            
        Returns:
            Fragment data or None if not found
        """
        fragment_file = self.fragments_dir / f"{fragment_name}.json"
        if fragment_file.exists():
            import json
            with open(fragment_file) as f:
                return json.load(f)
        return None
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return expert metadata."""
        return self.metadata.copy()
    
    def is_offline_capable(self) -> bool:
        """Check if expert can work offline."""
        return self.metadata.get('offline_capable', False)
    
    def requires_approval(self) -> bool:
        """Check if expert output requires human approval."""
        safety = self.metadata.get('safety', {})
        return safety.get('require_approval', True)
```

### Example Expert Implementation

```python
"""
Code Analysis Expert

Analyzes code for quality, patterns, and best practices.
"""

from typing import Dict, Any, List
from .base import BaseExpert


class CodeAnalysisExpert(BaseExpert):
    """Expert in code analysis and quality assessment."""
    
    def __init__(self, expert_dir):
        super().__init__(expert_dir)
        self.tools = self.metadata.get('tools', [])
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> List[Dict[str, Any]]:
        """Load design patterns from fragments."""
        patterns = []
        patterns_dir = self.fragments_dir / 'patterns'
        if patterns_dir.exists():
            for pattern_file in patterns_dir.glob('*.json'):
                pattern = self.load_fragment(f'patterns/{pattern_file.stem}')
                if pattern:
                    patterns.append(pattern)
        return patterns
    
    def analyze(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code for quality and patterns.
        
        Args:
            task: Dictionary with 'code' and optional 'context'
            
        Returns:
            Analysis results
        """
        code = task.get('code', '')
        context = task.get('context', {})
        
        findings = []
        
        # Analyze complexity
        complexity_finding = self._analyze_complexity(code)
        if complexity_finding:
            findings.append(complexity_finding)
        
        # Check for patterns
        pattern_findings = self._detect_patterns(code)
        findings.extend(pattern_findings)
        
        # Check code smells
        smell_findings = self._detect_code_smells(code)
        findings.extend(smell_findings)
        
        return {
            'expert_id': self.id,
            'expert_name': self.name,
            'analysis_type': 'code_quality',
            'findings': findings,
            'confidence': self._calculate_confidence(findings),
            'requires_human_review': True,
            'recommendations': self._generate_recommendations(findings),
            'metadata': {
                'analyzed_at': self._get_timestamp(),
                'code_length': len(code),
                'language': context.get('language', 'unknown')
            }
        }
    
    def _analyze_complexity(self, code: str) -> Optional[Dict[str, Any]]:
        """Analyze code complexity."""
        # Simplified complexity analysis
        lines = code.split('\n')
        if len(lines) > 50:
            return {
                'category': 'complexity',
                'severity': 'medium',
                'message': 'Function is too long',
                'recommendation': 'Consider breaking into smaller functions',
                'location': {'start_line': 1, 'end_line': len(lines)}
            }
        return None
    
    def _detect_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Detect design patterns in code."""
        findings = []
        
        for pattern in self.patterns:
            if self._matches_pattern(code, pattern):
                findings.append({
                    'category': 'design_pattern',
                    'severity': 'info',
                    'message': f"Detected {pattern['name']} pattern",
                    'recommendation': pattern.get('best_practice', ''),
                    'confidence': 0.7
                })
        
        return findings
    
    def _detect_code_smells(self, code: str) -> List[Dict[str, Any]]:
        """Detect code smells."""
        findings = []
        
        # Example: Detect long parameter lists
        if 'def ' in code and code.count(',') > 5:
            findings.append({
                'category': 'code_smell',
                'severity': 'low',
                'message': 'Long parameter list detected',
                'recommendation': 'Consider using a configuration object'
            })
        
        return findings
    
    def _calculate_confidence(self, findings: List[Dict]) -> float:
        """Calculate overall confidence score."""
        if not findings:
            return 0.5
        
        confidences = [f.get('confidence', 0.8) for f in findings]
        return sum(confidences) / len(confidences)
    
    def _generate_recommendations(self, findings: List[Dict]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        for finding in findings:
            if rec := finding.get('recommendation'):
                recommendations.append(rec)
        
        return recommendations
    
    def _matches_pattern(self, code: str, pattern: Dict) -> bool:
        """Check if code matches a design pattern."""
        # Simplified pattern matching
        indicators = pattern.get('indicators', [])
        return any(indicator in code for indicator in indicators)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_capabilities(self) -> List[Dict[str, Any]]:
        """Return expert capabilities."""
        return self.metadata.get('capabilities', [])
```

## Knowledge Fragments

### Fragment Structure

```json
{
  "name": "Singleton Pattern",
  "type": "design_pattern",
  "category": "creational",
  "description": "Ensure a class has only one instance",
  "indicators": [
    "__new__",
    "_instance",
    "getInstance"
  ],
  "best_practice": "Use module-level variables in Python instead",
  "examples": [
    {
      "language": "python",
      "code": "class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance"
    }
  ],
  "references": [
    "Gang of Four Design Patterns"
  ]
}
```

### Fragment Categories

- **patterns/**: Design patterns
- **best_practices/**: Coding best practices
- **common_issues/**: Common problems and solutions
- **tools/**: Tool configurations and usage
- **templates/**: Code templates

## Expert Loader

### Discovering Experts

```python
"""Expert Loader for dynamic expert discovery and loading."""

from pathlib import Path
from typing import Dict, List, Optional
import importlib.util


class ExpertLoader:
    """Loads and manages expert modules."""
    
    def __init__(self, experts_base_dir: Path):
        self.experts_base_dir = experts_base_dir
        self.loaded_experts = {}
    
    def discover_experts(self) -> List[str]:
        """
        Discover all available experts.
        
        Returns:
            List of expert IDs
        """
        expert_ids = []
        
        for expert_dir in self.experts_base_dir.glob('*/'):
            if expert_dir.is_dir():
                metadata_file = expert_dir / 'metadata.yaml'
                if metadata_file.exists():
                    expert_ids.append(expert_dir.name)
        
        return expert_ids
    
    def load_expert(self, expert_id: str) -> Optional[BaseExpert]:
        """
        Load an expert by ID.
        
        Args:
            expert_id: Expert identifier
            
        Returns:
            Expert instance or None if not found
        """
        if expert_id in self.loaded_experts:
            return self.loaded_experts[expert_id]
        
        expert_dir = self.experts_base_dir / expert_id
        if not expert_dir.exists():
            return None
        
        # Load expert module
        expert_file = expert_dir / 'expert.py'
        if not expert_file.exists():
            return None
        
        spec = importlib.util.spec_from_file_location(
            f"experts.{expert_id}",
            expert_file
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find expert class
        for item_name in dir(module):
            item = getattr(module, item_name)
            if (isinstance(item, type) and 
                issubclass(item, BaseExpert) and 
                item is not BaseExpert):
                expert = item(expert_dir)
                self.loaded_experts[expert_id] = expert
                return expert
        
        return None
    
    def get_expert_metadata(self, expert_id: str) -> Optional[Dict]:
        """Get expert metadata without loading the expert."""
        expert_dir = self.experts_base_dir / expert_id
        metadata_file = expert_dir / 'metadata.yaml'
        
        if metadata_file.exists():
            import yaml
            with open(metadata_file) as f:
                return yaml.safe_load(f)
        
        return None
```

## Best Practices

### 1. Expert Design
- Focus on a single domain or expertise area
- Make experts as self-contained as possible
- Minimize external dependencies
- Support offline operation when feasible

### 2. Safety and Ethics
- Always require human approval for critical actions
- Include confidence scores with all outputs
- Validate inputs and outputs
- Document limitations and biases

### 3. Performance
- Cache frequently used data
- Load fragments lazily
- Set appropriate timeouts
- Use async operations for long tasks

### 4. Testing
- Unit test all expert methods
- Test with various inputs and edge cases
- Validate metadata schema
- Test offline capabilities

### 5. Documentation
- Document all capabilities in metadata
- Provide usage examples
- Explain confidence scoring
- Document fragment formats

## Usage Examples

### Loading and Using an Expert

```python
from pathlib import Path
from experts.loader import ExpertLoader

# Initialize loader
experts_dir = Path('experts/core_experts')
loader = ExpertLoader(experts_dir)

# Discover available experts
available = loader.discover_experts()
print(f"Available experts: {available}")

# Load specific expert
code_expert = loader.load_expert('code_analysis')

# Use expert
result = code_expert.analyze({
    'code': '''
def calculate_total(a, b, c, d, e, f, g):
    return a + b + c + d + e + f + g
''',
    'context': {
        'language': 'python',
        'purpose': 'code_review'
    }
})

# Process results
if result['requires_human_review']:
    print("Human review required!")
    
for finding in result['findings']:
    print(f"{finding['severity']}: {finding['message']}")
    print(f"  Recommendation: {finding['recommendation']}")
```

### Creating a Custom Expert

```python
# 1. Create directory structure
mkdir -p experts/custom/my_expert/fragments

# 2. Create metadata.yaml
cat > experts/custom/my_expert/metadata.yaml << EOF
name: "My Custom Expert"
id: "my_expert"
version: "1.0.0"
specialization: "Custom domain expertise"
EOF

# 3. Create expert.py
cat > experts/custom/my_expert/expert.py << EOF
from experts.base import BaseExpert

class MyExpert(BaseExpert):
    def analyze(self, task):
        return {
            'expert_id': self.id,
            'findings': [],
            'confidence': 0.9,
            'requires_human_review': True
        }
    
    def get_capabilities(self):
        return self.metadata.get('capabilities', [])
EOF

# 4. Test expert
python -c "
from pathlib import Path
from experts.loader import ExpertLoader

loader = ExpertLoader(Path('experts/custom'))
expert = loader.load_expert('my_expert')
result = expert.analyze({'test': 'data'})
print(result)
"
```

## Troubleshooting

### Expert Not Loading

Check:
1. Expert directory exists
2. `metadata.yaml` is valid YAML
3. `expert.py` has expert class
4. Expert class inherits from `BaseExpert`
5. Required methods are implemented

### Import Errors

Ensure:
1. All dependencies are installed
2. Python path includes expert directory
3. `__init__.py` exists if needed
4. Module names don't conflict

### Performance Issues

Optimize:
1. Cache frequently used data
2. Load fragments lazily
3. Use appropriate timeouts
4. Profile expert code

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines on contributing experts to GHST.

---

Happy expert development! 👻
