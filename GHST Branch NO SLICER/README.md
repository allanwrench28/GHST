# The Machine Studio 🎬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **The Machine Studio** is the development and experimentation platform for **FANTOM** - an AI-driven 3D printing ecosystem. This repository contains all the core components, AI collaboration tools, and infrastructure **except** the slicer functionality.

## 🌟 What's Included

- **AI Collaboration Framework**: Ghosts in the Machine system for automated improvements
- **Plugin System**: Extensible architecture for 3D printing tools
- **Configuration Management**: Klipper-like YAML system for printer/material settings
- **UI Components & Themes**: Orca-based interface elements
- **Utility Libraries**: Shared tools and helpers
- **Developer Tools**: Safety checks, build scripts, and automation
- **Documentation**: Complete project documentation and guides

## 🚫 What's NOT Included

This studio version **excludes** all slicer-specific functionality:
- Slicer UI components (`src/slicer_ui/`)
- Slicer demonstration scripts (`demo_slicer.py`)
- Slicer test files (`test_slicer.py`)
- Slicer configuration files

The complete slicer functionality can be found in the main [FANTOM repository](https://github.com/allanwrench28/The_Machine).

## 🎯 Purpose

The Machine Studio serves as:
- **Development Environment**: Core components without slicer complexity
- **Integration Testing**: Plugin and AI systems validation
- **Research Platform**: AI collaboration and automation experiments
- **Component Library**: Reusable modules for 3D printing applications

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git for Ghost-driven development
- Internet connection for AI features

### Installation

```bash
# Clone the repository
git clone https://github.com/allanwrench28/The_Machine_Studio.git
cd The_Machine_Studio

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Run demo applications
python demo.py                    # Core demo
python demo_plugin_system.py      # Plugin system demo
python demo_nightly_automation.py # Automation demo
```

## 👻 Ghosts in the Machine

The Studio includes the full AI collaboration framework:

- **Error Analysis**: Automated error capture and pattern recognition
- **Research Integration**: Internet-enabled FOSS research capabilities  
- **Pull Request Generation**: Automated improvement submissions
- **Safety Validation**: Ethical and safety constraint enforcement

## 🔧 Development Structure

```
The_Machine_Studio/
├── src/
│   ├── ai_collaboration/   # Ghost framework and AI tools
│   ├── plugins/           # Plugin system and built-in plugins
│   ├── ui_components/     # Reusable UI elements
│   ├── ui_themes/         # Theme engine and Orca themes
│   └── utils/             # Configuration and utility libraries
├── config/               # YAML configurations
├── docs/                 # Documentation
├── scripts/              # Build and automation scripts
└── Clockwork/           # Clockwork automation system
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create Feature Branch**: `git checkout -b feature/studio-enhancement`
3. **Develop & Test**: Use the studio environment for validation
4. **Submit PR**: Ghosts and humans review together
5. **Integration**: Approved changes flow to main FANTOM project

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[FANTOM](https://github.com/allanwrench28/The_Machine)**: Complete 3D printing slicer with UI
- **The Machine Studio**: Development platform (this repository)

---

**Built with ❤️ by humans and 👻 by Ghosts in the Machine**

*The Machine Studio: Where innovation meets automation in 3D printing development.*

