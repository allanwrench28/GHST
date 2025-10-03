# GHST - AI Coding Engine

An AI-driven, natural language coding LLM framework featuring a **Mixture of Experts (MoE)** architecture for intelligent, domain-specific assistance.

## 🎯 What is GHST?

GHST is an advanced AI coding framework that uses a Mixture of Experts approach to provide specialized assistance across multiple domains. Instead of a single monolithic AI, GHST coordinates multiple expert AI agents, each specializing in specific areas like:

- 🎨 **UI/UX Design** - Color theory, typography, interface design
- 🏗️ **Engineering** - Physics, materials science, mechanical engineering
- 🎵 **Music Theory** - Audio processing, composition, harmony
- 🔒 **Security** - Vulnerability analysis, secure coding practices
- ⚡ **Performance** - Code optimization, profiling
- 🔧 **3D Printing** - Mesh processing, slicing algorithms
- 📊 **Data Science** - Data analysis, machine learning
- And many more...

## ✨ Key Features

### Mixture of Experts (MoE) System
- **Dynamic Expert Selection**: Automatically routes queries to the most relevant experts
- **Domain Organization**: Experts organized by specialty (UI/UX, Engineering, Music, etc.)
- **Scalable Architecture**: Easily add new experts without modifying core code
- **Context-Aware Routing**: Considers user preferences and query history

### Modular Design
- **Clean Core**: Universal LLM functionality separate from domain experts
- **Plugin System**: Extensible architecture for custom functionality
- **Branch-Based Domains**: Domain-specific experts in dedicated branches

### Community-Driven
- **Standardized Templates**: Easy expert creation with templates
- **Contribution Guidelines**: Clear process for adding experts and domains
- **Documentation**: Comprehensive guides and examples

## 🚀 Quick Start

### Basic Usage

```python
from core.src.ai_collaboration.expert_manager import ExpertManager
from core.src.ai_collaboration.moe_integration import integrate_moe_with_expert_manager

# Initialize the system
expert_manager = ExpertManager()
moe = integrate_moe_with_expert_manager(expert_manager)

# Query the system
result = moe.query_experts("How can I improve my UI color scheme?")

# View selected experts
for expert in result['experts']:
    print(f"{expert['name']}: {expert['relevance_score']:.2f}")
```

### Try the Demo

```bash
python examples/moe_demo.py
```

This runs 6 demonstrations showing:
1. Basic query routing
2. Domain-specific experts
3. Expert search
4. Available domains
5. Router statistics
6. Context-based selection

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](docs/MOE_README.md)** - Get up and running quickly
- **[Demo Script](examples/moe_demo.py)** - See the system in action

### Architecture
- **[MoE Architecture](docs/MOE_ARCHITECTURE.md)** - System design and components
- **[Implementation Summary](docs/MOE_IMPLEMENTATION_SUMMARY.md)** - Complete overview

### Contributing
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Expert Template](docs/EXPERT_TEMPLATE.md)** - Create new experts
- **[Branch Organization](docs/BRANCH_ORGANIZATION.md)** - Branch management

### Examples
- **[Domain Config Example](docs/examples/domain_config_example.json)** - Domain configuration
- **[Expert Metadata Example](docs/examples/expert_metadata_example.json)** - Expert metadata

## 🎭 Available Domains

- **Core** - Universal functionality (Analysis, Optimization, Error handling)
- **Music Theory** - Music composition, audio processing
- **3D Printing** - Mesh processing, manufacturing
- **UI/UX Design** - Interface design, color theory, typography
- **Engineering** - Physics, materials science, mathematics
- **Security** - Code security, ethical AI
- **Performance** - Optimization, profiling
- **Documentation** - Technical writing
- **Testing** - Quality assurance
- **Deployment** - CI/CD, releases
- **AI/ML** - Machine learning
- **Data Science** - Data processing
- **Ethics** - Responsible AI
- **Research** - Innovation, FOSS solutions

## 🧪 Testing

Run the comprehensive test suite:

```bash
cd core/src/ai_collaboration
python test_moe_system.py
```

**Status**: ✅ All 20 tests passing

## 🤝 Contributing

We welcome contributions! To add a new expert or domain:

1. Review the [Contributing Guide](CONTRIBUTING.md)
2. Use the [Expert Template](docs/EXPERT_TEMPLATE.md)
3. Follow the [Branch Organization](docs/BRANCH_ORGANIZATION.md) strategy
4. Submit a pull request

### Creating a New Expert

```python
from core.src.ai_collaboration.expert_metadata import ExpertMetadata, ExpertDomain

# Define metadata
metadata = ExpertMetadata(
    expert_id='your_expert',
    name='Your Expert Name',
    domain=ExpertDomain.YOUR_DOMAIN,
    expertise='Your expertise area',
    specialization='Your specialization',
    keywords=['keyword1', 'keyword2']
)

# Implement expert class
class YourExpert(BaseGhost):
    def analyze_task(self, task: str) -> dict:
        return {
            'recommendations': ['Recommendation 1', 'Recommendation 2'],
            'confidence': 0.85
        }
```

## 📊 System Statistics

- **Total Experts**: 12+ predefined experts
- **Domains**: 15 domains
- **Test Coverage**: 100% (20/20 tests passing)
- **Documentation**: 60+ pages
- **Lines of Code**: 7,500+

## 🔮 Future Enhancements

- **Dynamic Branch Loading**: Load domain experts on-demand from branches
- **Machine Learning Router**: Train router on query history
- **Expert Collaboration**: Enable experts to consult each other
- **Performance Tracking**: Monitor expert effectiveness
- **Domain Marketplace**: Community domain sharing

## 📄 License

[View License](LICENSE)

## 🙏 Acknowledgments

Built with ❤️ by the GHST community. Special thanks to all contributors!

---

**Ready to get started?** Check out the [Quick Start Guide](docs/MOE_README.md) or run `python examples/moe_demo.py`!
