# GHST Modern UI - Visual Testing Guide

## Overview

This guide helps you verify the visual quality and functionality of the GHST Modern UI implementation.

## ✅ Pre-Launch Checklist

### 1. Environment Setup
- [ ] Python 3.7+ installed
- [ ] PyQt5 5.15.0+ installed (`pip install PyQt5>=5.15.0`)
- [ ] GUI environment available (X11/Wayland on Linux, native on Windows/macOS)

### 2. Launch the UI
```bash
# Method 1: Using the launch script
python launch_modern_ui.py

# Method 2: Direct module execution
python -m core.src.ui_components.main

# Method 3: From code
python -c "
from PyQt5.QtWidgets import QApplication
from core.src.ui_components.modern_main_window import ModernMainWindow
import sys
app = QApplication(sys.argv)
window = ModernMainWindow()
window.show()
sys.exit(app.exec_())
"
```

## 🎨 Visual Verification Checklist

### Theme & Colors
- [ ] **Background**: Dark (#0d1117) - GitHub Dark inspired
- [ ] **Text**: Light (#e6edf3) - High contrast, easy to read
- [ ] **Accents**: Blue (#1f6feb) for primary, Cyan (#00d4ff) for AI
- [ ] **Borders**: Subtle gray (#30363d) - Not too prominent

### Layout & Structure
- [ ] **Three-pane layout**: Left (controls), Center (workspace), Right (chat)
- [ ] **Resizable splitters**: Can adjust pane sizes smoothly
- [ ] **Proper spacing**: 16px margins, consistent padding
- [ ] **Window size**: Opens at 1600x1000 (can be resized)

### Animations
- [ ] **Window fade-in**: Smooth 400ms fade from transparent to opaque
- [ ] **Loading spinner**: 30 FPS rotation, no jitter
- [ ] **Button hover**: Smooth color transitions
- [ ] **Tab switching**: Smooth content transitions

### Left Pane (Controls)
- [ ] **SPEEDBUILD slider**: Visible with label
- [ ] **AI Experts list**: 12 experts visible
  - 🔍 Code Analysis
  - 🐛 Debugging Expert
  - 🛠️ Problem Solving
  - 📚 Research Specialist
  - ⚡ Performance Optimizer
  - 🔒 Security Auditor
  - 📝 Documentation Writer
  - 🧪 Testing Engineer
  - 🏗️ Architecture Designer
  - 🎨 UI/UX Specialist
  - 🚀 DevOps Engineer
  - 📊 Data Scientist
- [ ] **Tools list**: 4 tools visible
  - 📦 Plugin Manager
  - ⚙️ Settings
  - 📋 Templates
  - ✂️ Code Snippets
- [ ] **View Documentation button**: At bottom of pane

### Center Pane (Workspace)
- [ ] **Three tabs visible**:
  1. 🏠 Welcome
  2. 💻 Code Editor
  3. 📚 Documentation

#### Welcome Tab
- [ ] Large heading: "🚀 Welcome to GHST"
- [ ] Subtitle: "Your AI Coding Engine with Expert Agent Think Tank"
- [ ] Features section with 5 bullet points
- [ ] Getting Started section with 4 steps
- [ ] Pro Tip box at bottom with blue left border
- [ ] All text readable with proper contrast

#### Code Editor Tab
- [ ] Code block widget visible
- [ ] Python syntax highlighting active:
  - Keywords in red (#ff7b72)
  - Strings in blue (#a5d6ff)
  - Comments in gray (#8b949e)
  - Functions in purple (#d2a8ff)
- [ ] Copy button at top right
- [ ] Code properly formatted with monospace font
- [ ] Sample code includes:
  - Function definitions
  - Comments
  - Classes
  - Docstrings

#### Documentation Tab
- [ ] Header: "📚 GHST Documentation"
- [ ] Welcome text visible
- [ ] Quick Links section with 4 links

### Right Pane (Chat)
- [ ] Header: "💬 AI Assistant"
- [ ] Welcome message visible:
  - "🧠 AI Expert" bubble
  - Welcome text
  - Pro tip in italics
- [ ] Message input field at bottom
- [ ] Send button visible: "✉️ Send Message"
- [ ] Input field placeholder: "Type your message here..."

### Menu Bar
- [ ] **File menu**: New Project, Open Project, Exit
- [ ] **View menu**: Toggle Documentation, Theme Settings
- [ ] **AI Experts menu**: Expert Status, Configure Experts
- [ ] **Tools menu**: Plugin Manager, Settings
- [ ] **Help menu**: About GHST, Documentation

### Status Bar
- [ ] Left side: "✅ GHST AI Coding Engine - Ready"
- [ ] Right side: "🟢 Connected"
- [ ] Small text, readable

### Documentation Panel (Hidden by Default)
- [ ] Click "📄 View Documentation" button to show
- [ ] Panel slides in from right
- [ ] Three tabs: 📖 Documentation, 💻 Code, 📁 Files
- [ ] Close button (×) at top right
- [ ] Clicking close hides panel smoothly

## 🧪 Functional Testing

### 1. Expert Selection
- [ ] Click on any expert in the list
- [ ] Item highlights in blue
- [ ] No console errors

### 2. Chat Functionality
- [ ] Type a message in the input field
- [ ] Click "Send Message" button
- [ ] User message appears as bubble with blue border
- [ ] AI response appears 500ms later with cyan border
- [ ] Chat auto-scrolls to bottom

### 3. Code Copy Functionality
- [ ] Go to "Code Editor" tab
- [ ] Click "📋 Copy" button
- [ ] Button text changes to "✓ Copied!"
- [ ] Button turns green
- [ ] Button resets after 2 seconds
- [ ] Code is actually in clipboard (paste to verify)

### 4. Tab Switching
- [ ] Click each tab in center pane
- [ ] Content switches smoothly
- [ ] No lag or flicker
- [ ] All content loads properly

### 5. Documentation Panel
- [ ] Click "📄 View Documentation" button
- [ ] Panel appears on right
- [ ] Click each tab (Documentation, Code, Files)
- [ ] Content switches properly
- [ ] Click × button to close
- [ ] Panel hides smoothly

### 6. SPEEDBUILD Slider
- [ ] Drag slider left and right
- [ ] Label updates to show current value
- [ ] At 0: "SPEEDBUILD: Fully Automated (No Prompts)"
- [ ] At 100: "Personalized: Full User Input Mode"
- [ ] In between: "Personalization: X% (Mixed Mode)"

### 7. Menu Actions
- [ ] Try each menu item
- [ ] Appropriate dialog appears
- [ ] About dialog shows version 2.0.0-modern
- [ ] Settings dialog opens (if implemented)

### 8. Window Resizing
- [ ] Resize window smaller/larger
- [ ] All panes adjust proportionally
- [ ] No content cutoff
- [ ] Scrollbars appear when needed
- [ ] Minimum size respected

### 9. Splitter Resizing
- [ ] Drag splitter between left and center pane
- [ ] Drag splitter between center and right pane
- [ ] Panes resize smoothly
- [ ] Content reflows properly

## 🎯 Quality Verification

### Typography
- [ ] All text uses Apple system font stack
- [ ] Monospace font for code (SF Mono, Monaco, Consolas)
- [ ] Font sizes appropriate:
  - Headers: 16-36px
  - Body: 13-15px
  - Small: 11-12px

### Contrast & Accessibility
- [ ] Primary text has high contrast (should be 14.8:1)
- [ ] Secondary text readable (should be 7.2:1)
- [ ] All interactive elements have hover states
- [ ] Focus indicators visible when using keyboard
- [ ] No flashing or seizure-inducing animations

### Performance
- [ ] Window opens within 1 second
- [ ] Fade-in animation smooth (no jitter)
- [ ] UI remains responsive during operations
- [ ] No memory leaks during extended use
- [ ] CPU usage reasonable (< 5% when idle)

### Error Handling
- [ ] No console errors during normal use
- [ ] Error dialogs appear for unimplemented features
- [ ] Application doesn't crash on edge cases

## 📸 Screenshot Checklist

Take screenshots to document:
1. **Main window** - Full interface at launch
2. **Code editor tab** - Showing syntax highlighting
3. **Chat with messages** - User and AI bubbles
4. **Documentation panel open** - Side panel visible
5. **Menu bar expanded** - Showing menu items
6. **About dialog** - Version and info

## 🐛 Known Limitations

1. **Headless environments**: UI won't launch without display server
2. **Platform-specific fonts**: May fall back to system defaults
3. **High DPI**: May need manual scaling adjustment on some systems

## ✅ Success Criteria

The implementation is successful if:
- ✅ All visual elements match the design specification
- ✅ GitHub Dark theme applied consistently
- ✅ Animations are smooth (30-60 FPS)
- ✅ All functional tests pass
- ✅ No console errors during normal use
- ✅ Performance is acceptable
- ✅ Accessibility requirements met

## 📝 Reporting Issues

If you find any issues during testing:

1. **Note the issue**: What doesn't work or look right?
2. **Reproduction steps**: How to reproduce the issue?
3. **Expected behavior**: What should happen?
4. **Actual behavior**: What actually happens?
5. **Screenshots**: Visual evidence of the issue
6. **Environment**: OS, Python version, PyQt5 version

## 🎉 Conclusion

If all checklist items pass, the GHST Modern UI implementation is:
- **Production-ready** ✅
- **Visually excellent** ✅
- **Functionally complete** ✅
- **Error-free** ✅

Congratulations on a successful UI modernization! 🚀
