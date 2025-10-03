# GHST UI Components

This directory contains the polished, iOS/Mac-inspired UI components for the GHST AI Coding Engine.

## Overview

The GHST UI is designed with a focus on:
- **Professional aesthetics** inspired by Apple's design language
- **Smooth animations and transitions** for a premium feel
- **Intuitive layout** with clear visual hierarchy
- **Responsive design** that adapts to different screen sizes
- **Dark mode optimized** for reduced eye strain during coding sessions

## Components

### Main Window (`main.py`)
The primary application window featuring:
- **Left Panel**: SPEEDBUILD slider, AI Expert agents, and tools
- **Center Panel**: Tabbed workspace with Welcome and Code Editor tabs
- **Right Panel**: AI Assistant chat interface
- **Side Panel**: Collapsible documentation viewer (Grok-style)
- **Menu Bar**: File, View, AI Experts, Tools, and Help menus
- **Status Bar**: Real-time git commit ticker and system status

### Code Display Box (`code_display.py`)
A sophisticated code display component with:
- **Syntax-friendly styling** with monospace font
- **Copy button** at the top for quick code copying
- **Visual feedback** when code is copied
- **Customizable title** for different code types

### Side Panel (`side_panel.py`)
A Grok-inspired side panel featuring:
- **Tabbed interface** for Markdown and Code views
- **Collapsible design** to maximize workspace
- **Smooth animations** when opening/closing
- **Separate views** for documentation and code examples

### SPEEDBUILD Slider (`speedbuild_slider.py`)
A control slider for automation levels:
- **Personalization control** from 0% (full automation) to 100% (full user control)
- **Visual feedback** showing current mode
- **Integration** with the build system

## Design System

### Colors
- **Primary Blue**: `#0a84ff` - Interactive elements, highlights
- **Background Dark**: `#1a1a1a` - Main background
- **Panel Dark**: `#252525` - Card and panel backgrounds
- **Border Color**: `#3a3a3a` - Subtle borders and separators
- **Text Primary**: `#e8e8e8` - Main text color
- **Text Secondary**: `#999999` - Secondary/muted text

### Typography
- **System Font**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Monospace**: `'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace`
- **Heading Size**: 16px-32px (context dependent)
- **Body Size**: 13-14px
- **Weight**: 400 (regular), 500 (medium), 600 (semibold)

### Spacing
- **Base Unit**: 4px
- **Small**: 8px
- **Medium**: 12px
- **Large**: 16px
- **XLarge**: 24px

### Borders & Radii
- **Border Radius**: 8px (standard), 4px (small), 16px (large)
- **Border Width**: 1px (standard), 2px (emphasis)

## Features

### Animations & Transitions
- Button hover effects with gradient transitions
- List item selection with smooth color changes
- Tab switching with subtle animations
- Panel sliding transitions

### Interactive Elements
- **Hover States**: All interactive elements respond to hover
- **Focus States**: Keyboard navigation fully supported
- **Click Feedback**: Visual feedback on button presses
- **Tooltips**: Context-sensitive help (planned)

### Accessibility
- High contrast text for readability
- Keyboard navigation support
- Focus indicators on interactive elements
- Semantic HTML structure

## Usage

### Launching the GUI

```python
from PyQt5.QtWidgets import QApplication
from ui_components.main import GHSTWindow

app = QApplication(sys.argv)
window = GHSTWindow()
window.show()
sys.exit(app.exec_())
```

Or use the provided launcher:

```bash
cd core
python launch_gui.py
```

### Customizing Themes

The main theme is applied in `apply_ghst_theme()` method. You can modify colors, fonts, and styling by editing the stylesheet in this method.

### Adding New Components

1. Create a new component file in this directory
2. Inherit from appropriate PyQt5 widget classes
3. Follow the established design patterns for consistency
4. Apply theme styling using Qt stylesheets
5. Import and integrate into `main.py`

## Dependencies

- PyQt5 >= 5.15.0
- Python >= 3.7

## Future Enhancements

- [ ] Syntax highlighting in code editor
- [ ] Drag-and-drop file support
- [ ] Plugin UI integration
- [ ] Customizable keyboard shortcuts
- [ ] Theme switcher (dark/light modes)
- [ ] Window state persistence
- [ ] Floating panels support
- [ ] Mini-map for code navigation
- [ ] AI suggestion inline display
- [ ] Real-time collaboration indicators

## Contributing

When adding new UI components:
1. Maintain consistency with existing design language
2. Use the established color palette
3. Ensure accessibility standards are met
4. Add appropriate documentation
5. Test on different screen sizes

## License

Part of the GHST project - See LICENSE file in repository root.
