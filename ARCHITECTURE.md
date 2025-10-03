# GHST Architecture - Modular Offline LLM System

## Overview

GHST is a modular offline LLM system where the **main branch** provides the core AI engine and infrastructure, while **specialized branches** contribute domain-specific expertise that can be dynamically loaded as plugins.

## Architecture Components

### Core System (Main Branch)

```
GHST/
├── core/
│   ├── llm_engine/              # Offline LLM implementation
│   │   ├── ghost_core.py        # Main LLM orchestrator
│   │   ├── context_manager.py   # Handles expertise plugin contexts
│   │   ├── memory_system.py     # Fragmented data storage/retrieval
│   │   └── plugin_loader.py     # Dynamic branch loading system
│   ├── ghosts/                  # Base ghost AI personalities
│   │   ├── base_ghost.py        # Abstract ghost class
│   │   ├── core_ghost.py        # General purpose ghost
│   │   └── system_ghost.py      # System management ghost
│   ├── src/                     # Existing codebase (preserved)
│   │   ├── ai_collaboration/    # Ghost management
│   │   ├── plugins/             # Plugin system
│   │   └── utils/               # Utilities
│   │       └── branch_scanner.py # Scans for expertise branches
│   └── config/
│       ├── llm_config.yaml      # LLM engine settings
│       ├── ghost_config.yaml    # Ghost personality settings
│       └── plugin_config.yaml   # Available expertise branches
└── data/
    ├── base_knowledge/          # Core LLM training data
    ├── plugin_cache/            # Downloaded expertise modules
    └── conversation_memory/     # Chat history and context
```

### Expertise Branches (Modular Plugins)

Each branch provides specialized expertise:

```
GHST/ (expertise-branch-name)
├── expertise/
│   ├── manifest.yaml           # Branch metadata and capabilities
│   ├── expert_ghosts/          # Specialized domain ghosts
│   │   ├── expert_1.py
│   │   ├── expert_2.py
│   │   └── expert_3.py
│   ├── knowledge_fragments/    # Pre-processed expertise data
│   │   ├── category_1/
│   │   ├── category_2/
│   │   └── category_3/
│   └── tools/                  # Domain-specific utilities
│       └── tool_1.py
├── training_data/              # Raw training materials
│   └── ...
└── auto_update/
    ├── research_scraper.py     # Continuously updates knowledge
    └── optimization_engine.py  # Self-improving algorithms
```

## How It Works

### 1. System Initialization

1. **Core LLM Engine** (`ghost_core.py`) starts up
2. **Context Manager** initializes context window management
3. **Memory System** prepares fragmented storage
4. **Core Ghosts** (general purpose, system manager) activate
5. **Branch Scanner** discovers available expertise branches

### 2. Plugin Loading

When expertise is needed:

1. User requests specific domain knowledge (e.g., "3D printing help")
2. **Core Ghost** identifies relevant expertise branch
3. **Plugin Loader** downloads/loads branch from cache
4. **Expert Ghosts** from branch are activated
5. **Knowledge Fragments** are indexed in memory system
6. **Context Manager** adds expertise to LLM context

### 3. Query Processing

1. User sends query
2. **Core Ghost** determines if expert consultation is needed
3. Query routed to appropriate **Expert Ghost(s)**
4. **Memory System** retrieves relevant knowledge fragments
5. **Context Manager** builds combined context
6. **LLM Engine** processes with full context
7. Response returned to user

### 4. Plugin Unloading

When expertise is no longer needed:

1. User or system decides to unload plugin
2. **Expert Ghosts** are deactivated
3. **Knowledge Fragments** removed from active memory
4. **Context Manager** clears expertise context
5. Cache retained for fast reload if needed

## Key Features

### ✅ Modular Design
- Core engine separate from expertise
- Add/remove domains without affecting core
- Easy to create new expertise branches

