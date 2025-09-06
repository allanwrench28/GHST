# Contributing to FANTOM

Welcome to the FANTOM AI-driven 3D printing platform! We're excited to have you contribute to the Ghost collective.

## 🤖 AI-Human Collaboration

FANTOM features a unique AI Ghost collective that collaborates with human developers. All contributions go through both automated AI analysis and human review.

### 👻 Ghost Collective Overview

Our 26 PhD-level AI Ghosts provide:
- **Automated code review** and quality analysis
- **Ethical oversight** for AI-related changes
- **Security scanning** and vulnerability detection
- **Documentation enhancement** suggestions
- **Testing recommendations** and coverage analysis

⚠️ **Important**: Human approval is always the final authority. Ghosts provide analysis and suggestions, but humans make all final decisions.

## 📋 Repository Ruleset

This repository follows strict coding standards enforced by our comprehensive ruleset:

### 🔧 Pre-commit Hooks

All commits automatically run:
- **Black** code formatting
- **isort** import sorting
- **Flake8** linting
- **MyPy** type checking
- **Bandit** security scanning
- **Ghost Ethical Review** for AI code
- **License header validation**

### 📏 Code Quality Standards

- **Line length**: 88 characters (Black standard)
- **Type hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Test coverage**: Minimum 80%
- **Security**: No critical vulnerabilities allowed

### 🚨 Safety Requirements

For AI-related code:
- Human approval required for all AI functionality
- Ethical review by Ghost collective
- Safety disclaimers and liability warnings
- Comprehensive error handling
- User consent for experimental features

## 🚀 Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/Clockwork.git
cd Clockwork
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### 3. Verify Setup

```bash
# Run tests
pytest

# Run linting
black --check src/
flake8 src/
mypy src/

# Run security scan
bandit -r src/
```

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Testing improvements
- `ghost/` - Ghost collective enhancements
- `security/` - Security improvements

### 2. Make Changes

Follow our coding standards:

```python
"""
Example Python module with proper formatting.

This module demonstrates FANTOM coding standards.
⚠️ AI-generated content - verify before use
"""

from typing import List, Optional

import numpy as np
from some_package import SomeClass


class ExampleClass:
    """Example class following FANTOM standards.
    
    Args:
        name: The name of the example.
        values: Optional list of values.
    
    Raises:
        ValueError: If name is empty.
    """
    
    def __init__(self, name: str, values: Optional[List[float]] = None) -> None:
        if not name:
            raise ValueError("Name cannot be empty")
        
        self.name = name
        self.values = values or []
    
    def process_data(self, data: np.ndarray) -> np.ndarray:
        """Process input data with safety checks.
        
        Args:
            data: Input data array.
            
        Returns:
            Processed data array.
            
        Raises:
            ValueError: If data is invalid.
            
        Note:
            ⚠️ Always validate input data for safety.
        """
        if data.size == 0:
            raise ValueError("Input data cannot be empty")
        
        # Process data with error handling
        try:
            result = data * 2.0
            return result
        except Exception as e:
            raise ValueError(f"Data processing failed: {e}")
```

### 3. Write Tests

All new code requires tests:

```python
"""Test module for ExampleClass."""

import pytest
import numpy as np

from your_module import ExampleClass


class TestExampleClass:
    """Test suite for ExampleClass."""
    
    def test_init_valid_name(self) -> None:
        """Test initialization with valid name."""
        example = ExampleClass("test")
        assert example.name == "test"
        assert example.values == []
    
    def test_init_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            ExampleClass("")
    
    def test_process_data_valid_input(self) -> None:
        """Test data processing with valid input."""
        example = ExampleClass("test")
        data = np.array([1.0, 2.0, 3.0])
        result = example.process_data(data)
        expected = np.array([2.0, 4.0, 6.0])
        np.testing.assert_array_equal(result, expected)
    
    def test_process_data_empty_input_raises_error(self) -> None:
        """Test that empty input raises ValueError."""
        example = ExampleClass("test")
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            example.process_data(np.array([]))
```

### 4. Commit Changes

Use conventional commit messages:

```bash
# Format: type(scope): description
git commit -m "feat(ai): add new Ghost ethical review system"
git commit -m "fix(ui): resolve layout issue in settings panel"
git commit -m "docs: update installation instructions"
git commit -m "test: add coverage for config manager"
```

