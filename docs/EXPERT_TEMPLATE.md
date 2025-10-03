# Expert Template

This document provides a standardized template for creating new AI experts in the GHST Mixture of Experts (MoE) system.

## Expert File Structure

```
experts/
├── {domain}/
│   ├── {expert_id}/
│   │   ├── metadata.json          # Expert metadata
│   │   ├── expert_class.py        # Expert implementation
│   │   ├── fragments/             # Saved research/tools
│   │   │   ├── articles/          # Research articles
│   │   │   ├── tools/             # Utility scripts
│   │   │   └── models/            # Any ML models or data
│   │   └── README.md              # Expert documentation
```

## 1. Metadata File (metadata.json)

Every expert must have a `metadata.json` file describing its capabilities:

```json
{
  "expert_id": "example_expert",
  "name": "Example Expert",
  "domain": "example_domain",
  "expertise": "Broad area of expertise",
  "specialization": "Specific focus area",
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
  ],
  "enabled": true,
  "version": "1.0.0",
  "description": "Detailed description of what this expert does",
  "fragments_path": "experts/example_domain/example_expert/fragments/",
  "model_path": null,
  "dependencies": [
    "dependency1",
    "dependency2"
  ],
  "author": "Your Name",
  "created": "2025-01-01",
  "last_updated": "2025-01-01"
}
```

### Metadata Fields

- **expert_id** (required): Unique identifier, use snake_case
- **name** (required): Human-readable name
- **domain** (required): One of the predefined domains (see domains list below)
- **expertise** (required): Broad area of knowledge (1-2 sentences)
- **specialization** (required): Specific focus (1 sentence)
- **keywords** (required): List of relevant terms for query matching
- **enabled** (optional): Whether expert is active (default: true)
- **version** (required): Semantic versioning (e.g., "1.0.0")
- **description** (optional): Detailed description
- **fragments_path** (optional): Path to saved resources
- **model_path** (optional): Path to ML models or data
- **dependencies** (optional): List of required packages
- **author** (optional): Creator's name
- **created** (optional): Creation date
- **last_updated** (optional): Last update date

### Available Domains

- `core` - Fundamental operations
- `music_theory` - Music and audio
- `3d_printing` - Manufacturing and 3D printing
- `ui_ux_design` - User interface and experience
- `engineering` - Engineering disciplines
- `mathematics` - Mathematical operations
- `security` - Security and safety
- `performance` - Performance optimization
- `documentation` - Technical writing
- `testing` - Quality assurance
- `deployment` - CI/CD and releases
- `ai_ml` - Machine learning
- `data_science` - Data processing
- `ethics` - Ethical AI
- `research` - Research and innovation

## 2. Expert Class (expert_class.py)

Every expert should implement the `BaseGhost` interface:

```python
"""
{Expert Name} - {Brief Description}

{Detailed description of the expert's purpose and capabilities}
"""

from core.src.ai_collaboration.expert_manager import BaseGhost


class ExampleGhost(BaseGhost):
    """
    {One-line description}
    
    Specialization: {specialization}
    Domain: {domain}
    """
    
    def __init__(self, ghost_id: str, manager):
        """
        Initialize the expert.
        
        Args:
            ghost_id: Unique identifier for this expert instance
            manager: Reference to ExpertManager
        """
        super().__init__(ghost_id, manager)
        
        # Expert-specific initialization
        self.expertise = "Your expertise area"
        self.specialization = "Your specialization"
        self.domain = "your_domain"
        
        # Load any necessary resources
        self._load_resources()
    
    def _load_resources(self):
        """Load saved fragments or models."""
        # Implementation for loading offline resources
        pass
    
    def monitor_cycle(self):
        """
        Main monitoring loop for this expert.
        
        This method is called periodically when the expert is active.
        Implement domain-specific monitoring and analysis here.
        """
        # Example monitoring tasks
        tasks = [
            "Task 1: Description",
            "Task 2: Description",
            "Task 3: Description"
        ]
        
        task = tasks[int(time.time()) % len(tasks)]
        self.manager.log_activity(f"🎯 {self.ghost_id}: {task}")
    
    def analyze_task(self, task: str) -> dict:
        """
        Analyze a specific task and provide recommendations.
        
        Args:
            task: Task description or query
        
        Returns:
            Dictionary containing analysis and recommendations
        """
        # Implement task analysis logic
        return {
            'analysis_type': self.domain,
            'recommendations': [
                "Recommendation 1",
                "Recommendation 2",
                "Recommendation 3"
            ],
            'confidence': 0.85,
            'priority': 'medium',
            'estimated_time': '30-60 minutes',
            'references': self._get_relevant_fragments(task)
        }
    
    def _get_relevant_fragments(self, task: str) -> list:
        """
        Retrieve relevant saved fragments for the task.
        
        Args:
            task: Task description
        
        Returns:
            List of relevant fragment references
        """
        # Implementation for finding relevant offline resources
        return []
    
    def provide_solution(self, problem: str, context: dict = None) -> dict:
        """
        Provide a solution for a specific problem.
        
        Args:
            problem: Problem description
            context: Additional context information
        
        Returns:
            Dictionary containing solution and supporting information
        """
        # Implement solution generation logic
        return {
            'solution': "Detailed solution description",
            'steps': [
                "Step 1: ...",
                "Step 2: ...",
                "Step 3: ..."
            ],
            'code_examples': [],
            'warnings': [],
            'further_reading': []
        }
```

