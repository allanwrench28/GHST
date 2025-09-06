# 🧠 GHST PhD Think Tank System

An open-source AI collaboration framework where PhD-level AI agents debate, collaborate, and reach consensus on coding solutions through evidence-based reasoning.

## ✨ Features

### 🎓 PhD Expert Collective
- **Dr. Algorithm** - PhD in Computer Science (Algorithms & Data Structures)
- **Dr. Architect** - PhD in Software Engineering (Software Architecture)
- **Dr. Performance** - PhD in Systems Engineering (Performance & Scalability)
- **Dr. Mathematics** - PhD in Mathematics (Optimization Theory)
- **Dr. Security** - PhD in Security (Cybersecurity)
- **Dr. MachineLearning** - PhD in Machine Learning (AI/ML Systems)
- **Dr. UserExperience** - PhD in HCI (Human-Computer Interaction)
- **Dr. Database** - PhD in Database Systems (Data Management)

### 🗣️ Think Tank Debate System
- **Multi-agent debates** with PhD-level expertise
- **Evidence-based reasoning** with citations and peer review
- **Consensus building algorithms** with weighted voting
- **Real-time collaboration** between specialized agents
- **Cross-examination and rebuttals** for thorough analysis

### 🎨 VS Code-Style Interface
- **Dark theme** with professional VS Code styling
- **Expert cards** showing PhD specializations and status
- **Real-time progress tracking** during think tank sessions
- **Rich results display** with confidence scores and implementation plans
- **Responsive layout** with resizable panels

## 🚀 Quick Start

### Option 1: Interactive Launcher
```bash
python launch_think_tank.py
```

Choose from:
1. 🧠 Console demo with think tank debate
2. 🎨 VS Code-style GUI interface
3. 🔍 Test all components
4. 📊 System status and statistics

### Option 2: Direct Console Demo
```bash
python core/src/ai_collaboration/phd_think_tank.py
```

### Option 3: GUI Interface
```bash
python core/src/ai_collaboration/think_tank_gui.py
```

## 📋 Usage Examples

### Console Interface
```python
from ai_collaboration.phd_think_tank import think_tank
import asyncio

problem = """
I need to optimize a Python function that processes large CSV files (10GB+) 
with memory constraints. Current implementation loads entire file into memory 
and causes out-of-memory errors.
"""

context = {
    'language': 'Python',
    'data_size': '10GB+',
    'memory_limit': '8GB',
    'performance_requirement': '< 5 minutes'
}

# Get PhD think tank consensus
consensus = await think_tank.solve_problem(problem, context)
print(f"Solution: {consensus.solution}")
print(f"Confidence: {consensus.confidence_score:.2f}")
```

### Integration Interface
```python
from ai_collaboration.think_tank_integration import ghst_think_tank

result = await ghst_think_tank.solve_coding_problem(problem, context)
print(f"PhD Experts Supporting: {result['phd_experts']['supporting']}")
print(f"Implementation Plan: {result['implementation_plan']}")
```

## 🏗️ Architecture

### Core Components

```
GHST Think Tank System
├── phd_think_tank.py          # Core debate system
├── think_tank_integration.py   # GHST integration layer
├── think_tank_gui.py          # VS Code-style interface
└── launch_think_tank.py       # Main launcher
```

### PhD Agent Workflow

1. **Problem Analysis** - Each PhD agent analyzes from their expertise
2. **Evidence Gathering** - Agents collect domain-specific evidence
3. **Initial Positions** - Agents present their recommended approaches
4. **Cross-Examination** - Agents debate and challenge each other
5. **Consensus Building** - Weighted voting with evidence quality
6. **Solution Synthesis** - Final consensus with implementation plan

### Debate Lifecycle

```
INITIATING → ACTIVE_DEBATE → EVIDENCE_GATHERING → 
CONSENSUS_BUILDING → SOLUTION_REACHED → IMPLEMENTATION
```

