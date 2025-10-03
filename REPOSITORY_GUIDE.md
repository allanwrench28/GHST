# GHST Repository Organization Guide

## Overview

This document provides comprehensive guidelines for organizing and maintaining the GHST repository to ensure modularity, clarity, and community engagement.

## Repository Structure

```
GHST/
├── core/                   # Core LLM functionality (universal)
│   ├── src/
│   │   ├── ai_collaboration/   # Expert system core
│   │   ├── plugins/            # Plugin system
│   │   ├── ui_components/      # UI framework
│   │   └── utils/              # Utilities
│   ├── config/                 # Configuration files
│   ├── docs/                   # Core documentation
│   └── requirements.txt        # Core dependencies
├── experts/                # Modular expert system
│   ├── core_experts/           # Built-in experts
│   ├── custom/                 # User-created experts
│   └── README.md              # Expert documentation
├── plugins/                # Plugin extensions
│   ├── builtin/               # Built-in plugins
│   └── custom/                # User plugins
├── docs/                   # Documentation
│   ├── REPOSITORY_RULESET.md
│   ├── GUI_STANDARDS.md
│   └── ...
├── examples/               # Usage examples
├── releases/               # Release builds
├── install_wizard.py       # Installation wizard
├── CONTRIBUTING.md         # Contribution guidelines
├── REPOSITORY_GUIDE.md     # This file
└── README.md              # Main documentation
```

## Branch Organization

### Main Branch (`main`)

**Purpose**: Universal LLM core functionality only

**Contents**:
- Core AI collaboration framework
- Base expert system (no domain-specific experts)
- Plugin system infrastructure
- Configuration management
- Universal utilities
- Installation tools

**What NOT to Include**:
- Domain-specific features
- Experimental code
- Platform-specific implementations
- Third-party integrations (unless universally needed)

### Feature Branches

**Naming Convention**: `feature/descriptive-name`

**Purpose**: New features under development

**Examples**:
- `feature/improved-plugin-loader`
- `feature/expert-caching`
- `feature/multi-language-support`

**Lifecycle**:
1. Branch from `main`
2. Develop and test
3. Submit PR to `main`
4. Merge when approved
5. Delete branch after merge

### Expert Branches

**Naming Convention**: `expert/expert-domain`

**Purpose**: Developing new expert modules

**Examples**:
- `expert/music-theory`
- `expert/data-science`
- `expert/web-development`

**Process**:
1. Create branch for expert development
2. Test expert thoroughly
3. Merge to `main` when ready (expert goes to `experts/core_experts/`)
4. Or keep in `experts/custom/` for community experts

### Domain-Specific Branches

**Naming Convention**: `domain/area-name`

**Purpose**: Domain-specific features and tools

**Examples**:
- `domain/3d-printing` - 3D printing slicer and tools
- `domain/music-theory` - Music composition and analysis
- `domain/ui-ux` - UI/UX design tools

**Characteristics**:
- Remain separate from main
- Can pull from main for core updates
- Maintain their own releases
- Document unique requirements

**Best Practices**:
- Clear README explaining domain purpose
- Documented dependencies
- Maintain compatibility with core
- Regular sync with main for updates

### Release Branches

**Naming Convention**: `release/vX.Y.Z`

**Purpose**: Prepare and stabilize releases

**Process**:
1. Branch from `main` or relevant feature branch
2. Final testing and bug fixes
3. Version bumps and changelog updates
4. Tag and create release
5. Merge back to `main`

## Code Organization

### Universal Code (Goes in Main)

✅ **Include**:
- Core AI/LLM interfaces
- Base expert classes
- Plugin system base
- Configuration management
- Logging and monitoring
- Error handling
- Base UI components
- Core utilities

❌ **Do NOT Include**:
- Domain-specific algorithms
- Specialized tools
- Platform-specific implementations
- Experimental features
- Third-party service integrations (unless universal)

### Domain-Specific Code (Separate Branches)

Keep these in domain branches:
- Specialized algorithms
- Domain-specific experts
- Industry-specific tools
- Vertical integrations
- Experimental features

## Managing Domain-Specific Features

### Option 1: Plugin Architecture
Make domain features available as plugins:

```python
# In domain branch
plugins/
└── domain_3d_printing/
    ├── plugin.yaml
    ├── slicer.py
    └── mesh_tools.py
```

### Option 2: Conditional Imports
Use optional imports for domain features:

```python
try:
    from domain_features import SpecialTool
    DOMAIN_AVAILABLE = True
except ImportError:
    DOMAIN_AVAILABLE = False
    SpecialTool = None
```

