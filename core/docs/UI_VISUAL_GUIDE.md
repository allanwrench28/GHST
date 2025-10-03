# GHST UI Visual Guide

## Layout Overview

```
╔════════════════════════════════════════════════════════════════════════════╗
║ GHST - AI Coding Engine                                      [- □ ×]       ║
╠════════════════════════════════════════════════════════════════════════════╣
║ File  AI Experts  Tools  Help                                             ║
╠═══════════════╦══════════════════════════════════════════╦═════════════════╣
║               ║                                          ║                 ║
║  ⚡ SPEEDBUILD ║  🏠 Welcome | 📝 Code Editor | 📚 Docs  ║  💬 AI Chat     ║
║  ═══════════  ║  ──────────────────────────────────────  ║  ═════════════  ║
║  [████░░░░░░] ║                                          ║                 ║
║   50% Mixed   ║  🚀 Welcome to GHST                      ║  🧠 AI Expert   ║
║               ║                                          ║  Collective:    ║
║  🧠 AI Experts║  Your open-source AI coding assistant   ║  Ready to help! ║
║  ═══════════  ║                                          ║                 ║
║  🔍 Code      ║  ✨ Features:                            ║  💡 Tips:       ║
║  🐛 Debug     ║  • AI Collaboration Framework           ║  Ask questions, ║
║  🛠️ Problem   ║  • Plugin System                        ║  request code   ║
║  📚 Research  ║  • Configuration Management             ║  reviews, or    ║
║  ⚡ Perf      ║  • Modern UI                            ║  get debugging  ║
║  🔒 Security  ║  • Developer Tools                      ║  help.          ║
║  📝 Docs      ║                                          ║                 ║
║  🧪 Testing   ║  🎯 Getting Started:                     ║  ─────────────  ║
║  🏗️ Arch      ║  1. Select an AI expert                 ║  Your Message:  ║
║  🎨 UI/UX     ║  2. Open or create a project            ║  ┌───────────┐ ║
║  🚀 DevOps    ║  3. Get AI assistance                   ║  │           │ ║
║  📊 Data      ║                                          ║  │ Type here │ ║
║               ║  Remember: You maintain full control.   ║  │ ...       │ ║
║  🔧 Tools     ║  All AI recommendations require your    ║  └───────────┘ ║
║  ═══════════  ║  validation.                            ║                 ║
║  Plugin Mgr   ║                                          ║  ┌───────────┐ ║
║  Config       ║                                          ║  │ 📤 Send   │ ║
║  Templates    ║                                          ║  │ to Experts│ ║
║  Snippets     ║                                          ║  └───────────┘ ║
║               ║                                          ║                 ║
╠═══════════════╩══════════════════════════════════════════╩═════════════════╣
║ GHST AI Coding Engine - Ready            🔄 Last autocommit: 2h ago       ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Color Scheme (GitHub Dark)

### Background Colors
```
┌─────────────────┬──────────┬──────────────────────┐
│ Level           │ Hex      │ Usage                │
├─────────────────┼──────────┼──────────────────────┤
│ Background      │ #0d1117  │ Window background    │
│ Surface         │ #161b22  │ Cards, panels        │
│ Elevated        │ #1c2128  │ Hover, headers       │
│ Border          │ #30363d  │ Subtle separators    │
└─────────────────┴──────────┴──────────────────────┘
```

### Text Colors
```
┌─────────────────┬──────────┬──────────────────────┐
│ Level           │ Hex      │ Usage                │
├─────────────────┼──────────┼──────────────────────┤
│ Primary         │ #e6edf3  │ Main text            │
│ Secondary       │ #8b949e  │ Muted, labels        │
│ Accent Blue     │ #1f6feb  │ Primary actions      │
│ Accent Cyan     │ #00d4ff  │ Highlights, headers  │
└─────────────────┴──────────┴──────────────────────┘
```

## Component Examples

### Message Bubble (User)
```
╔════════════════════════════════════════════════════════╗
║ ┃👤 You                                                ║
║ ┃How do I optimize this function?                     ║
╚════════════════════════════════════════════════════════╝
     ▲
     └─ Blue accent border (#1f6feb)
     Dark background (#1c2128)
```

### Message Bubble (AI)
```
╔════════════════════════════════════════════════════════╗
║ ┃🧠 AI Expert Collective                               ║
║ ┃I can help optimize that function. Here's what I     ║
║ ┃recommend...                                          ║
╚════════════════════════════════════════════════════════╝
     ▲
     └─ Cyan accent border (#00d4ff)
     Darker background (#1e3a4c)
```

### Code Block
```
╔════════════════════════════════════════════════════════╗
║ 📄 PYTHON                                  📋 Copy    ║
╟────────────────────────────────────────────────────────╢
║ def optimize_function(data):                          ║
║     """Optimized version"""                           ║
║     # Process data efficiently                        ║
║     result = [x for x in data if x > 0]              ║
║     return sorted(result)                             ║
╚════════════════════════════════════════════════════════╝
     ▲                                        ▲
     └─ Language label                       └─ Copy button
     Header background (#1c2128)
     Code area background (#0d1117)
```

### Button States

#### Primary Button
```
Normal:    ┌──────────────────┐
           │  📤 Send Message │  #1f6feb (blue)
           └──────────────────┘

Hover:     ┌──────────────────┐
           │  📤 Send Message │  #388bfd (lighter blue)
           └──────────────────┘

Pressed:   ┌──────────────────┐
           │  📤 Send Message │  #1a5fdc (darker blue)
           └──────────────────┘
```

#### Modern Button
```
Normal:    ┌──────────────────┐
           │  📋 Copy Code    │  #21262d with border
           └──────────────────┘

Hover:     ┌──────────────────┐
           │  📋 Copy Code    │  #30363d (lighter)
           └──────────────────┘

Active:    ┌──────────────────┐
           │  ✅ Copied!      │  Shows feedback
           └──────────────────┘
```

## Tab Bar Design

```
┌─────────────┬──────────────────┬──────────────────┐
│ 🏠 Welcome  │  📝 Code Editor  │  📚 Docs         │
│─────────────│                  │                  │
│  Selected   │   Unselected     │   Unselected     │
│  #0d1117    │   #161b22        │   #161b22        │
│  #00d4ff    │   #8b949e        │   #8b949e        │
│  (cyan)     │   (muted)        │   (muted)        │
└─────────────┴──────────────────┴──────────────────┘
      ▲
      └─ Blue underline on selected (#1f6feb)
```

## List Items

```
┌────────────────────────────────────────┐
│  🔍 Code Analysis Expert               │  Normal
│                                        │  #161b22
├────────────────────────────────────────┤
│  🐛 Debugging Expert                   │  Hover
│                                        │  #1c2128
├────────────────────────────────────────┤
│  🛠️ Problem Solving Expert             │  Selected
│                                        │  #1f6feb (blue)
├────────────────────────────────────────┤
│  📚 Research Expert                    │  Normal
│                                        │  #161b22
└────────────────────────────────────────┘
```

## Scrollbar Design

```
Vertical:        ┃
                 ┃  Track: transparent
                 █  Handle: #30363d
                 █  Hover: #484f58
                 █  Width: 12px
                 █  Radius: 6px
                 ┃
```

## Spacing & Sizing

### Container Spacing
```
┌─ 16px ─┬────────────────────┬─ 16px ─┐
│        │                    │        │
├─ 16px ─┤  Content Area      ├─ 16px ─┤
│        │                    │        │
│        │  • Margin: 8-16px  │        │
│        │  • Padding: 8-16px │        │
│        │  • Gap: 8-12px     │        │
│        │                    │        │
└─ 16px ─┴────────────────────┴─ 16px ─┘
```

### Border Radius
```
Small:    6px  (buttons, inputs)
Medium:   8px  (cards, panels)
```

### Font Sizes
```
Headers:      14px (600 weight)
Body:         13px (400 weight)
Small:        12px (labels, meta)
Code:         10-11px (monospace)
```

## Animation Timing

```
Window Fade-in:   400ms (OutCubic easing)
Button Hover:     150ms (CSS transition)
Copy Feedback:    2000ms (button state)
```

## Accessibility

### Contrast Ratios
```
Primary text (#e6edf3) on background (#0d1117): 14.8:1 ✅ AAA
Secondary text (#8b949e) on background:          6.4:1 ✅ AA
Accent cyan (#00d4ff) on background:            11.2:1 ✅ AAA
```

### Interactive Elements
```
Minimum size: 40px height for buttons
Clear focus indicators on all controls
Keyboard navigation support
Semantic HTML structure
```

## Responsive Behavior

### Window Sizes

#### Minimum (1000x600)
```
Left: 200px | Center: 600px | Right: 200px
```

#### Medium (1400x900)
```
Left: 280px | Center: 840px | Right: 280px
```

#### Large (1920x1080)
```
Left: 384px | Center: 1152px | Right: 384px
```

## Syntax Highlighting Colors

### Python Code
```python
# Keyword:    #ff79c6 (pink)
def function_name():
    # String:     #f1fa8c (yellow)
    message = "Hello, World!"
    # Comment:    #6272a4 (blue-gray, italic)
    # Function:   #50fa7b (green)
    print(message)
    # Number:     #bd93f9 (purple)
    return 42
```

## Implementation Details

All styling is achieved through Qt StyleSheets:
- CSS-like syntax for easy customization
- Object names for specific targeting
- State selectors (hover, pressed, selected)
- Pseudo-elements for complex components

Example:
```css
QPushButton#primaryButton {
    background-color: #1f6feb;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
}

QPushButton#primaryButton:hover {
    background-color: #388bfd;
}
```

## Comparison to Reference UIs

### ChatGPT-like Features
✅ Message bubbles with rounded corners
✅ Code blocks with syntax highlighting
✅ Copy buttons on code
✅ Smooth dark theme
✅ Clean typography

### Grok-like Features
✅ Side panel for documentation
✅ Modern color scheme
✅ Professional layout
✅ Responsive design

### iOS-inspired Elements
✅ System font stack
✅ Smooth animations
✅ Rounded corners throughout
✅ Clear visual hierarchy
✅ Touch-friendly spacing

## Future Enhancements

Planned improvements:
- Light theme variant
- More syntax highlighters
- Markdown rendering
- Drag-and-drop support
- Theme customization
- Export functionality
