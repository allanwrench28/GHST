# FANTOM Repository Ruleset - Quick Reference

## 🚀 Quick Start

```bash
# Setup development environment
pip install -r requirements.txt
pip install -e .[dev]
pre-commit install

# Run quality checks
black --check src/
flake8 src/
mypy src/
pytest tests/

# Test custom checks
python scripts/ghost_ethical_review.py src/ai_collaboration/
python scripts/ai_safety_check.py src/ai_collaboration/
```

## 📋 File Checklist

### Required Files ✅
- [x] `.github/rulesets.json` - GitHub repository rules
- [x] `.pre-commit-config.yaml` - Pre-commit hooks
- [x] `pyproject.toml` - Python tool configuration
- [x] `.github/workflows/ci.yml` - CI/CD pipeline
- [x] `.github/workflows/security.yml` - Security scanning
- [x] `.github/CODEOWNERS` - Code ownership
- [x] `.github/labeler.yml` - Auto-labeling rules
- [x] `.secrets.baseline` - Secrets detection baseline
- [x] `.gitignore` - Git ignore patterns
- [x] `.markdownlint.json` - Markdown style rules
- [x] `CONTRIBUTING.md` - Contribution guidelines
- [x] `scripts/ghost_ethical_review.py` - AI ethics check
- [x] `scripts/ai_safety_check.py` - AI safety validation
- [x] `scripts/check_license_headers.py` - License verification

## 🎯 Commit Message Format

```
type(scope): description

feat(ai): add new Ghost ethical review system
fix(ui): resolve layout issue in settings panel
docs: update installation instructions
test: add coverage for config manager
ghost: enhance collective oversight capabilities
security: implement additional vulnerability scanning
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ghost`, `security`, `config`

## 🔧 Tool Configurations

### Black (Code Formatting)
- Line length: 88 characters
- Target: Python 3.8+
- Config: `pyproject.toml [tool.black]`

### Flake8 (Linting)
- Max line length: 88
- Ignores: E203, W503 (Black compatibility)
- Plugins: docstrings, security, complexity
- Config: `pyproject.toml [tool.flake8]`

### MyPy (Type Checking)
- Strict mode enabled
- Disallow untyped definitions
- Config: `pyproject.toml [tool.mypy]`

### Pytest (Testing)
- Min coverage: 80%
- Reports: terminal, HTML, XML
- Config: `pyproject.toml [tool.pytest.ini_options]`

## 🛡️ Security Standards

### Blocked Content
- Secrets, API keys, credentials
- Binary files: `.exe`, `.dll`, `.so`
- Large files: >100MB
- Build artifacts: `__pycache__/`, `*.pyc`

### Required Scans
- Bandit: Python security vulnerabilities
- Safety: Dependency vulnerabilities
- Secrets: Credential detection
- License: Header verification

## 🤖 AI Ethics Requirements

### For AI-Related Code
- ✅ Human approval required
- ✅ Ethical review by Ghost collective
- ✅ Safety disclaimers included
- ✅ Error handling implemented
- ✅ Input validation present
- ✅ Bias considerations documented

### Review Process
1. Automated detection of AI code
2. Ghost collective ethical analysis
3. Safety validation scoring
4. Human oversight verification
5. Documentation requirements check

## 📏 Quality Gates

### Code Quality Thresholds
- **Test Coverage**: ≥80%
- **Safety Score**: ≥70/100
- **Security**: No critical vulnerabilities
- **Type Hints**: Required for public APIs
- **Documentation**: Required for public functions

### CI/CD Status Checks
- ✅ `ci/tests` - Test suite passes
- ✅ `ci/lint` - Code quality checks
- ✅ `ci/security-scan` - Security validation
- ✅ `ghost-collective/ethical-review` - AI ethics review

## 🚨 Common Issues & Solutions

### Pre-commit Hook Failures
```bash
# Fix formatting issues
black src/ tests/ scripts/
isort src/ tests/ scripts/

# Check specific hooks
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

### AI Ethics Review Flags
- Add human oversight documentation
- Include safety disclaimers
- Implement proper error handling
- Document bias considerations

### Security Scan Issues
- Update vulnerable dependencies
- Remove hardcoded secrets
- Add proper input validation
- Review file permissions

## 📋 PR Checklist

### Before Creating PR
- [ ] All pre-commit hooks pass
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Conventional commit messages used
- [ ] AI ethics considerations addressed
- [ ] Security implications reviewed

### PR Description Should Include
- Clear description of changes
- Testing instructions
- Security considerations
- AI ethics implications (if applicable)
- Screenshots for UI changes
- Related issue references

## 🔍 Review Requirements

### Standard Changes
- 1 approval required
- All CI checks pass
- Documentation updated

### AI/Ghost Changes
- Enhanced ethical review
- Safety validation required
- Human oversight documented
- Bias considerations addressed

### Security Changes
- Security-focused review
- Vulnerability assessment
- Impact analysis
- Mitigation strategies

## ⚙️ Local Development

### Environment Setup
```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Pre-commit hooks
pre-commit install
```

### Quality Checks
```bash
# Format code
black src/ tests/ scripts/
isort src/ tests/ scripts/

# Lint code
flake8 src/ tests/ scripts/
mypy src/

# Security scan
bandit -r src/
safety check

# Run tests
pytest tests/ --cov=src

# AI-specific checks
python scripts/ghost_ethical_review.py src/ai_collaboration/
python scripts/ai_safety_check.py src/ai_collaboration/
```

## 📞 Getting Help

### Documentation
- `CONTRIBUTING.md` - Detailed contribution guide
- `docs/REPOSITORY_RULESET.md` - Complete ruleset documentation
- `ETHICAL_AI_FRAMEWORK.md` - AI ethics guidelines

### Support Channels
- **Issues**: GitHub Issues for bugs/features
- **Discussions**: GitHub Discussions for questions
- **Security**: security@fantom-ai.dev
- **General**: hello@fantom-ai.dev

### Tool Help
```bash
# Tool documentation
black --help
flake8 --help
mypy --help
pytest --help
pre-commit --help

# Configuration validation
python -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml'))"
python -c "import json; json.load(open('.github/rulesets.json'))"
python -c "import toml; toml.load('pyproject.toml')"
```

---

**🎯 Remember**: This ruleset is designed to enhance code quality while supporting the unique AI-human collaboration of the FANTOM Ghost collective. Human oversight and ethical considerations are paramount.

**📄 License**: MIT License - see `LICENSE` file  
**🤖 AI Notice**: Some content may be AI-generated - verify before use  
**⚖️ Liability**: FANTOM assumes no liability - use at your own risk