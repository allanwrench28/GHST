# Mixture of Experts (MoE) Architecture

## Overview

The GHST repository implements a **Mixture of Experts (MoE)** approach to organize and coordinate AI experts for various coding and problem-solving tasks. This architecture enables dynamic expert selection based on query analysis, providing modular, domain-specific responses.

## Core Concepts

### 1. Expert Metadata System

Each expert in the GHST system has associated metadata that describes:

- **Expert ID**: Unique identifier
- **Name**: Human-readable name
- **Domain**: Primary domain of expertise (e.g., UI/UX, Engineering, Music Theory)
- **Expertise**: Broad area of knowledge
- **Specialization**: Specific focus area
- **Keywords**: Terms that indicate relevance
- **Version**: Expert version for tracking updates
- **Fragments Path**: Location of saved research/tools for offline use
- **Model Path**: Location of any specific models or data

### 2. Expert Domains

Experts are organized into logical domains:

- **Core**: Fundamental analysis, optimization, and error handling
- **Music Theory**: Audio, sound design, musical composition
- **3D Printing**: Mesh processing, slicing, manufacturing
- **UI/UX Design**: Interface design, color theory, typography
- **Engineering**: Physics, materials science, mechanical engineering
- **Mathematics**: Computational geometry, algorithms, optimization
- **Security**: Vulnerability analysis, safe coding practices
- **Performance**: Code optimization, profiling
- **Documentation**: Technical writing, API docs
- **Testing**: Test strategies, quality assurance
- **Deployment**: CI/CD, release management
- **AI/ML**: Machine learning, neural networks
- **Data Science**: Data processing, analytics
- **Ethics**: Responsible AI, bias mitigation
- **Research**: FOSS solutions, innovation

### 3. MoE Router

The router is the central component that:

1. **Analyzes Queries**: Parses user queries to understand intent and domain
2. **Selects Experts**: Identifies the most relevant experts based on:
   - Keyword matching
   - Domain relevance
   - Specialization alignment
   - Historical performance
3. **Scores and Ranks**: Assigns relevance scores to experts
4. **Coordinates Responses**: Manages expert interactions and combines insights

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Query                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       MoE Router                             │
│  • Query Analysis                                            │
│  • Domain Detection                                          │
│  • Expert Scoring                                            │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ├──────────────┬──────────────┬────────────
                    ▼              ▼              ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │   Expert 1     │ │   Expert 2     │ │   Expert 3     │
        │  (Relevance:   │ │  (Relevance:   │ │  (Relevance:   │
        │    0.85)       │ │    0.72)       │ │    0.45)       │
        └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
                 │                  │                  │
                 └─────────┬────────┴─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Combined        │
                  │  Response        │
                  └─────────────────┘
```

## Expert Selection Algorithm

The router uses a multi-factor scoring system:

1. **Keyword Matching** (up to 0.6 points)
   - Keywords from query found in expert's keyword list
   - More matches = higher score

2. **Expertise Match** (0.3 points)
   - Query mentions expert's primary expertise area

3. **Specialization Match** (0.2 points)
   - Query relates to expert's specific specialization

4. **Domain Match** (0.1 points)
   - Query falls within expert's domain

5. **Context Modifiers**
   - Historical performance (+0.2)
   - User preferences (+0.1)
   - Primary domain boost (+0.15)

**Maximum Score**: 1.0

**Selection Threshold**: Configurable (default 0.1)

## Usage Examples

### Example 1: UI Design Query

**Query**: "How can I improve the color scheme of my interface?"

**Router Analysis**:
- Detects UI/UX domain
- Keywords: "color", "interface"
- Selects:
  1. `colorscience_ghost` (score: 0.85) - Direct color expertise
  2. `uxdesign_ghost` (score: 0.62) - Interface design
  3. `typography_ghost` (score: 0.25) - Visual design context

### Example 2: 3D Printing Optimization

**Query**: "Optimize mesh processing for faster slicing"

**Router Analysis**:
- Detects 3D Printing + Performance domains
- Keywords: "optimize", "mesh", "slicing"
- Selects:
  1. `optimization_ghost` (score: 0.90) - Algorithm optimization
  2. `analysis_ghost` (score: 0.75) - Mesh analysis
  3. `performance_ghost` (score: 0.65) - Performance tuning

### Example 3: Security Review

**Query**: "Check this code for security vulnerabilities"

**Router Analysis**:
- Detects Security domain
- Keywords: "security", "vulnerabilities"
- Selects:
  1. `security_ghost` (score: 0.95) - Security analysis
  2. `ethics_ghost` (score: 0.40) - Responsible practices
  3. `testing_ghost` (score: 0.35) - Quality assurance

## Integration with Existing System

The MoE system integrates with the existing `ExpertManager` by:

1. **Maintaining Backward Compatibility**: All existing ghost classes continue to work
2. **Adding Dynamic Selection**: Router can now select appropriate experts
3. **Enabling Extensibility**: New experts can be added via metadata
4. **Supporting Offline Fragments**: Experts can have saved research/tools

## Branch Organization Strategy

For future implementation across branches:

### Main Branch (Core LLM)
- Core experts (analysis, optimization, error, research)
- MoE router infrastructure
- Base expert classes
- Registry system

### Domain-Specific Branches
Each branch contains:
- Domain experts with full implementation
- Saved fragments (research articles, tools, models)
- Domain-specific configurations
- Metadata files

**Branch Examples**:
- `domain/music-theory` - Music and audio experts
- `domain/3d-printing` - 3D printing specialists
- `domain/ui-ux-design` - Design experts
- `domain/engineering` - Engineering specialists

### Dynamic Loading
The core system can:
1. Detect available domain branches
2. Load relevant experts on-demand
3. Pull in saved fragments when needed
4. Cache frequently used domains

## Configuration

Expert configuration is stored in JSON format:

```json
{
  "expert_id": "colorscience_ghost",
  "name": "Color Science Ghost",
  "domain": "ui_ux_design",
  "expertise": "Color theory and color science",
  "specialization": "Color harmony and perception",
  "keywords": ["color", "design", "visual", "aesthetics"],
  "enabled": true,
  "version": "1.0.0",
  "fragments_path": "fragments/ui_ux/color_science/",
  "model_path": null,
  "dependencies": []
}
```

## Benefits

1. **Modularity**: Experts can be added, removed, or updated independently
2. **Scalability**: System can grow to hundreds of specialized experts
3. **Efficiency**: Only relevant experts are invoked for each query
4. **Maintainability**: Clear separation of concerns
5. **Community-Driven**: Easy for contributors to add new experts
6. **Offline Capability**: Saved fragments enable offline operation

## Future Enhancements

1. **Machine Learning Router**: Train router on query history for better selection
2. **Expert Collaboration**: Enable experts to consult each other
3. **Dynamic Expert Loading**: Load experts from branches on-demand
4. **Expert Performance Tracking**: Monitor and optimize expert effectiveness
5. **User Customization**: Allow users to prefer certain experts
6. **Expert Ensembles**: Combine multiple experts for complex queries

## API Reference

See:
- `core/src/ai_collaboration/expert_metadata.py` - Metadata definitions
- `core/src/ai_collaboration/moe_router.py` - Router implementation
- `docs/EXPERT_TEMPLATE.md` - Template for creating new experts
