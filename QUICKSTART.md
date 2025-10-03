# GHST Quick Start Guide

## Installation (2 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/allanwrench28/GHST.git
cd GHST
```

### 2. Run Install Wizard
```bash
# Interactive installation (recommended for first time)
python install_wizard.py

# Automated installation (use defaults)
python install_wizard.py --auto
```

### 3. Activate Virtual Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Launch GHST
```bash
python core/launch_gui.py
```

## What Just Happened?

The install wizard:
- ✅ Checked prerequisites (Python, pip, git)
- ✅ Created directory structure (logs/, exports/, etc.)
- ✅ Set up virtual environment
- ✅ Installed dependencies
- ✅ Generated configuration files
- ✅ Validated installation

## Directory Structure

```
GHST/
├── core/                   # Core LLM functionality
│   ├── src/                # Source code
│   └── requirements.txt    # Dependencies
├── experts/                # Expert system
│   ├── core_experts/       # Built-in experts
│   └── custom/             # Your custom experts
├── plugins/                # Plugin extensions
├── logs/                   # Application logs
├── exports/                # Exported files
├── backups/                # Backups
├── config/user/            # Your configuration
└── install_wizard.py       # Installation tool
```

## Configuration

Edit your settings at: `config/user/settings.yaml`

```yaml
app:
  theme: "ghost_dark"  # or "ghost_light", "professional"
  
expert_system:
  enabled: true
  max_concurrent_experts: 8

syntax_supervisors:
  enabled: true
  scan_interval: 30
```

## Creating Your First Custom Expert

### 1. Create Expert Directory
```bash
mkdir -p experts/custom/my_expert
```

### 2. Create Metadata
Create `experts/custom/my_expert/metadata.yaml`:
```yaml
name: "My Custom Expert"
id: "my_expert"
version: "1.0.0"
specialization: "My domain expertise"
capabilities:
  - "Custom analysis"
safety:
  require_approval: true
```

### 3. Implement Expert
Create `experts/custom/my_expert/expert.py`:
```python
from typing import Dict, Any, List

class MyExpert:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def analyze(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'expert_id': self.config['id'],
            'findings': [],
            'confidence': 0.9,
            'requires_human_review': True
        }
    
    def get_capabilities(self) -> List[str]:
        return self.config.get('capabilities', [])
```

### 4. Test Your Expert
```bash
python examples/experts/example_expert_usage.py
```

## Common Tasks

### Update GHST
```bash
git pull origin main
python install_wizard.py --auto  # Reinstall if needed
```

### View Logs
```bash
tail -f logs/ghst.log
```

### Backup Your Work
```bash
# Backups are automatically created in backups/
ls -la backups/
```

### Add Dependencies
Edit `core/requirements.txt`, then:
```bash
pip install -r core/requirements.txt
```

## Getting Help

- **Documentation:** `docs/` directory
- **Expert System:** `docs/EXPERT_SYSTEM.md`
- **Repository Guide:** `REPOSITORY_GUIDE.md`
- **Contributing:** `CONTRIBUTING.md`
- **Issues:** https://github.com/allanwrench28/GHST/issues

## Quick Reference

### Commands
```bash
# Install GHST
python install_wizard.py

# Run GHST
python core/launch_gui.py

# Run example
python examples/experts/example_expert_usage.py

# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Important Files
- `config/user/settings.yaml` - Your configuration
- `experts/README.md` - Expert system guide
- `CONTRIBUTING.md` - How to contribute
- `REPOSITORY_GUIDE.md` - Repository organization

### Key Directories
- `experts/custom/` - Your custom experts
- `logs/` - Application logs
- `exports/` - Exported files
- `config/user/` - Your settings

## Next Steps

1. ✅ Install GHST (you just did this!)
2. 📖 Read `experts/README.md` to understand the expert system
3. 🔧 Customize `config/user/settings.yaml` to your preferences
4. 🎨 Create your first custom expert
5. 🤝 Contribute back to the community

## Troubleshooting

### Installation Issues
- **Python version:** Ensure Python 3.8+
- **pip not found:** Install pip or use `python -m pip`
- **Permission denied:** Use sudo or run as administrator

### Runtime Issues
- **Module not found:** Activate virtual environment
- **Configuration errors:** Check `config/user/settings.yaml`
- **Expert not loading:** Verify metadata.yaml syntax

### Getting More Help
1. Check the logs: `logs/ghst.log`
2. Review documentation in `docs/`
3. Search GitHub issues
4. Ask in GitHub Discussions

## Safety Reminders

⚠️ **Important:**
- Always review AI recommendations before applying
- Human approval required for critical actions
- Test changes in a safe environment
- Maintain backups of important work

## Contributing

We welcome contributions! See `CONTRIBUTING.md` for guidelines.

Quick contribution process:
1. Fork the repository
2. Create a branch (`feature/my-feature`)
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Welcome to GHST! Happy coding! 👻**

For detailed documentation, see:
- Full documentation: `docs/`
- Expert system: `docs/EXPERT_SYSTEM.md`
- Repository guide: `REPOSITORY_GUIDE.md`
