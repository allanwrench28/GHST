# Branch Organization Strategy

This document describes the branch organization strategy for the GHST repository using the Mixture of Experts (MoE) approach.

## Overview

GHST uses a branch-based organization where:

- **Main Branch**: Contains the core LLM functionality and universal experts
- **Domain Branches**: Contain domain-specific experts and resources
- **Feature Branches**: For development of new features
- **Release Branches**: For stable releases

## Branch Naming Conventions

### Main Branch
- `main` - The primary branch containing core functionality

### Domain Branches
Domain branches follow the pattern: `domain/{domain-name}`

Examples:
- `domain/music-theory` - Music and audio experts
- `domain/3d-printing` - 3D printing and manufacturing experts
- `domain/ui-ux-design` - UI/UX design experts
- `domain/engineering` - Engineering specialists
- `domain/data-science` - Data science experts

### Feature Branches
Feature branches follow the pattern: `feature/{feature-name}`

Examples:
- `feature/moe-router-enhancements`
- `feature/expert-performance-tracking`
- `feature/dynamic-expert-loading`

### Experimental Branches
Experimental branches follow the pattern: `experimental/{experiment-name}`

Examples:
- `experimental/ml-router`
- `experimental/expert-collaboration`

## Branch Structure

### Main Branch

The main branch should contain:

```
main/
├── core/
│   ├── src/
│   │   ├── ai_collaboration/
│   │   │   ├── expert_manager.py      # Core expert management
│   │   │   ├── expert_metadata.py     # Metadata system
│   │   │   ├── moe_router.py          # MoE router
│   │   │   └── expert_classes.py      # Base classes
│   │   ├── plugins/                   # Plugin system
│   │   └── utils/                     # Utilities
│   └── config/                        # Core configurations
├── docs/                              # Documentation
│   ├── MOE_ARCHITECTURE.md
│   ├── EXPERT_TEMPLATE.md
│   └── BRANCH_ORGANIZATION.md
├── tests/                             # Core tests
└── README.md
```

**What belongs in main:**
- Core LLM functionality
- MoE infrastructure (router, registry, metadata)
- Universal experts (analysis, optimization, error handling)
- Base classes and interfaces
- Documentation
- Build and deployment scripts

**What does NOT belong in main:**
- Domain-specific experts (beyond core)
- Experimental features
- Large datasets or models
- Domain-specific tools and fragments
- Backup or archive files

### Domain Branches

Each domain branch should contain:

```
domain/{domain-name}/
├── experts/
│   ├── {expert_id_1}/
│   │   ├── metadata.json
│   │   ├── expert_class.py
│   │   ├── fragments/
│   │   │   ├── articles/
│   │   │   ├── tools/
│   │   │   └── models/
│   │   └── README.md
│   └── {expert_id_2}/
│       └── ...
├── domain_config.json                 # Domain configuration
├── tests/                             # Domain-specific tests
└── README.md                          # Domain documentation
```

**Domain Configuration File** (`domain_config.json`):

```json
{
  "domain": "music_theory",
  "display_name": "Music Theory & Audio",
  "description": "Experts specializing in music theory, audio processing, and sound design",
  "version": "1.0.0",
  "experts": [
    "music_theory_ghost",
    "audio_processing_ghost",
    "sound_design_ghost"
  ],
  "maintainers": [
    {
      "name": "Maintainer Name",
      "github": "username",
      "email": "email@example.com"
    }
  ],
  "dependencies": [
    "librosa>=0.9.0",
    "music21>=7.0.0"
  ],
  "keywords": [
    "music",
    "audio",
    "sound",
    "composition",
    "theory"
  ],
  "status": "active",
  "last_updated": "2025-01-01"
}
```

## Domain Organization

### Current Domains

1. **Core** (`main` branch)
   - Universal functionality
   - Analysis, optimization, error handling
   - Research and innovation

2. **Music Theory** (`domain/music-theory`)
   - Music composition
   - Audio processing
   - Sound design
   - Musical theory

3. **3D Printing** (`domain/3d-printing`)
   - Mesh processing
   - Slicing algorithms
   - Manufacturing optimization
   - Quality control

4. **UI/UX Design** (`domain/ui-ux-design`)
   - Color theory
   - Typography
   - Interface design
   - User experience

5. **Engineering** (`domain/engineering`)
   - Mechanical engineering
   - Materials science
   - Physics simulations
   - Manufacturing

6. **Data Science** (`domain/data-science`)
   - Data analysis
   - Statistical modeling
   - Machine learning
   - Data visualization

7. **Security** (`domain/security`)
   - Code security
   - Vulnerability analysis
   - Best practices
   - Ethical AI

