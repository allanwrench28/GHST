# GHST UI Guide

## Overview

The GHST AI Coding Engine features a super polished, commercial-grade user interface inspired by iOS and macOS design principles. This guide provides an overview of the UI features, components, and user experience enhancements.

## Design Philosophy

The GHST UI follows these core principles:

1. **Simplicity**: Clean, uncluttered interface focusing on essential features
2. **Consistency**: Uniform design language across all components
3. **Accessibility**: High contrast, clear typography, keyboard navigation
4. **Performance**: Smooth animations and responsive interactions
5. **Professional**: Commercial-grade polish suitable for production use

## Main Interface Layout

### Three-Panel Design

The main window uses a three-panel layout for optimal workflow:

```
┌─────────────┬──────────────────────┬─────────────┐
│             │                      │             │
│  Left Panel │   Center Workspace   │ Right Panel │
│             │                      │             │
│ AI Experts  │   Code Editor        │ AI Chat     │
│ Tools       │   Welcome Tab        │ Assistant   │
│ Controls    │                      │             │
│             │                      │             │
└─────────────┴──────────────────────┴─────────────┘
```

**Resizable**: All panels can be resized by dragging the splitters between them.

### Left Panel - AI Experts & Tools

**SPEEDBUILD Control**
- Slider for adjusting automation level (0% to 100%)
- Visual indicator showing current mode
- Real-time mode updates

**AI Experts List**
- 12 specialized AI experts available
- Each expert has specific domain expertise
- Click to activate/select expert assistance

**Tools List**
- Quick access to core tools
- Plugins, Settings, Templates, Snippets
- One-click access to functionality

**View Documentation Button**
- Opens the side panel for quick reference
- Context-sensitive documentation

### Center Panel - Workspace

**Tabbed Interface**
- Multiple tabs for different workspaces
- Welcome tab with getting started guide
- Code Editor tab with enhanced display

**Code Display Features**
- Syntax-friendly monospace font
- Copy-to-clipboard button at the top
- Visual feedback when code is copied
- Clean, readable code presentation

**Welcome Tab**
- Feature overview
- Quick start guide
- Key features highlighted
- Professional typography

### Right Panel - AI Assistant

**Chat Interface**
- Styled message bubbles for user/AI messages
- Color-coded for easy distinction
- Smooth scrolling
- Real-time responses

**Message Input**
- Multi-line text input
- Send button with icon
- Keyboard shortcuts supported

### Side Panel - Documentation (Grok-Style)

**Collapsible Panel**
- Opens from the right side
- Tabbed interface (Markdown/Code views)
- Close button for quick dismissal
- Smooth slide-in animation

**Content Views**
- **Markdown Tab**: Formatted documentation
- **Code Tab**: Code examples and snippets
- Syntax highlighting
- Copy functionality

## Menu Bar

### 📁 File Menu
- **New Project**: Create a new coding project
- **Open Project**: Open existing project
- **Exit**: Close the application

### 👁️ View Menu
- **Toggle Documentation Panel**: Show/hide side panel

### 🧠 AI Experts Menu
- **Expert Status**: View active AI experts
- **Configure Experts**: Customize expert behavior

### 🔧 Tools Menu
- **Plugin Manager**: Manage installed plugins
- **Configuration**: Open settings dialog

### ❓ Help Menu
- **About GHST**: Application information

## Settings Dialog

Access via **Tools → Configuration** or **⚙️ Settings**

### Tabs

1. **General**
   - Auto-save settings
   - Project preferences
   - File handling options

2. **AI Experts**
   - Model selection (GPT-4, Claude 3, Local LLaMA, Mixtral)
   - Expert behavior configuration
   - Automatic suggestions toggle

3. **Appearance**
   - Theme selection (GHST Dark, Light, High Contrast, Solarized)
   - Font size adjustment
   - UI customization

4. **Advanced**
   - Performance settings
   - Hardware acceleration
   - Worker thread configuration
   - Developer options

## Color Palette

### Primary Colors
- **Blue Accent**: `#0a84ff` - Interactive elements, highlights, links
- **Light Blue**: `#3a9aff` - Hover states
- **Dark Blue**: `#0066cc` - Active/pressed states
- **Cyan Accent**: `#00d9ff` - Secondary highlights

### Background Colors
- **Main Background**: `#1a1a1a` - Primary dark background
- **Panel Background**: `#252525` - Cards and panels
- **Header/Footer**: `#2a2a2a` - Top and bottom sections
- **Hover Background**: `#2f2f2f` - Hover states

### Text Colors
- **Primary Text**: `#e8e8e8` - Main content
- **Secondary Text**: `#999999` - Labels, descriptions
- **White Text**: `#ffffff` - Headers, emphasis

### Border Colors
- **Primary Border**: `#3a3a3a` - Standard borders
- **Hover Border**: `#4a4a4a` - Interactive borders
- **Focus Border**: `#0a84ff` - Active element border