## 📊 System Capabilities

### Evidence-Based Reasoning
- **Peer-reviewed sources** with confidence scoring
- **Citation tracking** for academic credibility
- **Cross-domain validation** between PhD specializations
- **Quality metrics** for evidence assessment

### Consensus Algorithms
- **Weighted voting** based on expertise relevance
- **Evidence quality scoring** for argument strength
- **Similarity analysis** for convergence detection
- **Minority opinion preservation** for edge cases

### Performance Metrics
- **Time to consensus** tracking
- **Agent performance statistics** 
- **Success rate monitoring**
- **Evidence quality trends**

## 🎯 Use Cases

### 1. Code Optimization
```
Problem: Slow database queries affecting user experience
Experts: Dr. Database, Dr. Performance, Dr. Algorithm
Result: Multi-level optimization strategy with indexing and caching
```

### 2. Security Analysis
```
Problem: Authentication system vulnerability assessment
Experts: Dr. Security, Dr. Architect, Dr. Database
Result: Zero-trust architecture with multi-factor authentication
```

### 3. Algorithm Design
```
Problem: Efficient pathfinding for large graphs
Experts: Dr. Algorithm, Dr. Mathematics, Dr. Performance
Result: Hierarchical A* with precomputed landmarks
```

### 4. UI/UX Optimization
```
Problem: Complex interface causing user confusion
Experts: Dr. UserExperience, Dr. Architect, Dr. Performance
Result: Progressive disclosure with cognitive load reduction
```

## 🔧 Configuration

### Agent Weights
Customize expert voting weights based on problem domain:
```python
agent.vote_weight = 1.5  # Higher weight for domain experts
```

### Evidence Thresholds
Set minimum evidence quality requirements:
```python
consensus_threshold = 0.7  # 70% agreement required
evidence_minimum = 0.6     # 60% evidence confidence
```

### Debate Parameters
Control debate rounds and timing:
```python
max_rounds = 5            # Maximum debate rounds
timeout = 300            # 5-minute timeout
min_participants = 3     # Minimum expert count
```

## 📈 Statistics Dashboard

The system tracks comprehensive metrics:

- **Total Debates Conducted**
- **Successful Consensus Rate**
- **Average Time to Consensus**
- **Expert Performance Rankings**
- **Evidence Quality Trends**
- **Problem Domain Distribution**

## 🎨 GUI Features

### Expert Panel
- Live status indicators for each PhD agent
- Expertise areas and specializations
- Participation history and performance

### Problem Input
- Rich text editor with syntax highlighting
- JSON context configuration
- Real-time validation and suggestions

### Results Display
- Confidence score visualization
- Supporting vs. dissenting expert breakdown
- Detailed implementation plans
- Evidence quality metrics

## 🔮 Future Enhancements

### Advanced AI Integration
- **GPT-4/Claude integration** for enhanced reasoning
- **Specialized fine-tuned models** for each PhD domain
- **Real-time knowledge base updates** from academic sources

### Collaborative Features
- **Multi-user sessions** with human expert participation
- **Version control integration** for solution tracking
- **Automated testing** of proposed solutions

### Open Source Ecosystem
- **Plugin architecture** for custom PhD specializations
- **Community contributions** of expert knowledge
- **Academic partnership** with research institutions

## 🤝 Contributing

We welcome contributions to expand the PhD expert collective:

1. **New PhD Specializations** - Add domain experts
2. **Evidence Sources** - Expand academic databases
3. **Consensus Algorithms** - Improve decision-making
4. **UI/UX Enhancements** - Better user experience

## 📜 License

Open source under MIT License - encouraging academic collaboration and transparency.

## 🙏 Acknowledgments

Inspired by:
- Academic peer review processes
- Collaborative problem-solving methodologies  
- Open source AI democratization
- Evidence-based software engineering

---

**GHST PhD Think Tank** - Where AI expertise meets collaborative intelligence for superior coding solutions.
