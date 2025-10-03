# Mixture of Experts (MoE) System - Quick Start Guide

Welcome to the GHST Mixture of Experts system! This guide will help you get started with understanding and using the MoE framework.

## What is the MoE System?

The Mixture of Experts (MoE) system is a modular architecture that allows GHST to dynamically select and coordinate specialized AI experts based on user queries. Instead of having a monolithic AI system, MoE enables:

- **Domain Specialization**: Experts focused on specific areas (Music Theory, 3D Printing, UI/UX, etc.)
- **Dynamic Selection**: Automatically choose the best experts for each query
- **Scalability**: Easily add new experts without modifying core code
- **Efficiency**: Only load and use relevant experts for each task

## Key Components

### 1. Expert Metadata (`expert_metadata.py`)
Defines the structure and properties of each expert, including:
- Domain (e.g., music_theory, ui_ux_design)
- Expertise and specialization
- Keywords for query matching
- Fragments (saved resources for offline use)

### 2. MoE Router (`moe_router.py`)
Routes queries to appropriate experts by:
- Analyzing query content
- Scoring expert relevance
- Selecting top experts
- Tracking usage statistics

### 3. MoE Integration (`moe_integration.py`)
Integrates the MoE system with existing ExpertManager:
- Backward compatibility
- Seamless expert coordination
- Query processing
- Statistics and monitoring

## Quick Start

### Basic Usage

```python
from core.src.ai_collaboration.expert_manager import ExpertManager
from core.src.ai_collaboration.moe_integration import integrate_moe_with_expert_manager

# Initialize ExpertManager
expert_manager = ExpertManager()

# Integrate MoE system
moe = integrate_moe_with_expert_manager(expert_manager)

# Query the system
result = moe.query_experts("How can I improve the color scheme of my interface?")

# View selected experts
for expert in result['experts']:
    print(f"Expert: {expert['name']} (Score: {expert['relevance_score']:.2f})")
    print(f"Reasoning: {expert['reasoning']}")

# View analyses
for analysis in result['analyses']:
    print(f"\nAnalysis from {analysis['expert_name']}:")
    print(analysis['analysis'])
```

### Get Expert Suggestions for a Task

```python
suggestions = moe.get_expert_suggestions(
    "I need to optimize 3D mesh processing for faster slicing"
)

for suggestion in suggestions:
    print(f"{suggestion['name']}: {suggestion['specialization']}")
    print(f"Relevance: {suggestion['relevance_score']:.2f}")
```

### List Available Domains

```python
domains = moe.list_all_domains()

for domain in domains:
    print(f"{domain['display_name']}: {domain['expert_count']} experts")
    print(f"  Experts: {', '.join(domain['experts'])}")
```

### Get Domain-Specific Experts

```python
ui_experts = moe.get_domain_experts('ui_ux_design')

for expert in ui_experts:
    print(f"{expert['name']}: {expert['specialization']}")
```

### Get System Statistics

```python
stats = moe.get_statistics()

print(f"Total Experts: {stats['total_experts']}")
print(f"Enabled Experts: {stats['enabled_experts']}")
print(f"Total Queries: {stats['router_stats']['total_queries']}")
print(f"\nMost Used Experts:")
for expert in stats['router_stats']['most_used_experts']:
    print(f"  {expert['expert_id']}: {expert['count']} times")
```

## Creating a New Expert

### Step 1: Define Metadata

Create `experts/your_domain/your_expert/metadata.json`:

```json
{
  "expert_id": "your_expert_id",
  "name": "Your Expert Name",
  "domain": "your_domain",
  "expertise": "Your area of expertise",
  "specialization": "Your specific focus",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "version": "1.0.0",
  "description": "What your expert does"
}
```

### Step 2: Implement Expert Class

Create `experts/your_domain/your_expert/expert_class.py`:

```python
from core.src.ai_collaboration.expert_manager import BaseGhost

class YourExpertGhost(BaseGhost):
    """Your expert description."""
    
    def __init__(self, ghost_id: str, manager):
        super().__init__(ghost_id, manager)
        self.expertise = "Your expertise"
        self.specialization = "Your specialization"
    
    def monitor_cycle(self):
        """Periodic monitoring logic."""
        pass
    
    def analyze_task(self, task: str) -> dict:
        """Analyze a task and provide recommendations."""
        return {
            'recommendations': ["Recommendation 1", "Recommendation 2"],
            'confidence': 0.85,
            'priority': 'medium'
        }
```