## Typography

### Font Families
- **UI Elements**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif`
- **Code/Monospace**: `'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace`

### Font Sizes
- **Heading 1**: 32px (Welcome screen)
- **Heading 2**: 20px (Section headers)
- **Heading 3**: 16px (Subsections)
- **Body Text**: 13-14px (Standard content)
- **Small Text**: 12px (Meta information)
- **Menu Text**: 13px

### Font Weights
- **Light**: 300 (Close buttons)
- **Regular**: 400 (Body text)
- **Medium**: 500 (Tabs, secondary labels)
- **Semibold**: 600 (Headers, buttons)

## Interactive Elements

### Buttons

**Primary Button**
- Gradient background (`#0a84ff` to `#0066cc`)
- White text, 8px border radius
- Hover: Lighter gradient
- Press: Darker gradient, slight position shift

**Ghost Button**
- Transparent background
- Blue border and text
- Hover: Semi-transparent blue background

**Icon Buttons**
- Square shape (32x32px typically)
- Icon-only or icon + text
- Subtle hover effects

### List Items
- 8px padding, 6px border radius
- Hover: `#2f2f2f` background
- Selected: `#0a84ff` background, white text
- Smooth transitions

### Input Fields
- `#252525` background, `#3a3a3a` border
- 6px border radius
- Focus: `#0a84ff` border
- Hover: Blue border hint

### Sliders
- Custom styled handle
- Blue accent color
- Smooth dragging
- Visual value feedback

## Animations & Transitions

### Button Animations
- **Hover**: 150ms ease-in-out
- **Press**: Immediate feedback
- **Release**: 150ms ease-in-out

### Panel Transitions
- **Side Panel**: 300ms slide animation
- **Tabs**: 200ms fade transition
- **Dialog**: 250ms fade + scale

### List Selections
- **Color Change**: 150ms ease-in-out
- **Background**: 150ms ease-in-out

### Copy Feedback
- **Button Text Change**: Immediate
- **Color Change**: 100ms
- **Reset**: 2000ms delay, 300ms transition

## Keyboard Shortcuts

### Global
- `Ctrl/Cmd + N`: New Project
- `Ctrl/Cmd + O`: Open Project
- `Ctrl/Cmd + S`: Save
- `Ctrl/Cmd + ,`: Settings
- `Ctrl/Cmd + Q`: Quit

### Navigation
- `Tab`: Move forward through controls
- `Shift + Tab`: Move backward through controls
- `Enter`: Activate button/control
- `Esc`: Close dialog/panel

### Chat
- `Enter`: Send message (with Shift for new line)
- `Ctrl/Cmd + L`: Clear chat

## Responsive Behavior

### Window Resize
- Minimum window size: 1400x900
- Panels adjust proportionally
- Content wraps appropriately
- Scrollbars appear when needed

### Panel Resizing
- Left Panel: 200-400px
- Center Panel: Flexible (largest)
- Right Panel: 300-500px
- Side Panel: 300-600px

## Accessibility Features

### Visual
- High contrast text (WCAG AA compliant)
- Clear focus indicators
- Sufficient color contrast ratios
- Scalable font sizes

### Keyboard
- Full keyboard navigation
- Logical tab order
- Escape key closes dialogs
- Enter key activates buttons

### Screen Readers
- Semantic HTML structure
- ARIA labels where appropriate
- Descriptive button text
- Alt text for icons

## Best Practices

### For Users
1. Use keyboard shortcuts for faster navigation
2. Resize panels to fit your workflow
3. Customize settings for your preferences
4. Toggle side panel for quick reference
5. Use AI chat for assistance

### For Developers
1. Follow the established design patterns
2. Use the color palette consistently
3. Apply proper spacing and typography
4. Test keyboard navigation
5. Ensure responsive behavior

## Troubleshooting

### UI Not Displaying Correctly
- Ensure PyQt5 is installed: `pip install PyQt5>=5.15.0`
- Check Python version: Python 3.7 or higher required
- Try resetting window geometry in settings

### Performance Issues
- Disable hardware acceleration in settings
- Reduce number of open tabs
- Check system resources
- Update graphics drivers

### Theme Not Applying
- Restart the application
- Check settings dialog theme selection
- Verify no conflicting stylesheets

## Future Enhancements

- Light mode theme
- Customizable color schemes
- Syntax highlighting in code editor
- Minimap for code navigation
- Floating panels
- Plugin UI integration
- Collaborative features
- Real-time AI suggestions overlay

## Credits

Designed with inspiration from:
- Apple's macOS Big Sur interface
- iOS design guidelines
- Grok's documentation panel
- Modern code editors (VS Code, Sublime Text)

Built with PyQt5 and Python.

---

**Version**: 1.0.0
**Last Updated**: October 2025
**License**: MIT
