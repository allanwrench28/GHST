# Expertise Branch Template

This is a template for creating new expertise branches for the GHST system. Use this as a starting point for your own domain-specific expertise module.

## Structure

```
expertise_branch_template/
├── manifest.yaml              # Branch metadata and capabilities
├── expertise/
│   ├── expert_ghosts/         # Domain expert AI personalities
│   │   └── example_expert.py  # Example expert implementation
│   ├── knowledge_fragments/   # Pre-processed knowledge
│   │   ├── fundamentals/
│   │   ├── advanced/
│   │   └── troubleshooting/
│   └── tools/                 # Domain-specific utilities
│       └── example_tool.py
├── training_data/             # Raw training materials
│   └── README.md
├── auto_update/               # Self-improvement scripts
│   └── README.md
└── README.md                  # This file
```

## Creating Your Own Expertise Branch

### 1. Create a New Branch

```bash
git checkout -b my-expertise-branch
```

### 2. Copy This Template

```bash
cp -r examples/expertise_branch_template/* .
```

### 3. Customize manifest.yaml

Update the manifest with your domain information:
- Change `name`, `description`, `author`
- Update `domain` with your expertise area
- List your expert ghosts
- Document knowledge categories
- List any tools you provide

### 4. Create Expert Ghosts

Create Python files in `expertise/expert_ghosts/` that inherit from `BaseGhost`:

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
        # Your domain logic here
        return response
    
    def get_capabilities(self):
        return {
            "type": "expert",
            "capabilities": [...]
        }
```

### 5. Add Knowledge Fragments

Create JSON files in `expertise/knowledge_fragments/`:

```json
{
  "id": "fragment_001",
  "category": "fundamentals",
  "title": "Basic Concept",
  "content": "Explanation...",
  "keywords": ["keyword1", "keyword2"],
  "references": ["source1", "source2"]
}
```

### 6. Add Domain Tools

Create Python utilities in `expertise/tools/`:

```python
def my_analysis_tool(data):
    """Analyzes domain-specific data."""
    # Tool implementation
    return results
```

### 7. Test Your Branch

```python
# Test your expert ghost
python3 expertise/expert_ghosts/my_expert.py

# Test with GHST core
from core.llm_engine.plugin_loader import PluginLoader
loader = PluginLoader()
loader.load_plugin("my-expertise-branch", path="/path/to/branch")
```

### 8. Document Your Branch

Update this README with:
- What expertise your branch provides
- What expert ghosts are included
- What tools are available
- How to use your expertise
- Examples and use cases

## Example Expertise Branches

### 3D Printing (slicer-branch)
- Material science expert
- Mechanical engineering expert
- Slicing algorithm expert
- G-code analyzer tool
- Mesh optimizer tool

### Web Development (web-dev-branch)
- Frontend expert (HTML/CSS/JS)
- Backend expert (servers, databases)
- Security expert
- DevOps expert
- Code analyzer tools

### Data Science (data-science-branch)
- Statistics expert
- Machine learning expert
- Visualization expert
- Data cleaning tools
- Model evaluation tools

## Knowledge Fragment Structure

Knowledge fragments should be small, focused pieces of information:

```json
{
  "id": "unique_id",
  "category": "category_name",
  "title": "Fragment Title",
  "content": "Detailed content...",
  "keywords": ["relevant", "keywords"],
  "difficulty": "beginner|intermediate|advanced",
  "references": ["source urls"],
  "last_updated": "2024-01-01",
  "quality_score": 0.95
}
```

## Auto-Update Scripts

Create scripts in `auto_update/` to keep your expertise fresh:

```python
# research_scraper.py
def scrape_latest_research():
    """Scrapes latest research papers and updates knowledge."""
    pass

# optimization_engine.py
def optimize_responses():
    """Analyzes response quality and improves knowledge base."""
    pass
```

## Best Practices

1. **Keep fragments atomic**: One concept per fragment
2. **Use consistent keywords**: Help with search
3. **Include references**: Credit sources, enable verification
4. **Test thoroughly**: Ensure expert responses are accurate
5. **Document well**: Help others understand your expertise
6. **Version control**: Track changes to knowledge
7. **Quality metrics**: Monitor and improve response quality

## Loading Your Branch

Once created, your branch can be loaded by the GHST core:

```python
from core.llm_engine.plugin_loader import PluginLoader

loader = PluginLoader()
loader.load_plugin("my-expertise-branch")
```

Or configure auto-loading in `core/config/plugin_config.yaml`:

```yaml
plugin_system:
  auto_load_on_startup:
    - "my-expertise-branch"
```

## Contributing

When your expertise branch is ready:

1. Test thoroughly with GHST core
2. Document all capabilities
3. Ensure manifest.yaml is complete
4. Add example use cases
5. Submit for review

## License

Specify your license here. GHST core is MIT licensed.