Commit types:
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Test additions/changes
- `chore` - Build/tool changes
- `ghost` - Ghost collective updates
- `security` - Security improvements
- `config` - Configuration changes

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Create a pull request with:
- Clear description of changes
- Reference to related issues
- Testing instructions
- Screenshots for UI changes
- Security considerations for AI code

## 🔍 Code Review Process

### Automated Review

1. **Pre-commit hooks** run locally
2. **CI pipeline** runs full test suite
3. **Ghost collective** analyzes changes
4. **Security scanning** checks for vulnerabilities
5. **License compliance** verification

### Human Review

1. **Code owner** review required
2. **AI ethics review** for AI-related changes
3. **Security review** for sensitive changes
4. **Documentation review** for user-facing changes

### Review Criteria

- ✅ Code follows style guidelines
- ✅ Tests pass and coverage maintained
- ✅ Security vulnerabilities addressed
- ✅ Documentation updated
- ✅ AI ethics considerations addressed
- ✅ Performance impact assessed
- ✅ Backward compatibility maintained

## 🛡️ Security Guidelines

### Sensitive Data

- Never commit secrets, API keys, or credentials
- Use environment variables for configuration
- Add `.env` files to `.gitignore`
- Use proper authentication and authorization

### AI Safety

- All AI functionality requires human approval
- Include safety disclaimers and warnings
- Implement proper error handling
- Validate all inputs and outputs
- Consider bias and fairness implications

### Dependencies

- Regularly update dependencies
- Use only trusted packages
- Pin versions in requirements.txt
- Run security scans on dependencies

## 📚 Documentation Standards

### Code Documentation

- Use Google-style docstrings
- Document all public functions and classes
- Include type hints for all parameters
- Add usage examples for complex functions

### User Documentation

- Update README.md for user-facing changes
- Add to CHANGELOG.md for releases
- Include screenshots for UI changes
- Provide clear installation instructions

### AI Ethics Documentation

- Document AI decision-making processes
- Explain bias mitigation strategies
- Include human oversight requirements
- Add safety warnings and disclaimers

## 🤝 Community Guidelines

### Respectful Communication

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Celebrate diverse perspectives

### AI-Human Collaboration

- Trust but verify AI suggestions
- Maintain human oversight
- Report AI misbehavior
- Contribute to ethical AI development

### Open Source Values

- Share knowledge and expertise
- Contribute to common good
- Support community growth
- Maintain transparency

## 🚨 Issue Reporting

### Bug Reports

Use the bug report template with:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages or logs

### Feature Requests

Include:
- Problem description
- Proposed solution
- Alternative solutions considered
- Implementation considerations
- AI ethics implications

### Security Issues

Report security vulnerabilities privately:
- Email: security@fantom-ai.dev
- Include detailed description
- Provide reproduction steps
- Suggest mitigation if known

## 📋 Release Process

### Version Numbering

We follow Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Security scan clean
- [ ] Ghost collective approval
- [ ] Human review complete
- [ ] Version number bumped
- [ ] Release notes prepared

## 🎯 Development Focus Areas

### High Priority

- AI ethics and safety
- Security improvements
- Test coverage expansion
- Documentation enhancement
- Performance optimization

### Medium Priority

- New slicing algorithms
- UI/UX improvements
- Platform compatibility
- Integration capabilities
- Developer experience

### Low Priority

- Code refactoring
- Style improvements
- Optional features
- Experimental capabilities

## 📞 Getting Help

### Resources

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **FAQ**: [docs/faq.md](docs/faq.md)
- **Troubleshooting**: [docs/troubleshooting.md](docs/troubleshooting.md)

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community questions and ideas
- **Code Review**: PR feedback and suggestions
- **Ghost Collective**: AI assistance and analysis

### Contact

- **Maintainer**: @allanwrench28
- **Security**: security@fantom-ai.dev
- **General**: hello@fantom-ai.dev

---

## ⚖️ Legal and Ethical Considerations

### Liability Disclaimer

⚠️ **IMPORTANT**: FANTOM assumes no liability for:
- AI-generated code or suggestions
- User modifications or customizations
- 3D printing results or outcomes
- Hardware damage or safety issues

### AI Ethics Commitment

We are committed to:
- Transparent AI decision-making
- Human oversight and control
- Bias detection and mitigation
- Privacy protection and consent
- Safety-first approach

### License

This project is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same license.

---

**Thank you for contributing to FANTOM! Together, humans and AI can build amazing things. 🚀👻**