### Option 3: Separate Repositories
For large domain-specific projects:
- Create separate repository
- Reference core GHST as dependency
- Maintain independence

## Archiving and Cleanup

### When to Archive Branches

Archive branches that are:
- Completed and merged
- No longer maintained
- Superseded by newer implementations
- Experimental and failed

### Archiving Process

1. **Document**: Update changelog with archive reason
2. **Tag**: Create tag before archiving
3. **Archive**: Use GitHub's archive feature or delete

```bash
# Tag before archiving
git tag archive/branch-name branch-name
git push origin archive/branch-name

# Delete branch
git branch -d branch-name
git push origin --delete branch-name
```

### Renaming Branches

For clarity, rename branches:

```bash
# Rename local branch
git branch -m old-name new-name

# Update remote
git push origin -u new-name
git push origin --delete old-name
```

## Release Management

### Version Numbering

Follow Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Process

1. **Prepare Release Branch**:
```bash
git checkout -b release/v1.2.0 main
```

2. **Update Version Numbers**:
- `version_info.txt`
- `pyproject.toml`
- `setup.py`

3. **Update Documentation**:
- `CHANGELOG.md`
- `README.md`
- Release notes

4. **Test Thoroughly**:
- Run all tests
- Test installation wizard
- Validate documentation

5. **Create Release**:
```bash
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

6. **Merge Back**:
```bash
git checkout main
git merge --no-ff release/v1.2.0
git push origin main
```

## Maintaining Modularity

### Core Functionality Checklist

Before adding to core, ask:
- [ ] Is this universally applicable?
- [ ] Does it have minimal dependencies?
- [ ] Is it well-documented?
- [ ] Does it follow coding standards?
- [ ] Is it tested?
- [ ] Does it maintain backward compatibility?

### Domain Feature Checklist

For domain-specific features:
- [ ] Is it clearly domain-specific?
- [ ] Can it be implemented as a plugin?
- [ ] Are dependencies documented?
- [ ] Does it work independently?
- [ ] Is fallback behavior provided?

## Community Contributions

### Accepting Contributions

Evaluate contributions based on:
1. **Alignment**: Fits GHST vision and architecture
2. **Quality**: Well-written, tested, documented
3. **Modularity**: Maintains separation of concerns
4. **Completeness**: Includes tests, docs, examples
5. **Safety**: Includes appropriate safeguards

### Contribution Types

**Core Contributions** (to main):
- Bug fixes
- Performance improvements
- Core feature enhancements
- Documentation improvements
- Test additions

**Expert Contributions** (to expert branches):
- New expert modules
- Expert improvements
- Expert documentation
- Expert tools and utilities

**Domain Contributions** (to domain branches):
- Domain-specific tools
- Specialized algorithms
- Vertical integrations
- Domain documentation

## Best Practices

### 1. Keep Main Clean
- Only universal functionality
- Well-tested code
- Comprehensive documentation
- No experimental features

### 2. Document Everything
- READMEs for all directories
- Inline code comments
- API documentation
- Usage examples

### 3. Test Thoroughly
- Unit tests for core functionality
- Integration tests for systems
- Manual testing for UI
- Performance testing for critical paths

### 4. Communicate Changes
- Clear commit messages
- Detailed PR descriptions
- Changelog updates
- Release notes

### 5. Maintain Compatibility
- Semantic versioning
- Deprecation warnings
- Migration guides
- Backward compatibility

## Automation

### Recommended Automations

1. **CI/CD Pipeline**:
- Automated testing
- Code quality checks
- Documentation generation
- Release automation

2. **Branch Protection**:
- Require PR reviews
- Require passing tests
- Prevent force pushes
- Enforce code owners

3. **Issue Management**:
- Issue templates
- Automated labeling
- Stale issue cleanup
- Release planning

## Support and Resources

### For Contributors
- `CONTRIBUTING.md` - Contribution guidelines
- `experts/README.md` - Expert system guide
- `docs/` - Technical documentation
- `examples/` - Code examples

### For Maintainers
- `REPOSITORY_GUIDE.md` - This document
- `docs/REPOSITORY_RULESET.md` - Repository rules
- Release checklists
- Review guidelines

## Questions?

- **General**: Open a GitHub Discussion
- **Bug Reports**: Create an Issue
- **Feature Requests**: Create an Issue with `feature` label
- **Security**: Email security@ghst.dev (when available)

---

**Remember**: The goal is to make GHST functional, user-friendly, and modular while fostering community engagement. Keep code clean, documentation clear, and contributions welcome! 👻
