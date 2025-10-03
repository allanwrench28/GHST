# GHST Quick Start Guide

Welcome to GHST - a modular offline LLM system with expertise branch plugins!

## What is GHST?

GHST (Ghost in the Shell) is an AI coding engine where:
- **Main Branch** = Core LLM engine with base ghost AI system
- **Other Branches** = Specialized expertise modules (3D printing, web dev, etc.)
- **Plug-and-Play** = Dynamically load/unload expertise as needed
- **Offline-First** = Everything runs locally with pre-trained knowledge

## Quick Start

### 1. Launch GHST

```bash
python3 launch_ghst.py
```

This will:
- Initialize the core LLM engine
- Activate base ghosts (Core Assistant, System Manager)
- Scan for available expertise branches
- Display system status

### 2. Verify Installation

You should see:
```
✅ GHST Core initialized successfully!
============================================================
GHST is ready to assist you!
============================================================
```

### 3. Understanding the Architecture

```
core/
├── llm_engine/          # LLM orchestration
├── ghosts/              # AI personalities
├── config/              # Configuration files
└── src/                 # Existing codebase

data/
├── plugin_cache/        # Cached expertise
└── conversation_memory/ # Chat history

examples/
└── expertise_branch_template/  # Template for new branches
```

## Creating Your First Expertise Branch

### Option 1: Use the Template

```bash
# Create a new branch
git checkout -b my-expertise-branch

# Copy the template
cp -r examples/expertise_branch_template/* .

# Customize manifest.yaml with your domain
# Create your expert ghosts
# Add knowledge fragments
```

### Option 2: Start from Scratch

```bash
# Create branch structure
mkdir -p expertise/{expert_ghosts,knowledge_fragments,tools}
mkdir -p training_data auto_update

# Create manifest.yaml
cat > manifest.yaml << EOF
metadata:
  name: "my-expertise"
  version: "1.0.0"
  description: "My domain expertise"

domain:
  primary: "My Domain"

experts:
  - id: "my_expert"
    name: "My Expert"
    specialization: "My Specialty"
    file: "expert_ghosts/my_expert.py"
EOF
```

## Example: Creating a Simple Expert Ghost

Create `expertise/expert_ghosts/my_expert.py`:

```python
from core.ghosts.base_ghost import BaseGhost
from typing import Dict, Optional

class MyExpertGhost(BaseGhost):
    def __init__(self):
        super().__init__(
            ghost_id="my_expert",
            name="My Expert",
            specialization="My Domain"
        )
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        return f"My Expert: Here's help with {query}"
    
    def get_capabilities(self) -> Dict:
        return {
            "type": "expert",
            "capabilities": ["Domain help", "Troubleshooting"]
        }
```

## Testing Your Expertise Branch

```python
# Test the expert ghost standalone
python3 expertise/expert_ghosts/my_expert.py

# Test with GHST core
python3 -c "
from core.llm_engine.plugin_loader import PluginLoader
loader = PluginLoader()
loader.load_plugin('my-expertise', path='.')
"
```

## Configuration

### LLM Settings (`core/config/llm_config.yaml`)

```yaml
llm:
  backend: "ollama"  # or lm_studio, llamacpp
  model:
    name: "mistral"
    version: "7b-instruct-v0.2"
  context:
    max_tokens: 4096
```

### Ghost Settings (`core/config/ghost_config.yaml`)

```yaml
behavior:
  response_style: "conversational"
  personality:
    formality: 0.5
    verbosity: 0.7
    creativity: 0.6
```

### Plugin Settings (`core/config/plugin_config.yaml`)

```yaml
plugin_system:
  auto_discover: true
  auto_load_on_startup:
    - "my-expertise-branch"
  cache_path: "data/plugin_cache"
```

## Common Use Cases

### Use Case 1: 3D Printing Assistant

```bash
# Create 3D printing expertise branch
git checkout -b slicer-branch

# Add experts:
# - Material Scientist Ghost
# - Mechanical Engineer Ghost
# - Slicer Expert Ghost

# Add knowledge:
# - Materials database
# - Slicing algorithms
# - Troubleshooting guides
```

### Use Case 2: Web Development Assistant

```bash
# Create web dev expertise branch
git checkout -b web-dev-branch

# Add experts:
# - Frontend Ghost (HTML/CSS/JS)
# - Backend Ghost (servers, APIs)
# - Security Ghost

# Add knowledge:
# - Frameworks database
# - Best practices
# - Security patterns
```

### Use Case 3: Data Science Assistant

```bash
# Create data science expertise branch
git checkout -b data-science-branch

# Add experts:
# - Statistics Ghost
# - ML/AI Ghost
# - Visualization Ghost

# Add knowledge:
# - Statistical methods
# - ML algorithms
# - Visualization techniques
```

## Troubleshooting

### Problem: GHST won't start

**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check logs
cat logs/ghst.log
```

### Problem: No expertise branches found

**Solution:**
This is normal for fresh installations. Create your first branch:
```bash
cp -r examples/expertise_branch_template/* /tmp/my-branch
cd /tmp/my-branch
# Customize and test
```

### Problem: Expert ghost import errors

**Solution:**
```python
# Make sure core is in Python path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core"))
```

## Next Steps

1. **Read Full Documentation**
   - `ARCHITECTURE.md` - Complete architecture guide
   - `examples/expertise_branch_template/README.md` - Branch creation guide

2. **Create Your First Branch**
   - Use the template in `examples/`
   - Start with a simple domain you know well
   - Test thoroughly before sharing

3. **Contribute**
   - Share your expertise branches
   - Improve core components
   - Add documentation

4. **Join the Community**
   - Report issues on GitHub
   - Share your branches
   - Help others get started

## Key Concepts

### Ghosts
AI personalities with specific expertise. Can be:
- **Core Ghosts**: General purpose (always active)
- **Expert Ghosts**: Domain specialists (loaded from branches)

### Expertise Branches
Git branches that provide:
- Expert ghosts for a domain
- Knowledge fragments (pre-processed data)
- Tools and utilities
- Training data

### Plugin System
Dynamically loads expertise branches:
- Auto-discovers branches
- Caches for fast loading
- Manages memory efficiently
- Enables on-demand expertise

### Context Management
Efficiently manages LLM context:
- Combines conversation history
- Integrates expertise data
- Stays within token limits
- Optimizes for relevance

## Resources

- **Documentation**: `ARCHITECTURE.md`
- **Examples**: `examples/expertise_branch_template/`
- **Configuration**: `core/config/`
- **Logs**: `logs/ghst.log`

## Help

Need help? Check:
1. This guide (QUICKSTART.md)
2. Full architecture (ARCHITECTURE.md)
3. Example branch template
4. GitHub issues

---

**Ready to build something amazing with GHST?** 🚀👻