### ✅ Offline-First
- Everything runs locally
- No cloud dependencies
- Pre-trained expert knowledge

### ✅ Dynamic Loading
- Load only needed expertise
- Conserves resources
- Fast context switching

### ✅ Self-Improving
- Expertise branches can auto-update
- Optimization engines improve over time
- Validation ensures quality

### ✅ Scalable
- Unlimited expertise domains
- Efficient memory management
- Handles large knowledge bases

## Ghost System

### Ghost Types

1. **Core Ghosts** (always active)
   - Core Assistant: General queries and routing
   - System Manager: Infrastructure monitoring

2. **Expert Ghosts** (loaded from branches)
   - Domain specialists (e.g., 3D Printing Expert)
   - Collaborate with core ghosts
   - Access to specialized knowledge

### Ghost Communication

Ghosts can:
- Discuss queries together
- Share knowledge across domains
- Reach consensus on complex questions
- Escalate to human when uncertain

## Configuration

### LLM Configuration (`llm_config.yaml`)
- LLM backend selection (Ollama, LM Studio, etc.)
- Model settings and quantization
- Context window management
- Generation parameters

### Ghost Configuration (`ghost_config.yaml`)
- Personality settings
- Response style preferences
- Collaboration rules
- Expert coordination

### Plugin Configuration (`plugin_config.yaml`)
- Available expertise branches
- Auto-load preferences
- Cache management
- Validation rules

## Example: 3D Printing Expertise Branch

### Branch Structure
```
GHST/ (slicer-branch)
├── expertise/
│   ├── manifest.yaml
│   ├── expert_ghosts/
│   │   ├── material_scientist_ghost.py
│   │   ├── mechanical_engineer_ghost.py
│   │   └── slicer_expert_ghost.py
│   ├── knowledge_fragments/
│   │   ├── materials_database/
│   │   ├── slicing_algorithms/
│   │   └── troubleshooting_guides/
│   └── tools/
│       ├── gcode_analyzer.py
│       └── mesh_optimizer.py
└── ...
```

### Usage Flow

1. User: "How do I fix warping on my 3D prints?"
2. Core Ghost recognizes 3D printing query
3. System loads `slicer-branch` if not already loaded
4. Material Scientist Ghost analyzes warping causes
5. Mechanical Engineer Ghost suggests structural fixes
6. Slicer Expert Ghost recommends settings
7. Knowledge fragments provide specific solutions
8. Combined response returned to user

## Development Workflow

### Creating a New Expertise Branch

1. Create new branch from main
2. Set up expertise structure:
   ```bash
   mkdir -p expertise/{expert_ghosts,knowledge_fragments,tools}
   ```
3. Create `manifest.yaml` with metadata
4. Implement expert ghost classes
5. Add knowledge fragments
6. Test with core system
7. Document capabilities

### Adding Expert Ghosts

Expert ghosts inherit from `BaseGhost`:

```python
from core.ghosts.base_ghost import BaseGhost

class MyExpertGhost(BaseGhost):
    def __init__(self):
        super().__init__(
            ghost_id="my_expert",
            name="My Expert",
            specialization="My Domain"
        )
    
    def process_query(self, query, context=None):
        # Process domain-specific query
        return response
    
    def get_capabilities(self):
        return {
            "type": "expert",
            "capabilities": [...]
        }
```

## Future Enhancements

- [ ] Semantic search for knowledge fragments
- [ ] Multi-modal expertise (images, code, etc.)
- [ ] Plugin sandboxing for security
- [ ] Distributed expertise loading
- [ ] Collaborative learning between branches
- [ ] Plugin marketplace/repository

## Migration Path

The new architecture is designed to coexist with existing code:

1. ✅ Core syntax errors fixed
2. ✅ New modular structure created
3. ⏳ Existing functionality preserved
4. ⏳ Gradual migration of features
5. ⏳ Full integration completed

This allows incremental adoption without breaking existing workflows.