## 3. Fragments Directory

The fragments directory stores offline resources for the expert:

### articles/
Research articles, papers, or documentation relevant to the expert's domain.

**Format**: Markdown files with metadata

```markdown
---
title: "Article Title"
author: "Author Name"
date: "2025-01-01"
source: "URL or publication"
tags: ["tag1", "tag2"]
---

# Article Content

Article text here...
```

### tools/
Utility scripts, calculators, or helper functions.

**Format**: Python scripts with documentation

```python
"""
Tool Name - Brief Description

Usage:
    python tool_name.py [arguments]
"""

def main():
    # Tool implementation
    pass

if __name__ == "__main__":
    main()
```

### models/
ML models, datasets, or other data files specific to the expert.

**Structure**:
```
models/
├── model_name/
│   ├── model.pkl          # Serialized model
│   ├── config.json        # Model configuration
│   └── README.md          # Model documentation
```

## 4. Expert README

Each expert should have a README.md documenting:

```markdown
# {Expert Name}

## Overview
Brief description of the expert and its purpose.

## Expertise
- Primary expertise area
- Specialization
- Key capabilities

## Keywords
List of relevant keywords for this expert.

## Use Cases
Examples of when this expert should be consulted:
- Use case 1
- Use case 2
- Use case 3

## Fragments
Description of available offline resources:
- **Articles**: List of saved articles
- **Tools**: Available utility tools
- **Models**: Any ML models or datasets

## Dependencies
List of required packages:
```bash
pip install dependency1 dependency2
```

## Integration
How to integrate this expert into the system:
```python
from experts.{domain}.{expert_id}.expert_class import ExampleGhost

# Register with ExpertManager
expert_manager.register_expert(ExampleGhost('example_id', expert_manager))
```

## Examples
Usage examples and sample queries.

## Author
- Name: Your Name
- Contact: your.email@example.com
- GitHub: @yourusername

## License
Specify the license for this expert's code and resources.
```

## 5. Testing

Create tests for your expert in `tests/test_{expert_id}.py`:

```python
"""
Tests for {Expert Name}
"""

import unittest
from experts.{domain}.{expert_id}.expert_class import ExampleGhost


class TestExampleGhost(unittest.TestCase):
    """Test cases for ExampleGhost."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = MockExpertManager()
        self.expert = ExampleGhost('test_expert', self.manager)
    
    def test_initialization(self):
        """Test expert initialization."""
        self.assertEqual(self.expert.domain, 'example_domain')
        self.assertIsNotNone(self.expert.expertise)
    
    def test_analyze_task(self):
        """Test task analysis."""
        result = self.expert.analyze_task("test task")
        self.assertIn('recommendations', result)
        self.assertIn('confidence', result)
    
    def test_provide_solution(self):
        """Test solution generation."""
        result = self.expert.provide_solution("test problem")
        self.assertIn('solution', result)
        self.assertIn('steps', result)


if __name__ == '__main__':
    unittest.main()
```

## 6. Registration

To register your expert with the system:

1. Create metadata file
2. Implement expert class
3. Add fragments (if applicable)
4. Create tests
5. Update the expert registry:

```python
from core.src.ai_collaboration.expert_metadata import ExpertMetadata, ExpertDomain

# Create metadata
metadata = ExpertMetadata(
    expert_id='example_expert',
    name='Example Expert',
    domain=ExpertDomain.EXAMPLE_DOMAIN,
    expertise='Broad expertise',
    specialization='Specific specialization',
    keywords=['keyword1', 'keyword2'],
    description='Detailed description'
)

# Register with registry
registry.register(metadata)
```

## 7. Best Practices

1. **Clear Naming**: Use descriptive names for experts and domains
2. **Focused Expertise**: Each expert should have a specific, well-defined purpose
3. **Comprehensive Keywords**: Include all relevant terms for accurate routing
4. **Quality Fragments**: Curate high-quality, relevant offline resources
5. **Documentation**: Provide clear documentation and examples
6. **Testing**: Write thorough tests for your expert
7. **Version Control**: Use semantic versioning and document changes
8. **Dependencies**: Minimize external dependencies when possible
9. **Performance**: Ensure expert operations are efficient
10. **Ethics**: Consider ethical implications of your expert's recommendations

## 8. Contribution Checklist

Before submitting a new expert:

- [ ] Created metadata.json with all required fields
- [ ] Implemented expert class inheriting from BaseGhost
- [ ] Added relevant keywords for router matching
- [ ] Created fragments directory with resources
- [ ] Written comprehensive README
- [ ] Added tests covering main functionality
- [ ] Updated expert registry
- [ ] Documented use cases and examples
- [ ] Verified integration with MoE system
- [ ] Checked for security and ethical considerations
- [ ] Added author and license information

## Questions?

For help creating experts, see:
- `docs/MOE_ARCHITECTURE.md` - System architecture
- `docs/CONTRIBUTING.md` - Contribution guidelines
- `core/src/ai_collaboration/expert_metadata.py` - Metadata system
- `core/src/ai_collaboration/moe_router.py` - Router implementation
