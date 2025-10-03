# Contributing to GHST

Thank you for your interest in contributing to GHST! We welcome contributions from everyone. Here are some guidelines to help you get started.

## How to Contribute
1. **Fork the Repository**: Start by forking the repository to your own GitHub account.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
3. **Create a New Branch**: Create a new branch for your feature or bug fix.
4. **Make Changes**: Implement your changes, ensuring you follow the project's coding style and conventions.
5. **Commit Your Changes**: Write clear and concise commit messages that describe your changes.
6. **Push to Your Fork**: Push your changes to your forked repository.
7. **Open a Pull Request**: Go to the original repository and open a pull request, describing your changes and why they should be merged.

## Guidelines
- Follow the existing code style.
- Write meaningful commit messages.
- Include tests for new features or bug fixes, if applicable.
- Ensure your code is well-documented.

## Contributing to the Expert System

GHST features a modular expert system. You can contribute new experts or improve existing ones:

### Adding a New Expert

1. **Create Expert Directory**:
```bash
mkdir -p experts/custom/your_expert_name
```

2. **Define Expert Metadata** (`metadata.yaml`):
```yaml
name: "Your Expert Name"
id: "your_expert_id"
version: "1.0.0"
specialization: "Your domain expertise"
expertise_level: "PhD"
domain: "Your Domain"

capabilities:
  - "Capability 1"
  - "Capability 2"

safety:
  require_approval: true
  validation_level: "standard"
```

3. **Implement Expert Class** (`expert.py`):
```python
from typing import Dict, Any, List

class YourExpert:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name')
    
    def analyze(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide expert analysis."""
        return {
            'expert_id': self.config['id'],
            'findings': [],
            'requires_human_review': True
        }
    
    def get_capabilities(self) -> List[str]:
        """Return expert capabilities."""
        return self.config.get('capabilities', [])
```

4. **Test Your Expert**:
- Ensure it follows modularity principles
- Validate human oversight requirements
- Test offline capabilities

5. **Submit Pull Request**:
- Include comprehensive documentation
- Provide usage examples
- Explain the expert's purpose and value

### Modifying Existing Experts

- Maintain backward compatibility when possible
- Update version numbers appropriately
- Document all changes in commit messages
- Test thoroughly before submitting

### Expert System Best Practices

1. **Modularity**: Keep experts focused on single domains
2. **Self-Contained**: Include all necessary tools and data
3. **Human Oversight**: Always require validation for critical decisions
4. **Documentation**: Clearly document capabilities and limitations
5. **Safety**: Include appropriate disclaimers and validation

See `experts/README.md` for detailed expert development guidelines.

## Branch Organization

GHST uses a branch-based organization for domain-specific features:

### Main Branch
- Contains universal LLM core functionality only
- No domain-specific features
- Stable, production-ready code

### Feature Branches
- `feature/*` - New features
- `expert/*` - Expert system additions/modifications
- `plugin/*` - Plugin system additions
- `docs/*` - Documentation updates
- `fix/*` - Bug fixes

### Domain-Specific Branches
- Keep domain-specific code in separate branches
- Examples: `music-theory`, `3d-printing`, `ui-ux-design`
- Merge to main only when universally applicable

### Branch Naming Convention
- Use descriptive, lowercase names with hyphens
- Prefix with category (feature/, expert/, domain/)
- Example: `expert/code-analysis-improvements`

## Code Quality Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write docstrings for all public functions and classes
- Maximum line length: 88 characters (Black standard)

### Documentation
- Update README.md for user-facing changes
- Add docstrings with examples for complex functions
- Include safety disclaimers for AI-generated content
- Document assumptions and limitations

### Testing
- Add tests for new functionality
- Ensure existing tests pass
- Test edge cases and error conditions
- Include integration tests for experts

## Repository Modularity

When contributing, maintain the modular structure:

### Core Components (Universal)
- AI collaboration framework
- Plugin system infrastructure
- Configuration management
- Base expert classes
- Utilities and helpers

### Domain-Specific Components
- Keep in separate branches or clearly marked directories
- Document domain requirements
- Make dependencies optional
- Provide fallback behavior

### Example: Good Modularity
```python
# Good: Optional domain-specific import
try:
    from domain_specific import SpecialTool
    DOMAIN_AVAILABLE = True
except ImportError:
    DOMAIN_AVAILABLE = False

def process_task(task):
    if DOMAIN_AVAILABLE:
        return SpecialTool().process(task)
    return basic_process(task)
```

## Contribution Checklist

Before submitting your pull request:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Expert metadata complete (if applicable)
- [ ] Safety requirements addressed
- [ ] Human oversight implemented where needed
- [ ] Backward compatibility maintained
- [ ] Commit messages are clear and descriptive
- [ ] Changes are focused and minimal

## Getting Help

- **Documentation**: See `docs/` directory
- **Examples**: Check `examples/` for code samples
- **Expert System**: Read `experts/README.md`
- **Issues**: Browse existing issues for similar questions
- **Discussions**: Start a discussion for design questions

## Code of Conduct
By participating in this project, you agree to abide by the Code of Conduct. Please read it to understand our expectations for participation.

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- Expert metadata for expert authors
- README.md for major feature additions

Thank you for considering contributing to GHST! Your help is greatly appreciated! 👻