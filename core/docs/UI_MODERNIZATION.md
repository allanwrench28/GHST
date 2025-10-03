# GHST UI Modernization (Issue #39)

## Overview

The GHST UI has been modernized to match the style and features of modern LLM interfaces such as Grok and ChatGPT, with an iOS-inspired aesthetic.

## Key Features

### 1. Modern Design & Styling

#### Color Palette
- **Background**: `#0d1117` (GitHub Dark theme)
- **Surface**: `#161b22` (Cards, panels)
- **Border**: `#30363d` (Subtle borders)
- **Text**: `#e6edf3` (Primary text)
- **Accent Blue**: `#1f6feb` (Primary actions)
- **Accent Cyan**: `#00d4ff` (Highlights, links)
- **Muted**: `#8b949e` (Secondary text)

#### Typography
- **Font Stack**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif`
- **Code Font**: `'Consolas', 'Monaco', 'Courier New', monospace`
- **Base Size**: 13px
- **Headers**: 14px, weight 600

#### Spacing & Layout
- **Border Radius**: 6-8px for cards and buttons
- **Padding**: 8-16px depending on element
- **Margins**: Consistent 8px spacing between elements

### 2. Enhanced Chat Interface

#### Message Bubbles
- User messages: Blue border-left accent (`#1f6feb`)
- AI messages: Cyan border-left accent (`#00d4ff`)
- Rounded corners with proper padding
- Color-coded headers

#### Code Display
- Syntax highlighting for Python code
- Language label in header
- Copy button with visual feedback
- Monospace font with proper line spacing

### 3. Side Panel for Documentation

The center pane now includes three tabs:
1. **Welcome Tab**: Styled introduction and feature overview
2. **Code Editor Tab**: Text editing area for code
3. **Documentation Tab**: Markdown/code viewer with copy functionality

Features:
- Collapsible and scrollable content
- Copy button for documentation
- Clean, readable layout

### 4. Responsive Layout

#### Three-Pane Layout
```
┌─────────────────────────────────────────────────┐
│  Left (1)  │     Center (3)      │  Right (1)  │
│            │                     │             │
│  Controls  │   Main Workspace    │  AI Chat    │
│  Experts   │   (Tabs)            │             │
│  Tools     │                     │             │
└─────────────────────────────────────────────────┘
```

#### Constraints
- Minimum size: 1000x600 pixels
- Splitter ratios: 1:3:1
- Resizable panes with splitter handles

### 5. UI Polish

#### Animations
- Window fade-in on launch (400ms, OutCubic easing)
- Smooth hover transitions for buttons
- Copy button state feedback

#### Interactive Elements
- **Primary Buttons**: Bold blue style (`#1f6feb`)
- **Modern Buttons**: Subtle gray with borders
- **Hover Effects**: Background color transitions
- **Pressed States**: Darker background

#### Scrollbars
- Thin, rounded design (12px width)
- Hover state for better visibility
- Matches overall dark theme

### 6. Components

#### CodeBlockWidget
A reusable widget for displaying code with syntax highlighting.

**Features:**
- Python syntax highlighting
- Header with language label
- Copy button with feedback
- Dracula-inspired color scheme for syntax

**Usage:**
```python
from ui_components.code_block_widget import CodeBlockWidget

code = "def hello():\n    print('Hello, World!')"
widget = CodeBlockWidget(code, language="python")
```

**Syntax Highlighting Colors:**
- Keywords: `#ff79c6` (pink)
- Strings: `#f1fa8c` (yellow)
- Comments: `#6272a4` (blue-gray, italic)
- Functions: `#50fa7b` (green)
- Numbers: `#bd93f9` (purple)

## Technical Details

### Dependencies
- PyQt5 >= 5.15.0
- Python 3.7+

### File Structure
```
core/src/ui_components/
├── main.py                  # Main window and UI layout
├── code_block_widget.py     # Code display widget
└── speedbuild_slider.py     # SPEEDBUILD control slider
```

### Styling System
All styling is done via Qt StyleSheets with:
- Object names for specific component targeting
- CSS-like syntax for consistency
- Hover and pressed states for all interactive elements

### Customization

To modify the theme, edit the `apply_modern_styling()` method in `main.py`. Key areas:
- Color definitions (search for hex colors)
- Font sizes and families
- Border radius values
- Padding and margins

## Comparison to Modern LLM Interfaces

### Inspired by ChatGPT/Grok
✅ Dark theme with proper contrast
✅ Message bubbles for chat
✅ Code blocks with syntax highlighting
✅ Copy buttons on code
✅ Smooth animations
✅ Modern, clean typography
✅ Responsive layout

### iOS Design Principles
✅ Rounded corners throughout
✅ Subtle shadows and depth
✅ System font stack
✅ Smooth transitions
✅ Touch-friendly spacing
✅ Clear visual hierarchy

## Future Enhancements

Potential improvements for future releases:
- [ ] Markdown rendering in documentation panel
- [ ] More syntax highlighters (JavaScript, Java, C++, etc.)
- [ ] Drag-and-drop file support
- [ ] Theme switcher (dark/light/auto)
- [ ] Customizable accent colors
- [ ] Export chat history
- [ ] Code folding in editor
- [ ] Search in documentation

## Accessibility

The UI includes:
- High contrast text (WCAG AA compliant)
- Keyboard navigation support
- Clear focus indicators
- Readable font sizes
- Proper semantic structure

## Performance

Optimizations implemented:
- Efficient rendering with Qt
- Lazy loading for tabs
- Minimal animations (400ms max)
- Hardware acceleration via Qt

## Testing

To test the UI:
```bash
cd core
python3 launch_gui.py
```

For component testing:
```bash
cd core/src/ui_components
python3 code_block_widget.py  # Test code block widget
python3 main.py               # Test main window
```

## Screenshots

*Screenshots to be added after manual testing*

## Credits

- Design inspiration: GitHub, ChatGPT, Grok
- Color palette: GitHub Dark theme
- Syntax highlighting: Dracula theme
- Font stack: Apple Human Interface Guidelines

## License

This UI is part of the GHST project and follows the same MIT license.
