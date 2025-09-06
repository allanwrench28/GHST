#!/usr/bin/env python3
"""
GHST Simple Auto-Continue
========================

Simplified automation for VS Code terminal continue prompts.
Works with keyboard shortcuts and simple automation.
"""

import time
import keyboard
import subprocess
import sys
from datetime import datetime


class SimpleAutoContinue:
    """Simple automation for VS Code terminal interactions."""
    
    def __init__(self):
        self.active = False
        self.stats = {'continues_sent': 0, 'start_time': None}
        self.hotkeys_registered = False
    
    def setup_hotkeys(self):
        """Set up keyboard shortcuts for automation."""
        
        if self.hotkeys_registered:
            return
        
        try:
            # Main automation hotkeys
            keyboard.add_hotkey('ctrl+shift+enter', self.send_continue)
            keyboard.add_hotkey('ctrl+shift+y', self.send_yes)
            keyboard.add_hotkey('ctrl+shift+space', self.send_space)
            keyboard.add_hotkey('ctrl+shift+q', self.stop_automation)
            
            # Auto-mode toggle
            keyboard.add_hotkey('ctrl+shift+a', self.toggle_auto_mode)
            
            self.hotkeys_registered = True
            print("✅ Hotkeys registered successfully")
            
        except Exception as e:
            print(f"❌ Error registering hotkeys: {e}")
            return False
        
        return True
    
    def send_continue(self):
        """Send continue signal to active window."""
        try:
            # Send Enter key
            keyboard.send('enter')
            self.stats['continues_sent'] += 1
            print(f"📤 Continue sent #{self.stats['continues_sent']}")
            return True
        except Exception as e:
            print(f"❌ Error sending continue: {e}")
            return False
    
    def send_yes(self):
        """Send yes response."""
        try:
            keyboard.write('y')
            keyboard.send('enter')
            print("📤 Sent: y")
            return True
        except Exception as e:
            print(f"❌ Error sending yes: {e}")
            return False
    
    def send_space(self):
        """Send space key."""
        try:
            keyboard.send('space')
            print("📤 Sent: space")
            return True
        except Exception as e:
            print(f"❌ Error sending space: {e}")
            return False
    
    def toggle_auto_mode(self):
        """Toggle automatic continue mode."""
        self.active = not self.active
        
        if self.active:
            self.stats['start_time'] = time.time()
            print("🤖 Auto-mode ENABLED")
            print("   Will automatically send Enter every 5 seconds")
            print("   Press CTRL+SHIFT+A again to disable")
            self.start_auto_continue()
        else:
            print("⏹️ Auto-mode DISABLED")
    
    def start_auto_continue(self):
        """Start automatic continue sending."""
        
        def auto_loop():
            while self.active:
                try:
                    time.sleep(5)  # Wait 5 seconds
                    if self.active:  # Check if still active
                        self.send_continue()
                except Exception as e:
                    print(f"❌ Auto-continue error: {e}")
                    break
        
        # Start in background
        import threading
        auto_thread = threading.Thread(target=auto_loop, daemon=True)
        auto_thread.start()
    
    def stop_automation(self):
        """Stop all automation."""
        self.active = False
        
        if self.stats['start_time']:
            duration = time.time() - self.stats['start_time']
            print(f"\n⏹️ Automation stopped")
            print(f"⏱️ Duration: {duration:.1f} seconds")
            print(f"📊 Total continues: {self.stats['continues_sent']}")
        
        print("👋 Goodbye!")
        sys.exit(0)
    
    def show_help(self):
        """Show help information."""
        print("\n" + "="*50)
        print("🤖 GHST SIMPLE AUTO-CONTINUE")
        print("="*50)
        print("📝 Hotkeys:")
        print("   CTRL+SHIFT+ENTER: Send continue (Enter)")
        print("   CTRL+SHIFT+Y:     Send yes (y + Enter)")
        print("   CTRL+SHIFT+SPACE: Send space")
        print("   CTRL+SHIFT+A:     Toggle auto-mode")
        print("   CTRL+SHIFT+Q:     Quit automation")
        print("\n🤖 Auto-mode:")
        print("   Automatically sends Enter every 5 seconds")
        print("   Perfect for long-running processes")
        print("\n💡 Tips:")
        print("   - Keep VS Code terminal focused")
        print("   - Use auto-mode when going AFK")
        print("   - Press hotkeys from any window")
        print("="*50)


def check_dependencies():
    """Check if required packages are available."""
    try:
        import keyboard
        return True
    except ImportError:
        print("📦 Installing keyboard package...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 'keyboard'
            ])
            print("✅ Keyboard package installed")
            return True
        except Exception as e:
            print(f"❌ Failed to install keyboard: {e}")
            print("💡 Try: pip install keyboard")
            return False


def main():
    """Main entry point."""
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create automation instance
    auto_continue = SimpleAutoContinue()
    
    # Show help
    auto_continue.show_help()
    
    # Set up hotkeys
    if not auto_continue.setup_hotkeys():
        print("❌ Failed to set up hotkeys")
        return False
    
    print(f"\n🚀 Automation ready!")
    print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"🔥 Press CTRL+SHIFT+A to start auto-mode")
    print(f"⏹️ Press CTRL+SHIFT+Q to quit\n")
    
    try:
        # Keep the program running
        print("👂 Listening for hotkeys...")
        keyboard.wait()  # Wait indefinitely for hotkeys
        
    except KeyboardInterrupt:
        auto_continue.stop_automation()
    
    return True


if __name__ == "__main__":
    main()
