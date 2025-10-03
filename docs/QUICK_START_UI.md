# GHST UI Quick Start Guide

Get started with the GHST AI Coding Engine's polished interface in minutes!

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
cd /path/to/GHST
pip install -r requirements.txt
```

This will install PyQt5 and other required packages.

## Launching GHST

### Method 1: Using the Launcher Script

```bash
cd core
python launch_gui.py
```

### Method 2: Direct Launch

```bash
cd core
python -c "from PyQt5.QtWidgets import QApplication; from src.ui_components.main import GHSTWindow; import sys; app = QApplication(sys.argv); window = GHSTWindow(); window.show(); sys.exit(app.exec_())"
```

## First Time Setup

When you first launch GHST, you'll see the welcome screen. Here's what to do:

### 1. Explore the Interface

The interface has three main panels:

- **Left Panel**: AI Experts and Tools
- **Center Panel**: Your workspace with tabs
- **Right Panel**: AI Assistant chat

### 2. Adjust Your Preferences

Click **Tools → Configuration** to open the settings dialog:

1. **General Tab**
   - Enable/disable auto-save
   - Set save interval (default: 60 seconds)

2. **AI Experts Tab**
   - Select your preferred AI model (GPT-4, Claude 3, etc.)
   - Enable automatic suggestions

3. **Appearance Tab**
   - Choose your theme (default: GHST Dark)
   - Adjust font size (default: 13px)

4. **Advanced Tab**
   - Configure performance settings
   - Set worker threads (default: 4)

Click **Save** to apply your settings.

### 3. Customize Your Layout

Drag the panel dividers to resize panels to your preference. The layout will be saved automatically.

## Basic Usage

### Working with AI Experts

1. **Select an Expert**
   - Click on any expert in the left panel
   - Each expert specializes in different areas:
     - 🔍 Code Analysis
     - 🐛 Debugging
     - 🛠️ Problem Solving
     - 📚 Research
     - And 8 more!

2. **Ask for Help**
   - Type your question in the AI Assistant panel (right side)
   - Click "✉️ Send Message" or press Enter
   - The AI will respond with assistance

### Using the Code Editor

1. **Open Code Editor Tab**
   - Click the "Code Editor" tab in the center panel
   - You'll see a code display box with a copy button

2. **View or Edit Code**
   - The code editor shows your code with syntax-friendly formatting
   - Click the "📋 Copy" button to copy code to clipboard
   - You'll see "✓ Copied!" confirmation

### Viewing Documentation

1. **Open Side Panel**
   - Click "📄 View Documentation" button in the left panel
   - Or use **View → Toggle Documentation Panel** from the menu

2. **Switch Between Views**
   - **Markdown Tab**: Formatted documentation
   - **Code Tab**: Code examples and snippets

3. **Close Panel**
   - Click the "×" button in the side panel header
   - Or click "📄 View Documentation" again

### Using SPEEDBUILD

The SPEEDBUILD slider controls automation level:

- **0%**: Fully automated (no prompts)
- **50%**: Balanced (default, mixed mode)
- **100%**: Full user control

Drag the slider to adjust, or click specific positions.

## Keyboard Shortcuts

Master these shortcuts for faster workflow:

### Global
- `Ctrl/Cmd + N` - New Project
- `Ctrl/Cmd + O` - Open Project
- `Ctrl/Cmd + S` - Save
- `Ctrl/Cmd + ,` - Settings
- `Ctrl/Cmd + Q` - Quit

### Navigation
- `Tab` - Move to next control
- `Shift + Tab` - Move to previous control
- `Enter` - Activate button/control
- `Esc` - Close dialog/panel

### Chat
- `Enter` - Send message
- `Shift + Enter` - New line in message
- `Ctrl/Cmd + L` - Clear chat (planned)

## Tips & Tricks

### Maximize Your Productivity

1. **Use the Side Panel**
   - Keep documentation open while coding
   - Quick reference without leaving GHST

2. **Customize Panel Sizes**
   - Make the center panel larger for coding
   - Shrink panels you don't use often

3. **Leverage AI Experts**
   - Different experts for different tasks
   - Switch experts based on your needs

4. **Save Your Layout**
   - Your panel sizes are remembered
   - Settings persist between sessions

### Pro Tips

- **Double-click** to select an expert quickly
- **Right-click** for context menus (planned)
- **Drag files** into GHST to open them (planned)
- **Use keyboard shortcuts** for faster navigation

## Troubleshooting

### Application Won't Start

**Problem**: Import errors or PyQt5 not found

**Solution**:
```bash
pip install --upgrade PyQt5
```

### UI Looks Wrong

**Problem**: Fonts or colors not displaying correctly

**Solutions**:
1. Check your display settings
2. Try a different theme in Settings
3. Restart the application

### Performance Issues

**Problem**: UI feels slow or laggy

**Solutions**:
1. Open Settings → Advanced
2. Disable hardware acceleration
3. Reduce worker threads
4. Close unused tabs

### Can't Find a Feature

**Problem**: Looking for a specific feature

**Solutions**:
1. Check the menu bar
2. Look in Settings dialog
3. Read the [UI Guide](UI_GUIDE.md)
4. Search the documentation

## Next Steps

### Learn More

- Read the [Complete UI Guide](UI_GUIDE.md) for detailed information
- Check [Component Documentation](../core/src/ui_components/README.md)
- Explore the [GHST Documentation](../README.md)

### Get Help

- Ask the AI Assistant in GHST
- Check the Help menu
- Read troubleshooting guides

### Customize Further

- Explore plugin manager
- Try different themes
- Configure AI expert behavior
- Set up your workflow

## Example Workflows

### Code Review Workflow

1. Open your code file
2. Select **🔍 Code Analysis** expert
3. Ask: "Can you review this code for issues?"
4. Review suggestions in chat
5. Make changes in code editor

### Debugging Workflow

1. Identify the bug
2. Select **🐛 Debugging** expert
3. Describe the issue in chat
4. Follow debugging suggestions
5. Test and iterate

### Learning Workflow

1. Select **📚 Research** expert
2. Ask about a concept or technology
3. View documentation in side panel
4. Try code examples
5. Ask follow-up questions

## Welcome to GHST!

You're now ready to use the GHST AI Coding Engine. The interface is designed to be intuitive, but don't hesitate to explore and experiment.

**Remember**: The AI experts are here to help you. Don't be afraid to ask questions!

---

**Need more help?** Check out the [UI Guide](UI_GUIDE.md) or ask the AI Assistant in GHST!

**Version**: 1.0.0  
**Last Updated**: October 2025  
**License**: MIT
