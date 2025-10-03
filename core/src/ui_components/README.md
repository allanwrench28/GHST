# GHST UI Components

Modern, professional UI components for the GHST AI Coding Engine, inspired by ChatGPT, Grok, and iOS design principles.

## Components

### `main.py` - Main Window
The primary application window with three-pane layout.

**Features:**
- Three-pane splitter: Controls | Workspace | Chat
- Modern GitHub Dark theme
- Smooth fade-in animation
- Status bar with autocommit ticker
- Responsive layout

**Usage:**
```python
from ui_components.main import GHSTWindow

window = GHSTWindow()
window.show()
```

### `code_block_widget.py` - Code Display
Syntax-highlighted code blocks with copy functionality.

**Features:**
- Python syntax highlighting (Dracula theme)
- Copy button with visual feedback
- Language label
- Modern dark styling

**Usage:**
```python
from ui_components.code_block_widget import CodeBlockWidget

code = "def hello():\n    print('Hello, World!')"
widget = CodeBlockWidget(code, language="python")
```

**Syntax Colors:**
- Keywords: `#ff79c6` (pink)
- Strings: `#f1fa8c` (yellow)
- Comments: `#6272a4` (blue-gray)
- Functions: `#50fa7b` (green)
- Numbers: `#bd93f9` (purple)

### `loading_widget.py` - Loading Animations
Modern loading indicators for async operations.

**Widgets:**
1. **LoadingSpinner**: Circular rotating spinner
2. **LoadingMessage**: Spinner with text message
3. **PulseLoader**: Three-dot pulse animation

**Usage:**
```python
from ui_components.loading_widget import LoadingSpinner, LoadingMessage

# Simple spinner
spinner = LoadingSpinner(size=50, color="#1f6feb")
spinner.start()

# Spinner with message
loader = LoadingMessage("Processing your request...")
loader.start()
```

### `speedbuild_slider.py` - SPEEDBUILD Control
Slider for controlling automation level.

**Features:**
- Horizontal slider (0-100)
- Mode labels (Automated/Mixed/Personalized)
- Tick marks
- Modern styling

## Styling System

All components use Qt StyleSheets with a consistent design system:

### Color Palette (GitHub Dark)
```python
BACKGROUND = "#0d1117"      # Main background
SURFACE = "#161b22"         # Cards, panels
ELEVATED = "#1c2128"        # Hover states
BORDER = "#30363d"          # Borders
TEXT_PRIMARY = "#e6edf3"    # Main text
TEXT_SECONDARY = "#8b949e"  # Muted text
ACCENT_BLUE = "#1f6feb"     # Primary actions
ACCENT_CYAN = "#00d4ff"     # Highlights
```

### Typography
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
font-size: 13px;
line-height: 1.5;
```

### Spacing
```css
border-radius: 6-8px;
padding: 8-16px;
margin: 8px;
gap: 12px;
```

### Animations
```python
FADE_IN_DURATION = 400      # Window fade-in (ms)
HOVER_TRANSITION = 150      # Button hover (ms)
SPINNER_FPS = 33            # Loading spinner (ms per frame)
```

## Object Names for Styling

Use these object names to target specific elements:

```python
# Section headers
label.setObjectName("sectionHeader")

# Primary buttons (blue, prominent)
button.setObjectName("primaryButton")

# Modern buttons (gray, subtle)
button.setObjectName("modernButton")

# Code block header
widget.setObjectName("codeBlockHeader")

# Code display area
textedit.setObjectName("codeBlockDisplay")
```

## Layout Patterns

### Three-Pane Layout
```python
splitter = QSplitter(Qt.Horizontal)
splitter.addWidget(left_pane)    # 1 part
splitter.addWidget(center_pane)  # 3 parts
splitter.addWidget(right_pane)   # 1 part
splitter.setStretchFactor(0, 1)
splitter.setStretchFactor(1, 3)
splitter.setStretchFactor(2, 1)
```

### Card-Style Panel
```python
card = QWidget()
card.setStyleSheet("""
    QWidget {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
    }
""")
```

### Message Bubble
```python
message_html = f"""
<div style="background: #1c2128; padding: 12px; border-radius: 8px; 
            margin: 8px 0; border-left: 3px solid #1f6feb;">
    <p style="margin: 0; color: #00d4ff; font-weight: 600;">User</p>
    <p style="margin: 4px 0 0 0; color: #e6edf3;">{text}</p>
</div>
"""
```

## Responsive Behavior

### Window Sizes
- **Minimum**: 1000x600 (enforced)
- **Default**: 1400x900 (recommended)
- **Maximum**: Unrestricted

### Splitter Ratios
- Left pane: 1 part (~20%)
- Center pane: 3 parts (~60%)
- Right pane: 1 part (~20%)

## Accessibility

### Contrast Ratios
- Primary text: 14.8:1 (AAA)
- Secondary text: 6.4:1 (AA)
- Accent colors: 11.2:1 (AAA)

### Interactive Elements
- Minimum button height: 40px
- Clear focus indicators
- Keyboard navigation support
- Semantic structure

## Best Practices

### Creating New Components
1. Inherit from appropriate Qt widget
2. Use object names for styling
3. Apply modern styling in init
4. Support keyboard navigation
5. Add docstrings

Example:
```python
class MyWidget(QWidget):
    """Brief description of widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Set object name for styling
        self.setObjectName("myWidget")
        
        # Apply styling
        self.setStyleSheet("""
            QWidget#myWidget {
                background-color: #161b22;
                border-radius: 8px;
            }
        """)
```

### Adding Animations
```python
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

# Fade-in animation
effect = QGraphicsOpacityEffect()
widget.setGraphicsEffect(effect)

animation = QPropertyAnimation(effect, b"opacity")
animation.setDuration(400)
animation.setStartValue(0.0)
animation.setEndValue(1.0)
animation.setEasingCurve(QEasingCurve.OutCubic)
animation.start()
```

## Dependencies

```
PyQt5>=5.15.0
Python>=3.7
```

Install with:
```bash
pip install PyQt5
```

## Testing

Run individual component tests:
```bash
# Test main window
python3 main.py

# Test code block widget
python3 code_block_widget.py

# Test loading animations
python3 loading_widget.py
```

## Documentation

See also:
- `../../docs/UI_MODERNIZATION.md` - Feature overview
- `../../docs/UI_VISUAL_GUIDE.md` - Visual examples
- Component docstrings for detailed API

## Contributing

When adding new UI components:
1. Follow the established color palette
2. Use consistent spacing (8px grid)
3. Add hover and pressed states
4. Include docstrings and examples
5. Test at different window sizes
6. Verify contrast ratios

## License

Part of the GHST project - MIT License
