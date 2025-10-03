# GHST Expert System

## Overview

The GHST Expert System is a modular architecture that allows domain-specific AI experts to be added, removed, or modified independently. Each expert is a self-contained module with metadata, tools, and saved fragments for offline use.

## Architecture

### Expert Structure

Each expert module follows this structure:

```
experts/
├── custom/              # User-created custom experts
├── core_experts/        # Built-in core experts
│   ├── code_analysis/
│   │   ├── expert.py
│   │   ├── metadata.yaml
│   │   └── fragments/
│   ├── debugging/
│   ├── problem_solving/
│   └── ...
└── README.md           # This file
```

## Creating Custom Experts

See full documentation in `docs/EXPERT_SYSTEM.md`

### Quick Start

1. Create expert directory:
```bash
mkdir -p experts/custom/my_expert
```

2. Add metadata.yaml and expert.py

3. Test your expert

## Best Practices

- Keep experts focused on a single domain
- Minimize dependencies between experts  
- Always require human validation for critical decisions
- Document capabilities clearly
- Support offline operation where possible

## Safety and Ethics

All experts must:
- Require human approval for critical actions
- Include appropriate safety disclaimers
- Validate inputs and outputs
- Respect user privacy and data security

Happy expert building! 👻
