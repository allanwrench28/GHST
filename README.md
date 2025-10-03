# GHST - AI Coding Engine 👻

> **G**host-driven **H**uman-**S**upervised **T**echnology

An open-source AI-driven coding engine with modular expert system and collaborative development framework.

## 🚀 Quick Start

### Installation

GHST includes a comprehensive installation wizard:

```bash
# Clone the repository
git clone https://github.com/allanwrench28/GHST.git
cd GHST

# Run the installation wizard
python install_wizard.py
```

For automated installation with defaults:
```bash
python install_wizard.py --auto
```

### Running GHST

After installation:

```bash
# Activate virtual environment (if created)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Launch the application
python core/launch_gui.py
```

## ✨ Features

- **🧠 Modular Expert System**: Domain-specific AI experts that can be added or removed independently
- **🔌 Plugin Architecture**: Extensible system for adding new functionality
- **⚙️ Configuration Management**: YAML-based configuration for easy customization
- **🎨 Modern UI**: Clean, themed interface with customizable appearance
- **👥 Human-Centered**: AI recommendations always require human validation
- **📦 Self-Contained**: Experts include metadata and knowledge fragments for offline use

## 📚 Documentation

- **[REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md)** - Repository organization and branch management
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to GHST
- **[experts/README.md](experts/README.md)** - Expert system development guide
- **[docs/](docs/)** - Additional technical documentation

## 🏗️ Architecture

### Core Components

```
GHST/
├── core/                   # Universal LLM core functionality
│   ├── src/
│   │   ├── ai_collaboration/   # AI expert framework
│   │   ├── plugins/            # Plugin system
│   │   ├── ui_components/      # UI components
│   │   └── utils/              # Utilities
│   └── requirements.txt        # Dependencies
├── experts/                # Modular expert system
│   ├── core_experts/           # Built-in experts
│   └── custom/                 # User-created experts
├── plugins/                # Plugin extensions
└── install_wizard.py       # Installation tool
```

### Modular Expert System

GHST uses a modular architecture where domain-specific experts can be:
- Added without modifying core code
- Removed cleanly
- Developed independently
- Shared with the community

See [experts/README.md](experts/README.md) for details.

## 🎯 Design Principles

1. **Modularity**: Components are independent and self-contained
2. **Human Oversight**: AI provides recommendations, humans make decisions
3. **Safety First**: All AI functionality includes appropriate safeguards
4. **Community-Driven**: Open to contributions from everyone
5. **Transparency**: Clear documentation and ethical guidelines

## 🤝 Contributing

We welcome contributions! Please see:
- **[CONTRIBUTING.md](CONTRIBUTING.md)** for general guidelines
- **[experts/README.md](experts/README.md)** for expert system contributions
- **[REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md)** for repository organization

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our guidelines
4. Test thoroughly
5. Submit a pull request

## 🌿 Branch Organization

- **`main`**: Universal LLM core functionality only
- **`feature/*`**: New features under development
- **`expert/*`**: Expert system additions/modifications
- **`domain/*`**: Domain-specific branches (e.g., 3d-printing, music-theory)

See [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) for detailed branch management.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All contributors who help make GHST better
- The open-source community for inspiration and tools
- Users who provide feedback and bug reports

## 📞 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: [GitHub Issues](https://github.com/allanwrench28/GHST/issues)
- **Discussions**: [GitHub Discussions](https://github.com/allanwrench28/GHST/discussions)

## ⚠️ Important Notes

- GHST is an AI-powered tool; always validate AI-generated code
- Human approval is required for all critical decisions
- This is open-source software provided "as-is"
- Users maintain full control and responsibility

---

**Built with ❤️ by humans and 👻 by AI**

*GHST: Where AI meets human creativity in code development*