### Creating a New Domain Branch

1. **Plan Your Domain**
   - Define scope and boundaries
   - Identify experts needed
   - List required resources

2. **Create Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b domain/your-domain-name
   ```

3. **Set Up Structure**
   ```bash
   mkdir -p experts
   touch domain_config.json
   touch README.md
   ```

4. **Create Domain Config**
   - Fill in `domain_config.json` with domain details
   - List all experts
   - Specify dependencies
   - Add maintainer information

5. **Add Experts**
   - Create expert directories
   - Implement expert classes
   - Add metadata files
   - Include fragments/resources

6. **Document Domain**
   - Write comprehensive README
   - Explain domain purpose
   - List experts and capabilities
   - Provide usage examples

7. **Test Domain**
   - Create tests for all experts
   - Verify integration with core
   - Test expert routing

8. **Submit for Review**
   - Push branch to repository
   - Open pull request
   - Request review from maintainers

## Merging Strategy

### Main Branch Updates
- Protected branch requiring reviews
- Automated tests must pass
- Documentation must be updated
- No direct commits (use PRs)

### Domain Branch Updates
- Domain maintainers can approve changes
- Tests must pass for domain
- Changes should not affect other domains

### Cross-Domain Changes
- Require approval from core maintainers
- Must not break existing functionality
- Should maintain backward compatibility

## Branch Lifecycle

### Active Branches
- Actively maintained
- Receive regular updates
- Part of core system

### Deprecated Branches
- No longer actively maintained
- Marked as deprecated in domain_config.json
- May be archived after notification period

### Archived Branches
- Historical reference only
- Not loaded by default
- Can be restored if needed

### Experimental Branches
- Testing new ideas
- May become domain branches
- Can be deleted if unsuccessful

## Branch Cleanup

### Criteria for Archiving
- No activity for 6+ months
- No maintainers available
- Superseded by newer domain
- Low usage metrics

### Cleanup Process
1. Announce deprecation (1 month notice)
2. Mark as deprecated in config
3. Allow community to adopt or fork
4. Archive after notice period
5. Update documentation

### Redundant Branches to Clean Up
Based on repository analysis, consider archiving:
- Backup branches (e.g., `backup-*`)
- Old release branches (keep only last 2-3)
- Abandoned feature branches
- Duplicate development branches

## Dynamic Expert Loading

### Future Enhancement
The MoE system will support dynamic loading of domain experts:

```python
from core.src.ai_collaboration.domain_loader import DomainLoader

# Load domain experts on-demand
loader = DomainLoader()
music_experts = loader.load_domain('music-theory')

# Unload when not needed
loader.unload_domain('music-theory')
```

### Benefits
- Reduced memory footprint
- Faster startup time
- Load only needed domains
- Easy domain updates

## Best Practices

### For Main Branch
1. Keep it minimal and universal
2. No domain-specific code
3. Maintain backward compatibility
4. Comprehensive documentation
5. Rigorous testing

### For Domain Branches
1. Clear scope definition
2. Independent from other domains
3. Complete documentation
4. Quality fragments/resources
5. Active maintenance

### For All Branches
1. Follow naming conventions
2. Regular updates and maintenance
3. Clear commit messages
4. Code reviews before merging
5. Automated testing

## Migration Guide

### Moving Experts to Domain Branches

If you have experts in main that should be in domain branches:

1. **Identify Domain**
   - Determine appropriate domain
   - Check if domain branch exists

2. **Create Domain Branch** (if needed)
   - Follow creation process above

3. **Move Expert Code**
   ```bash
   git checkout domain/your-domain
   git checkout main -- path/to/expert
   git commit -m "Move expert to domain branch"
   ```

4. **Update Main Branch**
   ```bash
   git checkout main
   git rm -r path/to/expert
   git commit -m "Remove expert from main (moved to domain branch)"
   ```

5. **Update References**
   - Update imports
   - Update documentation
   - Update tests

6. **Test Integration**
   - Ensure expert still works
   - Verify routing works
   - Run all tests

## Questions and Support

For questions about branch organization:
- Open an issue with tag `branch-organization`
- Contact domain maintainers
- See `docs/MOE_ARCHITECTURE.md`
- See `CONTRIBUTING.md`

## Future Enhancements

1. **Automated Branch Management**
   - Automatic domain detection
   - Branch health monitoring
   - Usage analytics

2. **Domain Marketplace**
   - Discover available domains
   - Rate and review domains
   - Community contributions

3. **Version Management**
   - Domain versioning
   - Compatibility tracking
   - Automatic updates

4. **Performance Optimization**
   - Lazy loading
   - Caching strategies
   - Pre-loading hints
