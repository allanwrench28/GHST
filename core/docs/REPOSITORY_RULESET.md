# FANTOM Repository Ruleset Documentation

## 📋 Overview

This document describes the comprehensive repository ruleset implemented for the FANTOM AI-driven 3D printing platform. The ruleset enhances coding standards, security, and ethical AI practices while maintaining the unique Ghost collective workflow.

## 🏗️ Ruleset Components

### 1. 🔧 GitHub Repository Rulesets (`.github/rulesets.json`)

**Purpose**: Repository-level rules enforced by GitHub's native ruleset system.

**Features**:
- **Branch Protection**: Main branch requires PR reviews and status checks
- **Code Quality Standards**: File restrictions, size limits, and extension controls
- **Commit Message Standards**: Conventional commit format enforcement
- **AI Ethics Integration**: Special rules for AI-related code changes

**Key Rules**:
- Require 1 approval for main branch PRs
- Mandatory status checks: `ci/tests`, `ci/lint`, `ci/security-scan`, `ghost-collective/ethical-review`
- File size limit: 100MB
- Blocked file types: `.exe`, `.dll`, `.so`, `.dylib`
- Conventional commit message pattern enforcement

### 2. 🎣 Pre-commit Hooks (`.pre-commit-config.yaml`)

**Purpose**: Automated quality checks before code commits.

**Hooks Included**:
- **Code Formatting**: Black, isort
- **Linting**: Flake8 with security/complexity plugins, MyPy type checking
- **Security**: Bandit vulnerability scanning, secret detection
- **Documentation**: PyDocStyle, Markdown linting
- **File Validation**: YAML/JSON/TOML syntax, trailing whitespace
- **Ghost Integration**: Custom ethical review and safety checks

**Special Features**:
- AI-specific ethical review for Ghost collective code
- Automated safety validation for AI functionality
- License header verification
- Large file detection and prevention

### 3. ⚙️ Python Configuration (`pyproject.toml`)

**Purpose**: Centralized configuration for Python tooling and project metadata.

**Tool Configurations**:
- **Black**: 88-character line length, Python 3.8+ targets
- **isort**: Black-compatible import sorting
- **Flake8**: Style enforcement with security extensions
- **MyPy**: Strict type checking with AI library support
- **Pytest**: Test discovery, coverage reporting, marker definitions
- **Bandit**: Security scanning with AI-specific rules

**Project Metadata**:
- Package information and dependencies
- Entry points for CLI tools
- Development/testing/AI/docs dependency groups
- Ghost collective integration settings

### 4. 🔒 Security Configuration

**Components**:
- **Secrets Detection** (`.secrets.baseline`): Baseline for detect-secrets tool
- **Security Workflows** (`.github/workflows/security.yml`): Automated vulnerability scanning
- **Dependency Scanning**: Safety, pip-audit, and Semgrep integration

### 5. 🏷️ Automated Labeling (`.github/labeler.yml`)

**Purpose**: Automatic PR and issue labeling based on file patterns.

**Label Categories**:
- **Component**: ai, ghost-collective, core, ui, backend
- **Type**: documentation, testing, security, configuration
- **Size**: small/medium/large based on change volume
- **Special**: ethics-review-required for AI code

### 6. 👥 Code Ownership (`.github/CODEOWNERS`)

**Purpose**: Define review requirements for different code areas.

**Key Ownership**:
- AI/Ghost components require specialized review
- Security and ethics files have strict ownership
- Documentation and configuration changes tracked
- Repository governance files protected

### 7. 🚀 CI/CD Pipeline (`.github/workflows/ci.yml`)

**Purpose**: Comprehensive automated testing and validation.

**Pipeline Stages**:
1. **Pre-flight Checks**: Detect AI code changes, determine review requirements
2. **Code Quality**: Black, isort, Flake8, MyPy validation
3. **Security Scanning**: Bandit, Safety, vulnerability detection
4. **AI Ethics Review**: Ghost collective ethical analysis
5. **Testing**: Multi-platform, multi-Python version test matrix
6. **Compliance**: License headers, documentation validation
7. **Build**: Package creation and artifact uploading
8. **Approval Gate**: Human approval required for production

### 8. 📖 Documentation Standards

**Files**:
- **CONTRIBUTING.md**: Comprehensive contribution guide
- **CODEOWNERS**: Review assignment automation
- **This document**: Ruleset overview and usage

## 🤖 AI Ethics Integration

### Ghost Collective Oversight

The ruleset includes special provisions for the FANTOM Ghost collective:

1. **Automated Ethical Review**: AI code changes trigger ethical analysis
2. **Safety Validation**: Comprehensive safety checks for AI functionality
3. **Human Oversight**: All AI decisions require human approval
4. **Transparency**: Clear documentation of AI involvement
5. **Accountability**: Tracking and logging of AI contributions

### Ethical Review Process

```
AI Code Change → Ghost Analysis → Safety Check → Human Review → Approval
```

### Safety Requirements

