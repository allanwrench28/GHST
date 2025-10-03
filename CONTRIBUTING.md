# Contributing to GHST

Thank you for your interest in contributing to GHST! We welcome contributions from everyone. Here are some guidelines to help you get started.

## How to Contribute

### General Contributions
1. **Fork the Repository**: Start by forking the repository to your own GitHub account.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
3. **Create a New Branch**: Create a new branch for your feature or bug fix.
4. **Make Changes**: Implement your changes, ensuring you follow the project's coding style and conventions.
5. **Commit Your Changes**: Write clear and concise commit messages that describe your changes.
6. **Push to Your Fork**: Push your changes to your forked repository.
7. **Open a Pull Request**: Go to the original repository and open a pull request, describing your changes and why they should be merged.

### Contributing AI Experts

GHST uses a **Mixture of Experts (MoE)** architecture where specialized AI experts handle different domains. Contributing a new expert is a great way to extend GHST's capabilities!

#### Creating a New Expert

1. **Choose Your Domain**: Select an appropriate domain for your expert:
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

2. **Create Expert Structure**: Follow the template in `docs/EXPERT_TEMPLATE.md`:
   ```
   experts/
   ├── {domain}/
   │   ├── {expert_id}/
   │   │   ├── metadata.json          # Expert metadata
   │   │   ├── expert_class.py        # Expert implementation
   │   │   ├── fragments/             # Saved research/tools
   │   │   └── README.md              # Expert documentation
   ```

3. **Define Metadata**: Create a `metadata.json` file:
   ```json
   {
     "expert_id": "your_expert_id",
     "name": "Your Expert Name",
     "domain": "your_domain",
     "expertise": "Broad area of expertise",
     "specialization": "Specific focus area",
     "keywords": ["keyword1", "keyword2", "keyword3"],
     "enabled": true,
     "version": "1.0.0",
     "description": "What your expert does"
   }
   ```

4. **Implement Expert Class**: Create your expert by extending `BaseGhost`:
   ```python
   from core.src.ai_collaboration.expert_manager import BaseGhost
   
   class YourExpert(BaseGhost):
       def __init__(self, ghost_id: str, manager):
           super().__init__(ghost_id, manager)
           self.expertise = "Your expertise"
           self.specialization = "Your specialization"
       
       def monitor_cycle(self):
           # Implement monitoring logic
           pass
       
       def analyze_task(self, task: str) -> dict:
           # Implement task analysis
           return {
               'recommendations': [],
               'confidence': 0.85
           }
   ```

5. **Add Fragments** (Optional): Include offline resources:
   - **Articles**: Research papers, documentation
   - **Tools**: Utility scripts, calculators
   - **Models**: ML models, datasets

6. **Write Tests**: Create tests in `tests/test_{expert_id}.py`

7. **Register Expert**: Add your expert to the registry

8. **Submit PR**: Open a pull request with:
   - Expert implementation
   - Metadata file
   - Documentation
   - Tests
   - Example use cases

#### Expert Contribution Checklist

- [ ] Created metadata.json with all required fields
- [ ] Implemented expert class inheriting from BaseGhost
- [ ] Added relevant keywords for router matching
- [ ] Created fragments directory with resources (if applicable)
- [ ] Written comprehensive README
- [ ] Added tests covering main functionality
- [ ] Documented use cases and examples
- [ ] Verified integration with MoE system
- [ ] Checked for security and ethical considerations

For detailed guidance, see `docs/EXPERT_TEMPLATE.md` and `docs/MOE_ARCHITECTURE.md`.

### Managing Branches and Domains

#### Branch Organization

GHST uses branches to organize domain-specific experts:

- **Main Branch**: Core LLM functionality and universal experts
- **Domain Branches**: Specialized experts for specific domains (e.g., `domain/music-theory`, `domain/3d-printing`)

#### Creating a Domain Branch

1. Create a new branch from main: `git checkout -b domain/your-domain`
2. Add domain-specific experts and resources
3. Include a `domain_config.json` file:
   ```json
   {
     "domain": "your_domain",
     "description": "Domain description",
     "experts": ["expert_id_1", "expert_id_2"],
     "maintainers": ["username1", "username2"]
   }
   ```
4. Submit a PR to create the domain branch

#### Adding Metadata to Experts

All experts should have comprehensive metadata:

- **Expertise**: What the expert knows
- **Specialization**: What the expert focuses on
- **Keywords**: Terms for query matching
- **Fragments**: Saved resources for offline use
- **Dependencies**: Required packages

#### Adding Fragments and Tools

Fragments are offline resources that experts can reference:

1. Create a `fragments/` directory in your expert folder
2. Organize by type:
   - `articles/` - Research papers, documentation
   - `tools/` - Scripts, utilities
   - `models/` - ML models, datasets
3. Include metadata for each fragment
4. Document usage in the expert README

## Guidelines

- Follow the existing code style.
- Write meaningful commit messages.
- Include tests for new features or bug fixes, if applicable.
- Ensure your code is well-documented.
- For experts, follow the template in `docs/EXPERT_TEMPLATE.md`
- Keep experts focused on specific domains
- Curate high-quality fragments and resources
- Consider performance and efficiency
- Address ethical implications in your contributions

## Code of Conduct

By participating in this project, you agree to abide by the Code of Conduct. Please read it to understand our expectations for participation.

## Getting Help

- **MoE Architecture**: See `docs/MOE_ARCHITECTURE.md`
- **Expert Template**: See `docs/EXPERT_TEMPLATE.md`
- **Issues**: Open an issue for questions or problems
- **Discussions**: Join discussions for ideas and feedback

Thank you for considering contributing to GHST! Your help is greatly appreciated!