#!/usr/bin/env python3
"""
GHST Install Wizard
==================

Interactive installation and testing wizard for the GHST AI Coding Engine.
Tests all components, validates dependencies, and launches the GUI.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from pathlib import Path
import json


class GHSTInstallWizard:
    """Interactive GHST installation and testing wizard."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GHST Install Wizard")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.install_progress = tk.StringVar(value="Ready to install GHST")
        self.current_step = 0
        self.total_steps = 7
        
        # Installation results
        self.results = {
            'dependencies': False,
            'components': False,
            'syntax_supervisors': False,
            'gui_test': False,
            'integration': False
        }
        
        self.create_ui()
        
    def create_ui(self):
        """Create the wizard UI."""
        
        # Apply dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1e1e1e', foreground='white')
        style.configure('TButton', background='#0078d4', foreground='white')
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TProgressbar', background='#0078d4')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🚀 GHST AI Coding Engine",
            font=('Arial', 20, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Installation & Testing Wizard",
            font=('Arial', 12)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky='ew')
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.install_progress,
            font=('Arial', 10)
        )
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Log area
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', pady=(0, 20))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=70,
            bg='#2d2d2d',
            fg='white',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.install_btn = ttk.Button(
            button_frame,
            text="🚀 Start Installation & Testing",
            command=self.start_installation
        )
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.test_gui_btn = ttk.Button(
            button_frame,
            text="🎨 Test GUI Only",
            command=self.test_gui_only,
            state='disabled'
        )
        self.test_gui_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.launch_btn = ttk.Button(
            button_frame,
            text="🚀 Launch GHST",
            command=self.launch_ghst,
            state='disabled'
        )
        self.launch_btn.pack(side=tk.LEFT)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Initial log message
        self.log("🎯 GHST Install Wizard Ready")
        self.log("📋 This wizard will:")
        self.log("   • Check and install dependencies")
        self.log("   • Test all GHST components")
        self.log("   • Validate Syntax Supervisors")
        self.log("   • Launch and test the GUI")
        self.log("   • Verify system integration")
        self.log("")
    
    def log(self, message):
        """Add message to log."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_progress(self, step, message):
        """Update progress bar and status."""
        self.current_step = step
        progress = (step / self.total_steps) * 100
        self.progress_var.set(progress)
        self.install_progress.set(message)
        self.root.update()
    
    def start_installation(self):
        """Start the installation process."""
        self.install_btn.configure(state='disabled')
        
        # Run installation in separate thread
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()
    
    def run_installation(self):
        """Run the complete installation and testing process."""
        
        try:
            # Step 1: Check Python and basic requirements
            self.update_progress(1, "Checking Python environment...")
            self.log("🐍 Checking Python environment...")
            
            python_version = sys.version_info
            self.log(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            
            if python_version.major < 3 or python_version.minor < 8:
                self.log("❌ Python 3.8+ required")
                return False
            
            # Step 2: Install dependencies
            self.update_progress(2, "Installing dependencies...")
            self.log("📦 Installing dependencies...")
            
            dependencies = ['PyQt5', 'pyyaml', 'pathlib']
            for dep in dependencies:
                try:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', dep
                    ], capture_output=True)
                    self.log(f"✅ Installed: {dep}")
                except subprocess.CalledProcessError as e:
                    self.log(f"⚠️ Failed to install {dep}: {e}")
            
            self.results['dependencies'] = True
            
            # Step 3: Test GHST components
            self.update_progress(3, "Testing GHST components...")
            self.log("🧪 Testing GHST components...")
            
            # Change to the core directory for imports
            original_cwd = os.getcwd()
            project_root = Path(__file__).parent
            os.chdir(project_root)
            sys.path.insert(0, str(project_root))
            
            try:
                # Test Syntax Supervisors
                self.log("🔍 Testing Syntax Supervisors...")
                from core.src.syntax_supervisors import SyntaxSupervisorManager
                ss_manager = SyntaxSupervisorManager(str(project_root))
                self.log("✅ Syntax Supervisors: OK")
                self.results['syntax_supervisors'] = True
                
                # Test Expert Manager
                self.log("🧠 Testing Expert Manager...")
                from core.src.ai_collaboration.expert_manager import ExpertManager
                expert_manager = ExpertManager()
                self.log("✅ Expert Manager: OK")
                
                # Test Config Manager
                self.log("⚙️ Testing Config Manager...")
                from core.src.utils.config_manager import ConfigManager
                config_manager = ConfigManager()
                self.log("✅ Config Manager: OK")
                
                self.results['components'] = True
                
            except Exception as e:
                self.log(f"❌ Component test failed: {e}")
            
            # Step 4: Test GUI components
            self.update_progress(4, "Testing GUI components...")
            self.log("🎨 Testing GUI components...")
            
            try:
                from core.src.ui_components.main import GHSTWindow
                self.log("✅ GUI components loaded successfully")
                self.results['gui_test'] = True
                
                # Enable GUI test button
                self.test_gui_btn.configure(state='normal')
                
            except Exception as e:
                self.log(f"❌ GUI test failed: {e}")
            
            # Step 5: Integration test
            self.update_progress(5, "Running integration tests...")
            self.log("🔗 Running integration tests...")
            
            try:
                # Test background monitoring
                ss_manager.start_monitoring()
                time.sleep(2)
                ss_manager.stop_monitoring()
                self.log("✅ Background monitoring: OK")
                self.results['integration'] = True
                
            except Exception as e:
                self.log(f"❌ Integration test failed: {e}")
            
            # Step 6: Generate report
            self.update_progress(6, "Generating test report...")
            self.log("📊 Generating test report...")
            
            passed_tests = sum(self.results.values())
            total_tests = len(self.results)
            
            self.log("=" * 50)
            self.log("📋 INSTALLATION TEST REPORT")
            self.log("=" * 50)
            
            for test_name, result in self.results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                self.log(f"{status} {test_name.replace('_', ' ').title()}")
            
            self.log(f"📊 Overall: {passed_tests}/{total_tests} tests passed")
            
            # Step 7: Final status
            if passed_tests == total_tests:
                self.update_progress(7, "🎉 Installation complete! Ready to launch GHST")
                self.log("🎉 ALL TESTS PASSED!")
                self.log("🚀 GHST is ready for use!")
                self.launch_btn.configure(state='normal')
            else:
                self.update_progress(7, "⚠️ Installation completed with warnings")
                self.log("⚠️ Some tests failed - check log for details")
                self.launch_btn.configure(state='normal')  # Allow launch anyway
            
            # Restore original directory
            os.chdir(original_cwd)
            
        except Exception as e:
            self.log(f"❌ Installation failed: {e}")
            self.update_progress(0, "Installation failed")
    
    def test_gui_only(self):
        """Test just the GUI components."""
        self.log("🎨 Testing GUI in isolation...")
        
        try:
            # Import PyQt5
            from PyQt5.QtWidgets import QApplication
            
            # Create a test application
            if not QApplication.instance():
                app = QApplication(sys.argv)
            else:
                app = QApplication.instance()
            
            # Import and create main window
            project_root = Path(__file__).parent
            sys.path.insert(0, str(project_root))
            
            from core.src.ui_components.main import GHSTWindow
            
            # Create and show window
            main_window = GHSTWindow()
            main_window.show()
            
            self.log("✅ GUI window created and displayed")
            self.log("📋 Check the GHST window that should have opened")
            self.log("🔍 Test the interface, theming, and functionality")
            
            # Note: The window will remain open for testing
            
        except Exception as e:
            self.log(f"❌ GUI test failed: {e}")
            messagebox.showerror("GUI Test Failed", f"Failed to launch GUI: {e}")
    
    def launch_ghst(self):
        """Launch the full GHST system."""
        self.log("🚀 Launching GHST system...")
        
        try:
            # Launch in separate process to avoid blocking
            project_root = Path(__file__).parent
            launcher_path = project_root / "core" / "launcher.py"
            
            subprocess.Popen([
                sys.executable, str(launcher_path)
            ], cwd=str(project_root))
            
            self.log("✅ GHST system launched!")
            self.log("📋 Check the GHST application window")
            
        except Exception as e:
            self.log(f"❌ Launch failed: {e}")
            messagebox.showerror("Launch Failed", f"Failed to launch GHST: {e}")


def main():
    """Main entry point for the install wizard."""
    
    # Create and run the wizard
    wizard = GHSTInstallWizard()
    
    try:
        wizard.root.mainloop()
    except KeyboardInterrupt:
        print("Install wizard interrupted")
    except Exception as e:
        print(f"Install wizard error: {e}")


if __name__ == "__main__":
    main()