- **Input Validation**: All AI inputs must be validated
- **Error Handling**: Comprehensive exception management
- **Safety Disclaimers**: Required for all AI functionality
- **Human Approval**: Critical decisions need human oversight
- **Bias Detection**: Automated bias and fairness checking

## 🛠️ Usage Guide

### For Developers

1. **Setup Development Environment**:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   pre-commit install
   ```

2. **Before Committing**:
   - Pre-commit hooks run automatically
   - Address any failures before pushing
   - Review AI ethics warnings carefully

3. **Creating Pull Requests**:
   - Follow conventional commit messages
   - Include clear description and testing instructions
   - Add security considerations for AI code
   - Reference related issues

### For Reviewers

1. **Automated Checks**:
   - Verify all CI checks pass
   - Review security scan results
   - Check Ghost collective analysis

2. **Manual Review**:
   - Validate AI ethics considerations
   - Ensure human oversight requirements met
   - Check documentation updates
   - Verify test coverage

### For Repository Maintainers

1. **Ruleset Updates**:
   - Modify `.github/rulesets.json` for GitHub rules
   - Update `.pre-commit-config.yaml` for hook changes
   - Adjust `pyproject.toml` for tool configuration

2. **Security Management**:
   - Review security scan results regularly
   - Update dependency vulnerability baselines
   - Monitor AI ethics compliance

## 📊 Compliance Metrics

### Code Quality Targets

- **Test Coverage**: ≥80%
- **Type Hint Coverage**: 100% for public APIs
- **Documentation Coverage**: 100% for public functions
- **Security Score**: No critical vulnerabilities
- **AI Safety Score**: ≥70/100

### Review Requirements

- **Standard Changes**: 1 approval required
- **AI/Ghost Changes**: Enhanced review + ethics check
- **Security Changes**: Security-focused review
- **Documentation**: Style and accuracy validation

## 🔧 Configuration Management

### Tool Versions

All tools pinned to specific versions for consistency:
- Black: 23.0.0+
- Flake8: 6.0.0+
- MyPy: 1.5.0+
- Pytest: 7.0.0+
- Pre-commit: 3.3.0+

### Update Process

1. Test new tool versions in feature branches
2. Update configuration in `pyproject.toml`
3. Verify CI pipeline compatibility
4. Update documentation as needed

## ⚡ Performance Considerations

### CI/CD Optimization

- **Caching**: Dependencies and build artifacts cached
- **Matrix Strategy**: Parallel testing across platforms
- **Conditional Execution**: AI reviews only for AI code
- **Artifact Management**: Efficient storage and retrieval

### Local Development

- **Pre-commit Speed**: Hooks optimized for quick feedback
- **Incremental Analysis**: Only changed files analyzed
- **Tool Integration**: Unified configuration reduces overhead

## 🚨 Troubleshooting

### Common Issues

1. **Pre-commit Hook Failures**:
   - Run `pre-commit run --all-files` to check all files
   - Use `pre-commit run --hook-stage manual <hook-name>` for specific hooks
   - Check tool versions and configuration compatibility

2. **AI Ethics Review Flags**:
   - Review flagged patterns carefully
   - Add human oversight documentation
   - Include safety disclaimers
   - Consider bias and fairness implications

3. **Security Scan Issues**:
   - Address critical and high-severity findings
   - Update vulnerable dependencies
   - Add security exceptions with justification
   - Review AI-specific security considerations

### Getting Help

- **Documentation**: Check `CONTRIBUTING.md` for detailed guidance
- **Issues**: Create GitHub issues for ruleset problems
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@fantom-ai.dev for security concerns

## 📈 Future Enhancements

### Planned Improvements

1. **Enhanced AI Analysis**: More sophisticated ethical review algorithms
2. **Performance Monitoring**: Code performance regression detection
3. **Documentation Generation**: Automated API documentation
4. **Dependency Management**: Automated dependency updates
5. **Security Hardening**: Additional security scanning tools

### Community Feedback

We welcome feedback on the ruleset implementation:
- **Effectiveness**: Are the rules improving code quality?
- **Usability**: Is the developer experience smooth?
- **Coverage**: Are there gaps in our quality gates?
- **Performance**: Are CI times acceptable?

## ⚖️ Legal and Compliance

### Licensing

- All code must include proper license headers
- MIT License requirements enforced
- AI-generated content clearly marked
- Liability disclaimers included

### AI Ethics Compliance

- Human oversight required for AI decisions
- Transparency in AI involvement
- Bias detection and mitigation
- Safety-first approach maintained

### Data Protection

- No sensitive data in repository
- Secret detection and prevention
- Privacy considerations for AI features
- User consent mechanisms

---

## 📞 Contact

- **Maintainer**: @allanwrench28
- **Security**: security@fantom-ai.dev
- **General**: hello@fantom-ai.dev
- **Issues**: [GitHub Issues](https://github.com/allanwrench28/Clockwork/issues)

---

**Last Updated**: September 4, 2024  
**Version**: 1.0.0  
**Status**: ✅ Active and Enforced