### Step 3: Register Expert

```python
from core.src.ai_collaboration.expert_metadata import ExpertMetadata, ExpertDomain

metadata = ExpertMetadata(
    expert_id='your_expert_id',
    name='Your Expert Name',
    domain=ExpertDomain.YOUR_DOMAIN,
    expertise='Your expertise',
    specialization='Your specialization',
    keywords=['keyword1', 'keyword2']
)

moe.registry.register(metadata)
```

### Step 4: Add Fragments (Optional)

Create directory structure for saved resources:

```
experts/your_domain/your_expert/fragments/
├── articles/          # Research papers, documentation
├── tools/             # Utility scripts
└── models/            # ML models, datasets
```

## Working with Domains

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

### Creating a Domain Branch

1. Create branch: `git checkout -b domain/your-domain`
2. Create `domain_config.json` (see `docs/examples/domain_config_example.json`)
3. Add experts to the domain
4. Create domain README
5. Submit pull request

## Advanced Features

### Custom Scoring

You can influence expert selection using context:

```python
context = {
    'preferred_experts': ['optimization_ghost'],
    'primary_domain': ExpertDomain.PERFORMANCE,
    'user_preferences': {
        'favorite_experts': ['physics_ghost']
    }
}

result = moe.query_experts("Optimize this code", context)
```

### Enable/Disable Experts

```python
# Disable an expert
moe.disable_expert('expert_id')

# Enable an expert
moe.enable_expert('expert_id')
```

### Add Custom Expert at Runtime

```python
moe.add_custom_expert(
    expert_id='custom_expert',
    name='Custom Expert',
    domain='core',
    expertise='Custom expertise',
    specialization='Custom specialization',
    keywords=['custom', 'expert']
)
```

### Export/Import Registry

```python
# Export registry
moe.export_registry('experts/registry.json')

# Import registry
moe.import_registry('experts/registry.json')
```

## Testing

Run the test suite:

```bash
cd core/src/ai_collaboration
python test_moe_system.py
```

All 20 tests should pass.

## Documentation

- **[MoE Architecture](MOE_ARCHITECTURE.md)** - Detailed system architecture
- **[Expert Template](EXPERT_TEMPLATE.md)** - Complete expert creation guide
- **[Branch Organization](BRANCH_ORGANIZATION.md)** - Branch management strategy
- **[Contributing Guide](../CONTRIBUTING.md)** - Contribution guidelines

## Examples

See `docs/examples/` for:
- `domain_config_example.json` - Example domain configuration
- `expert_metadata_example.json` - Example expert metadata

## Troubleshooting

### No experts selected for query
- Check if keywords match query terms
- Verify experts are enabled
- Try lowering the threshold in router
- Add more keywords to expert metadata

### Import errors
- Ensure all modules are in the correct locations
- Check for relative import issues
- Verify Python path includes core directory

### Expert not responding
- Check if expert is in `active_ghosts`
- Verify expert has `analyze_task` method
- Check logs for errors

## Best Practices

1. **Clear Keywords**: Use descriptive keywords for better matching
2. **Focused Experts**: Each expert should have a specific purpose
3. **Quality Fragments**: Curate high-quality offline resources
4. **Testing**: Always test new experts thoroughly
5. **Documentation**: Document all experts and their capabilities
6. **Version Control**: Use semantic versioning for experts
7. **Performance**: Keep experts lightweight and efficient

## Getting Help

- Open an issue with tag `moe-system`
- See documentation in `docs/`
- Check examples in `docs/examples/`
- Review test cases in `test_moe_system.py`

## Future Enhancements

- **Machine Learning Router**: Train router on query history
- **Dynamic Loading**: Load domain experts from branches on-demand
- **Expert Collaboration**: Enable experts to consult each other
- **Performance Tracking**: Monitor expert effectiveness
- **User Preferences**: Persistent user preferences for experts

## Contributing

We welcome contributions! See `CONTRIBUTING.md` for guidelines on:
- Creating new experts
- Adding domains
- Improving the router
- Adding features

---

**Ready to get started?** Begin by exploring existing experts and trying the quick start examples above!
